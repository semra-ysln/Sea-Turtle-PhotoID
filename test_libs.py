try:
    import cv2
    print("cv2 found")
except ImportError:
    print("cv2 NOT found")

try:
    import numpy as np
    print("numpy found")
except ImportError:
    print("numpy NOT found")

try:
    import sklearn
    print("sklearn found")
except ImportError:
    print("sklearn NOT found")
