# Bundles all emojis rendered to PNG in zip archives, one archive for each resolution

import glob
import hashlib
import json
import os
import zipfile

version = json.load(open("../config.json"))['version']
BASE_PATH = os.path.dirname(__file__) + "/../../"
OUTPUT_PATH = os.path.normpath(BASE_PATH + "/output/")
PNG_PATH = os.path.normpath(BASE_PATH + "/output/noto_rendered")

OUTPUT_RESOLUTIONS = [128, 256, 512, 1024, 2048, 4096]

emoji_db_dict = {}


def main():
    for resolution in OUTPUT_RESOLUTIONS:
        cur_path = PNG_PATH + f"/{resolution}"
        filenames = [element for element in glob.glob(cur_path + "/**") if element.endswith(".png")]
        output_filename = OUTPUT_PATH + "/" + f'scistag_png_emojis_{resolution}_{version.replace(".", "_")}.zip'
        local_filename = f'scistag_png_emojis_{resolution}.zip'
        archive = zipfile.ZipFile(
            output_filename, "w",
            compression=zipfile.ZIP_DEFLATED)
        archive.writestr(f"LICENSE.md", open(BASE_PATH + "/LICENSE.md").read())
        archive.writestr(f"README.md", open(BASE_PATH + "/README.md").read())
        for element in filenames:
            data = open(element, "rb").read()
            archive.writestr(f"images/noto/{os.path.basename(element)}", data)
        archive.close()
        data = open(output_filename, 'rb').read()
        digest = hashlib.md5(data).hexdigest()
        new_entry = {"remoteFilename": os.path.basename(output_filename),
                     "localFilename": local_filename,
                     "md5": digest,
                     "size": len(data)}
        emoji_db_dict[str(resolution)] = new_entry
        print(new_entry)

    json.dump(emoji_db_dict, open(OUTPUT_PATH + "/emoji_png_db.json", "w"), indent=4)


if __name__ == "__main__":
    main()
