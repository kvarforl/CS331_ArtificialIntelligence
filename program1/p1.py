#!/usr/bin/env python3

import argparse
import ast
from queue import LifoQueue, Queue

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

def expand(state):
    print("incomplete: expand(state) :/")
    return []

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

#start gsearch psuedo code
frontier.put(initial_state) 
explored = set()

while(1):
    if frontier.empty():
        #return failure
        break
    leaf = frontier.get()
    if(leaf == goal_state):
        #return solution
        break
    explored.add(leaf)
    #need to define expand func: takes state, returns list of reachable states
    reachable = expand(leaf)

    for s in reachable:
        if s not in explored and s not in frontier.queue:
            frontier.put(s)
    


