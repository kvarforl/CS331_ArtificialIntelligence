#!/usr/bin/env python3

import argparse
import ast

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

args = get_args()

initial_state = read_from_file(args.initial_state)
goal_state = read_from_file(args.goal_state)

visited_states = set(initial_state)

