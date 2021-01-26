# wallscraper
#### An image scraper for reddit using PRAW (by /u/WeirdAlexGuy)

decription:

> This is an image scraper for reddit that randomly downloads
> images from the specified subs in the "subs.txt" file and
> adds them to the directory specified for wallpaper selection
> 
> The goal is to have an app that updates the wallpaper
> directory with random images every time you open your computer.

---------------------
## Installation

**prerequisites:**
* A reddit account
* Python 3
* git
* pip
* cron (optional)

### step 1:
first of all you have to create a reddit app. You can do this by going to [the reddit apps manager](https://www.reddit.com/prefs/apps).

then select `Create a new app`
with the following information

name: `wallscraper`

description: `an image scraper for downloading desktop wallpapers`

redirect uri: `http://localhost:8080`

### step 2:
move into the directory you want to do the installation and clone the github repository

```bash
git clone 'https://github.com/weird-alex/wallscraper.git'
cd wallscraper/
```

### step 3:
installing python libraries

run the following commands in your terminal
```bash
pip3 install praw
```

### step 4:
(make sure you're logged in on reddit on your primary browser)

run the following command to begin the authentication process
```bash
python3 auth.py
```
you will be asked to provide your `reddit username` and your app's `client id` and `client secret`

then you will be prompted with a link for reddit.
copy and paste into your browser and
give necessary permissions to reddit.

you will be redirected to `https://localhost:8080` to complete the authentification process.

check if program has the following output:
```
Authorization Successful
``` 
and if so you can close the `localhost` tab on your browser

### step 5:
open the file named subs.txt and add the subreddits you want to scrape from seperated by new lines (without the '/r/')

for example:
```
pics
wallpapers
art
```
etc.

### step 6:
at this point you can run the program

test this by doing
```bash
python3 main.py
```

if everything went well then the subdirectory `wallscraper/pics/` should have around 20 image files.

you can change the desktop wallpaper folder to be the `wallscraper/pics/` folder and set the option to cycle through the photos.

#### Note:
you can also silence the output of the program using `-s` as a command line argument:
```bash
python3 main.py -s
```

### step 7 (optional):
you might want to run the program every hour or maybe just every time your computer boots.

for this you can use `cron` which comes installed on most linux distributions

firstly, it's useful to make `main.py` executable. run:
```bash
chmod u+x main.py
```

to access it run
```bash
crontab -e
```

select an editor (`nano` reccomended) and add the following line in the end of the file
```
0 * * * * /path/to/wallscraper/main.py -s
```

the `0 * * * *` in the beginning is called a schedule expression and describes when the command should be run.
this particular one runs the command in the "0th" minute of every hour.

you might do the same thing with the `@hourly` tag like this
```
@hourly  /path/to/wallscraper/main.py -s
```

or every time your computer reboots with the `@reboot` tag:
```
@reboot /path/to/wallscraper/main.py -s
```

if you want to make your own custom expression you can use 
[this website](https://crontab.guru/) to get a description of what your expression will do.

------------
## Future plans:
* better windows support (it should still run on windows but you'll have to figure some stuff out)
* implement a basic UI
* better image filtering (only filters NSFW images right now)
