# Creates an archive of binary test data required for SciStag's unit tests

import json
import zipfile
import glob
import os

OUTPUT_PATH = os.path.dirname(__file__) + "/../../output"
version = json.load(open("../config.json"))['version']
OUTPUT_ARCHIVE = OUTPUT_PATH + f"/scistag_test_data_{version.replace('.', '_')}.zip"
INPUT_PATH = os.path.normpath(os.path.dirname(__file__) + "/../../test_data")


def main():
    print("Building test data archive...")
    extensions = {".md", ".jpg", ".png"}
    filenames = glob.glob(INPUT_PATH + "/**", recursive=True)
    filenames = [element for element in filenames if os.path.splitext(element)[1] in extensions]
    zip_archive = zipfile.ZipFile(OUTPUT_ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9)
    for element in filenames:
        data = open(element, "rb").read()
        rel_filename = element[len(INPUT_PATH) + 1:]
        zip_archive.writestr(rel_filename, data)
    zip_archive.close()
    print("Done")


if __name__ == "__main__":
    main()
