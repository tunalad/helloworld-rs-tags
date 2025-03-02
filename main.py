#!/usr/bin/env python
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring

from urllib.parse import quote
import requests
from bs4 import BeautifulSoup as bs
from matplotlib import pyplot


def get_soup(url):
    result = requests.get(url)
    return bs(result.content, "html.parser")


def get_job_tags_array(soup):
    tags = soup.find_all(
        "a", class_="btn btn-xs btn-primary w-auto jobtag __jobtag __ga4_job_tech_tag"
    )

    tags_list = []
    for tag in tags:
        tags_list.append(tag.text)

    page_next = get_next_page(soup)

    if page_next is not None:
        soup2 = get_soup(page_next)
        tags_list += get_job_tags_array(soup2)

    return tags_list


def get_next_page(soup):
    try:
        pages_list = soup.find(
            "div", class_="flex items-center justify-center gap-3 md:gap-4 pagination"
        )
        btn_next = pages_list.find(
            "i", class_="las la-angle-right text-lg pagination-new-design"
        ).parent

        print("https://www.helloworld.rs" + btn_next["href"])
        return "https://www.helloworld.rs" + btn_next["href"]
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
    return text_in.replace(" ", "-")


def main():
    search = input_handler("Search by keyword: ")
    search = f"q={quote(search)}&"
    senioritet = input_handler(
        """Seniority
    1 - junior
    2 - intermediate
    3 - senior
    (other numbers will ignore seniority filtering)
    >: """
    )

    url = f"https://www.helloworld.rs/oglasi-za-posao?{search}scope=full&senioritet[0]={senioritet}"

    # scrapping website data
    doc = get_soup(url)
    tags_list = get_job_tags_array(doc)

    # organizing data into a dictionary
    tags_dict = []
    for tag in list(dict.fromkeys(tags_list)):
        tags_dict.append({"tag": tag, "count": int(tags_list.count(tag))})

    print("Scrapping tags, please wait")

    print(len(tags_list), "tags counted")
    print(f'Tags found for "{search[2:-1]}":', len(tags_dict))

    get_bars = int(input_handler("Display how many first tags?: "))

    if get_bars <= 0:
        exit("Invalid input")

    # sorting data (from most to least)
    tags_dict = sorted(tags_dict, key=lambda x: x["count"], reverse=True)

    # regrouping data for plotting
    tag_names = []
    tag_counts = []
    for t in range(len(tags_dict[:get_bars])):
        tag_names.append(tags_dict[t].get("tag"))
        tag_counts.append(tags_dict[t].get("count"))

    draw_plot(tag_names, tag_counts)


if __name__ == "__main__":
    main()
