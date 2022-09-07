# Renders all noto emojis to PNG from low to high resolution

import glob
import io
import os.path

import PIL.Image
import cairosvg
import PIL
import multiprocessing

CPU_CORES = 32
BASE_PATH = os.path.dirname(__file__) + "/../../"
SVG_PATH = os.path.normpath(BASE_PATH + "/images/noto/emojis/svg")

OUTPUT_RESOLUTIONS = [128, 256, 512, 1024, 2048, 4096]


def render_svg(task):
    filename = task['filename']
    target_name = task['outputFilename']
    output_width = output_height = task['resolution']
    svg_data = open(filename, "rb").read()
    image_data = io.BytesIO()
    cairosvg.svg2png(svg_data, write_to=image_data, output_width=output_width, output_height=output_height)
    data = image_data.getvalue()
    png: PIL.Image = PIL.Image.open(io.BytesIO(data))
    with open(target_name, "wb") as output_file:
        output_file.write(image_data.getvalue())
    output_fn = target_name[0:-4] + ".png"
    png.save(output_fn, optimize=True, compression=100)


def main():
    pool = multiprocessing.Pool(CPU_CORES)

    for resolution in OUTPUT_RESOLUTIONS:
        output_path = os.path.normpath(BASE_PATH + f"/output/noto_rendered/{resolution}")
        os.makedirs(output_path, exist_ok=True)
        all_svgs = [element for element in glob.glob(SVG_PATH + "/**") if element.endswith(".svg")]
        tasks = []
        for cur_filename in all_svgs:
            output_fn = output_path + "/" + os.path.basename(cur_filename)[0:-3] + "png"
            task = {"filename": cur_filename, "outputFilename": output_fn,
                    "resolution": resolution}
            tasks.append(task)
        pool.map(render_svg, tasks)


if __name__ == "__main__":
    main()
