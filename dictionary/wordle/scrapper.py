import requests
import time
from bs4 import BeautifulSoup
from datetime import date


def main():
    five_letter_words = []

    start_time = time.time()

    # There are 15 pages at the time of run
    for page_idx in range(1, 16):
        if page_idx == 1:
            url = "https://www.bestwordlist.com/5letterwords.htm"
        else:
            url = "https://www.bestwordlist.com/5letterwordspage{}.htm".format(
                page_idx)

        response = requests.get(url)

        if response.ok:
            parsed_html = BeautifulSoup(response.text, "html.parser")

            for idx, a in enumerate(
                    parsed_html.find_all("span", attrs={"class": "mot"})):
                for word in a.text.lower().strip(" ").split(" "):
                    five_letter_words.append(word)

        if (page_idx % 3 == 0) or (page_idx == 15):
            print("Processed pages: {} out of {}".format(page_idx, 15))
            print("Time elapsed: {} seconds".format(time.time() - start_time))

    # Add date suffix in the filepath to version the dictionary
    with open("dictionary/wordle/{}.txt".format(str(date.today())),
              "w") as outfile:
        for word in five_letter_words:
            outfile.write(word + "\n")


if __name__ == '__main__':
    main()
