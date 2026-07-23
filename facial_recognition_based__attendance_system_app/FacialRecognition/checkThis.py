import numpy as np
from PIL import Image
from pillow_heif import register_heif_opener
from mtcnn_detector import MTCnnDetector

# 1. Register the HEIF opener to allow PIL to read .HEIC files
register_heif_opener()

# The original path from your snippet
image_path = "C:/Users/becka/Desktop/FRAS/media/testing_data/Bekan_Shiferaw_UGR_61569_14/IMG_4943.HEIC"

# 2. Load the HEIC image and convert it to a standard RGB array
# This converts the path into data the detector can actually "see"
heic_image = Image.open(image_path)
image_array = np.array(heic_image)

# 3. Initialize the detector with the loaded image data
# We keep the names face_detector and MTCnnDetector exactly as requested
face_detector = MTCnnDetector(image_array)

# 4. Run the process_image method
resized_faces = face_detector.process_image(plot=False)

# Optional: Print results to verify it worked
print(f"Detected and resized {len(resized_faces)} faces.")