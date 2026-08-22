#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont, ImageOps
import argparse, emoji, json, os
from datetime import datetime, timezone

arguments = argparse.ArgumentParser()
arguments.add_argument("--path", "-P", type=str, required=True, help="Path to the image.")
arguments.add_argument("--caption", "-C", type=str, help="GIF text caption. Default is \"caption\" if not specified.")
arguments.add_argument("--output", "-O", type=str, help="Directory of the output GIF. You will be prompted to specify the output directory if not specified.")
arguments.add_argument("--width", "-W", type=int, help="GIF width. Default is 720 if not specified.")
arguments.add_argument("--height", "-H", type=int, help="GIF height. Default is 600 if not specified.")

args = arguments.parse_args()
path = args.path
caption = args.caption
width = args.width
height = args.height
output = args.output

if caption == None:
    caption = "caption"
if width == None:
    width = 720
if height == None:
    height = 600
    
def output_path(path):
    if not os.path.exists('config.json'):
        with open("config.json", "w") as f:
            f.write('{"destination": ""}') 
    with open('config.json', 'r') as f:
        configList = json.load(f)
    if path == None:
        destinationPath = input("Specify the output path: ")
    else:
        destinationPath = path
    configList["destination"] = destinationPath

    with open("config.json", "w+") as addJson:
        addJson.write(json.dumps(configList))
        
    return configList["destination"]

def create_image(width, height, caption, path, output):
    try:
        current = datetime.now(timezone.utc)
        timestamp = current.astimezone().strftime("%Y-%m-%d-%H-%M-%S")
        print("Processing caption...")
        im = Image.new(mode="RGB", size=(width, height), color=(255, 255, 255))
        im2 = Image.new(mode="RGB", size=(width, height), color=(0, 0, 0))
        image2 = Image.open(path)
        text = ImageDraw.Draw(im)
        textFont = ImageFont.truetype("Oswald-Bold.ttf", 60)
        caption = emoji.demojize(caption)
        
        heightText = round(height / 20)
        text.text((width / 2, heightText), caption, fill=(0, 0, 0), font=textFont, anchor="ma", embedded_color=True)
        print("Processing image...")
        image2 = ImageOps.fit(image2, (width, height-heightText), centering=(0.3, 0.5))
        im.paste(image2, (0, 150))
        print("Generating GIF file...")
        frames = []
        for i in range(51):
            out = Image.blend(im, im2, (1 - (0.02 * i)))
            frames.append(out)
        for i in range(40):
            frames.append(Image.blend(im, im2, 0))
        frames[0].save(f"{output}/memed-{timestamp}.gif", save_all=True, append_images=frames[1:], duration=40, loop=0)
        print("Saved!")
    except Exception as e:
        print(e)

create_image(width, height, caption, path, output_path(output))