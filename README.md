# GIF-Meme-Maker
A simple Discord-style text-and-image fade in GIF generator.

## Installation
### Clone this repository
``` bash
git clone https://github.com/mbti0n/GIF-Meme-Maker && cd GIF-Meme-Maker
```

### Make the script execuable
``` bash
chmod +x setup.sh
```

### Install to PATH (plus required pip libraries)
``` bash
./setup.sh
```

## Usage
```
memed [-h] --path PATH [--caption CAPTION] [--width WIDTH] [--height HEIGHT]
```

### Arguments
|Command|Type|Description|
|---|---|---|
|-h, --help|N/A|Help message|
|--path <path/to/image>|String|Path to the image. **(REQUIRED)**|
|--caption <some_caption>|String|GIF text caption. Default is "caption" if not specified.|
|--width <width>|Integer|GIF width. Default is 720 if not specified.|
|--height <height>|Integer|GIF height. Default is 600 if not specified.|

## Roadmap
- [ ] GUI version
- [ ] Emoji support for caption
- [ ] Customizable fonts for caption
