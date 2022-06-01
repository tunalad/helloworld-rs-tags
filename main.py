#!/usr/bin/env python
from pprint import pprint

import requests
from bs4 import BeautifulSoup as bs


def get_soup(url):
    result = requests.get(url)
    return bs(result.content, "html.parser")


def get_job_tags_array(soup):
    tags = soup.find_all("button", class_="btn btn-xs btn-primary jobtag __jobtag w-auto")
    print("Total tag count:", len(tags))

    list = []
    for tag in tags:
        list.append(tag.span.string)

    return list


if __name__ == "__main__":
    search, senioritet = "python", "0"
    URL = f"https://www.helloworld.rs/oglasi-za-posao?q={search}&scope=full&senioritet[0]={senioritet}"

    doc = get_soup(URL)
    tags_list = get_job_tags_array(doc)

    pprint(tags_list)
