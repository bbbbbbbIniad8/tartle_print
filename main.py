from PIL import Image
import numpy as np
import turtle

class TurtlePrint:
    def __init__(self,image,faster):
        self.first_pos = turtle.pos()
        self.img_path = image
        self.faster = faster

    def img_prosessing(self):
        # Image loading
        img_data = Image.open(self.img_path).convert("RGBA").transpose(Image.ROTATE_90)
        self.width, self.height = img_data.size
        
        # Analyze the image pixel by pixel and store the RGB values ​​of each pixel in a list
        self.image_array = np.array(img_data, dtype=np.uint8)
        self.image_array[..., 3] = 255 

    # Move the turtle to the output start point
    def turtle_prepare(self):
        turtle.shape("turtle")
        turtle.penup()
        turtle.left(45)
        # The coordinates when the function is called will be the center of the image.
        turtle.forward(((self.width / 2) ** 2 + (self.height / 2) ** 2) ** (1 / 2)) 
        turtle.left(45)
        turtle.forward(1)
        turtle.left(90)
        turtle.pendown()

        turtle.speed('fastest')

    # Move the turtle to the next line
    def turtle_move_nextline(self):
            turtle.penup()
            turtle.left(90)
            turtle.forward(1)
            turtle.tracer(True) if self.faster == True else None
            turtle.left(90)
            turtle.tracer(False) if self.faster == True else None
            turtle.forward(self.height)
            turtle.left(180)
            turtle.tracer(True) if self.faster == True else None

    def run(self):
        self.img_prosessing()
        self.turtle_prepare()
        
        # Based on the loaded image data RGB array, we draw the image using a double for loop
        for Y in range(self.width):
            turtle.tracer(False) if self.faster == True else None
            turtle.pendown()
            total_combo = 0
            for X in range(self.height):
                AX = X + total_combo
                if AX < self.height:
                    # ink settings
                    RED = self.image_array[AX ,Y ,0]/255.0 
                    GREEN = self.image_array[AX ,Y ,1]/255.0
                    BLUE = self.image_array[AX ,Y ,2]/255.0
                    turtle.pencolor(RED,GREEN,BLUE)

                    forward_distance = 1
                    # Contiguous arrays with the same RGB values ​​will draw consecutive lines.
                    while(AX + forward_distance < self.height):
                        if np.any(self.image_array[AX,Y] != self.image_array[AX + forward_distance,Y]):
                            break
                        total_combo += 1
                        forward_distance += 1
                    turtle.forward(forward_distance) 
                else:
                    break

            self.turtle_move_nextline()
        turtle.tracer(True) if self.faster == True else None

        turtle.penup()
        turtle.right(180)
        turtle.goto(self.first_pos)
        turtle.forward(self.width//2)
        turtle.pendown()

# turtle.setup(width=800, height=600)

TurtlePrint("img_file/0x7bcat.png",faster = True).run()

input("end")
