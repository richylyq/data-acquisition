# Reddit | PRAW


## Introduction
Scrape reddit post from Old Reddit with the use of PRAW library

### Requirements
* Python 3 (tested and preferred on Python 3.9)
* PRAW
* pyyaml
* bs4

### Code Structure

#### Folders:
* ...

#### Files:
* `index.py` - python script to scrape reddit posts from old Reddit
* `linkcrawl.py` - python script to crawl for reddit links
* ...

## Usage

### Python
Have your `secrets.yaml` file ready for the credentials necessary to instantiate an instance of PRAW

Run `python index.py --keyword <keyword>` to scrape reddit posts based on keyword input

## Todo

Automatically try to rescrape when hit count of reddit post is zero 


