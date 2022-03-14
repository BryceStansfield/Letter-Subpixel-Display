from PIL import Image
import os
import itertools

# Image I/O
image_folder_path = 'images'
def open_image(image_path: str) -> Image.Image:
    return Image.open(os.path.join(image_folder_path, image_path))

def save_image(image: Image.Image, path: str) -> None:
    image.save(os.path.join(image_folder_path, path))

class StencilCreator:
    letter_width = 5
    num_letters = 26

    def __init__(self, letter_format_path: str, background_colour: tuple[int, int, int] = (0,0,0,), foreground_colour: tuple[int,int,int] = (255,255,255,)):
        """ Initialize a StencilCreator with the format in images/`letter_format_path`,
            Where each letter is repainted with `background_colour` as its background,
            And `foreground_colour` as its forground colour.

            (Important) attributes:
            self.letters = a list of PIL images, s.t. self.letters[0] = an image of 'a' e.t.c.
            StencilCreator.letter_width = the assumed width of stencil images.
            StencilCreator.num_letters = the assumed number of letters.
        """

        if background_colour == foreground_colour:
            raise Exception("Forground and background colour should differ")

        self.foreground_colour = foreground_colour
        self.background_colour = background_colour

        letter_stencil = open_image(letter_format_path)
        letter_stencil = letter_stencil.convert('RGB')

        self.letters = [letter_stencil.crop((i*self.letter_width,0,(i+1)*self.letter_width,5,))
                    for i in range(self.num_letters)]
        
        # Determining the colour scaling
        def pixels_in_letter(letter: Image.Image) -> int:
            count = 0
            for (y,x) in itertools.product(range(letter.height), range(letter.width)):
                if letter.getpixel((x,y,)) == (0,0,0,):
                    count += 1
            return count

        self.pixels_per_letter = [pixels_in_letter(letter) for letter in self.letters]
        self.min_pixels = min(self.pixels_per_letter)
        
        # Setting the foreground and background colour
        for letter in self.letters:
            for (y,x) in itertools.product(range(letter.height), range(letter.width)):
                cur_pixel = letter.getpixel((x,y,))
                if cur_pixel == (0,0,0,):   # Foreground
                    letter.putpixel((x,y,), foreground_colour)
                else:                       # Background
                    letter.putpixel((x,y,), background_colour)
    
    def paint_letter_with_colour(self, letter: Image.Image, colour: tuple[int, int, int]):
        """Returns the letter `letter` but with its foreground painted 'colour'
        NOTE: This is known to be slow.
        """
        for x,y in itertools.product(range(letter.size[0]), range(letter.size[1])):
            if letter.getpixel((x,y,)) == self.foreground_colour:
                letter.putpixel((x,y,), colour)
        
        return letter

    def convert_to_colour(self, letter_index: int, colour: tuple[int, int, int]) -> Image:
        """ Returns the letter with index `letter_index` (e.g. a=0, b=1, ...)
            But with its foreground painted `colour`
        """
        letter = self.letters[letter_index].copy()

        return self.paint_letter_with_colour(letter, colour)

    def convert_to_colour_scaled(self, letter_index: int, colour: tuple[int, int, int]) -> Image:
        """ Like convert_to_colour, but scales pixel intensity s.t. all letters have the same average brightness
            This implicitly assumes the background is black.
        """
        letter = self.letters[letter_index].copy()
        pixels = self.pixels_per_letter[letter_index]

        scaling_factor = self.min_pixels/pixels
        scaled_colour = (round(colour[0]*scaling_factor), round(colour[1]*scaling_factor), round(colour[2]*scaling_factor),)

        return self.paint_letter_with_colour(letter, scaled_colour)