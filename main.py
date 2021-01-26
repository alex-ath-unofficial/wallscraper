#!/usr/bin/python3

'''
~Wallscraper~
An image scraper for reddit using PRAW by WeirdAlex.

This is an image scraper for reddit that randomly downloads
images from the specified subs in the "subs.txt" file and
adds them to the directory specified for wallpaper selection

The goal is to have an app that updates the wallpaper
directory with random images every time you open your computer.
'''

import praw
import requests
import random

import sys

from os import listdir, remove
from os.path import isfile, join, exists

silence = '-s' in sys.argv

# This is the directory of the script
SCRIPT_DIR = sys.path[0] + '/'

# DIR is the wallpaper directory where the images will be saved
IMG_DIR = SCRIPT_DIR + 'pics/'

# img_count is the number of images to download
img_count = 20

# Reading the client information
if exists(SCRIPT_DIR + 'client.txt'):
    with open(SCRIPT_DIR + 'client.txt', 'r') as client_info:
        reddit_user_name = client_info.readline().strip('\n')
        reddit_client_id = client_info.readline().strip('\n')
        reddit_client_secret = client_info.readline().strip('\n')
else:
    print('please run auth.py before this. read README for detailed instruction')
    sys.exit()


# Reading the refresh token
if exists(SCRIPT_DIR + '.refresh_token.txt'):
    with open(SCRIPT_DIR + '.refresh_token.txt', 'r') as token_file:
        token = token_file.readline().strip(' \n')
else:
    print('please run auth.py before this. read README for detailed instruction')
    sys.exit()

# Creating the Reddit instance
reddit = praw.Reddit(
    client_id=reddit_client_id,
    client_secret=reddit_client_secret,
    refresh_token=token,
    user_agent=f"linux:wallscraper image scraper:v0.0.2 (by /u/{reddit_user_name})"
)

# Accessing the subreddits and logging the image URLs
urls = []
with open(SCRIPT_DIR + 'subs.txt', 'r') as subs_list:
    subs_list = [sub.strip(' \n') for sub in subs_list if sub.strip(' \n') != '']
    for sub in subs_list:
        if sub:
            if sub[0] == '#':
                continue
            if not silence:
                print('accessing /r/' + sub + '...')
            for post in reddit.subreddit(sub).hot(limit=(10*img_count//len(subs_list))):
                url=post.url
                if not post.over_18 and '.jpg' in url or '.png' in url:
                    urls.append(url)

if not silence:
    print()
    print('Number of pictures:', len(urls))
    print()

# Deleting all image files in DIR
files = [join(IMG_DIR, f) for f in listdir(IMG_DIR) if isfile(join(IMG_DIR, f)) and ('.png' in f or '.jpg' in f)]
for file in files:
    remove(file)

# Shuffling the URLs so that you select random images each time.
random.shuffle(urls)

# Downloading the images using the URLs
for url in urls[:img_count]:
    if not silence:
        print('\n', 'Downloading', url.split('/')[-1], end=' ')
    img_data = requests.get(url).content

    # checking if image is error image (removed or missing)
    with open(SCRIPT_DIR + 'invalid_images/' + ('invalid.png' if '.png' in url else 'invalid.jpg'), 'rb') as invalid:
        if img_data == invalid.read():
            if not silence:
                print('IMAGE INVALID', end='')
            continue

    # writing to file
    with open(IMG_DIR + url.split('/')[-1], 'wb') as img_file:
        img_file.write(img_data)

if not silence:
    print()
