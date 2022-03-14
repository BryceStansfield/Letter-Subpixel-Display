from PIL import Image
from project_common import *
import itertools

# Stencil Setup
stencil = StencilCreator("CompressedSubpixelLetterFormat.png")
word = 'bryce'

# Duplicating the image, with one letter per pixel
test_image = open_image("test_image.png")
test_image = test_image.convert("RGB")
new_image = Image.new('RGB', (test_image.width*stencil.letter_width, test_image.height*stencil.letter_width,))


for i, (y,x) in enumerate(itertools.product(range(test_image.height), range(test_image.width))):
    letter_index = ord(word[i%len(word)]) - ord('a')

    new_image.paste(stencil.convert_to_colour(letter_index, test_image.getpixel((x,y,))),
                    (x*stencil.letter_width, y*stencil.letter_width,))

save_image(new_image, 'test_image_converted.png')