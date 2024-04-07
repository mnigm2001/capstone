
import cv2

def preprocess_image(image, blur_strength=9):
    """
    Applies preprocessing steps to the image: blurring, grayscale conversion, adaptive thresholding, and edge detection.
    
    :param image: Input image as a numpy array.
    :param blur_strength: Kernel size for Gaussian blurring.
    :return: Image after edge detection.
    """
    blurred = cv2.GaussianBlur(image, (blur_strength, blur_strength), 0)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    adaptive_thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    edges = cv2.Canny(adaptive_thresh, 100, 200)
    return edges



def compute_contours(edges):
    """
    Computes and returns contours from an edge-detected image.
    
    :param edges: Edge-detected version of the image.
    :return: Detected contours.
    """
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def find_largest_image(images):
    """
    Finds the largest image in a list of images based on area.

    :param images: List of images as numpy arrays.
    :return: The largest image idx.
    """
    max_area = 0
    largest_image_idx = None

    for idx, img in enumerate(images):
        area = img.shape[0] * img.shape[1]  # Calculate the area of the image
        if area > max_area:
            max_area = area
            largest_image_idx = idx

    return largest_image_idx


def find_closest_label_box(text_box, label_boxes):
    """
    Finds the index of the label box whose centroid is closest to the centroid of the given text box.

    :param text_box: A dictionary with 'Left', 'Top', 'Width', and 'Height' keys for the text box.
    :param label_boxes: A list of dictionaries with 'Left', 'Top', 'Width', and 'Height' for label boxes.
    :return: Index of the closest label box to the text box.
    """
    # Calculate the centroid of the text box
    text_centroid_x = text_box['Left'] + text_box['Width'] / 2
    text_centroid_y = text_box['Top'] + text_box['Height'] / 2

    closest_index = None
    min_distance = float('inf')

    # Iterate through label boxes to find the closest one to the text box centroid
    for index, label_box in enumerate(label_boxes):
        # Calculate the centroid of the label box
        label_centroid_x = label_box['Left'] + label_box['Width'] / 2
        label_centroid_y = label_box['Top'] + label_box['Height'] / 2

        # Calculate the Euclidean distance between centroids
        distance = ((text_centroid_x - label_centroid_x) ** 2 + (text_centroid_y - label_centroid_y) ** 2) ** 0.5

        # Update closest label box if this is the minimum distance found
        if distance < min_distance:
            min_distance = distance
            closest_index = index

    return closest_index

def find_covering_label_box(text_box, label_boxes):
    """
    Finds the index of the label box that covers the most area of the given text box.

    :param text_box: A dictionary with 'Left', 'Top', 'Width', and 'Height' keys for the text box.
    :param label_boxes: A list of dictionaries with 'Left', 'Top', 'Width', and 'Height' for label boxes.
    :return: Index of the label box that covers the most area of the text box.
    """
    max_overlap_area = 0
    covering_index = None

    # Calculate the coordinates of the text box
    text_left = text_box['Left']
    text_top = text_box['Top']
    text_right = text_left + text_box['Width']
    text_bottom = text_top + text_box['Height']

    # Iterate through label boxes to find the one that covers the most area of the text box
    for index, label_box in enumerate(label_boxes):
        # Calculate the coordinates of the label box
        label_left = label_box['Left']
        label_top = label_box['Top']
        label_right = label_left + label_box['Width']
        label_bottom = label_top + label_box['Height']

        # Determine the overlap between the text box and the label box
        overlap_left = max(text_left, label_left)
        overlap_top = max(text_top, label_top)
        overlap_right = min(text_right, label_right)
        overlap_bottom = min(text_bottom, label_bottom)

        # Calculate overlap area only if there is an actual overlap
        if overlap_right > overlap_left and overlap_bottom > overlap_top:
            overlap_area = (overlap_right - overlap_left) * (overlap_bottom - overlap_top)
            if overlap_area > max_overlap_area:
                max_overlap_area = overlap_area
                covering_index = index

    return covering_index