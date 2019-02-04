'''
    Copyright (c) 2018 Elliott Pardee <me [at] vypr [dot] xyz>
    This file is part of BGBookNames.

    BGBookNames is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    BGBookNames is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with BGBookNames.  If not, see <http://www.gnu.org/licenses/>.
'''

import requests
import json
import os
import sys
from bs4 import BeautifulSoup
import logging
from http.client import HTTPConnection
HTTPConnection.debuglevel = 0

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path + "/")

from vylogger import VyLogger  # noqa: E501

logger = VyLogger("default")

versionsURL = "https://www.biblegateway.com/versions/"

book_names = {
    "gen": ["Gen", "Ge", "Gn"],
    "exod": ["Ex", "Exod"],
    "lev": ["Lev", "Le", "Lv"],
    "num": ["Num", "Nu", "Nm", "Nb"],
    "deut": ["Deut", "De", "Dt"],
    "josh": ["Josh", "Jos", "Jsh"],
    "judg": ["Judg", "Jdg", "Jg", "Jdgs"],
    "ruth": ["Rth", "Ru"],
    "1sam": ["1 Sam", "1 Sm", "1 Sa", "1st Samuel", "1st Sam", "1st Sm", "1st Sa"],
    "2sam": ["2 Sam", "2 Sm", "2 Sa", "2nd Samuel", "2nd Sam", "2nd Sm", "2nd Sa"],
    "1kgs": ["1 Kgs", "1 Kin", "1 Ki", "1st Kings", "1st Kgs", "1st Kin", "1st Ki"],
    "2kgs": ["2 Kgs", "2 Kin", "2 Ki", "2nd Kings", "2nd Kgs", "2nd Kin", "2nd Ki"],
    "1chr": ["1 Chr", "1 Ch", "1st Chronicles", "1st Chr", "1st Ch", "3 Kings", "3rd Kings", "3 Kgs", "3 Kin", "3 Ki", "3rd Kings", "3rd Kgs", "3rd Kin", "3rd Ki"],
    "2chr": ["2 Chr", "2 Ch", "2nd Chronicles", "2nd Chr", "2nd Ch", "4 Kings", "4th Kings", "4 Kgs", "4 Kin", "4 Ki", "4th Kings", "4th Kgs", "4th Kin", "4th Ki"],
    "ezra": ["Ezr"],
    "neh": ["Neh"],
    "esth": ["Esth"],
    "job": ["Jb"],
    "ps": ["Psalms", "Ps", "Pslm", "Psa", "Psm"],
    "prov": ["Prov", "Prv"],
    "eccl": ["Eccl", "Eccles", "Eccle", "Ecc"],
    "song": ["Song"],
    "isa": ["Isa"],
    "jer": ["Jer"],
    "lam": ["Lam"],
    "ezek": ["Ezek"],
    "dan": ["Dan"],
    "hos": ["Hos"],
    "joel": [],
    "amos": [],
    "obad": ["Obad"],
    "jonah": ["Jnh"],
    "mic": ["Mic"],
    "nah": ["Nah"],
    "hab": ["Hab"],
    "zeph": ["Zeph"],
    "hag": ["Hag"],
    "zech": ["Zech"],
    "mal": ["Mal"],
    "matt": ["Mt"],
    "mark": ["Mk", "Mrk"],
    "luke": ["Lk", "Luk"],
    "john": ["Jn", "Jhn"],
    "acts": [],
    "rom": ["Rom", "Ro", "Rm"],
    "1cor": ["1 Cor", "1 Co" "1st Corinthians", "1st Cor", "1st Co"],
    "2cor": ["2 Cor", "2 Co" "2nd Corinthians", "2nd Cor", "2nd Co"],
    "gal": ["Gal", "Ga"],
    "eph": ["Eph", "Ephes"],
    "phil": ["Phil", "Php", "Pp"],
    "col": ["Col"],
    "1thess": ["1 Thess", "1 Thes", "1 Th", "1st Thessalonians", "1st Thess", "1st Thes", "1st Th"],
    "2thess": ["2 Thess", "2 Thes", "2 Th", "2nd Thessalonians", "2nd Thess", "2nd Thes", "2nd Th"],
    "1tim": ["1 Tim", "1 Ti", "1st Timothy", "1st Tim", "1st Ti"],
    "2tim": ["2 Tim", "2 Ti", "2nd Timothy", "2nd Tim", "2nd Ti"],
    "titus": ["Titus", "Ti"],
    "phlm": ["Philem", "Phm", "Pm"],
    "heb": ["Heb"],
    "jas": ["Jas", "Jm"],
    "1pet": ["1 Pet", "1 Pe", "1 Pt", "1st Peter", "1st Pet", "1st Pe", "1st Pt"],
    "2pet": ["2 Pet", "2 Pe", "2 Pt", "2nd Peter", "2nd Pet", "2nd Pe", "2nd Pt"],
    "1john": ["1 Jn", "1 Jhn", "1st John", "1st Jn", "1st Jhn"],
    "2john": ["2 Jn", "2 Jhn", "2nd John", "2nd Jn", "2nd Jhn"],
    "3john": ["3 Jn", "3 Jhn", "3rd John", "3rd Jn", "3rd Jhn"],
    "jude": ["Jud", "Jd"],
    "rev": ["Rev", "Apoc", "Apocalypse"],
    "tob": ["Tob"],
    "jdt": ["Jdt"],
    "gkest": [],
    "wis": ["Wis"],
    "sir": ["Sir"],
    "bar": ["Bar"],
    "epjer": [],
    "praz": ["Azariah"],
    "sus": ["Sus"],
    "bel": ["Bel"],
    "1macc": ["1 Macc", "1 Mac", "1st Maccabees", "1st Macc", "1st Mac"],
    "2macc": ["2 Macc", "2 Mac", "2nd Maccabees", "2nd Macc", "2nd Mac"],
    "1esd": ["1 Esd", "1st Esdras", "1st Esd"],
    "prman": ["Manasseh"],
    "ps151": ["Ps 151"],
    "3ma": ["3 Macc", "3 Mac", "3rd Maccabees", "3rd Macc", "3rd Mac"],
    "2esd": ["2 Esd", "2nd Esdras", "2nd Esd"],
    "4ma": ["4 Macc", "4 Mac", "4th Maccabees", "4th Macc", "4th Mac"],
}

