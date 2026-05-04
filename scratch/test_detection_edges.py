import cv2
import numpy as np
from PIL import Image

def test_detection_edges(image_path, output_path):
    img = cv2.imread(image_path)
    if img is None: return
    
    # Resize for faster processing
    scale = 0.25
    small = cv2.resize(img, None, fx=scale, fy=scale)
    gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    
    # Blur and Canny
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 30, 150)
    
    # Dilate to close gaps
    kernel = np.ones((5,5), np.uint8)
    dilated = cv2.dilate(edged, kernel, iterations=2)
    
    # Find contours
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        
        # Upscale back
        x, y, w, h = int(x/scale), int(y/scale), int(w/scale), int(h/scale)
        
        # Ensure it's not too small or too large
        if w > 100 and h > 100:
            crop = img[y:y+h, x:x+w]
            cv2.imwrite(output_path, crop)
            print(f"Cropped to {x}, {y}, {w}, {h}")
        else:
            print("Detected region too small, using original")
    else:
        print("No contours found")

if __name__ == "__main__":
    test_img = "turtles-data/data/images/t001/CAluWEgwPX.JPG"
    test_detection_edges(test_img, "test_crop_edges.jpg")
