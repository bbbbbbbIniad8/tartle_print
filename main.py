from PIL import Image, ImageOps
import numpy as np
import turtle
import math

class TurtlePrint():
    def __init__(self, image, resize=None, faster=False):
        self.first_pos = turtle.pos()
        self.img_path = image
        self.faster = faster
        
        self.img_data = Image.open(self.img_path).convert("RGB")
        self.img_data = ImageOps.exif_transpose(self.img_data)
        if resize != None:
            self.img_data = self.img_data.resize(resize)
        self.width, self.height = self.img_data.size
        turtle.colormode(cmode=255)

    # Move the turtle to the output start point
    def turtle_prepare(self):
        turtle.penup()
        theta_rad = math.atan(self.height / self.width)
        theta_deg = math.degrees(theta_rad)
        turtle.left(180-theta_deg)
        # The coordinates when the function is called will be the center of the image.
        turtle.forward(((self.width/2)**2 + (self.height/2)**2)**(1/2))
        turtle.left(theta_deg)
        turtle.forward(1)
        turtle.left(180)
        turtle.pendown()

        turtle.speed('fastest')

    # Move the turtle to the next line
    def turtle_move_nextline(self, count):
        turtle.penup()
        turtle.left(-90 if count % 2 == 0 else 90)
        turtle.forward(1)
        turtle.left(-90 if count % 2 == 0 else 90)
        turtle.forward(1)
    
    def turtle_return(self):
        turtle.tracer(True) if self.faster == True else None
        turtle.penup()
        turtle.goto(self.first_pos)
        turtle.forward(self.width//2)
        turtle.pendown()


    def run(self):
        self.turtle_prepare()
        # Based on the loaded image data RGB array, we draw the image using a double for loop
        for y in range(self.height):
            turtle.tracer(False) if self.faster == True else None
            turtle.pendown()
            total_combo = 0
            for x in range(self.width):
                adjust_x = x + total_combo
                direction = 1
                if y % 2 == 1:
                    adjust_x = (self.width-1) - x - total_combo
                    direction = -1
                if  0 <= adjust_x and adjust_x < self.width:
                    # ink settings
                    turtle.pencolor(self.img_data.getpixel((adjust_x, y)))
                    forward_distance = 1
                    adjust = adjust_x + (forward_distance * direction)
                    # Contiguous arrays with the same RGB values ​​will draw consecutive lines.
                    while(0 <= adjust and adjust < self.width):
                        if np.any(self.img_data.getpixel((adjust_x, y)) != self.img_data.getpixel((adjust, y))):
                            break
                        forward_distance += 1
                        adjust += direction
                    total_combo += forward_distance - 1
                    turtle.forward(forward_distance) 
                else:
                    print(adjust_x)
                    break
            self.turtle_move_nextline(y)
        
        self.turtle_return()

# turtle.shape("turtle")
TurtlePrint("img_file/INNU.png",resize = (64,64), faster = True).run()

input("end")
