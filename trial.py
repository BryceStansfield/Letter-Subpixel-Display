from PIL import Image
from project_common import *

stencil = StencilCreator("CompressedSubpixelLetterFormat.png")

colours = [(255,0,0), (0,255,0), (0,0,255)]    # [red, green, blue]
coloured_letters = []
for colour in colours:
    coloured_letters.append([stencil.convert_to_colour(i, colour) for i in range(stencil.num_letters)]) # Replace with class thing

stencil_size = (stencil.letter_width * stencil.num_letters, stencil.letter_width,)

new_image = Image.new('RGB', (stencil_size[0]*100, stencil_size[1]*500,), (0,0,0))

for y in range(500):
    for x in range(stencil.num_letters*100):
        new_image.paste(coloured_letters[x%len(colours)][x%26], (stencil.letter_width*x, stencil_size[1]*y,))
    print(y)

save_image(new_image, 'shading_test_coloured.png')