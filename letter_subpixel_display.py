from PIL import Image
from project_common import *

# Stencil setup
stencil = StencilCreator("CompressedSubpixelLetterFormat.png")
word = 'bryce'

# Duplicating the image, but using letters as rgb subpixels
test_image = open_image("test_image.png")
test_image = test_image.convert("RGB")

new_image = Image.new('RGB', (test_image.width*stencil.letter_width*3, test_image.height*stencil.letter_width*3,))

for i, (y,x) in enumerate(itertools.product(range(test_image.height), range(test_image.width))):
    r_letter_index = ord(word[(i*3)%len(word)]) - ord('a')
    g_letter_index = ord(word[(i*3+1)%len(word)]) - ord('a')
    b_letter_index = ord(word[(i*3+2)%len(word)]) - ord('a')

    pixel = test_image.getpixel((x,y,))
    r_letter = stencil.convert_to_colour(r_letter_index, (pixel[0], 0, 0,))
    g_letter = stencil.convert_to_colour(g_letter_index, (0, pixel[1], 0,))
    b_letter = stencil.convert_to_colour(b_letter_index, (0, 0, pixel[2],))

    for j in range(0, 3):
        new_image.paste(r_letter,
                        ((3*x)*stencil.letter_width, (3*y+j)*stencil.letter_width,))
        new_image.paste(g_letter,
                        ((3*x+1)*stencil.letter_width, (3*y+j)*stencil.letter_width,))
        new_image.paste(b_letter,
                        ((3*x+2)*stencil.letter_width, (3*y+j)*stencil.letter_width,))

save_image(new_image, 'test_image_subpixel_converted.png')