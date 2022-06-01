#!/usr/bin/env python
from pprint import pprint

import requests
from bs4 import BeautifulSoup as bs


def get_soup(url):
    result = requests.get(url)
    return bs(result.content, "html.parser")


def get_job_tags_array(soup):
    tags = soup.find_all("button", class_="btn btn-xs btn-primary jobtag __jobtag w-auto")
    print("Total tag count on this page:", len(tags))

    list = []
    for tag in tags:
        list.append(tag.span.string)

    page_next = get_next_page(soup)

    if page_next != None:
        soup2 = get_soup(page_next)
        list += get_job_tags_array(soup2)
    else:
        print("That all of the pages")

    return list


def get_next_page(soup):
    try:
        pages_list = soup.find("div", class_="flex items-center justify-center gap-3 md:gap-4 pagination")
        btn_next = pages_list.find("i", class_="las la-angle-right text-lg").parent

        print("https://www.helloworld.rs" + btn_next['href'])
        return "https://www.helloworld.rs" + btn_next['href']
    except:
        return None

if __name__ == "__main__":
    search, senioritet = "python", "0"
    URL = f"https://www.helloworld.rs/oglasi-za-posao?q={search}&scope=full&senioritet[0]={senioritet}"

    doc = get_soup(URL)
    tags_list = get_job_tags_array(doc)

    pprint("Total tags count (including duplicates):", len(tags_list))
