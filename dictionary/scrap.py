import pickle
import requests
import string
import time
from bs4 import BeautifulSoup
from datetime import date


def main():
    five_letter_words = []

    start_time = time.time()

    # There are 106 pages at the time of run
    for page_idx in range(1, 107):
        response = requests.get("https://www.kbbi.co.id/daftar-kata?page=" +
                                str(page_idx))

        if response.ok:
            parsed_html = BeautifulSoup(response.text, "html.parser")

            for idx, a in enumerate(parsed_html.find_all("a", href=True)):
                if "arti-kata" in a["href"]:
                    word = a["href"].split("/")[-1]
                    word = word.translate(
                        str.maketrans('', '', string.punctuation))

                    if len(word) == 5:
                        five_letter_words.append(word)

        if (page_idx % 10 == 0) or ((page_idx + 1) == 106):
            print("Processed pages: {} out of {}".format(page_idx, 106))
            print("Time elapsed: {} seconds".format(time.time() - start_time))

    # Add date suffix in the filepath to version the dictionary
    with open("dictionary/five_letter_words_{}.txt".format(str(date.today())),
              "w") as outfile:
        for word in five_letter_words:
            outfile.write(word + "\n")


if __name__ == '__main__':
    main()
