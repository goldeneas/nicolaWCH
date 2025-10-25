import framebuf
import util

class Image:
    """
        Wraps around an int array representing an image.
        An image has to be converted to a bit array
        where 0 is black and 1 is white.

        :param int_list: the list of ints which will be used to draw the image.
            each line in the array maps to a row of the image.

        Preconditions:
            - foreach row in int_list: bit_length(row) has to be the same

    """

    def __init__(self, int_list: list[int]):
        self._int_list = int_list
    
    def place(self, x: int, y: int, scale: int, display: framebuf.Framebuffer):
        bit_length = util.bit_length(self._int_list[0])

        for j, line in enumerate(self._int_list):
            for i in range(0, bit_length):
                bit = (line >> (bit_length - 1 - i)) & 1
                display.rect(x + i * scale, y + j * scale, 1 * scale, 1 * scale, bit, True)
