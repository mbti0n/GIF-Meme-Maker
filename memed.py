#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont, ImageOps
import argparse, emoji
from datetime import datetime, timezone

arguments = argparse.ArgumentParser()
arguments.add_argument("--path", type=str, required=True, help="Path to the image.")
arguments.add_argument("--caption", type=str, help="GIF text caption. Default is \"caption\" if not specified.")
arguments.add_argument("--width", type=int, help="GIF width. Default is 720 if not specified.")
arguments.add_argument("--height", type=int, help="GIF height. Default is 600 if not specified.")

args = arguments.parse_args()
path = args.path
caption = args.caption
width = args.width
height = args.height

if caption == None:
    caption = "caption"
if width == None:
    width = 720
if height == None:
    height = 600

def create_image(width, height, caption, path):
    try:
        current = datetime.now(timezone.utc)
        timestamp = current.astimezone().strftime("%Y-%m-%d-%H-%M-%S")
        im = Image.new(mode="RGB", size=(width, height), color=(255, 255, 255))
        im2 = Image.new(mode="RGB", size=(width, height), color=(0, 0, 0))
        image2 = Image.open(path)
        text = ImageDraw.Draw(im)
        textFont = ImageFont.truetype("Oswald-Bold.ttf", 60)
        caption = emoji.demojize(caption)
        
        heightText = round(height / 20)
        text.text((width / 2, heightText), caption, fill=(0, 0, 0), font=textFont, anchor="ma", embedded_color=True)
        image2 = ImageOps.fit(image2, (width, height-heightText), centering=(0.3, 0.5))
        im.paste(image2, (0, 150))
        frames = []
        for i in range(51):
            out = Image.blend(im, im2, (1 - (0.02 * i)))
            frames.append(out)
        for i in range(40):
            frames.append(Image.blend(im, im2, 0))
        frames[0].save(f"memed-{timestamp}.gif", save_all=True, append_images=frames[1:], duration=40, loop=0)
    except Exception as e:
        print(e)

create_image(width, height, caption, path) 