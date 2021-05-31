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