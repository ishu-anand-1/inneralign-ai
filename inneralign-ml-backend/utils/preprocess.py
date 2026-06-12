import cv2
import numpy as np

def preprocess_image(img):
  """
    Advanced handwriting preprocessing pipeline.

  ```
   Steps:
   1. Convert to grayscale
   2. Resize large images
   3. Contrast enhancement (CLAHE)
   4. Noise reduction
   5 . Adaptive thresholding
   6. Morphological cleanup
  """

# -----------------------------------
# Convert to grayscale
# -----------------------------------

  if len(img.shape) == 3:

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

  else:

    gray = img.copy()

# -----------------------------------
# Resize large images
# -----------------------------------

  max_width = 1200

  h, w = gray.shape

  if w > max_width:

    scale = max_width / w

    gray = cv2.resize(
        gray,
        (
            int(w * scale),
            int(h * scale)
        ),
        interpolation=cv2.INTER_AREA
    )

# -----------------------------------
# Contrast Enhancement
# -----------------------------------

  clahe = cv2.createCLAHE(
    clipLimit=2.0,
    tileGridSize=(8, 8)
  )

  enhanced = clahe.apply(gray)

# -----------------------------------
# Noise Reduction
# -----------------------------------

  denoised = cv2.GaussianBlur(
    enhanced,
    (5, 5),
    0
  )

# -----------------------------------
# Adaptive Threshold
# -----------------------------------

  binary = cv2.adaptiveThreshold(
    denoised,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY_INV,
    15,
    8
 )

# -----------------------------------
# Morphological Cleanup
# -----------------------------------

  kernel = np.ones(
    (2, 2),
    np.uint8
  )

  cleaned = cv2.morphologyEx(
    binary,
    cv2.MORPH_OPEN,
    kernel
  )

  cleaned = cv2.morphologyEx(
    cleaned,
    cv2.MORPH_CLOSE,
    kernel
  )

  return cleaned

