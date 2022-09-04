# Creates database files to convert enoji names, country names or short codes into the corresponding unicode sequence
# or receive details about a single emoji unicode character

import json
import sys
from typing import List

from scistag.webstag import web_fetch
import os

UNICODE_URL = "https://unicode.org/Public/emoji/14.0/emoji-test.txt"
COUNTRY_SHORT_CODE_URL = sys.argv[1]
NOTO_PATH = "images/noto/cpngs/"
BASE_PATH = os.path.dirname(__file__) + "/../../"
MARKDOWN_CODE_FILE = BASE_PATH + "/data/emoji/markdown_emoji_names.json"
OUTPUT_PATH = os.path.dirname(__file__) + "/../../data/emoji/"
os.makedirs(OUTPUT_PATH, exist_ok=True)

SUBGROUP_IDENTIFIER = "# subgroup:"
GROUP_IDENTIFIER = "# group:"

emoji_details = {}
emoji_mappings = {}
markdown_codes: dict = json.load(open(MARKDOWN_CODE_FILE, "r"))
markdown_codes_inv = {value: code for code, value in markdown_codes.items()}


def create_main_emoji_db(data: List[str]):
    """
    Creates the main emoji database based upon the unicode.org data and stores it in data/unicode/emoji_db.json
    :param data: The input data
    """
    global emoji_details
    data = [element for element in data if len(element) > 0]
    group = ""
    sub_group = ""
    existing_notos = 0

    for element in data:
        if element.startswith("#"):
            if element.startswith(GROUP_IDENTIFIER):
                group = element[len(GROUP_IDENTIFIER):].lstrip(" ")
            if element.startswith(SUBGROUP_IDENTIFIER):
                sub_group = element[len(SUBGROUP_IDENTIFIER):].lstrip(" ")
            continue
        components = element.split(";")
        code = components[0].rstrip(" ").split(" ")
        lowercase_code = [element.lower() for element in code]
        details = components[1].split("#")[1].lstrip(" ")
        name = " ".join(details.split(" ")[2:])
        noto_name = NOTO_PATH + "emoji_u" + "_".join(lowercase_code) + ".png"
        noto_exists = os.path.exists(BASE_PATH + "/" + noto_name)
        if not noto_exists:
            noto_name = ""
        existing_notos += 1
        details = {"group": group, "subgroup": sub_group, "name": name}
        code_identifier = "_".join(code)
        if code_identifier in markdown_codes_inv:
            details["markdownName"] = markdown_codes_inv[code_identifier]
        emoji_details[code_identifier] = details
        emoji_mappings[name] = code_identifier


def add_country_details(country_data):
    """
    Adds a country name and country short code to all country flag emojis
    :param country_data: The country data in the form List[{name: name, unnicode: spaced, unicode sequence,
    code: country short code)
    """
    data = json.loads(country_data)
    for element in data:
        country_name = element['name']
        country_code = element['code']
        code = element['unicode'].split(" ")
        code = [element[2:] for element in code]
        code = "_".join(code)
        if code not in emoji_details:
            print(f"{code} not found")
        emoji = emoji_details[code]
        if emoji['name'] != f"flag: {country_name}":
            print("Error, name mismatch", emoji['name'], country_name)
        else:
            emoji['countryCode'] = country_code
            emoji['countryName'] = country_name


def main():
    data = web_fetch(UNICODE_URL).decode("utf8").split("\n")
    create_main_emoji_db(data)
    country_data = web_fetch(COUNTRY_SHORT_CODE_URL).decode("utf8")
    add_country_details(country_data)
    json.dump(emoji_details, open(OUTPUT_PATH + "/emoji_db.json", "w"), indent=4, sort_keys=False)
    json.dump(emoji_mappings, open(OUTPUT_PATH + "/emoji_names.json", "w"), indent=4, sort_keys=False)


if __name__ == "__main__":
    main()
