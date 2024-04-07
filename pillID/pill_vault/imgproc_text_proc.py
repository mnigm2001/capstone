
import cv2
import numpy as np
from imgproc_utils import image_to_bytes


# -------------------- AWS Rekognition Text Detection -------------------- #

def detect_text_with_aws_rekognition(image, client):
    """
    Detects text in an image using AWS Rekognition.
    
    :param image: The image to process.
    :param client: The initialized AWS Rekognition client.
    :return: A tuple (raw detection response, detected imprint text).
    """
    response = client.detect_text(Image={'Bytes': image_to_bytes(image)})
    imprint = next((item['DetectedText'] for item in response['TextDetections'] if item['Type'] == 'LINE'), None)
    
    return response, imprint

# -------------------- Post processing of TEXT -------------------- #
def extract_text_boxes(text_detections):
    """
    Extracts bounding box information from AWS Rekognition detect_text response.
    
    :param text_detections: The 'TextDetections' field from the AWS Rekognition detect_text response.
    :return: A list of dictionaries, each representing a bounding box of detected text.
    """
    text_boxes = []
    for detection in text_detections:
        box = detection['Geometry']['BoundingBox']
        text_boxes.append({
            'Left': box['Left'],
            'Top': box['Top'],
            'Width': box['Width'],
            'Height': box['Height']
        })
    return text_boxes

def extract_label_boxes(label_detections):
    """
    Extracts bounding box information from AWS Rekognition detect_text response.
    
    :param text_detections: The 'TextDetections' field from the AWS Rekognition detect_text response.
    :return: A list of dictionaries, each representing a bounding box of detected text.
    """
    label_boxes = []
    for label in label_detections:
        if label['Name'] == 'Pill':
            for instance in label['Instances']:
                box = instance['BoundingBox']
                label_boxes.append({
                    'Left': box['Left'],
                    'Top': box['Top'],
                    'Width': box['Width'],
                    'Height': box['Height']
                })
    return label_boxes



def draw_text_boxes_on_image(image, text_boxes, color=(0, 255, 0)):
    """
    Draws bounding boxes around detected text on a copy of the image.

    :param image: The original image as a NumPy array.
    :param text_boxes: A list of dictionaries, each representing a bounding box of detected text.
    :return: Image copy with drawn bounding boxes.
    """
    # Create a copy of the original image to draw on
    image_copy = image.copy()

    # Image dimensions
    img_height, img_width = image.shape[:2]

    for box in text_boxes:
        # Calculate the coordinates of the bounding box
        left = int(box['Left'] * img_width)
        top = int(box['Top'] * img_height)
        width = int(box['Width'] * img_width)
        height = int(box['Height'] * img_height)

        # Calculate the bottom right point of the rectangle
        right = left + width
        bottom = top + height

        # Draw the rectangle on the image
        cv2.rectangle(image_copy, (left, top), (right, bottom), color, 2)

    return image_copy


# -------------------- Contour Based Processing -------------------- #

def find_closest_contours_to_text(cv2_img, contours, text_boxes, image_width, image_height, draw=False):
    """
    Find the contours closest to the text imprints and optionally draw them on a copy of the original image.
    
    :param cv2_img: The original image as a numpy array.
    :param contours: List of contours detected in the image.
    :param text_boxes: List of bounding boxes for detected text.
    :param image_width: Width of the original image.
    :param image_height: Height of the original image.
    :param draw: Boolean indicating whether to draw contours on the image copy.
    :return: A copy of the original image with the closest contours drawn if draw is True,
             and the list of the closest contours.
    """
    
    image_area = image_width * image_height

    # Calculate the proportion of the text area to the image area
    text_area = sum([(box['Width'] * box['Height']) for box in text_boxes]) * image_area
    text_area_proportion = text_area / image_area
    print("Text area:", text_area_proportion)

    # Determine the number of contours to consider based on text area proportion
    if text_area_proportion < 0.01:
        num_contours = len(contours) // 50  # smaller proportion, fewer contours
    elif (text_area_proportion < 0.03):
         num_contours = len(contours) // 30  
    elif text_area_proportion < 0.05:
        num_contours = len(contours) // 10  # medium proportion
    else:
        num_contours = len(contours) // 5  # larger proportion, more contours

    text_center = np.mean([((box['Left'] + box['Width'] / 2), 
                            (box['Top'] + box['Height'] / 2)) for box in text_boxes], axis=0)
    
    text_center_x = int(text_center[0] * image_width)
    text_center_y = int(text_center[1] * image_height)
    
    contour_distances = []
    for cnt in contours:
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
        else:
            continue
        distance = np.sqrt((cx - text_center_x) ** 2 + (cy - text_center_y) ** 2)
        contour_distances.append((cnt, distance))
    
    contour_distances.sort(key=lambda x: x[1])
    
    closest_contours = [cnt for cnt, _ in contour_distances[:num_contours]]

    if draw:
        img_copy = cv2_img.copy() if draw else cv2_img
        for cnt in closest_contours:
            cv2.drawContours(img_copy, [cnt], -1, (0, 255, 0), 2)
        return img_copy, closest_contours
    
    return cv2_img, closest_contours



def get_combined_bounding_box(text_detections):
    """
    Combines multiple text detection bounding boxes into one that encompasses all of them.

    :param text_detections: List of text detection dictionaries with bounding box information.
    :return: A single dictionary with combined bounding box coordinates.
    """
    # Initialize variables to store the max and min values of the bounding box edges
    min_left = float('inf')
    min_top = float('inf')
    max_right = 0
    max_bottom = 0

    # Loop through each detection and calculate the extremes of the combined bounding box
    for detection in text_detections:
        box = detection['Geometry']['BoundingBox']
        left = box['Left']
        top = box['Top']
        right = left + box['Width']
        bottom = top + box['Height']

        # Update the edges of the combined bounding box
        if left < min_left:
            min_left = left
        if top < min_top:
            min_top = top
        if right > max_right:
            max_right = right
        if bottom > max_bottom:
            max_bottom = bottom

    # Calculate the combined width and height
    combined_width = max_right - min_left
    combined_height = max_bottom - min_top

    # Create the combined bounding box dictionary
    combined_box = {
        'Left': min_left,
        'Top': min_top,
        'Width': combined_width,
        'Height': combined_height
    }

    return combined_box