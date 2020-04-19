#!/usr/bin/env python3

import argparse
import ast
from collections import defaultdict
from queue import LifoQueue, Queue, PriorityQueue

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("initial_state", help="a file of comma separated initial state")
    parser.add_argument("goal_state", help="a file of comma separated goal state")
    parser.add_argument("mode", help="argument to determine which algorithm to use", choices=["bfs","dfs","iddfs","astar"])
    parser.add_argument("output_filename", help="name of output file")
    return parser.parse_args()


#function to read a file into a state object
#returns state as a tuple of tuples: (left, right) == ((chickens, wolves, boats), (chickens, wolves, boats))
#should be nice for unpacking :)
def read_from_file(fname:str):
    with open("./"+fname, "r") as fp:
        left = "("+fp.readline()+")"
        right = "("+fp.readline()+")"
    return ast.literal_eval(left), ast.literal_eval(right)

def state_is_legal(state):
    left, right = state
    lc, lw, _ = left
    rc, rw, _ = right
    if (rw > rc and rc != 0) or (lw > lc and lc != 0):
        return False
    else:
        return True

def expand(state):
    left, right = state
    lc, lw, lb = left
    rc, rw, rb = right
    possible_states = set()
    all_possible_boats = ["c", ("c","c"), "w", ("w","c"), ("w","w")]
    if lb: #boat is on left
        pb = [b for b in all_possible_boats if b.count("c") <= lc and b.count("w") <= lw]
        for b in pb:
            new_left = (lc - b.count("c"), lw-b.count("w"), 0)
            new_right = (rc+b.count("c"), rw+b.count("w"), 1)
            possible_states.add((new_left, new_right))
    else: #boat is on right
        pb = [b for b in all_possible_boats if b.count("c") <= rc and b.count("w") <= rw]
        for b in pb:
            new_left = (lc + b.count("c"), lw+b.count("w"), 1)
            new_right = (rc-b.count("c"), rw-b.count("w"), 0)
            possible_states.add((new_left, new_right))

    for s in list(possible_states):
        if state_is_legal(s):
            yield s



def backtrace(back, start_from):
    curr = start_from
    while curr != -1:
        yield curr
        curr = back[curr]

def graph_search(frontier, intial_state, goal_state, depth_limit=-2):
    explored = set()
    cost = defaultdict(lambda: float('inf')) #use states as keys
    back = defaultdict(lambda: -1) #use states as keys
    expand_count = 0

    cost[initial_state] = 0
    frontier.put(initial_state)
    while(1):
        if frontier.empty() or depth_limit == -1:
            #solution not found
            return -1,-1, []

        leaf = frontier.get()
        if(leaf == goal_state):
            #return cost, number of expanded nodes, path of states to get there
            p = list(backtrace(back, leaf))
            p.reverse()
            return cost[leaf], expand_count, p

        explored.add(leaf)
        expand_count += 1
        reachable = expand(leaf)
        for s in list(reachable):
            if cost[leaf] +1 < cost[s]:
                cost[s] = cost[leaf] +1
                back[s] = leaf
            if s not in explored and s not in frontier.queue:
                frontier.put(s)
        depth_limit -= 1

def a_backtrace(back, start_from):
    curr = start_from
    while curr != -1:
        yield curr[1]
        curr = back[curr]

def astar(frontier, initial_state, goal_state):
    explored = set()
    cost = defaultdict(lambda: float('inf')) #use states as keys
    back = defaultdict(lambda: -1) #use states as keys
    heur = defaultdict(lambda: float('inf')) #use states as keys
    expand_count = 0

    cost[initial_state] = 0
    heur[initial_state] = initial_state[1][0] + initial_state[1][1]
    frontier.put((heur[initial_state], initial_state))
    while(1):
        if frontier.empty():
            #solution not found
            return -1,-1, []

        leaf = frontier.get()
        if(leaf[1] == goal_state):
            #return cost, number of expanded nodes, path of states to get there
            p = list(a_backtrace(back, leaf))
            p.reverse()
            return cost[leaf[1]], expand_count, p

        explored.add(leaf[1])
        expand_count += 1
        reachable = expand(leaf[1])
        for s in list(reachable):
            if cost[leaf[1]] +1 < cost[s]:
                cost[s] = cost[leaf[1]] + 1
                heur[s] = s[1][0] + s[1][1]
                back[(heur[s], s)] = leaf
            if s not in explored and s not in frontier.queue:
                frontier.put((heur[s], s))

def print_sol(path, cost, count, fp=None ):
    print("Total Cost:", cost, file=fp)
    print("# of Nodes Expanded:", count, file=fp)
    print("Steps taken: ", file=fp)

    row_format = "{:>15} {:>15}"
    print(row_format.format("Left Bank", "Right Bank"), file=fp)
    for l, r in path:
        print(row_format.format(str(l), str(r)),file=fp)


args = get_args()

initial_state = read_from_file(args.initial_state)
goal_state = read_from_file(args.goal_state)

#using python queue classes for consistency in gsearch algorithm :)
#docs for these data structs: https://docs.python.org/3/library/queue.html
if(args.mode == "bfs"):
    frontier = Queue()
elif(args.mode == "astar"):
    frontier = PriorityQueue()
elif (args.mode.find("dfs") != -1): #dfs or iddfs
    frontier = LifoQueue()
else:
    #print("need to add frontier data structure for Astar :)")
    exit()

if args.mode == "iddfs":
    for x in range(750): #unsure what to set this to. it works, but it could probably be smaller :)
        cost, count, path = graph_search(frontier, initial_state, goal_state, x)
        if cost != -1:
            break
elif args.mode == "astar":
    cost, count, path = astar(frontier, initial_state, goal_state)
else:
    cost, count, path = graph_search(frontier, initial_state, goal_state)

with open(args.output_filename, "w") as fp:
    if cost == -1:
        print("No solution found")
        fp.write("No solution found")
    else:
        print_sol(path, cost, count)
        print_sol(path, cost, count, fp)
