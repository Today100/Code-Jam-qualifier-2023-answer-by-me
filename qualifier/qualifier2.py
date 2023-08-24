
from PIL import Image

def valid_input(image_size: tuple[int, int], tile_size: tuple[int, int], ordering: list[int]) -> bool:
    """
    Return True if the given input allows the rearrangement of the image, False otherwise.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once.
    """
    
    x = image_size[0]/tile_size[0]
    y = image_size[1]/tile_size[1]
    if x.is_integer() and y.is_integer() and x*y == len(ordering) and len(set(ordering))==len(ordering):
        return True
    else: 
        return False


def rearrange_tiles(image_path: str, tile_size: tuple[int, int], ordering: list[int], out_path: str) -> None:
    """
    Rearrange the image.

    The image is given in `image_path`. Split it into tiles of size `tile_size`, and rearrange them by `ordering`.
    The new image needs to be saved under `out_path`.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once. If these conditions do not hold, raise a ValueError with the message:
    "The tile size or ordering are not valid for the given image".
    """

    img = Image.open(image_path)

    w, h = img.size
    # if img.size == (1104, 1600):
    #     f = valid_input((h, w), tile_size, ordering)
    # else:
    f = valid_input(img.size, tile_size, ordering)
    if f:
        dic_of_img = {}
        ind = 0
        for hi in range(0, h, tile_size[1]):
            for wi in range(0, w, tile_size[0]):

                box = (wi, hi, wi+tile_size[0], hi+tile_size[1])

                part_img = img.crop(box)

                dic_of_img[ind] = part_img
                ind += 1

        img.close()
        dst = Image.new(img.mode, size=img.size)
        new_ind = 0

        for hi in range(0, h, tile_size[1]):
            for wi in range(0, w, tile_size[0]):
                if new_ind > max(ordering):
                    new_ind = 0
                dst.paste(dic_of_img[ordering[new_ind]], (wi, hi))

                new_ind += 1

        dst.save('./images/user_output.png')


    else:
        raise ValueError("The tile size or ordering are not valid for the given image")
    