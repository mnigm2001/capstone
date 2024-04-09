
import os
import cv2
import numpy as np
import re

from .imgproc_utils import save_image, get_exponent, load_image, convert_to_cv2, image_to_bytes, find_most_recurring_number_or_none
from .imgproc_aws_rekog import setup_aws_client
from .imgproc_img_mnpltion import crop_to_contours, crop_image_largest_contour, crop_image_around_label
from .imgproc_text_proc import detect_text_with_aws_rekognition, extract_text_boxes, find_closest_contours_to_text, draw_text_boxes_on_image, extract_label_boxes, get_combined_bounding_box
from .imgproc_procs_ops import preprocess_image, compute_contours, find_largest_image, find_closest_label_box, find_covering_label_box

from .imgproc_colour_detection import colour_detection
from .imgproc_shape_detection import shape_detection

SAVE_ORIG_TEXT_IMGS = True # Save the initial image with text detections and bounding boxes
SAVE_ORIG_LABEL_IMGS = True
SAVE_CLOSEST_CONTOURS_IMGS = True # Save the image with the closest contours to the text imprints
SAVE_LABEL_IMGS = True
SAVE_TEXT_IMGS = True
SAVE_LABEL_BOX_IMGS = True
SAVE_TEXT_BOX_IMGS = True
SAVE_EDGES_IMGS = True

RUN_ALL_TESTS = True
TEST_IMG_DIR = '/home/mnigm2001/capstone/backend/imagerecog/Pills'
# PRE_PROCESSED_IMGS_DIR = '/home/mnigm2001/capstone/backend/imagerecog/pre_processed_imgs'
PRE_PROCESSED_IMGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pre_processed_imgs')


def detect_labels(image_bytes, client):
    detected_labels = client.detect_labels(Image={'Bytes': image_bytes},
                            MaxLabels=10,
                            Features=["GENERAL_LABELS"],
                            Settings={"GeneralLabels": {"LabelInclusionFilters":["Pill"]}}
                            )
    return detected_labels

def process_img_text(cv2_img, client, draw_text_boxes=False):
    # Detect text in the cropped image using AWS Rekognition
    text_result, imprints = detect_text_with_aws_rekognition(cv2_img, client)

    if text_result['TextDetections']:
        text_boxes = extract_text_boxes(text_result['TextDetections']) # Extract bounding boxes of detected text
        if draw_text_boxes:
            img_with_text_boxes = draw_text_boxes_on_image(cv2_img, text_boxes)
            return text_result, text_boxes, img_with_text_boxes
        return text_result, text_boxes, None
    else:
        return None, None, None
    

def crop_image_around_text(cv2_img, contours, text_boxes, img_width, img_height):
    # Find the closest contours to the text imprints
    # clustered_img, closest_contours = find_closest_contours_to_text(cv2_img, contours, text_boxes, img_width, img_height, len(contours)//10)
    clustered_img, closest_contours = find_closest_contours_to_text(cv2_img, contours, text_boxes, img_width, img_height)
    # Crop the image to the area covering the closest contours to the text
    cropped_clustered_img, cropped_img_coordinates = crop_to_contours(clustered_img, closest_contours)
    return closest_contours, clustered_img, cropped_clustered_img, cropped_img_coordinates


def process_img_labels(cv2_img, client, draw_label_boxes=False):
    label_result = detect_labels(image_to_bytes(cv2_img), client)
    num_labels = len(label_result['Labels'])

    confidences = []
    label_boxes = []
    cropped_images = []

    if num_labels:
        pill_instances = label_result['Labels'][0]['Instances']
        for instance in pill_instances:
            cropped_img = crop_image_around_label(image=cv2_img,
                                        bounding_box=instance['BoundingBox'],
                                        expansion=0)
            if cropped_img is not None:
                cropped_images.append(cropped_img)
                confidences.append(instance['Confidence'])
        label_boxes = extract_label_boxes(label_result['Labels'])
        
        if draw_label_boxes:
            img_with_label_boxes = draw_text_boxes_on_image(cv2_img, label_boxes, color=(0, 0, 255))
            return confidences, label_boxes, cropped_images, img_with_label_boxes
        return confidences, label_boxes, cropped_images, None
    return [], [], [], None
    

