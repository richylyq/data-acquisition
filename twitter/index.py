"""
This script is to scrape tweets from Twitter from 2006 to present 
with the use of snscrape library
Currently overlimit to 999999 tweets
"""

import snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import date
import argparse


def twittercrawl(keyword):
    """
    Scraping from Twitter based on their keywords

    Args:
        keyword (str): keyword of tweets you want to scrape
    """
    today = date.today()
    # Creating the list to append twitter data to
    tweets = []
    keyword = keyword.lower()
    # Using TwitterSearchScrapper to scrape data and append tweets into list
    for i, tweet in enumerate(
        sntwitter.TwitterSearchScraper(
            f"{keyword} since:2006-01-01 until:{today}"
        ).get_items()
    ):
        if i > 999999:  # set to overlimit to crawl more data
            break
        media_url, video_url = "", ""
        if tweet.media is not None:
            media_url = tweet.media[0]
            # if "Photo" in tweet.media[0]:
            #     image_url = tweet.media[0].fullUrl
            #     video_url = ""

            # elif "Video" in tweet.media[0]:
            #     image_url = ""
            #     video_url = tweet.media[0].url

        tweets.append(
            [
                tweet.date,
                tweet.id,
                tweet.user.username,
                tweet.url,
                tweet.lang,
                tweet.content,
                tweet.replyCount,
                tweet.retweetCount,
                tweet.likeCount,
                media_url,
            ]
        )

        # print(video_url)
    df = pd.DataFrame(
        tweets,
        columns=[
            "Datetime",
            "Tweet ID",
            "Username",
            "Tweet Url",
            "Tweet Lang",
            "Tweet Text",
            "Reply Count",
            "Retweet Count",
            "Like Count",
            "Media",
        ],
    )
    df.to_csv(f"{keyword}_tweets.csv")


if __name__ == "__main__":
    
    # Create the argument parser
    my_parser = argparse.ArgumentParser(description="Let user input search term")

    # Add the arguments
    my_parser.add_argument(
        "--keyword", action="store", type=str, help="Keyword for Search Term", required=True
    )

    # Execute the parser_args() method
    args = my_parser.parse_args()

    # keyword label
    keyword = args.keyword

    twittercrawl(keyword)
