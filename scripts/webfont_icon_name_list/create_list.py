# Creates a dictionary to quickly find an icon in the MaterialDesign font by it's name
# Download the newest https WebFont pack from ://materialdesignicons.com/ and store it's scss/_variables.scss file
# in fonts/MaterialDesign.
# The output file will be stored in output/material_design_icon_names.json
import logging
import os
import json
import sys

SOURCE_FILE = os.path.dirname(__file__) + "/../../fonts/MaterialDesign/_variables.scss"
OUTPUT_FILENAME = os.path.normpath(
    os.path.dirname(__file__) + "/../../fonts/MaterialDesign/material_design_icon_names.json")
os.makedirs(os.path.dirname(OUTPUT_FILENAME), exist_ok=True)

icon_dictionary = {}


def main():
    line_data = open(SOURCE_FILE, "r").readlines()
    stripped = [element.lstrip("\t").lstrip(" ").rstrip("\n").rstrip(",") for element in line_data]
    elements = [element for element in stripped if element.startswith('"')]
    for element in elements:
        name, value = element.split(":")
        name = name[1:-1]  # remove quotation marks
        value = value.lstrip(" ")
        icon_dictionary[name] = f"{value}"
    json.dump(icon_dictionary, open(OUTPUT_FILENAME, "w"), indent=4)
    logging.info(f"Material icon dictionary create successfully and stored in {OUTPUT_FILENAME}")


if __name__ == "__main__":
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    logging.getLogger().setLevel(logging.INFO)
    main()