# ----------------- Main Function -----------------

def process_image(image_file, image_name, pre_processed_imgs_path, save_img_prefix):
    client = setup_aws_client()
    # cv2_img, img_height, img_width = load_image(image_path)
    cv2_img = convert_to_cv2(image_file)
    img_height, img_width = cv2_img.shape[:2]

    print(f"Initial Image Processing...")
    edges = preprocess_image(cv2_img, 9)
    orig_img_contours = compute_contours(edges)
    
    #########################
    # [1] Run Text detection
    #########################
    text_result, original_text_boxes, img_with_text_boxes  = process_img_text(cv2_img=cv2_img,
                          client=client,
                          draw_text_boxes=SAVE_TEXT_BOX_IMGS)


    # Get unique text detections
    if text_result is not None:
        all_detected_text = [ text_detection['DetectedText'] for text_detection in text_result['TextDetections']]
        unique_text = list(set(all_detected_text))
        print("Unique Text: ", unique_text)
    else:
        print("**No text detected.")

    if SAVE_TEXT_BOX_IMGS and img_with_text_boxes is not None:
        save_image(img_with_text_boxes, image_name, pre_processed_imgs_path, image_cnt=save_img_prefix, prefix='original_text_boxes')
    
    # TODO: check condition if it makes sense
    if original_text_boxes:
        text_detected = True
        closest_contours, clustered_img, cropped_clustered_img, cropped_img_coordinates = crop_image_around_text(cv2_img=cv2_img,
                                contours=orig_img_contours,
                                text_boxes=original_text_boxes,
                                img_width=img_width,
                                img_height=img_height)
        if SAVE_CLOSEST_CONTOURS_IMGS:
            save_image(clustered_img, image_name, pre_processed_imgs_path, image_cnt=save_img_prefix, prefix='original_text_closest_contours_to_text')
            save_image(cropped_clustered_img, image_name, pre_processed_imgs_path, image_cnt=save_img_prefix, prefix='original_text_closest_contours_cropped')

    #########################
    # [2] Run Label detection
    #########################
    original_label_confidences, original_label_boxes, cropped_label_images, img_with_lable_box = process_img_labels(cv2_img=cv2_img, 
                                                                    client=client,
                                                                    draw_label_boxes=SAVE_LABEL_BOX_IMGS)
    # print("Number of labels: ", len(original_label_boxes))
    # print(original_label_boxes)
    # for conf, label_box in zip(original_label_confidences, original_label_boxes):
    #     print(f"Label conf {conf} -- has instance {True if label_box else False}")

    if SAVE_ORIG_LABEL_IMGS and len(cropped_label_images) > 0:
        for img_idx, cropped_img_label in enumerate(cropped_label_images):
            save_image(cropped_img_label, image_name, pre_processed_imgs_path, image_cnt=save_img_prefix, prefix=f'original_label_cropped_{img_idx}')
        save_image(img_with_lable_box, image_name, pre_processed_imgs_path, image_cnt=save_img_prefix, prefix='original_label_boxes')


    # If number of unique text detected is greater than 3, return None
    if (text_result is not None) and len(unique_text) > 5:
        print("**Too much text detected in image.")
        return None, None
    
    # Remove special characters
    # TODO

    #############################################
    # Option 1: Both text and label are detected
    ############################################
    if (text_result is not None) and (len(original_label_boxes) > 0):
        chosen_img = text_and_label_detected_processing(text_cropped_img=cropped_clustered_img,
                                        text_box=get_combined_bounding_box(text_result['TextDetections']),
                                        confidences=original_label_confidences,
                                        label_boxes=original_label_boxes,
                                        cropped_label_images=cropped_label_images)
        return unique_text, chosen_img
    
    print("**Initial image detection FAILED")
    
    ###############################
    # Option 2: Only text detected
    ###############################
    print(f"\nIterative Image Processing...")
    if (text_result is not None) and (len(original_label_boxes) == 0):
        chosen_img = text_detected_no_label_processing(cv2_img=cv2_img,
                                           client=client, 
                                           img_height=img_height, 
                                           img_width=img_width, 
                                           original_text=unique_text, 
                                           original_text_cropped_img=cropped_clustered_img,
                                           image_name=image_name)
        if chosen_img is None:
            print("**Iterative image detection FAILED")
            return unique_text, cropped_clustered_img
        return unique_text, chosen_img
    
    ################################
    # Option 3: Only label detected 
    ################################ 
    if (text_result is None) and (len(original_label_boxes) > 0):

        for label_idx, label_box in enumerate(original_label_boxes):
            scaled_label_img = crop_image_around_label(image=cv2_img,
                                        bounding_box=label_box,
                                        expansion=-20)
            save_image(scaled_label_img, image_name, pre_processed_imgs_path, image_cnt=save_img_prefix, prefix='scaled_label_box')

            cropped_img_text = label_detected_no_text_processing(cv2_img=scaled_label_img,
                                            client=client, 
                                            img_height=img_height, 
                                            img_width=img_width, 
                                            image_name=image_name,
                                            blur_start=5)
            if len(cropped_img_text) > 0:
                return cropped_img_text, cropped_label_images[label_idx]
            
        if cropped_img_text is None:
            print("**Iterative image detection FAILED")
            return None, None

    print("**No text or labels detected in image")
    return None, None
    

