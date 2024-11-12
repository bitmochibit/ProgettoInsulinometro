import colorsys


def scale_lightness(hex_str: str, scale_l) -> str:
    # Convert hexStr to rgb (tuple of 3 floats)
    rgb = [int(hex_str[i:i + 2], 16) / 255.0 for i in range(1, 6, 2)]
    h, l, s = colorsys.rgb_to_hls(*rgb)
    # manipulate h, l, s values and return as rgb
    new_rgb = colorsys.hls_to_rgb(h, min(1, l * scale_l), s=s)
    return "#" + "".join(f"{int(255 * x):02x}" for x in new_rgb)

def color_str_to_hex(color: str) -> int:
    return int(color[1:], 16)
