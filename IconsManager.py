import os
import json
import subprocess
from PIL import Image, ImageOps

from ColorsUtils import visibleFontColor

def getSafeFilename(filename):
    safefilename = filename.replace(' ', '')
    safefilename = safefilename.replace('-', '')
    safefilename = safefilename.rstrip('.')
    safefilename = safefilename.replace('.', 'dot')
    safefilename = safefilename.replace('&', 'and')
    safefilename = safefilename.replace('\'', '')
    safefilename = safefilename.replace('+', 'plus')
    safefilename = safefilename.replace('!', '')

    return safefilename

def mapIcons():
    with open('simple-icons/simple-icons.json', 'r') as simpleiconsdata:
        iconsdata = json.load(simpleiconsdata)['icons']

    iconsLUT = {}

    with open('simple-icons/notfound.txt', 'w') as notfoundfile:
        for icon in iconsdata:
            notfound = True
            for iconfile in os.listdir('simple-icons/icons'):
                if iconfile.lower().replace(' ', '') == getSafeFilename(icon['title'].lower()) + '.svg':
                    iconitem = {}
                    iconitem['color'] = '#' + icon['hex']
                    iconitem['file'] = iconfile
                    iconitem['href'] = 'https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/' + iconfile
                    iconsLUT[icon['title']] = iconitem
                    notfound = False
                    break
            if notfound:
                notfoundfile.write(icon['title'])
                notfoundfile.write('\n')

    with open('simple-icons/iconsLUT.json', 'w') as iconsLUTfile:
        json.dump(iconsLUT, iconsLUTfile, indent = 4)

    print('Found', len(iconsdata), 'icons')
    print('Successfully mapped', len(iconsLUT), 'icons')
    print('Couldn\'t map', len(iconsdata) - len(iconsLUT), 'icons')

def convertSVG2PNG(filename, dest):
    bashCommand = f'rsvg-convert -o {dest} {filename}'
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

def invertIMG(img):
    return img.point(lambda p: 255 - p)

def invertPNG(filename):
    img = Image.open(filename)
    img = img.convert('RGBA')
    r, g, b, a = img.split()
    r, g, b = map(invertIMG, (r, g, b))
    img = Image.merge(img.mode, (r, g, b, a))
    img.save(filename)

def generatePNGs():
    with open('simple-icons/iconsLUT.json', 'r') as iconsLUTFile:
        iconsLUT = json.load(iconsLUTFile)
    for icon in iconsLUT:
        filename = iconsLUT[icon]['file']
        if os.path.isfile('simple-icons/iconspng/' + filename.rstrip('.svg') + '.png'):
            continue

        convertSVG2PNG('simple-icons/icons/' + filename, 'simple-icons/iconspng/' + filename.rstrip('.svg') + '.png')
        col = iconsLUT[icon]['color']
        if visibleFontColor(col) == '#FFFFFF':
            invertPNG('simple-icons/iconspng/' + filename.rstrip('.svg') + '.png')

if __name__ == '__main__':
    generatePNGs()
