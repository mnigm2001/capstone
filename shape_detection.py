import cv2
import numpy as np
from colour_detection import colour_detection

#Determine largest contour in the image
def maxContour(contours):
    cnt_list = np.zeros(len(contours))
    for i in range(0,len(contours)):
        cnt_list[i] = cv2.contourArea(contours[i])

    max_value = np.amax(cnt_list)
    max_index = np.argmax(cnt_list)
    cnt = contours[max_index]

    return cnt, max_index

# Read image
image = cv2.imread('Pills/APO500_Oblong.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Preprocessing
blurred = cv2.GaussianBlur(gray, (9,9), 0)
# Setting All parameters 
t_lower = 100  # Lower Threshold 
t_upper = 150  # Upper threshold 
aperture_size = 7 # Aperture size 

edged = cv2.Canny(blurred, t_lower, t_upper,  
                 apertureSize=aperture_size)

# Find contours
contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# for contour in contours:
#     # Analyze shape

#     epsilon = 0.1 * cv2.arcLength(contours[0], True)
#     approx = cv2.approxPolyDP(contours[0], epsilon, True)
   
#     # Draw and label contours
#     cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)
#     #cv2.putText(image, 'Shape Name', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
mask = np.zeros_like(gray) # Create mask where white is what we want, black otherwise
#cv2.drawContours(mask, contours=[contours], 1, 255, -1) # Draw filled contour in mask
cnt, max_index = maxContour(contours)
cv2.drawContours(
    image=mask,
    contours=[cnt],
    contourIdx=-1,
    color=(255,255,255),
    thickness=cv2.FILLED)

M = cv2.moments(cnt)
cx = int(M['m10']/M['m00'])
cy = int(M['m01']/M['m00'])
print(cx)
print(cy)
pill_contour = max(contours, key=cv2.contourArea)

perimeter = cv2.arcLength(pill_contour, True)
approximation = cv2.approxPolyDP(pill_contour, 0.02 * perimeter, True)

# Bounding rectangle
x, y, w, h = cv2.boundingRect(pill_contour)

# Determine the aspect ratio
aspect_ratio = w / float(h)

# Shape classification
if len(approximation) > 15:
    shape = "Circle"
    
elif 0.8 < aspect_ratio < 1.2:
    shape = "Circle"
else:
    shape = "Oval" if aspect_ratio < 2 else "Oblong"
   
print(shape)
print(len(approximation))
print(aspect_ratio)
    

#cv2.putText(image, 'Center', (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

cv2.imshow('Output', image)
cv2.waitKey(0)

cv2.imshow('Output', mask)
cv2.waitKey(0)
cv2.destroyAllWindows()

test_colour = colour_detection(image,cx,cy)
print(test_colour.colour)

