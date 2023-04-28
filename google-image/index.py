"""
This script is to crawl images from Google Images
with the use of icrawler library
"""

import argparse
import os

from icrawler.builtin import GoogleImageCrawler

def google_crawler(choice, option):
    google_crawler = GoogleImageCrawler(downloader_threads=4, storage={'root_dir': keyword})
    google_crawler.crawl(keyword=keyword, filters={f'{choice}': f'{option}'}, file_idx_offset='auto', max_num=1000)

def image_crawler(keyword, filter):

    color_choices = [
            'color', 'blackandwhite', 'transparent', 'red', 'orange', 'yellow',
            'green', 'teal', 'blue', 'purple', 'pink', 'white', 'gray',
            'black', 'brown'
        ]

    type_choices = ['photo', 'face', 'clipart', 'linedrawing', 'animated']

    date_choices = ['anytime', 'pastday', 'pastweek', 'pastmonth', 'pastyear']

    if not os.path.exists(keyword):
        os.makedirs(keyword)
    if filter == 'color':
        for color in color_choices:
            google_crawler('color', color)
    elif filter == 'type':
        for type in type_choices:
            google_crawler('type', type)
    elif filter == 'date':
        for date in date_choices:
            google_crawler('date', date)

if __name__ == "__main__":

    # Create the argument parser
    my_parser = argparse.ArgumentParser(description="Let user input search term")

    # Add the arguments
    my_parser.add_argument(
        "-k", "--keyword", action="store", type=str, help="Keyword for Search Term", required=True
    )

    my_parser.add_argument(
        "-f", "--filter", action="store", type=str, help="filter for Google", required=True
    )

    # Execute the parser_args() method
    args = my_parser.parse_args()

    # keyword label
    keyword = args.keyword

    # filter setting
    filter = args.filter

    image_crawler(keyword, filter)