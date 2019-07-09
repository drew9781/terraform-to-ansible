#! /usr/bin/python3
import json
import sys

def main():
    file = sys.argv[1]
    parse(file)


def parse( file ):
     with open(file, 'r') as myFile:
        #buffer = (myFile.read())
        buffer = json.load(myFile)
     print(buffer['values']['root_module']['resources'][0]['name'])

main()