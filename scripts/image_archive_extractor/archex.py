# Helper tool which helps extracting images downloaded in zip archives to a local directory.
# All extracted images are numbered and name like their archive with a global file index
# Afterwards duplicated are detected and removed.

import argparse
import glob
import io
import os
import shutil
import sys
import zipfile


def extract_all(archive_filenames, output_path):
    """
    Extracts all images in all archives listed and stores them numerated in output_path
    :param archive_filenames: A list of zip archive filenames containing PNGs
    :param output_path: The target path
    """
    image_counter = 0
    for archive_name in archive_filenames:
        read_data = open(archive_name, "rb").read()
        source = io.BytesIO(read_data)
        archive = zipfile.ZipFile(source, "r")
        image_filenames = [element for element in archive.namelist() if element.endswith(".png")]
        cleaned_archive_name = os.path.basename(archive_name)[0:-4]
        if cleaned_archive_name.endswith(")"):
            if '(' in cleaned_archive_name:
                cleaned_archive_name = cleaned_archive_name[0:cleaned_archive_name.index('(')]
        cleaned_archive_name.rstrip(" ")
        for cur_image_filename in image_filenames:
            data = archive.read(cur_image_filename)
            with open(f"{output_path}/{cleaned_archive_name}_{image_counter:04d}.png", "wb") as outfile:
                outfile.write(data)
            image_counter += 1
        archive.close()
    print(f"{image_counter} images successfully extracted")


def clean_duplicates(output_path):
    """
    Removes duplicates of accidentally twice downloaded archives
    :param output_path: The path to which the images were extracted
    :return:
    """
    print(f"Removing duplicates...")
    images = [element for element in glob.glob(output_path + "/**") if element.endswith(".png")]
    if len(images) <= 1:
        return
    for index, element in enumerate(images[:-1]):
        if not os.path.exists(element):
            continue
        own_size = os.path.getsize(element)
        for comp_index, comp_element in enumerate(images[index + 1:]):
            if comp_element is None or not os.path.exists(comp_element):
                continue
            other_size = os.path.getsize(comp_element)
            if own_size == other_size:
                matches = open(element, "rb").read() == open(comp_element, "rb").read()
                if matches:
                    print(f"Removing duplicate {os.path.basename(comp_element)}")
                    os.remove(comp_element)
                    images[comp_index] = None


def main():
    parser = argparse.ArgumentParser(
        description='Image archive extractor',
        usage='''archex <path> [<args>]
        The most commonly used commands are:
            archex /home/scistag/downloaded_archives
        ''')
    parser.add_argument('path', help='Subcommand to run')
    args = parser.parse_args(sys.argv[1:])
    path = args.path
    archive_filenames = glob.glob(path + "/**")
    archive_filenames = [element for element in archive_filenames if element.endswith(".zip")]
    output_path = path + "/exported/"
    shutil.rmtree(output_path, ignore_errors=True)
    os.makedirs(output_path, exist_ok=True)
    extract_all(archive_filenames, output_path)
    clean_duplicates(output_path)
    print(f"Done")


if __name__ == "__main__":
    main()
