import praw
from server import get_request

import random

import sys
from os.path import exists

# return address should be the same you set on your reddit apps
IP = 'localhost'
PORT = 8080

if exists(sys.path[0] + '/client.txt'):
    with open(sys.path[0] + '/client.txt', 'r') as client_info:
        reddit_user_name = client_info.readline().strip('\n')
        reddit_client_id = client_info.readline().strip('\n')
        reddit_client_secret = client_info.readline().strip('\n')
else:
    reddit_user_name = input("reddit username: ").strip('/u/')
    reddit_client_id = input("client id: ")
    reddit_client_secret = input("client secret: ")

# creating the reddit instance
reddit = praw.Reddit(
    client_id=reddit_client_id,
    client_secret=reddit_client_secret,
    redirect_uri=f"http://{IP}:{PORT}",
    user_agent=f"linux:wallscraper authentification:v0.0.2 (by /u/{reddit_user_name})"
)

# State is a random string created to prevent nefarious activity from going through.
state = str(random.randint(0, 65000))

# this grants identity, read and submit permissions to the app
print('please go to the URL below to authenticate app')
print(reddit.auth.url(["identity", "read"], state, "permanent"))

# awaiting for response to IP:PORT
response = get_request(IP, PORT)

# parsing the response output to get the state and code variables
state_new, code = response.strip('/?').split('&')
state_new = state.split('=')[0]
code = code.split('=')[1]

# checking if state was changes and if so abort
if state_new != state:
    print('state changed. possible nefarious activity. running not reccomended')
    sys.exit()

try:
    with open('.refresh_token.txt', 'w') as token_file:
        # begin authorization with code and write the key to .refresh_token.txt
        token_file.write(reddit.auth.authorize(code))
    
    print('Authorization Successful')

    if not exists(sys.path[0] + '/client.txt'):
        with open(sys.path[0] + '/client.txt', 'w') as client_info:
            client_info.write(reddit_user_name + '\n')
            client_info.write(reddit_client_id + '\n')
            client_info.write(reddit_client_secret + '\n')

    if not exists(sys.path[0] + '/subs.txt'):
        with open(sys.path[0] + '/subs.txt', 'w') as subs:
            subs.write('# add subs here')

except Exception as e:
    print('ERROR: Something went wrong')
    print(e)
    sys.exit()

