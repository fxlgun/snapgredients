from PIL import Image
import torch
from transformers import VisionEncoderDecoderModel, TrOCRProcessor
import os
import time
import os
import cv2
import numpy as np
import time
import keras_ocr
import re 
from torch.nn.functional import interpolate



# Initialize the detector
detector = keras_ocr.detection.Detector()

# Path to the input image
image = cv2.imread("1.jpg")

# Directory to save output images
# output_directory = "Custom_Dataset"

# Load image
# image = cv2.imread(input_image_path)

# Perform object detection
t1 = time.time()
predictions = detector.detect([image])
t2 = time.time()
print("Inference Time for Keras:", t2 - t1)
    
    # Draw bounding boxes on the image
all_coordinates = []

# to view what keras had detected draws bounding boxes
# for sublist in predictions:
    
#     for coordinates in sublist:
#         coordinates = coordinates.astype(int)
#         cv2.polylines(image, [coordinates], isClosed=True, color=(0, 255, 0), thickness=2)
#         centroid = np.mean(coordinates, axis=0).astype(int)
#         all_coordinates.append(coordinates)  # Append coordinates to the array

#     # Save output image with prefix 'detector'
#     output_image_path = os.path.join(output_directory, "single_image_detected.jpg")
#     cv2.imwrite(output_image_path, image)
    
#     # Close all OpenCV windows
#     cv2.destroyAllWindows()

# ///////////////////////////////////////////////////////////////
    


all_coordinates = []
group_dictionary = {}

# Reset variables
collected_coordinates = 0
set_count = 1

for sublist in predictions:
    set_coordinates = []  # List to hold coordinates for the current set
    
    for coordinates in sublist:
        # Convert coordinates to integers
        coordinates = coordinates.astype(int)
        
        # Append all coordinates
        set_coordinates.append(coordinates)
        collected_coordinates += 1
        
        # Break the loop if we already have 6 coordinates
        if collected_coordinates >= 6:
            group_dictionary[f"filtered_coordinates_{set_count}"] = set_coordinates
            collected_coordinates = 0
            set_coordinates = []
            set_count += 1
    
    # If there are remaining coordinates, add them to the dictionary
    if set_coordinates:
        group_dictionary[f"filtered_coordinates_{set_count}"] = set_coordinates
        set_count += 1

# If the last set has less than 6 coordinates, adjust the key
if set_coordinates and collected_coordinates < 6:
    group_dictionary[f"filtered_coordinates_{set_count-1}"] = set_coordinates
coordinates_dict = {}
for key, coordinates_list in group_dictionary.items():
    coordinates_dict[key] = []
    for i, coordinates in enumerate(coordinates_list, start=1):
        coordinates_dict[key].append(coordinates.tolist())

# //////////////////////////////////////////////////////////////////////////////////
        



# Draw rectangles and save cropped images
for key, coordinates_list in group_dictionary.items():
    for i, coordinates in enumerate(coordinates_list):
        # Convert coordinates to numpy array
        coordinates = np.array(coordinates)
        # Get bounding box coordinates
        x, y, w, h = cv2.boundingRect(coordinates)
        
        # Determine the width of whitespace to be added on both sides
        whitespace_width = 10  # Adjust the width as needed
        
        # Create a whitespace image with the same height as the cropped image
        whitespace_image = np.ones((h, 2*whitespace_width, 3), dtype=np.uint8) * 255
        
        # Add whitespace to both sides of the cropped image
        padded_image = np.hstack((whitespace_image, image[y:y+h, x:x+w], whitespace_image))
        # Save the padded image
        cv2.imwrite(f'Cropped_Images/{key}_box_{i}.jpg', padded_image)


# ///////////////////////////////////////////////////////////////////////////////////
        
def stitch_images(images, panorama_path):
    # Get the dimensions of the first image
    height, width, _ = images[0].shape

    # Resize images if needed to ensure they have the same height
    for i in range(1, len(images)):
        images[i] = cv2.resize(images[i], (width, height))

    # Calculate the total width of the panorama
    panorama_width = width * len(images)

    # Create a blank canvas to stitch images
    panorama = np.zeros((height, panorama_width, 3), dtype=np.uint8)

    # Stitch images horizontally
    for i, image in enumerate(images):
        panorama[:, i*width:(i+1)*width] = image

    # Save the panorama
    cv2.imwrite(panorama_path, panorama)

# Path to the folder containing the images
folder_path = 'Cropped_Images/'

# Initialize an empty list to store the images
images = []

# List all files in the folder
files = os.listdir(folder_path)

