import argparse
from copy import deepcopy
from typing import List
from math import sqrt
import json
from PIL import Image


def parse_args():
    parser = argparse.ArgumentParser(description='Auxiliar script to generate Cell-DEVS environments')

    parser.add_argument('-i', '--image', type=str, required=True, help='Input image path')
    parser.add_argument('-c', '--in_config', type=str, required=True, help='Base configuration file path')
    parser.add_argument('-p', '--palette', type=str, required=True, help='Cell state palette file path')
    parser.add_argument('-w', '--width', type=int, help='Width of cells of the resulting model')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output directory path')
    return parser.parse_args()


def compute_distance(a: List[int], b: List[int], dims: int = 3) -> float:
    return sqrt(sum((a[i] - b[i])**2 for i in range(dims)))


if __name__ == '__main__':
    args = parse_args()
    with open(args.palette) as f:
        colors = json.load(f)    # It contains all the colors to explore in the image and their value
    with open(args.in_config) as f:
        config = json.load(f)   # It contains the base configuration file to be filled

    output_dir = args.output

    # 1. Open image and resize to match Cell-DEVS environment
    im = Image.open(args.image)
    width, height = im.size
    cd_width = args.width
    cd_height = int(cd_width * (height / width))
    im_res = im.resize((cd_width, cd_height))
    print("Cell-DEVS model size: (%d, %d)" % (cd_height, cd_width))
    im_res.save("{}/in_pixel.png".format(output_dir))

    # 2. We start adding the first elements to the JSON file
    config['scenario']['shape'] = [cd_height, cd_width]
    config['scenario']['default_cell_type'] = colors['default']['cell_type']
    config['scenario']['default_state'] = colors['default']['state']
    # 3. We combine default and other colors into a palette object
    palette = [colors['default']]
    palette.extend([other for other in colors['others']])

    # Generation of the identifiers matrix
    im_res = im_res.convert('RGB')
    pixels = im_res.load()
    cells = list()

    for i in range(im_res.size[0]):
        for j in range(im_res.size[1]):
            best_color, distance = None, None
            for color in palette:
                difference = compute_distance(pixels[i, j], color['color'])
                if distance is None or difference < distance:
                    best_color, distance = color, difference
            pixels[i, j] = tuple(best_color['color'])
            if best_color != colors['default']:
                aux = deepcopy(best_color)
                cell_id = aux.pop('color')
                aux['cell_id'] = cell_id
                cells.append(aux)
    im_res.save("{}/out.png".format(output_dir))
    config['cells'] = cells
    with open("{}/config.json".format(output_dir), 'w') as f:
        json.dump(config, f, indent=4)
