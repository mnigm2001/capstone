import cv2
import csv
import numpy as np
import pandas as pd

class colour_detection:

    def __init__(self,image,cx,cy):
         self.image = image
         self.cx = cx
         self.cy = cy
         self.setup_image_params()
         self.setup_csv()
         self.detect_colour()


    def setup_image_params(self):
        y,x,_= self.image.shape
        if(self.cx ==0):
            y = int(y/2)
            x = int(x/2)
        else:
            y = self.cy
            x = self.cx
        b,g,r = self.image[y,x]
        self.b = int(b)
        self.g = int(g)
        self.r = int(r)
        print(r,b,g)

    def setup_csv(self):
        # Reading csv file with pandas and giving names to each column
        index=["color","color_name","hex","R","G","B"]
        self.csv = pd.read_csv('colors.csv', names=index, header=None)

    def detect_colour(self):
        minimum = 10000
        for i in range(len(self.csv)):
            d = abs(self.r- int(self.csv.loc[i,"R"])) + abs(self.g- int(self.csv.loc[i,"G"]))+ abs(self.b- int(self.csv.loc[i,"B"]))
            if(d<=minimum):
                minimum = d
                self.colour = self.csv.loc[i,"color_name"]

if __name__ == "__main__":
    print(__name__)

