import csv
import boto3
import cv2
import matplotlib.pyplot as plt
#from colour_detection import colour_detection

class image_recognition:

    def __init__(self,image):
        self.image = image
        self.setup_image_params()
        self.setup_client()
        self.detect_labels()
        self.crop_image()
        self.detect_text()

    def setup_image_params(self):
        with open (self.image, 'rb') as source_image:
            self.image_bytes = source_image.read()

        self.cv2_img = cv2.imread(self.image)
        self.H,self.W,_= self.cv2_img.shape
    
    def setup_client(self):
        with open('test_accessKeys.csv','r') as input:
            next(input)
            reader = csv.reader(input)

            for line in reader:
                access_key_id = line[0]
                secret_access_key = line[1]

        self.client = boto3.client('rekognition',
                      aws_access_key_id = access_key_id,
                      aws_secret_access_key = secret_access_key,
                      region_name='us-east-2',)
        
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

            #frame = cv2.rectangle(self.cv2_img, (x_,y_),(x_+ w_,y_+h_), (0, 255, 0), 2)

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

        for label in self.detected_text ['TextDetections']:
                if(len(label['DetectedText']) > 0):
                    self.imprint = label ['DetectedText']
                    break

if __name__ == "__main__":
    image = 'Pills/APOB10_oval.jpg'

    test = image_recognition(image)
    print("Detected Text:", test.imprint)

    # if(test.pill_detected):
    #     test_colour = colour_detection(test.cropped_img)
    #     print(test_colour.colour)

    


