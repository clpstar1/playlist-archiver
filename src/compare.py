from archiver import filter_json
from sys import argv
import json 
from pprint import pprint

key = "videoId"

def get_inner(d):
        return d["snippet"]["resourceId"]["videoId"]

def invert(d):
    return { d["snippet"]["resourceId"]["videoId"] : d }

if __name__ == '__main__': 

    if len(argv) < 3:
        print ("Usage: file1, file2")
        exit(1)

    
    with open(argv[1]) as left:
        with open(argv[2]) as right:
            leftd = json.load(left)
            rightd = json.load(right)

            left_ids = set(map(get_inner, leftd,))
            right_ids = set(map(get_inner, rightd))

            leftinv = list(map(invert, leftd))
            rightinv = list(map(invert, rightd))

            leftonly = left_ids - right_ids
            rightonly = right_ids - left_ids

            rightfiltered = list(filter(lambda k : set(k.keys()).issubset(rightonly), rightinv))
            leftfiltered = list(filter(lambda k : set(k.keys()).issubset(leftonly), leftinv))

            print ("Only in Right:")
            pprint(rightfiltered, indent=4)
            print ("Only in Left:")
            pprint(leftfiltered, indent=4)


