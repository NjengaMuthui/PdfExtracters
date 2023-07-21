from PIL import Image
import pytesseract
from directory import getJpgFiles

def convert_black_to_white(image_path):
    # Open the image
    image = Image.open(image_path)
    print("Opening {}".format(image_path))

    # Convert the image to RGB if it's not already
    image = image.convert("RGB")

    # Get the pixel data from the image
    pixels = image.load()

    # Iterate over each pixel and check if it's black
    
    width, height = image.size
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            if (not (g > r and g > b)) or r==g==b==0:  # Check if the pixel is black
                pixels[x, y] = (255, 255, 255)  # Convert black to white

    # Save the modified image
    #image.save(output_path)
    output = ''
    lines = pytesseract.image_to_string(image).split("\n")
    for line in lines:
        if len(line) > 2:

            match line[:2]:
                case 'A)':
                    output += '\"A\",'
                case 'B)':
                    output += '\"B\",'
                case 'C)':
                    output += '\"C\",'
                case 'D)':
                    output += '\"D\",'            
    return output+'\n'

# Usage example

#print(convert_black_to_white('imgs/org/ECQB question bank-0010.jpg'))


answers =''
for img in getJpgFiles("imgs/org/"):
    answers += convert_black_to_white(img)

with open("txt/answers.txt",'w') as outfile:
    outfile.write(answers)