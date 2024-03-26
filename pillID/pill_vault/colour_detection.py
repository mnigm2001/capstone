import pandas as pd
import numpy as np
import cv2
from django.conf import settings
import os

class colour_detection:

    def __init__(self,image):
         self.image = image
         self.setup_image_params()
         self.setup_csv()
         self.avg_all_pixels()


    def setup_image_params(self):
        self.H,self.W,_= self.image.shape

    def increase_brightness(self, img, value=30):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value

        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return img

    def setup_csv(self):
        # Reading csv file with pandas and giving names to each column
        index=["color","color_name","hex","R","G","B"]
        color_csv_path = os.path.join(settings.PILL_VAULT_DIR, 'resources/colors.csv')
        self.csv = pd.read_csv(color_csv_path, names=index, header=None)

    def avg_all_pixels(self):
            self.image_bright = self.increase_brightness(self.image.copy())
            avg_color_per_row = np.average(self.image_bright, axis=0)
            avg_pixel = np.average(avg_color_per_row, axis=0)
    
            r,g,b = avg_pixel
            self.colour = self.detect_colour(r,g,b)


    def detect_colour(self,r,g,b):
        minimum = 10000
        for i in range(len(self.csv)):
            d = abs(r- int(self.csv.loc[i,"R"])) + abs(g- int(self.csv.loc[i,"G"]))+ abs(b- int(self.csv.loc[i,"B"]))
            if(d<=minimum):
                minimum = d
                colour = self.csv.loc[i,"color_name"]
            
        return colour

if __name__ == "__main__":
    print(__name__)

