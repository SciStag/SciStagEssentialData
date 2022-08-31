# Build scripts which automatically created the zip archives containing the essential files for SciStag which are
# bundled with the module itself as well as optionally downloadable packages such as pre-rendered SVGs for systems
# where Cairo is not available.

import io
import logging
import os
import glob
import sys
import time
import zipfile
import json
from typing import List

version = json.load(open("../config.json"))['version']
BASE_PATH = os.path.normpath(os.path.dirname(__file__) + "/../../") + "/"
OUTPUT_DIR = BASE_PATH + "/output"


def matches_any(filename, extensions):
    """
    Returns if the filename matches any of the extensions provided in extensions
    :param filename: The filename to check
    :param extensions: A list of extensions in th form [".txt", ".png"] etc.
    :return: True if any extension matches
    """
    basename = os.path.basename(filename)
    return any([basename.endswith(extension) for extension in extensions])


def store_files(all_files, archive_name):
    """
    Store all files found in the archive
    :param all_files: List of tuples of all source files and their target base directory in the zip archive
    :param archive_name: The filename of the output zip archive
    :return: The total size of the archive
    """
    target_stream = io.BytesIO()
    zip_archive = zipfile.ZipFile(target_stream, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9)
    for element in all_files:
        src_name, tar_dir = element
        tar_name = tar_dir + src_name
        with open(BASE_PATH + src_name, "rb") as src_file:
            data = src_file.read()
        zip_archive.writestr(tar_name, data)
    zip_archive.close()
    with open(archive_name, "wb") as output_file:
        zip_data = target_stream.getvalue()
        output_file.write(zip_data)
    return len(zip_data)


def create_file_list(data_paths) -> List:
    """
    Creates a file list of all files to be stored in the archive
    :param data_paths: List of tuples of the form (source_path, additional_archive_path, [file_ending_1, file_ending_2])
    :return: A list of files the relative target directory in the archive
    """
    bpl = len(BASE_PATH)
    all_files = []
    for path in data_paths:
        src_path = BASE_PATH + path[0]
        tar_path = path[1]
        file_extensions = path[2]
        new_files = [(element[bpl:], tar_path) for element in
                     glob.glob(src_path + "**", recursive=True) if matches_any(element, file_extensions)]
        all_files += new_files
    return all_files


def build_archive(data_paths_essential, output_dir, output_filename_essential):
    start_time = time.time()
    logging.info(f"Creating archive {output_filename_essential}....")
    all_files = create_file_list(data_paths_essential)
    total_size_mb = store_files(all_files, archive_name=f"{output_dir}/{output_filename_essential}") / (2 ** 20)
    logging.info(
        f"Finished creation of {output_filename_essential} in {time.time() - start_time:0.1f}s.\n"
        f"{len(all_files)} files stored.\n"
        f"Archive size: {total_size_mb:0.1f} MB")


def main():
    """
    Script entry point
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # --- essential archive with emojis and flags in ~128x128 ---
    data_paths_essential = [("fonts/", "", [".txt", ".ttf", ".json"]),
                            ("images/noto/cpngs/", "", [".png", ".txt", ".md"])]
    output_filename_essential = f"scistag_essentials_{version.replace('.', '_')}.zip"
    build_archive(data_paths_essential, OUTPUT_DIR, output_filename_essential)
    # --- svg archive for emojis ---
    data_paths_svg = [("images/noto/emojis/", "", [".svg", ".txt", ".md"]),
                      ("images/noto/flags/waved-svg/", "", [".svg", ".txt", ".md"])]
    output_filename_rendered = f"scistag_vector_emojis_{version.replace('.', '_')}.zip"
    build_archive(data_paths_svg, OUTPUT_DIR, output_filename_rendered)


if __name__ == "__main__":
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    logging.getLogger().setLevel(logging.INFO)
    main()
