# Script to wrap GitHub emoji names to simple dictionary.
# The result will be stored in data/emoji/markdown_emoji_names.json

import json
import os

NOTO_PATH = "images/noto/cpngs/"
BASE_PATH = os.path.dirname(__file__) + "/../../"
OUTPUT_FILENAME = BASE_PATH + '/data/emoji/markdown_emoji_names.json'

# load original data
data = json.load(open("emoji_names_org.json", "r"))

# result data
markdown_emoji_names = {}
data: dict
missed = 0
found = 0

for key, url in data.items():
    code = url.split("/")[-1].split(".")[0]
    code: str
    code = code.replace("-", "_")
    exists = os.path.exists(BASE_PATH + NOTO_PATH + "emoji_u" + code.lower() + ".png")
    if not exists:  # only stored emojis we also support
        print("Could not find", code, url)
        missed += 1
    else:
        markdown_emoji_names[key] = code.upper()
        found += 1

print(f"Found {found}, missed {missed}")
print("Storing data")

# Store data file
json.dump(markdown_emoji_names, open(OUTPUT_FILENAME, "w"), indent=4, sort_keys=False)
