import os, datetime, cv2, math
from collections import Counter


def load_image(image_path):
    """
    Loads an image from the specified path.
    
    :param image_path: Path to the image file.
    :return: Tuple of the loaded image and its dimensions (image, height, width).
    """
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"The image at {image_path} could not be loaded.")
    height, width = image.shape[:2]
    return image, height, width


def image_to_bytes(image):
    """
    Encodes an image as JPEG format into bytes.
    
    :param image: Image to encode as a numpy array.
    :return: Byte array of the JPEG encoded image.
    """
    _, encoded_image = cv2.imencode('.jpg', image)
    return encoded_image.tobytes()



def save_image(image, image_name, save_dir, image_cnt=None, prefix='processed_image', print_msg=False):
        # save_dir = os.path.join(settings.PILL_VAULT_DIR, 'temp/process_images/') 
        os.makedirs(save_dir, exist_ok=True)

        # Create a timestamped filename for the image
        # timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        # filename = f"{timestamp}_{prefix}_{image_name}.jpg"
        if image_cnt is not None:
                filename = f"{image_cnt}_{prefix}_{image_name}.jpg"
        file_path = os.path.join(save_dir, filename)

        # Save the image using OpenCV
        cv2.imwrite(file_path, image)
        if print_msg:
                print(f"Image saved to {file_path}")


def get_exponent(number):
    if number == 0:
        return "Undefined for 0"
    exponent = math.floor(math.log10(abs(number)))
    return exponent



def find_most_recurring_number_or_none(numbers):
    """
    Finds the most recurring number in a list or returns None if all numbers occur equally.

    :param numbers: List of numbers.
    :return: The number that occurs most frequently or None if all occurrences are equal.
    """
    if not numbers:
        return None  # Handle empty list case

    # Count the occurrences of each number
    number_counts = Counter(numbers)

    # Find the most common number and its occurrence count
    most_common_number, highest_count = number_counts.most_common(1)[0]

    # # Check if there are other numbers with the same occurrence count
    # if all(count == highest_count for count in number_counts.values()):
    #     return None  # All numbers occur the same number of times

    return most_common_number