# Group files based on the prefix (filtered_coordinates_1, filtered_coordinates_2, etc.)
grouped_files = {}
for file in files:
    prefix = file.split('_box_')[0]
    if prefix not in grouped_files:
        grouped_files[prefix] = []
    grouped_files[prefix].append(file)

# Sort groups based on the numeric suffix
grouped_files = {k: sorted(v) for k, v in grouped_files.items()}

# Stitch images for each group
for key, files in grouped_files.items():
    # Load the images
    images = []
    for file in files:
        filename = os.path.join(folder_path, file)
        image = cv2.imread(filename)
        if image is not None:
            images.append(image)
        else:
            print(f"Failed to load image: {filename}")

    # Create panorama path
    panorama_path = f'panaroma_images/panorama{key.split("_")[2]}.jpg'  # Extracting the number from the prefix

    # Stitch images into panorama
    stitch_images(images, panorama_path)
        

# ////////////////////////////////////////////////////////////////////////////
    
panorama_images_folder = "panaroma_images/"

# Get list of panorama image files in the folder
panorama_images = [f for f in os.listdir(panorama_images_folder) if os.path.isfile(os.path.join(panorama_images_folder, f))]

# Construct nested dictionary
nested_dict = {}
for panorama_image in panorama_images:
    panorama_number = int(panorama_image.split('.')[0].split('panorama')[-1])
    filtered_coordinates_key = f'filtered_coordinates_{panorama_number}'
    if filtered_coordinates_key in coordinates_dict:
        nested_dict[panorama_image] = {filtered_coordinates_key: coordinates_dict[filtered_coordinates_key]}

# //////////////////////////////////////////////////////////////////////////////////

# def clear_gpu_memory():
#     torch.cuda.empty_cache()

# torch.cuda.empty_cache()
device = torch.device("cpu")
print("TRocr begins and Device in use:", device)
# Load the pre-trained processor
processor = TrOCRProcessor.from_pretrained('microsoft/trocr-large-printed')
model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-large-printed').to(device)

# Path to the folder containing the images
folder_path = 'panaroma_images'

# List all files in the folder
files = os.listdir(folder_path)

# Sort the files based on the numbers extracted from their names
files.sort(key=lambda x: int(re.findall(r'\d+', x)[0]))
results = {}
# Loop through each image in the folder
for file in files:
    # Clear GPU memory
    # clear_gpu_memory()

    # Load the image
    image_path = os.path.join(folder_path, file)
    image = Image.open(image_path).convert('RGB')
    
    # Extract features from the image
    pixel_values = processor(image, return_tensors="pt").pixel_values.to(device)
    
    # Measure GPU memory usage before inference
    torch.cuda.reset_peak_memory_stats()
    
    # Measure time of inference
    start_time = time.time()
    
    # Perform inference
    generated_ids = model.generate(pixel_values)
    
    # Decode the generated text
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    
    # Print generated text
    print(f"Output for {file}: {generated_text}")
    words = generated_text.split(' ')
    results[file] = words
    # print(results)
    # Calculate inference time
    inference_time = time.time() - start_time
    print(inference_time)

# //////////////////////////////////////////////////////////////////////////

combined_dict = {}
# Iterate over the nested_dict
for img_key, nested_info in nested_dict.items():
    # Find the number in the key (e.g., filtered_coordinates_9)
    num = re.findall(r'\d+', list(nested_info.keys())[0])[0]
    # Form the new key
    new_key = f'filtered_coordinates_{num}'
    # Combine the coordinates and text from results
    combined_dict[new_key] = {'coordinates': nested_info[list(nested_info.keys())[0]], 'text': results[img_key]}

print(combined_dict)

# /////////////////////////////////////////////////////////////////////

# if u wanna draw boxes on image 

def draw_boxes(image, coordinates, text):
    for i, bbox in enumerate(coordinates):
        # Convert coordinates to numpy array
        bbox = np.array(bbox)
        # Draw bounding box
        cv2.polylines(image, [bbox], isClosed=True, color=(0, 255, 0), thickness=2)
        # Draw text
        if i < len(text):
            cv2.putText(image, text[i], (bbox[0][0], bbox[0][1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return image

# Load input image
input_image_path = "1.jpg"  # Replace with your image path
input_image = cv2.imread(input_image_path)

# Check if image is loaded successfully
if input_image is None:
    print("Error: Image not found or unable to load.")
else:
    # Draw bounding boxes and text on input image
    for key, value in combined_dict.items():
        coordinates = value['coordinates']
        text = value['text']
        input_image = draw_boxes(input_image, coordinates, text)

    # Display the image with OpenCV
    cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
    cv2.imshow('Image', input_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# # //////////////////////////////////////////////////////////////////////////////