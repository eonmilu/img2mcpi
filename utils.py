import os.path
import re
import json
import math
from PIL import Image

def scaleImageTo(name, max_size):
    raw_image = Image.open(name)
    raw_image.thumbnail(max_size, Image.ANTIALIAS)
    return raw_image

def findBestMatch(r, g, b, averages):
    best_match_id = "undefined"
    best_diff = 255 + 255 + 255
    curr_diff = 0
    r_diff, g_diff, b_diff = 0, 0, 0

    for i in averages:
        r_diff = abs(i["rgb"][0] - r)
        g_diff = abs(i["rgb"][1] - g)
        b_diff = abs(i["rgb"][2] - b)
        curr_diff = r_diff + g_diff + b_diff

        if best_diff > curr_diff:
            best_diff = curr_diff
            best_match_id = i["id"]

    print(best_match_id.split(":"))

    return best_match_id.split(":")

def configExists(path):
    return os.path.isfile(path)

def createConfig(path):
    cfg = []
    with open("materials.txt", "r") as materials:
        for line in materials:
            image_name, true_id = getLineProps(line)
            image = Image.open("./blocks/"+image_name)
            loaded_image = image.load()

            width, height = image.size
            r, g, b = getAverageColor(width, height, loaded_image)

            block_info = {"name": image_name, "id": true_id, "rgb": (int(r), int(g), int(b))}
            cfg.append(block_info)

    with open(path, "w") as file:
        file.write(json.dumps(cfg))

def readConfig(path):
    with open(path, "r") as conf:
        return json.loads(conf.read())

def getLineProps(line):
    line_values = line.split(",")
    image_name = re.findall(r"(?<=,)[^,]*\.png", line)[0]

    true_id = ""
    primary_id = line_values[3]
    secondary_id = line_values[4]

    if secondary_id == "-1":
        true_id = primary_id
    else:
        true_id = primary_id+":"+secondary_id

    return image_name, true_id

def getAverageColor(x, y, image):
    r, g, b = 0, 0, 0
    count = 0
    for s in range(x):
        for t in range(y):
            rgb = image[s, t]
            r += rgb[0] # Red
            g += rgb[1] # Blue
            b += rgb[2] # Green

            count += 1
    return ((r/count), (g/count), (b/count))