res = requests.get(versionsURL)

obj = {}

ignoredTranslations = ["Arabic Bible: Easy-to-Read Version (ERV-AR)", "Ketab El Hayat (NAV)",
                       "Farsi New Testament", "Farsi Ebook Bible", "Habrit Hakhadasha/Haderekh (HHH)",
                       "The Westminster Leningrad Codex (WLC)", "Urdu Bible: Easy-to-Read Version (ERV-UR)",
                       "Hawai‘i Pidgin (HWP)"]


def log_message(level, msg):
    message = "[shard 0] <BGBookNames@global> " + msg

    if level == "warn":
        logger.warning(message)
    elif level == "err":
        logger.error(message)
    elif level == "info":
        logger.info(message)
    elif level == "debug":
        logger.debug(message)


def get_books():
    if res is not None:
        soup = BeautifulSoup(res.text, "lxml")

        log_message("info", "Getting translations...")

        for translation in soup.findAll("td", {"class": ["collapse", "translation-name"]}):
            for a in translation.findAll("a", href=True):
                version = a.text
                link = a["href"]

                if "#booklist" in link and version not in ignoredTranslations:
                    obj[version] = {}
                    obj[version]["booklist"] = "https://www.biblegateway.com" + link

        if obj is not {}:
            log_message("info", "Getting book names... (this will take approx. 2-3 minutes)")
            for item in obj:
                booklist_url = obj[item]["booklist"]
                book_res = requests.get(booklist_url)

                if book_res is not None:
                    soup = BeautifulSoup(book_res.text, "html.parser")

                    table = soup.find("table", {"class": "chapterlinks"})

                    for table_field in table.findAll("td"):
                        book = dict(table_field.attrs).get("data-target")

                        for chapter_numbers in table_field.findAll("span", {"class": "num-chapters"}):
                            chapter_numbers.decompose()

                        if not str(book) == "None":
                            book = book[1:-5]
                            classes = dict(table_field.attrs).get("class")

                            try:
                                if book == "3macc":
                                    book = "3ma"
                                elif book == "gkesth" or book == "adest":
                                    book = "gkest"
                                elif book == "sgthree" or book == "sgthr":
                                    book = "praz"

                                if "book-name" in classes:
                                    if table_field.text not in book_names[book]:
                                        book_names[book].append(table_field.text)
                            except KeyError:
                                log_message("err", "found " + book + " in " + item)
                                book = input("[bfix] what should I rename this book to?")

                                if not book == "":
                                    if table_field.text not in book_names[book]:
                                        book_names[book].append(table_field.text)

        if os.path.isfile(dir_path + "/books.json"):
            log_message("info", "Found books.json, removing...")
            os.remove(dir_path + "/books.json")

        with open(dir_path + "/books.json", "w") as file:
            log_message("info", "Writing file...")
            file.write(json.dumps(book_names))
            log_message("info", "Write successful.")

        log_message("info", "Done.")


if __name__ == "__main__":
    get_books()
