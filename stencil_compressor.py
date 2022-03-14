from PIL import Image
import os
from project_common import *

letter_size = (5,5)
num_letters = 26
image_folder_path = 'images'
original_stencil = open_image("SubpixelLetterFormat.bmp")

compressed_stencil = Image.new('1', (letter_size[0]*26, letter_size[1],))

for i in range(num_letters):
    compressed_stencil.paste(original_stencil.crop((i*(letter_size[0]+1),0,(i+1)*(letter_size[0]+1),5,)),
                            (i*letter_size[0], 0))
save_image("CompressedSubpixelLetterFormat.png")