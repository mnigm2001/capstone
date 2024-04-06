import cv2

def crop_image_largest_contour(image, contours):
    """
    Crops the image based on the given criteria, e.g., around the largest contour.
    
    :param image: The source image.
    :param contours: Detected contours in the image.
    :param crop_type: Criteria for cropping ('largest' for the largest contour).
    :return: Cropped image, or None if no valid contours are found.
    """
    if contours is None:
        return None

    # Find the largest contour based on the contour area
    largest_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_contour)
    cropped_img = image[y:y+h, x:x+w]
    return cropped_img


def crop_image_around_label(image, bounding_box, expansion=0):
    """
    Crops the image based on the bounding box provided in the label_data.
    Optionally expands the crop area by a specified number of pixels.

    :param image: The input image as a numpy array.
    :param label_data: A dictionary representing the first item in the 'Labels' list from AWS Rekognition.
    :param expansion: Number of pixels to expand the crop area around the bounding box.
    :return: Cropped image as a numpy array or None if 'Instances' is empty.
    """
    
    box = bounding_box
    
    img_height, img_width, _ = image.shape
    left = int(box['Left'] * img_width) - expansion
    top = int(box['Top'] * img_height) - expansion
    right = left + int(box['Width'] * img_width) + (2 * expansion)
    bottom = top + int(box['Height'] * img_height) + (2 * expansion)

    # Ensure the expanded bounding box does not go beyond the image boundaries
    left = max(0, left)
    top = max(0, top)
    right = min(img_width, right)
    bottom = min(img_height, bottom)

    # Crop and return the image
    cropped_image = image[top:bottom, left:right]
    return cropped_image

def crop_to_contours(image, contours):
    """
    Crops the image to keep only the area covering the provided contours.
    
    :param image: The image as a numpy array.
    :param contours: List of contours to include in the crop.
    :return: Cropped image.
    """
    # Initialize variables to hold the extremes of the combined bounding box
    x_min, x_max, y_min, y_max = float('inf'), 0, float('inf'), 0
    
    # Loop through contours to find the bounding box that encloses them all
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        x_min = min(x, x_min)
        y_min = min(y, y_min)
        x_max = max(x + w, x_max)
        y_max = max(y + h, y_max)
    
    # Crop the image to the combined bounding box
    cropped_image = image[y_min:y_max, x_min:x_max]
    return cropped_image, [x_min, x_max, y_min, y_max]
