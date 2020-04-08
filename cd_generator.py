#!/usr/bin/env python
# coding: utf-8

import argparse
import os
from PIL import Image

COLOR_BACKGROUND = (0, 0, 0, 255)
COLOR_OBSTACLE = (255, 255, 255, 255)

BACKGROUND_ID = 0
OBSTACLE_ID = 1


def parse_args():
    parser = argparse.ArgumentParser(description='Auxiliar script to generate Cell-DEVS environments')

    parser.add_argument('-a', '--avoid_separation', type=str, help='Avoid separating the obstacles')
    parser.add_argument('-i', '--in_file', type=str, required=True, help='Input image')
    parser.add_argument('-b', '--back_color', type=str, default="255,255,255", help='Background color to separate obstacles')
    parser.add_argument('-d', '--delay', type=str, default=1000, help='Default delay')
    parser.add_argument('-n', '--neighborhood', type=str, default="vn", help='Neighborhood type (moore, vn, emoore, evn)')
    parser.add_argument('-m', '--top_name', type=str, help='Name of the resulting files')
    parser.add_argument('-o', '--out_path', type=str, default="out/", help='Output path')
    parser.add_argument('-r', '--rules_file', type=str, default="templates/default_rules.inc", help='File with the rules to include in the main file')
    parser.add_argument('-t', '--tolerance', type=int, default=10, help='Tolerance when separating background')
    parser.add_argument('-w', '--width', type=int, help='Width of the resulting model')

    return parser.parse_args()


def almost_equal(v1, v2, ediff=20):
    for i in range(len(v1)):
        if abs(v1[i] - v2[i]) > ediff:
            return False
    return True


if __name__ == '__main__':
    args = parse_args()

    back_color = list(map(int, args.back_color.split(",")))
    if not args.top_name:
        args.top_name = os.path.splitext(os.path.basename(args.in_file))[0]

    os.makedirs(os.path.join(args.out_path, args.top_name), exist_ok=True)

    im = Image.open(args.in_file)
    width, height = im.size

    cd_width = args.width
    cd_height = int(cd_width * (height / width))
    im_res = im.resize((cd_width, cd_height))
    print("Cell-DEVS model size: (%d, %d)" % (cd_height, cd_width))

    # Generation of the identifiers matrix
    pixels = im_res.load()
    mat_id = []

    for i in range(im_res.size[0]):
        mat_id.append([])
        for j in range(im_res.size[1]):
            if almost_equal(pixels[i, j][:3], back_color[:3], args.tolerance):
                pixels[i, j] = COLOR_BACKGROUND
                mat_id[-1].append(BACKGROUND_ID)
            else:
                pixels[i, j] = COLOR_OBSTACLE
                mat_id[-1].append(OBSTACLE_ID)
        
    im_res.save(os.path.join(args.out_path, args.top_name, args.top_name + ".png"))


    # Generation of initial values file (.val)
    with open(os.path.join(args.out_path, args.top_name, args.top_name + ".val"), "w") as out:
        for i in range(len(mat_id)):
            for j in range(len(mat_id[i])):
                if mat_id[i][j] == OBSTACLE_ID:
                    line = "(%d, %d) = %d\n" % (j, i, OBSTACLE_ID)
                    out.write(line)


    # Generation of main file from template (.ma)
    with open("templates/template.ma", "r") as template:
        ma = template.read()

    with open("templates/neighbors_%s.inc" % args.neighborhood, "r") as nei_template:
        neighborhood = nei_template.read()

    with open(args.rules_file, "r") as rules_template:
        rules = rules_template.read()

    neighborhood = neighborhood.replace("id", args.top_name)

    ma = ma.format(name=args.top_name,
                   width=cd_width,
                   height=cd_height,
                   delay=args.delay,
                   initial_value=BACKGROUND_ID,
                   val_file=args.top_name + ".val",
                   neighbors=neighborhood)

    with open(os.path.join(args.out_path, args.top_name, args.top_name + ".ma"), "w") as out:
        out.write(ma)
        out.write(rules)


    # Generation of palette file (.pal)
    pal_content = ""
    pal_line = "[%d;%d] %d %d %d\n"

    pal_content += pal_line % ((BACKGROUND_ID, BACKGROUND_ID + 1) + COLOR_BACKGROUND[:3])
    pal_content += pal_line % ((OBSTACLE_ID, OBSTACLE_ID + 1) + COLOR_OBSTACLE[:3])

    with open(os.path.join(args.out_path, args.top_name, args.top_name + ".pal"), "w") as out:
        out.write(pal_content)

