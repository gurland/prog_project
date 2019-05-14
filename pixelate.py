from PIL import Image, ImageDraw


WIDTH, HEIGHT = 1, 1


def get_avg_color(px, cur_x, cur_y):
    pixel_count = WIDTH * HEIGHT

    rgb = [0, 0, 0]

    for x in range(WIDTH):
        for y in range(HEIGHT):
            color = px[cur_x+x, cur_y+y]

            # rgb[0] += {r|g|b}/pixel_count
            rgb = list(map(lambda color_pair: color_pair[0] + color_pair[1], zip(rgb, color)))

    return tuple(map(lambda z: int(z/pixel_count), rgb))


def pixelate(im, chunk_size=5, mode=2):
    # 1.jpg - slow mode, 2 - fast mode
    width, height = im.size
    result_image = None

    if mode == 1:
        result_image = Image.new('RGB', im.size, (255, 255, 255))
        px = im.load()

        for x in range(int(width / chunk_size)):
            for y in range(int(height / chunk_size)):
                cur_x, cur_y = x * chunk_size, y * chunk_size
                box = (cur_x, cur_y, cur_x + chunk_size, cur_y + chunk_size)
                avg_rgb = get_avg_color(px, cur_x, cur_y)

                result_image.paste(avg_rgb, box)

    elif mode == 2:
        small_image = im.resize((int(width/chunk_size), int(height/chunk_size)), resample=Image.BILINEAR)
        result_image = small_image.resize(im.size, Image.NEAREST)

    return result_image
