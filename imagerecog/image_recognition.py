import csv
import boto3
import cv2
import json
from PIL import Image
from colour_detection import colour_detection
from shape_detection import shape_detection

class image_recognition:

    def __init__(self,image):
        self.image = image
        self.pill_detected = False
        self.blur = 9
        self.setup_image_params()
        self.setup_client()
        self.detect_pill()

    def detect_pill(self):
        while (self.pill_detected == False):
            self.blur +=2
            self.Preprocessing(self.blur)
            self.detect_labels()
            self.crop_image()
            self.detect_text()

            if (self.blur > 30):
                break

    def setup_image_params(self):
        self.cv2_img = cv2.imread(self.image)
        self.H,self.W,_= self.cv2_img.shape

        # with open (self.image_processed, 'rb') as source_image:
        #     self.image_bytes = source_image.read()

    def setup_client(self):
        access_key_id = None
        secret_access_key = None
        
        with open('test_accessKeys.csv', 'r') as input:
            # next(input)  # Skip the header, if present
            reader = csv.reader(input)
            for line in reader:
                print(line)
                access_key_id, secret_access_key = line[:2]
                break  # Assuming only one line of credentials
        
        if access_key_id and secret_access_key:
            self.client = boto3.client('rekognition',
                                    aws_access_key_id=access_key_id,
                                    aws_secret_access_key=secret_access_key,
                                    region_name='us-east-2',)
        else:
            raise ValueError("AWS credentials not found in the CSV file.")


    # def setup_client(self):
    #     with open('test_accessKeys.csv','r') as input:
    #         next(input)
    #         reader = csv.reader(input)
    #         print(reader, dir(reader))
    #         for line in reader:
    #             print(line)
    #             access_key_id = line[0]
    #             secret_access_key = line[1]

    #     self.client = boto3.client('rekognition',
    #                   aws_access_key_id = access_key_id,
    #                   aws_secret_access_key = secret_access_key,
    #                   region_name='us-east-2',)
    
    def Preprocessing(self,blur=9):
        blurred = cv2.GaussianBlur(self.cv2_img, (blur,blur), 0)
        # cv2.imwrite('cv2_img_processed.jpg', blurred)
        self.image_processed = cv2.imencode(".jpg", blurred)[1].tobytes()
        self.image_bytes = self.image_processed
        
    def detect_labels(self):
        self.detected_labels = self.client.detect_labels(Image={'Bytes': self.image_bytes},
                                MaxLabels=10,
                                Features=["GENERAL_LABELS"],
                                Settings={"GeneralLabels": {"LabelInclusionFilters":["Pill"]}}
                                )
        
    def crop_image(self):
        self.class_names=[]
        for label in self.detected_labels['Labels']:
            if(len(label['Instances']) > 0):
                name = label['Name']
                if name not in self.class_names:
                    self.class_names.append(name)

                for instance in label ['Instances']:
                    conf = instance['Confidence']
                    w = instance['BoundingBox']['Width']
                    h = instance['BoundingBox']['Height']
                    x = instance['BoundingBox']['Left']
                    y = instance['BoundingBox']['Top']

                    x_ = int(x * self.W)
                    y_ = int(y * self.H)
                    h_ = int(h * self.H)
                    w_ = int(w * self.W)

                    #frame = cv2.rectangle(self.cv2_img, (x_,y_),(x_+ w_,y_+h_), (0, 255, 0), 1)
        
        if(len(self.class_names) > 0):
            self.pill_detected = True
            self.cropped_img = self.cv2_img[y_:y_+h_, x_:x_+w_]
            
        else:
            self.pill_detected = False




    def detect_text(self):
        if(self.pill_detected):
            self.detected_text = self.client.detect_text(Image={'Bytes': cv2.imencode('.jpg', self.cropped_img)[1].tobytes()})
        else:
            self.detected_text = self.client.detect_text(Image={'Bytes': cv2.imencode('.jpg', self.cv2_img)[1].tobytes()})
       
        self.imprint = ""
        for label in self.detected_text ['TextDetections']:
                if(len(label['DetectedText']) > 0):
                    self.imprint = label ['DetectedText']
                    break

if __name__ == "__main__":
    image = 'Pills/APO500_Oblong.JPG'
    result = {}
    # "Pill Detected":"",
    #     "Imprint":"",
    #     "Colour",""
    #     "Shape":""

    test = image_recognition(image)

    result["Pill Detected"] = test.pill_detected
    result["Imprint"] = test.imprint

    if(result["Pill Detected"]):
        print("Pill Detected")
        shape_test = shape_detection(test.cropped_img)
    else:
        print("Pill not detected")
        shape_test = shape_detection(image)
    result["Shape"] = shape_test.shape

    
    test_colour = colour_detection(shape_test.cropped_img)
    result["Colour"] = test_colour.colour

    result_json = json.dumps(result,indent=2)
    print(result_json)



    