def text_and_label_detected_processing(text_cropped_img, text_box, confidences, label_boxes, cropped_label_images):
    # How many labels are detected? 
    #   One label:
    #       What is the labels confidence?
    #           Confidence > 85, return label image
    #           Confidence < 85, return text cropped img

    num_labels = len(cropped_label_images)
    if num_labels == 1:
        print("One Label Detected")
        if confidences[0] > 85:
            print("High confidence label")
            return cropped_label_images[0]
        else:
            return text_cropped_img
    
    #   Multiple labels:
    #       For each label run the following:
    #           Find the largest 
    #           Find one that has closest centroid to the text centroid
    #           Find one that covers the most area of the text bounding box
    #       Return the one that checks the most of the 3 criteria, otherwise return text cropped img

    else:
        lrgst_img_idx = find_largest_image(cropped_label_images)
        closest_to_center_idx = find_closest_label_box(text_box, label_boxes)
        covering_most_area_idx = find_covering_label_box(text_box, label_boxes)
        print("Largest img idx: ", lrgst_img_idx, end='\t')
        print("Closest to center idx: ", closest_to_center_idx, end='\t')
        print("Covering most area idx: ", covering_most_area_idx)
        chosen_img_idx = find_most_recurring_number_or_none([lrgst_img_idx, closest_to_center_idx, covering_most_area_idx])
        print("Chosen IMG idx: ", chosen_img_idx)
        if chosen_img_idx is not None:
            return cropped_label_images[chosen_img_idx]
        else:
            return cropped_label_images[confidences.index(max(confidences))]
    

    
def text_detected_no_label_processing(cv2_img, client, img_height, img_width, original_text, original_text_cropped_img, image_name, blur_start=9):

    blur = blur_start

    final_text = []
    final_img = None
    max_conf = 0

    while blur <= 30:
        print(f"## --- Blur: {blur} --- ##")

        outcome, result_data = max_crop_cycle(cv2_img=cv2_img,
                       client=client,
                       img_height=img_height,
                       img_width=img_width,
                       blur=blur,
                       original_text=original_text,
                       image_name=image_name)
        
        if (outcome is None):
            blur += 2
            continue
        elif (outcome == "text"):
            return original_text_cropped_img
        elif(outcome == "label"):
            confidence, cropped_img = result_data
            if confidence > max_conf:
                max_conf = confidence
                final_img = cropped_img
        else:

            print("UNEXPECTED OUTCOME")
        blur += 2
    
    return final_img


   
