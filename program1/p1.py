#!/usr/bin/env python3

import argparse
import ast
from collections import defaultdict
from queue import LifoQueue, Queue
from itertools import combinations

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
    left_bank_animals = ["c" for _ in range(lc)] + ["w" for _ in range(lw)]
    right_bank_animals = ["c" for _ in range(rc)] + ["w" for _ in range(rw)]
    possible_states = set()
    if lb: #boat is on left
        animals_to_move = list(set(list(combinations(left_bank_animals, 2)) + left_bank_animals))
        for b in animals_to_move:
            new_left = (lc - b.count("c"), lw-b.count("w"), 0)
            new_right = (rc+b.count("c"), rw+b.count("w"), 1)
            possible_states.add((new_left, new_right))
    else: #boat is on right
        animals_to_move = list(set(list(combinations(right_bank_animals, 2)) + right_bank_animals))
        for b in animals_to_move:
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

def graph_search(frontier, intial_state, goal_state):
    explored = set()
    cost = defaultdict(lambda: float('inf')) #use states as keys
    back = defaultdict(lambda: -1) #use states as keys

    cost[initial_state] = 0
    frontier.put(initial_state) 
    while(1):
        if frontier.empty():
            #solution not found
            return -1, []
         
        leaf = frontier.get()
        if(leaf == goal_state):
            #return cost and path of states to get there
            return cost[leaf], list(backtrace(back, leaf))
 
        explored.add(leaf)
        #need to define expand func: takes state, returns list of reachable states 
        reachable = expand(leaf)
        for s in list(reachable):
            if cost[leaf] +1 < cost[s]:
                cost[s] = cost[leaf] +1
                back[s] = leaf
            if s not in explored and s not in frontier.queue:
                frontier.put(s)
    


args = get_args()

initial_state = read_from_file(args.initial_state)
goal_state = read_from_file(args.goal_state)

#using python queue classes for consistency in gsearch algorithm :)
#docs for these data structs: https://docs.python.org/3/library/queue.html
if(args.mode == "bfs"):
    frontier = Queue()
elif (args.mode.find("dfs") != -1): #dfs or iddfs
    frontier = LifoQueue();
else:
    print("need to add frontier data structure for Astar :)")
    exit()

cost, path = graph_search(frontier, initial_state, goal_state)

if cost == -1:
    print("No solution found")
else:
    print("Cost:", cost, "Path:", path)