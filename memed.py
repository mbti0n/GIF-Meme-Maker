#!/usr/bin/env python3
from PIL import Image, ImageFont, ImageOps
import argparse, emoji, json, os
from datetime import datetime, timezone
from pilmoji import Pilmoji

# CLI Arguments
arguments = argparse.ArgumentParser()
arguments.add_argument("--path", "-P", type=str, required=True, help="Path to the image.")
arguments.add_argument("--caption", "-C", type=str, help="GIF text caption. Default is \"caption\" if not specified.")
arguments.add_argument("--width", "-W", type=int, help="GIF width. Default is 720 if not specified.")
arguments.add_argument("--height", "-H", type=int, help="GIF height. Default is 600 if not specified.")
arguments.add_argument("--output", "-O", type=str, help="Output directory. You will receive a prompt to specify the output directory if not specified.")

# Arguments variables
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

# Function to get outputPath
def outputPath(path):
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

# Function to create the GIF file
def createGIF(width, height, caption, path, output):
    try:
        current = datetime.now(timezone.utc)
        timestamp = current.astimezone().strftime("%Y-%m-%d-%H-%M-%S")
        print("Generating GIF file...")
        im = Image.new(mode="RGB", size=(width, height), color=(255, 255, 255))
        im2 = Image.new(mode="RGB", size=(width, height), color=(0, 0, 0))
        image2 = Image.open(path)
        textFont = ImageFont.truetype("Oswald-Bold.ttf", 60)
        caption = emoji.emojize(caption, language='alias')
        
        heightText = round(height / 20)
        # NOTE: Pilmoji integration is done thanks to Google Antigravity CLI 
        with Pilmoji(im) as pilmoji:
            pilmoji.text((width / 2, heightText), caption, fill=(0, 0, 0), font=textFont, anchor="ma")
        image2 = ImageOps.fit(image2, (width, height-heightText), centering=(0.3, 0.5))
        im.paste(image2, (0, 150))
        frames = []
        for i in range(51):
            out = Image.blend(im, im2, (1 - (0.02 * i)))
            frames.append(out)
        for i in range(40):
            frames.append(Image.blend(im, im2, 0))
        frames[0].save(f"{output}/memed-{timestamp}.gif", save_all=True, append_images=frames[1:], duration=40, loop=0)
        print(f"Saved! GIF file saved to {output}/memed-{timestamp}.gif")
    except Exception as e:
        print(e)

# Run
createGIF(width, height, caption, path, outputPath(output))