def label_detected_no_text_processing(cv2_img, client, img_height, img_width, image_name, blur_start=9):

    blur = blur_start
    while blur <= 30:
        print(f"\n## --- Iteration: {blur} --- ##")

        outcome, result_data = max_crop_cycle(cv2_img=cv2_img,
                       client=client,
                       img_height=img_height,
                       img_width=img_width,
                       blur=blur,
                       original_text=[],
                       image_name=image_name)

        if (outcome == "cropped_text"):
            return result_data
        else:
            blur += 2
            continue
    
    return []



def max_crop_cycle(cv2_img, client, img_height, img_width, blur, original_text, image_name):
    # [1] Apply processing, Find contours, Crop max contour
    edges = preprocess_image(cv2_img, blur)
    if SAVE_EDGES_IMGS:
        save_image(edges, image_name, os.path.join(PRE_PROCESSED_IMGS_DIR, image_name), image_cnt=blur, prefix='edges')

    contours = compute_contours(edges)
    cropped_img = crop_image_largest_contour(cv2_img, contours)
    
    # [2] If the image is too small skip
    cropped_image_ratio = get_exponent((cropped_img.shape[0]*cropped_img.shape[1])/(img_height*img_width))
    if (cropped_image_ratio <= -5 ) or (cropped_image_ratio == 0):
        print("\tCropped Image Too Small")
        return None, None

    # [3] Do text detection on image
    text_result, original_text_boxes, img_with_text_boxes  = process_img_text(cv2_img=cv2_img,
                          client=client,
                          draw_text_boxes=SAVE_TEXT_BOX_IMGS)
    # print("Text result: ", text_result)
    if text_result is not None:
        all_detected_text = [ text_detection['DetectedText'] for text_detection in text_result['TextDetections']]
        unique_text = list(set(all_detected_text))
        print("\tUnique Text: ", unique_text)
    else:
        print("\tNo text detected.")

    # [4] Do label detection on image
    label_confidences, label_boxes, cropped_label_images, img_with_lable_box = process_img_labels(cv2_img=cv2_img, 
                                                                    client=client,
                                                                    draw_label_boxes=SAVE_LABEL_BOX_IMGS)
    print("\tNumber of labels: ", len(label_boxes))
    for conf, label_box in zip(label_confidences, label_boxes):
        print(f"\tLabel conf {conf} -- has instance {True if label_box else False}")
    
    # Neither
    if (text_result is None) and (len(label_confidences) == 0):
        print("\tNo text or labels detected in cropped img")
        return None, None
    elif (text_result is None) and (len(label_confidences) > 0): # Label only, return highest conf
       print("\tOnly label detected")
       max_conf_idx = label_confidences.index(max(label_confidences))
       return "label", (label_confidences[max_conf_idx], cropped_label_images[max_conf_idx])
    elif (text_result is not None) and (len(label_confidences) == 0):   # text only, return 
        # Is the text detected the same as, or is a subset of the original text detections
            # Return original text cropped img
        print("\tOnly text detected")
        if (set(unique_text) == set(original_text)) or (set(unique_text).issubset(set(original_text))):
            print("\tDetected text is subset of original text")
            return "text", unique_text
        elif (len(original_text) == 0):
            print("\tText detected in cropped label image")
            return "cropped_text", unique_text
        print("\tDetected text is NOT a subset of original text")
        return None, None
    else:
        print("\tNo text or label detected")
        return None, None



