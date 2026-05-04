import cv2
import numpy as np
from PIL import Image

def test_detection(image_path, output_path):
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        print("Failed to load image")
        return
    
    # Convert to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Define range for "water" (blue/cyan)
    # This is a heuristic and might need tuning
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])
    
    # Mask out the water
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_inv = cv2.bitwise_not(mask)
    
    # Clean up mask
    kernel = np.ones((5,5), np.uint8)
    mask_inv = cv2.morphologyEx(mask_inv, cv2.MORPH_OPEN, kernel)
    mask_inv = cv2.morphologyEx(mask_inv, cv2.MORPH_CLOSE, kernel)
    
    # Find contours
    contours, _ = cv2.findContours(mask_inv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Find largest contour
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        
        # Draw for debugging
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Crop
        crop = img[y:y+h, x:x+w]
        cv2.imwrite(output_path, crop)
        print(f"Cropped to {x}, {y}, {w}, {h}")
    else:
        print("No turtle found")

if __name__ == "__main__":
    import os
    test_img = "turtles-data/data/images/t001/CAluWEgwPX.JPG"
    if os.path.exists(test_img):
        test_detection(test_img, "test_crop.jpg")
    else:
        print(f"Test image not found: {test_img}")
