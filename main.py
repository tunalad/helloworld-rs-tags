#!/usr/bin/env python
from pprint import pprint

import requests
from bs4 import BeautifulSoup as bs
from matplotlib import pyplot
from urllib.parse import quote


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


def draw_plot(x, y):
    pyplot.style.use("classic")
    pyplot.bar(x, y, color=(0.2, 0.35, 1))

    pyplot.ylabel("Occurrence", weight="normal")
    pyplot.xlabel("Tag", weight="normal")

    for i in range(len(x)):
        pyplot.text(i, y[i] // 2, y[i], color="#FFFFFF", weight="bold")
        # pyplot.text(i, y[i]//2, y[i], color="#000000", weight="normal")

    pyplot.show()


def input_handler(text=""):
    text_in = input(text)
    if text_in.isspace() or text_in == "":
        exit("Invalid input")
    else:

        return text_in.replace(" ", "-")


if __name__ == "__main__":
    search = input_handler("Keyword: ")
    search = quote(search)
    senioritet = input_handler("Seniority: ")


    URL = f"https://www.helloworld.rs/oglasi-za-posao?q={search}&scope=full&senioritet[0]={senioritet}"

    # scrapping website data
    doc = get_soup(URL)
    tags_list = get_job_tags_array(doc)

    # organizing data into a dictionary
    tags_dict = []
    for tag in list(dict.fromkeys(tags_list)):
        tags_dict.append({
            'tag': tag,
            'count': int(tags_list.count(tag))
        })

    print(f"Total tags count for {search} (including duplicates):", len(tags_list))
    print(f"Total tags found for {search}:", len(tags_dict))
    get_bars = int(input_handler("Display how many first tags?: "))
    if get_bars <= 0:
        exit("Invalid input")

    # sorting data (from most to least)
    tags_dict = sorted(tags_dict, key=lambda x: x['count'], reverse=True)

    # regrouping data for plotting
    tag_names = []
    tag_counts = []
    for t in range(len(tags_dict[:get_bars])):
        tag_names.append(tags_dict[t].get('tag'))
        tag_counts.append(tags_dict[t].get('count'))

    draw_plot(tag_names, tag_counts)
