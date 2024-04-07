import cv2
import numpy as np
import base64
from openai import OpenAI
import os, datetime
from PIL import Image

from django.core.files.uploadedfile import InMemoryUploadedFile

image_name = '1. APO White Oblong'
pre_processed_imgs_path = os.path.join('/home/mnigm2001/capstone/backend/imagerecog/pre_processed_imgs', image_name)


class shape_detection :
    def __init__(self, image_input):
        """
        Initializes the shape_detection class with either an image path or a cv2 image.
        
        :param image_input: Image path (str) or cv2 image (numpy.ndarray).
        """
        self.image_input = image_input
        self.setup_image_params()
        # The following methods are commented out for brevity
        # self.encode_image()
        # self.detect_shape_gpt()
        # self.final_shape()
    
    def find_shape(self):
        self.preprocessing()
        self.find_contours()
        self.determine_shape()

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
        # Check if the input is a string (path) or already an image (numpy array)
        if isinstance(self.image_input, str):
            self.cv2_img = cv2.imread(self.image_input)
        elif isinstance(self.image_input, np.ndarray):
            self.cv2_img = self.image_input
        elif isinstance(self.image_input, InMemoryUploadedFile):
            self.cv2_img = self.convert_to_cv2(self.image_input)
        else:
            raise ValueError("Image input must be a file path or a cv2 image.")

        self.H, self.W, _ = self.cv2_img.shape

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
        
        # self.save_image(self.edged, save_dir=pre_processed_imgs_path, prefix='shape_det')  # Saving the edge-detected image for review
    
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
            self.shape = "Round"
            
        elif 0.8 < aspect_ratio < 1.2:
            self.shape = "Round"
        else:
            self.shape = "Oval" if aspect_ratio < 1.5 else "Capsule/Oblong"
    
    def encode_image(self):
        #with open(self.image_path, "rb") as image_file:
        # return base64.b64encode(self.image_input).decode('utf-8')
        # Convert the cv2 image to a byte stream.
        _, buffer = cv2.imencode('.jpg', self.cv2_img)
        # Encode the byte stream to base64
        return base64.b64encode(buffer).decode('utf-8')
        
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
                        {"type": "text", "text": "Given the following pill image, the list of possible shapes is:\n \
                            ('Barrel', 'Barrel'), \
                            ('Capsule/Oblong', 'Capsule/Oblong'), \
                            ('Character-shape', 'Character-shape'), \
                            ('Egg-shape', 'Egg-shape'), \
                            ('Eight-sided', 'Eight-sided'), \
                            ('Oval', 'Oval'), \
                            ('Figure eight-shape', 'Figure eight-shape'), \
                            ('Five-sided', 'Five-sided'), \
                            ('Four-sided', 'Four-sided'), \
                            ('Gear-shape', 'Gear-shape'), \
                            ('Heart-shape', 'Heart-shape'), \
                            ('Kidney-shape', 'Kidney-shape'), \
                            ('Rectangle', 'Rectangle'), \
                            ('Round', 'Round'), \
                            ('Seven-sided', 'Seven-sided'), \
                            ('Six-sided', 'Six-sided'), \
                            ('Three-sided', 'Three-sided'), \
                            ('U-shape', 'U-shape'), \
                         \nIn one word, select the shape that best represents this pill"},
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


    def save_image(self, img, save_dir='/path/to/save/dir', prefix='processed_image'):
        os.makedirs(save_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.jpg"
        file_path = os.path.join(save_dir, filename)
        cv2.imwrite(file_path, img)
        print(f"Image saved to {file_path}")

    
if __name__ == "__main__":
    # print(__name__)
    file_path = "/home/mnigm2001/capstone/backend/imagerecog/pre_processed_imgs/1. APO White Oblong/0_original_text_closest_contours_cropped_1. APO White Oblong.jpg"
    file_path = "/home/mnigm2001/capstone/backend/imagerecog/pre_processed_imgs/4. 81 Blue Round/0_original_text_closest_contours_cropped_4. 81 Blue Round.jpg"
    file_path = "/home/mnigm2001/capstone/backend/imagerecog/pre_processed_imgs/2. HGH Biege Oblong Backwards/0_original_text_closest_contours_cropped_2. HGH Biege Oblong Backwards.jpg"

    obj = shape_detection(file_path)

    print("Shape = ", obj.shape)
    obj.detect_shape_gpt()
    print("gbt_shape = ", obj.gbt_shape)


