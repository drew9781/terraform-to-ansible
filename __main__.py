#! /usr/bin/python3
import json

def main():
    file = sys.argv[1]
    parse(file)


def parse( file ):
     buffer = json.loads(file)
     print(buffer['resources']['name'])