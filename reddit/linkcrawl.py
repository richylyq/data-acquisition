import time

import requests
from bs4 import BeautifulSoup

page_list = []
submission_list = []


def oldredditcrawlpage():
    link = f"https://old.reddit.com/search/?sort=new&q=url%3A{keyword}&t=all&restrict_sr=&count=25"
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")

    pass


def oldredditcrawl(keyword):
    link = f"https://old.reddit.com/search/?q=url%3A{keyword}&sort=new&limit=1000"
    page_list.append(link)
    page = requests.get(link)
    main_page = BeautifulSoup(page.content, "html.parser")
    time.sleep(100)
    # print(next_link)
    # while True:
    next_link = main_page.find_all("div", class_="nav-buttons")

    if len(next_link) != 0:
        print(next_link)
        for link in next_link:
            page_list.append(link.find("a")["href"])
    else:
        print("no next page?")
    return page_list


def getallsubmissionlink(keyword):
    link = f"https://old.reddit.com/search/?q=url%3A{keyword}&sort=new&limit=1000"
    page_list.append(link)


def getsubmissionlist(keyword):
    link = f"https://old.reddit.com/search/?q=url%3A{keyword}&sort=new&limit=1000"
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    submission_links = soup.find_all("header", class_="search-result-header")
    # print(len(submission_links))
    for submission_link in submission_links:

        submission_list.append(submission_link.find("a")["href"])
    print(len(submission_list))
    return submission_list


if __name__ == "__main__":
    print(oldredditcrawl("fifa"))
    # getsubmissionlist("evkeeza")