def main():
    
    image_name_list = []
    if RUN_ALL_TESTS == False:
        # image_filename = '2. HGH Biege Oblong Blurry2.jpg' # Pass -> text detected
        # image_filename = '2. CG Beige Oblong.jpg' # Pass -> largest contour is the pill, cropped correctly, label detection confidence is very high
        image_filename = '1. APO White Oblong.jpg' # Pass -> text detected
        # image_filename = 'MEL15_Circle.JPG' # Pass-ish -> text detected, but cropping clips the pill
        # image_filename = '6. Z White Oblong Flash.jpg'
        # image_filename = '5. 93 White Oblong.jpg'
        # image_filename = 'APOB10_oval.JPG'
        image_filename = '4. 81 Blue Round.jpg'
        image_filename = '2. HGH Biege Oblong Backwards.jpg'
        image_filename = '3. 93 7443 Yellow & Red Capsule.jpg'

        # image_name_list = ['4. 81 Blue Round', 'APO500_Oblong2', '3. 93 7443 Yellow & Red Capsule ', 'MEL15_Circle', '1. SI-ME White Oblong', 'APO500_Oblong_Full', '2. HGH Biege Oblong Backwards', 'APO500_Oblong', 'APOB10_oval', '2. HGH Biege Oblong Blurry2', 'APO_Circle']
        # image_name_list = ['2. CG Beige Oblong.jpg', '5. 93 White Oblong.jpg','6. Z White Oblong Blurry.jpg','6. Z White Oblong.jpg']

        
        image_name_list.append(image_filename)
    else:
        for _image_name in os.listdir(TEST_IMG_DIR):
            if _image_name.endswith('.JPG') or _image_name.endswith('.jpg'):
                image_name_list.append(_image_name)

    print("Image Name List: ", image_name_list)
   

    for image_filename in image_name_list:
        image_path = os.path.join(TEST_IMG_DIR, image_filename)
        
        extention = '.JPG' if '.JPG' in image_filename else '.jpg'
        image_name = "".join(image_filename.split(extention)[:-1])
        
        pre_processed_imgs_path = os.path.join(PRE_PROCESSED_IMGS_DIR, image_name)
        if not os.path.exists(pre_processed_imgs_path):
            os.makedirs(pre_processed_imgs_path)
        else:
            for file in os.listdir(pre_processed_imgs_path):
                os.remove(os.path.join(pre_processed_imgs_path, file))
        # print banner with image name
        print(f"{'='*50}")
        print(f"{'='*20} {image_name} {'='*20}\n")
        # process_images(image_path, image_name, pre_processed_imgs_path)
        detected_text, final_img = process_image(image_path=image_path,
                                  image_name=image_name,
                                  pre_processed_imgs_path=pre_processed_imgs_path, save_img_prefix=0)
        if detected_text is None:
            print("TEST FAILED")
        else:
            print("TEST PASSED")
            shape_obj = shape_detection(final_img)
            print("Shape = ", shape_obj.shape)
            shape_obj.detect_shape_gpt()
            print("gbt_shape = ", shape_obj.gbt_shape)

            color_obj = colour_detection(final_img)
            print("Color = ", color_obj.colour)
            color_obj.detect_colour_gpt()
            print("gbt_colour = ", color_obj.gbt_colour)
    


    # img_path = '/home/mnigm2001/capstone/backend/imagerecog/11_edges_2.jpg'
    # client = setup_aws_client()
    # cv2_img, img_height, img_width = load_image(img_path)
    # text_result, original_text_boxes, img_with_text_boxes  = process_img_text(cv2_img=cv2_img,
    #                       client=client,
    #                       draw_text_boxes=SAVE_TEXT_BOX_IMGS)
    # # print(text_result)
    # all_detected_text = [ text_detection['DetectedText'] for text_detection in text_result['TextDetections']]
    # unique_text = list(set(all_detected_text))
    # print("Unique Text: ", unique_text)
    

# if __name__ == "__main__":
#     main()

"""

Both detected:
1. APO White Oblong -- PASS
5. A11 White Oblong -- Passish - it detects All not A11

Text detected, no label:
4. 81 Blue Round -- PASS
APO500_Oblong2 -- PASS
3. 93 7443 Yellow & Red Capsule -- PASS
MEL15_Circle -- PASS
1. SI-ME White Oblong -- PASS
APO500_Oblong_Full -- PASS
2. HGH Biege Oblong Backwards -- Passish - it detects HOH instead of HGH
APO500_Oblong -- PASS
APOB10_oval -- PASS
2. HGH Biege Oblong Blurry2 -- PASS
APO_Circle -- PASS

No text detected:
2. CG Beige Oblong -- PASS
5. 93 White Oblong -- PASS
6. Z White Oblong Blurry -- FAIL
6. Z White Oblong -- FAIL

Redacted
5. A11 White Oblong VeryBlurry
5. 93 White Oblong VeryBlurry
2. HGH Biege Oblong Blurry
6. Z White Oblong Far
6. Z White Oblong Blurry2
6. Z White Oblong Far



"""