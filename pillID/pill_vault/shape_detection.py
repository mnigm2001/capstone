import cv2
import numpy as np
from .colour_detection import colour_detection
import base64
from openai import OpenAI

from PIL import Image

class shape_detection :
    def __init__(self,image_file):
        # self.image_path = image_file
        self.cv2_img = self.convert_to_cv2(image_file)
        # self.setup_image_params()
        self.preprocessing()
        self.find_contours()
        self.determine_shape()
        # self.encode_image()
        # self.detect_shape_gpt()
        # self.final_shape()

    def convert_to_cv2(self, image_file):
        # Read the image file in a PIL format
        pil_image = Image.open(image_file)
        pil_image = pil_image.convert('RGB')  # Ensure it's in RGB format

        # Convert the PIL image to a cv2 (OpenCV) image
        cv2_image = np.array(pil_image) 
        # Convert RGB to BGR (what OpenCV uses)
        cv2_image = cv2_image[:, :, ::-1].copy() 
        return cv2_image


    def setup_image_params(self):
        print(type(self.image_path))
        if(type(self.image_path) == str):
            print("if")
            self.cv2_img = cv2.imread(self.image_path)
        else:
            print("else")
            self.cv2_img = self.image_path
        self.H,self.W,_= self.cv2_img.shape

    def preprocessing(self):
        gray = cv2.cvtColor(self.cv2_img, cv2.COLOR_BGR2GRAY)

        # Preprocessing
        blurred = cv2.GaussianBlur(gray, (3,3), 0)
        # Setting All parameters 
        t_lower = 80  # Lower Threshold 
        t_upper = 150  # Upper threshold 
        aperture_size = 3 # Aperture size 

        self.edged = cv2.Canny(blurred, t_lower, t_upper,  
                        apertureSize=aperture_size)
    
    def find_contours(self):
        contours, _ = cv2.findContours(self.edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cnt, max_index = self.maxContour(contours)

        # get the bounding rect
        rect = cv2.minAreaRect(cnt)
        out = self.getSubImage(rect,self.cv2_img.copy())
        H,W,_= out.shape
       
        self.cropped_img = out[int(H/30):H-int(H/30):,int(W/10):W-int(W/10)]
        # cv2.imwrite('out.jpg', self.cropped_img)
        

        M = cv2.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

        self.test = self.cv2_img.copy()
        cv2.drawContours(
            image=self.test,
            contours=[cnt],
            contourIdx=-1,
            color=(0,255,0),
            thickness=2)
        # cv2.imwrite('detected_contour.jpg', self.test)
        # cv2.imshow('Output', self.test)
        # cv2.waitKey(0)
    
        self.pill_contour = max(contours, key=cv2.contourArea)

    def getSubImage(self, rect, src):
        # Get center, size, and angle from rect
        center, size, theta = rect
        # Convert to int 
        center, size = tuple(map(int, center)), tuple(map(int, size))
        # Get rotation matrix for rectangle
        M = cv2.getRotationMatrix2D( center, theta, 1)
        # Perform rotation on src image
        dst = cv2.warpAffine(src, M, src.shape[:2])
        out = cv2.getRectSubPix(dst, size, center)
        return out

    def maxContour(self, contours):
        cnt_list = np.zeros(len(contours))
        for i in range(0,len(contours)):
            cnt_list[i] = cv2.contourArea(contours[i])

        max_value = np.amax(cnt_list)
        max_index = np.argmax(cnt_list)
        cnt = contours[max_index]

        return cnt, max_index

    def determine_shape(self):
        perimeter = cv2.arcLength(self.pill_contour, True)
        approximation = cv2.approxPolyDP(self.pill_contour, 0.02 * perimeter, True)

        # Bounding rectangle
        x, y, w, h = cv2.boundingRect(self.pill_contour)

        # Determine the aspect ratio
        aspect_ratio = w / float(h)

        # Shape classification
        if len(approximation) > 15:
            self.shape = "Circle"
            
        elif 0.8 < aspect_ratio < 1.2:
            self.shape = "Circle"
        else:
            self.shape = "Oval" if aspect_ratio < 1.5 else "Oblong"
    
    def encode_image(self):
        #with open(self.image_path, "rb") as image_file:
        return base64.b64encode(self.image_path).decode('utf-8')
        
    def detect_shape_gpt(self):
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
                        {"type": "text", "text": "Given the following pill image, the list of possible shapes is:\nRound\nOval\nOblong\nEgg\n3 sided\n4 sided\nIn one word, select the shape that best represents this pill"},
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

        self.gbt_shape = r.choices[0].message.content
    
    def final_shape(self):
        if(self.gbt_shape!=self.shape):
            self.shape = self.gbt_shape



    
if __name__ == "__main__":
    print(__name__)

