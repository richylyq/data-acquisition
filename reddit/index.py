"""
This script is to scrape reddit posts from Reddit
with the use of praw library
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

import praw
import yaml
from linkcrawl import getsubmissionlist
from praw.models import MoreComments

def get_settings():
    full_file_path = Path(__file__).parent.joinpath('secrets.yaml')
    with open(full_file_path) as settings:
        settings_data = yaml.load(settings, Loader=yaml.Loader)
    return settings_data

secrets = get_settings()

reddit = praw.Reddit(
    client_id=secrets['client_id'],
    client_secret=secrets['client_secret'],
    user_agent=secrets['user_agent'],
)

submissions_list = []
submission_dict = {}
comments = {}

# dupixent_post = reddit.submission(
#     url="https://old.reddit.com/r/howardstern/comments/vklqz8/im_scoresman_damn_it_im_taking_care_of_business/"
#     # url="https://old.reddit.com/r/eczeJAKs/comments/vxtinu/rinvoq_cibinqo_dupixent/"
# )

# print(dupixent_post.title)
# for (
#     top_level_comment
# ) in dupixent_post.comments.list():  # comments are crawled by id alphabetically
#     if isinstance(top_level_comment, MoreComments):
#         continue
#     print(top_level_comment.author)
#     print(top_level_comment.ups)
#     print(top_level_comment.downs)
#     print(top_level_comment.created)

# pprint.pprint(vars(dupixent_post))

def reddit_submission_crawl(submission_list, keyword):
    """
    Crawl for reddit submissions with PRAW API based on
    list of submissions from specified keyword

    Args:
        submission_list (list): list of submissions from
        specifed keyword
    """
    comment_list = []
    for submission in submission_list:

        post = reddit.submission(url=submission)

        # Grab Reddit post Image Link
        if post.thumbnail == "default":
            image_link = ""
        else:
            try:
                image_link = post.preview["images"][0]["source"]["url"]
            except AttributeError:
                image_link = ""

        # Grab Reddit post author
        if post.author is None:
            post_author_name = "deleted"
        else:
            post_author_name = post.author.name

        post.comments.replace_more(limit=0)
        for (
            top_level_comment
        ) in post.comments.list():  # comments are crawled by id alphabetically
            if isinstance(top_level_comment, MoreComments):
                continue
            if top_level_comment.author is None:
                comment_author_name = ""
            else:
                comment_author_name = top_level_comment.author.name
            comments = (
                {
                    "_id": top_level_comment.id,
                    "author": comment_author_name,
                    "comment_datetime": timestamp_to_datetime(
                        top_level_comment.created
                    ),
                    "comment": top_level_comment.body,
                    "upvotes": top_level_comment.ups,
                    "downvote": top_level_comment.downs,
                },
            )
            comment_list.append(comments)
        submission_dict = {
            "_id": post.id,
            "author": post_author_name,
            "title": post.title,
            "post_datetime": timestamp_to_datetime(post.created),
            "link": submission,
            "image_link": image_link,
            "post_text": post.selftext,
            "upvotes": post.ups,
            "downvote": post.downs,
            "comments": comment_list,
        }
        submissions_list.append(submission_dict)
        comment_list = []
    # print(comment_list)
    with open(f"./{keyword}_data.json", "w", encoding="utf8") as outfile:
        json.dump(submissions_list, outfile, indent=4, ensure_ascii=False)


# # get 10 hot posts from the MachineLearning subreddit
# hot_posts = reddit.subreddit("MachineLearning").hot(limit=10)
# for post in hot_posts:
#     print(post.title)

# dupixent_post = reddit.submission(
#     url="https://old.reddit.com/r/EczemaUK/comments/a0esfo/dupixent/"
# )
# dupixent_post.comments.replace_more(limit=0)
# for top_level_comment in dupixent_post.comments.list():
#     if isinstance(top_level_comment, MoreComments):
#         continue
#     print(top_level_comment.body)

# subreddit_names = reddit.subreddits.search("dupixent")
# for srname in subreddit_names:
#     print(srname)

# subreddits = reddit.subreddits.search_by_name("eczema")
# for subreddit in subreddits:
#     print(subreddit)


def timestamp_to_datetime(created_timestamp):
    """
    Convert reddit timestamp into readable date time

    Args:
        created_timestamp (datetime.timestamp): timestamp retrieved from PRAW API

    Returns:
        datetime object: String Object of reddit post/comment datetime
    """
    dt_object = datetime.fromtimestamp(created_timestamp)
    return str(dt_object)


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

    submission_list = getsubmissionlist(keyword)

    # if len(submission_list) == 0:
    #     submission_list = getsubmissionlist("dupixent")
    #     test(submission_list)
    # else:
    reddit_submission_crawl(submission_list, keyword)
    # pass
