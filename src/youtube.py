#!/usr/bin/python

import os

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow


# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the {{ Google Cloud Console }} at
# {{ https://cloud.google.com/console }}.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
    
# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
SCOPES = ['https://www.googleapis.com/auth/youtube']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
    
# Authorize the request and store authorization credentials.
def get_authenticated_service(path_to_client_secret):
  flow = InstalledAppFlow.from_client_secrets_file(path_to_client_secret, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def add_video(youtube, playlist_id, video_id):
  
  # define the body for the request
  
  print("try to add video with id:" + video_id)

  res = youtube.playlistItems().insert(
        part="snippet",
        body={
          "snippet": {
            "playlistId": playlist_id,
            "resourceId": {
              "kind": "youtube#video",
              "videoId": video_id
            }
          }
        }
    ).execute()

  print("success, added video:" + video_id + " to playlist: " + playlist_id)

  return res


def fetch_playlist(youtube, playlist_id, next_page):
  
  res = youtube.playlistItems().list(
      part="snippet",
      playlistId=playlist_id,
      pageToken=next_page,
      maxResults=50
  ).execute()
  return res

def add_playlist(youtube, args):
  
  body = dict(
    snippet=dict(
      title=args.title,
      description=args.description
    ),
    status=dict(
      privacyStatus='private'
    ) 
  ) 
    
  playlists_insert_response = youtube.playlists().insert(
    part='snippet,status',
    body=body
  ).execute()

  print('New playlist ID: %s' % playlists_insert_response['id'])


# wrapper to handle requests equally

def execute_request(request, *r_args):
    try:
        return request(*r_args)
    # http request failed 
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content)) 
        # in case of failure return none 
        return None 

    # catch all for exceptions i have no idea could have happened
    # dont crash the bot here is the goal
    except Exception as e: 
        print(str(e))

