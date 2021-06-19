import colorsys

from MangoUI.utils.ColorOps import to_RGBAtuple, RGBAtuple_to_RGBAstr

def Hex_to_RGB(hexcolor):
    rgb = tuple(int(hexcolor.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
    return rgb

def visibleFontColor(hexcolor):
    rgb = Hex_to_RGB(hexcolor)
    weights = (0.299, 0.587, 0.114)

    weigted_sum = sum([rgb[i] * weights[i] for i in range(len(weights))])
    if weigted_sum > 150:
        return '#000000'
    else:
        return '#FFFFFF'

def brightnessAdjuster(color, scale = 2):
    rgba = to_RGBAtuple(color)
    h, l, s = colorsys.rgb_to_hls(*rgba[:3])

    rgbAdjusted = colorsys.hls_to_rgb(h, l * scale, s)
    if len(color) > 3:
        rgbAdjusted = rgbAdjusted + (rgba[3],)

    rgbAdjusted = tuple(int(i) for i in rgbAdjusted)
    rgbAdjusted = RGBAtuple_to_RGBAstr(rgbAdjusted)

    return rgbAdjusted

if __name__ == '__main__':
    rgbacolor = (122, 46, 126)
    rgb = brightnessAdjuster(rgbacolor, 0.5)
    print(rgb)