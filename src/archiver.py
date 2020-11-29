
import argparse
import requests
import json
from requests.exceptions import HTTPError
import time
import os.path
import sys

KEYS = ['title', 'position', 'videoId']

def setUpParser():
    parser = argparse.ArgumentParser()

    parser.add_argument('api_key', 
        help='api key for youtube access'
    )

    parser.add_argument('list_id',
        help='The id of the playlist(s) to retrieve',
        nargs='+'
    )

    parser.add_argument('-o',
        help='output directory'
    )

    return parser

#  'https://www.googleapis.com/youtube/v3/playlists?part=snippet&id=PLN9HStrYxE0AOE7xkRJSjqBpB8lIdl2QC&maxResults=50&key=[YOUR_API_KEY]' \

def fetch_playlist(playlist_id, nextpage, api_key):
    payload = {
        'part' : 'snippet',
        'playlistId' : playlist_id,
        'maxResults' : 50,
        'pageToken' : nextpage,
        'key' : api_key
    }
    return requests.get('https://www.googleapis.com/youtube/v3/playlistItems?', params=payload)

def playlist_fetch_all_items(playlist_id, nextpage, api_key):
    try: 
        res = dict(fetch_playlist(playlist_id, nextpage, api_key).json())
        nextPageToken = res['nextPageToken']
        return res['items'] + playlist_fetch_all_items(playlist_id, nextPageToken, api_key)
    except KeyError as e:
        return res['items']
    except HTTPError as e: 
        print('Http Error occured, Aborting')
        print(e)
        return []

def filter_json(json, keys):
    if isinstance(json, list):
        return filter_json_list(json, keys)
    return filter_json_dict(json, keys)

def filter_json_dict(json_dict, keys):
    # {}
    if len(json_dict) == 0:
        return json_dict
    tmp = {}
    for k, v in json_dict.items():
        if isinstance(v, list):
            v = filter_json_list(v, keys)
        if isinstance(v, dict):
            v = filter_json_dict(v, keys)
        if k in keys or (isinstance(v, (list, dict)) and len(v) > 0): 
            tmp[k] = v
    return tmp
    

def filter_json_list(json_list, keys):
    
    if len(json_list) == 0:
        return json_list
    
    tmp = []
    for item in json_list:
        if isinstance(item, dict):
            tmp.append(filter_json_dict(item, keys))
    return tmp 
    

if __name__ == '__main__':

    args = setUpParser().parse_args()
    
    out_dir = args.o or "."

    failed = False

    # do for every list id found
    for list_id in args.list_id:
        retries = 5
        errors = []
        
        filename = str(list_id  + "_" + str(int(time.time()))) + ".json"
        out_path = os.path.join(out_dir, filename)

        with (open(out_path, "x")) as f:
            while retries > 0: 
                try:
                    res = filter_json(
                        playlist_fetch_all_items(
                            list_id,
                            '',
                            args.api_key
                        ), KEYS
                    )
                    json.dump(res, f, indent=4)
                    retries = 0
                except Exception as e:
                    failed = True
                    retries-=1
                    errors.append(e)
            for e in errors:
                print(str(e))
    
    if (failed):
        sys.exit(1)
    sys.exit(0)
        


        
        
        
