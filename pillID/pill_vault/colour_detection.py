import cv2
import numpy as np
import pandas as pd
import base64
from openai import OpenAI
from django.conf import settings
import os

class colour_detection:
    def __init__(self, image_input):
        """
        Initializes the colour_detection class with either an image path or a cv2 image.
        
        :param image_input: Image path (str) or cv2 image (numpy.ndarray).
        """
        # Determine if the input is a path or an image and load or assign accordingly
        if isinstance(image_input, str):
            self.image = cv2.imread(image_input)
        elif isinstance(image_input, np.ndarray):
            self.image = image_input
        else:
            raise ValueError("Image input must be a file path or a cv2 image.")
        
        self.setup_image_params()
        self.setup_csv()
        self.avg_all_pixels()

    def setup_image_params(self):
        self.H, self.W, _ = self.image.shape

    def increase_brightness(self, img, value=30):
        # Increase the brightness of the image
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
        # Calculate the average color of all pixels after increasing brightness
        self.image_bright = self.increase_brightness(self.image.copy())
        avg_color_per_row = np.average(self.image_bright, axis=0)
        avg_pixel = np.average(avg_color_per_row, axis=0)
        
        r, g, b = avg_pixel
        self.colour = self.detect_colour(r, g, b)

    def detect_colour(self, r, g, b):
        # Find the closest color name based on RGB values
        minimum = 10000
        for i in range(len(self.csv)):
            d = abs(r - int(self.csv.loc[i, "R"])) + abs(g - int(self.csv.loc[i, "G"])) + abs(b - int(self.csv.loc[i, "B"]))
            if d <= minimum:
                minimum = d
                colour = self.csv.loc[i, "color_name"]
        
        return colour
    
    def encode_image(self):
        #with open(self.image_path, "rb") as image_file:
        # return base64.b64encode(self.image_input).decode('utf-8')
        # Convert the cv2 image to a byte stream.
        _, buffer = cv2.imencode('.jpg', self.image)
        # Encode the byte stream to base64
        return base64.b64encode(buffer).decode('utf-8')
        
    def detect_colour_gpt(self):
        image_url = f"data:image/jbeg;base64,{self.encode_image()}"

        gpt = OpenAI(
            organization="org-1YE6y1OohJmJIe8W3Xifd2RW",
            api_key="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",
        )
        r = gpt.chat.completions.create(
            model = 'gpt-4-vision-preview',
            messages = [
                {
                    "role" : "user",
                    "content" : [
                        {"type": "text", "text": "Given the following pill image, the list of possible colors is:\n  ('White', 'White'), \
        ('Beige', 'Beige'), \
        ('Black', 'Black'), \
        ('Blue', 'Blue'), \
        ('Brown', 'Brown'), \
        ('Clear', 'Clear'), \
        ('Gold', 'Gold'), \
        ('Gray', 'Gray'), \
        ('Green', 'Green'), \
        ('Maroon', 'Maroon'), \
        ('Orange', 'Orange'), \
        ('Peach', 'Peach'), \
        ('Pink', 'Pink'), \
        ('Purple', 'Purple'), \
        ('Red', 'Red'), \
        ('Tan', 'Tan'), \
        ('Yellow', 'Yellow'), \
        ('Beige & Red', 'Beige & Red'), \
        ('Black & Green', 'Black & Green'), \
        ('Black & Teal', 'Black & Teal'), \
        ('Black & Yellow', 'Black & Yellow'), \
        ('Blue & Brown', 'Blue & Brown'), \
        ('Blue & Gray', 'Blue & Gray'), \
        ('Blue & Green', 'Blue & Green'), \
        ('Blue & Orange', 'Blue & Orange'), \
        ('Blue & Peach', 'Blue & Peach'), \
        ('Blue & Pink', 'Blue & Pink'), \
        ('Blue & White', 'Blue & White'), \
        ('Blue & White Specks', 'Blue & White Specks'), \
        ('Blue & Yellow', 'Blue & Yellow'), \
        ('Brown & Clear', 'Brown & Clear'), \
        ('Brown & Orange', 'Brown & Orange'), \
        ('Brown & Peach', 'Brown & Peach'), \
        ('Brown & Red', 'Brown & Red'), \
        ('Brown & White', 'Brown & White'), \
        ('Brown & Yellow', 'Brown & Yellow'), \
        ('Clear & Green', 'Clear & Green'), \
        ('Dark & Light Green', 'Dark & Light Green'), \
        ('Gold & White', 'Gold & White'), \
        ('Gray & Peach', 'Gray & Peach'), \
        ('Gray & Pink', 'Gray & Pink'), \
        ('Gray & Red', 'Gray & Red'), \
        ('Gray & White', 'Gray & White'), \
        ('Gray & Yellow', 'Gray & Yellow'), \
        ('Green & Orange', 'Green & Orange'), \
        ('Green & Peach', 'Green & Peach'), \
        ('Green & Pink', 'Green & Pink'), \
        ('Green & Purple', 'Green & Purple'), \
        ('Green & Turquoise', 'Green & Turquoise'), \
        ('Green & White', 'Green & White'), \
        ('Green & Yellow', 'Green & Yellow'), \
        ('Lavender & White', 'Lavender & White'), \
        ('Maroon & Pink', 'Maroon & Pink'), \
        ('Orange & Turquoise', 'Orange & Turquoise'), \
        ('Orange & White', 'Orange & White'), \
        ('Orange & Yellow', 'Orange & Yellow'), \
        ('Peach & Purple', 'Peach & Purple'), \
        ('Peach & Red', 'Peach & Red'), \
        ('Peach & White', 'Peach & White'), \
        ('Pink & Purple', 'Pink & Purple'), \
        ('Pink & Red Specks', 'Pink & Red Specks'), \
        ('Pink & Turquoise', 'Pink & Turquoise'), \
        ('Pink & White', 'Pink & White'), \
        ('Pink & Yellow', 'Pink & Yellow'), \
        ('Red & Turquoise', 'Red & Turquoise'), \
        ('Red & White', 'Red & White'), \
        ('Red & Yellow', 'Red & Yellow'), \
        ('Tan & White', 'Tan & White'), \
        ('Turquoise & White', 'Turquoise & White'), \
        ('Turquoise & Yellow', 'Turquoise & Yellow'), \
        ('White & Blue Specks', 'White & Blue Specks'), \
        ('White & Red Specks', 'White & Red Specks'), \
        ('White & Yellow', 'White & Yellow'), \
        ('Yellow & Gray', 'Yellow & Gray'), \
        ('Yellow & White', 'Yellow & White'), \
                         In one word, select the colour that best represents this pill"},
                        {
                            "type" : "image_url",
                            "image_url": {
                                "url": image_url,
                                "detail" : "low"
                            },
                        }
                    ]
                }
            ],
            max_tokens=300,
        )

        self.gbt_colour = r.choices[0].message.content
    
if __name__ == "__main__":
    # print(__name__)
    file_path = "/home/mnigm2001/capstone/backend/imagerecog/pre_processed_imgs/1. APO White Oblong/0_original_text_closest_contours_cropped_1. APO White Oblong.jpg"
    file_path = "/home/mnigm2001/capstone/backend/imagerecog/pre_processed_imgs/4. 81 Blue Round/0_original_text_closest_contours_cropped_4. 81 Blue Round.jpg"
    # file_path = "/home/mnigm2001/capstone/backend/imagerecog/pre_processed_imgs/2. HGH Biege Oblong Backwards/0_original_text_closest_contours_cropped_2. HGH Biege Oblong Backwards.jpg"

    obj = colour_detection(file_path)
    print("Color = ", obj.colour)

    obj.detect_colour_gpt()
    print("gbt_colour = ", obj.gbt_colour)
       