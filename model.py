from PIL import Image
import torch
# from transformers import VisionEncoderDecoderModel, TrOCRProcessor
import os
import time
import os
import cv2
import numpy as np
import time
import keras_ocr
import re 
# from torch.nn.functional import interpolate
import requests



# Initialize the detector
detector = keras_ocr.detection.Detector()

# Path to the input image
image = cv2.imread("haldiram.jpg")

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
#     output_image_path = ("single_image_detected.jpg")
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

api_url = "https://api-inference.huggingface.co/models/microsoft/trocr-large-printed"


image_folder = "panaroma_images"


headers = {
    "Content-Type": "image/jpeg",  # Adjust content type based on your image format
    "Authorization": "Bearer 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"  # If API requires authentication
}
files = os.listdir(image_folder)
string1 = ''
results = {}

for filename in files:
    if filename.endswith(".jpg") or filename.endswith(".jpeg"):
        image_path = os.path.join(image_folder, filename)

        with open(image_path, "rb") as image_file:
            image_data = image_file.read()

        # Send POST request with image data
        response = requests.post(api_url, headers=headers, data=image_data)

        # Check if the request was successful
        if response.status_code == 200:
            # Extract text from response
            text = response.json()
            string1 = text[0]['generated_text']
            # print(f"Output for {filename}: {string1}")
            words = string1.split(' ')
            results[filename] = words
 



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



# /////////////////////////////////////////////////////////////////////

# if u wanna draw boxes on image 

# def draw_boxes(image, coordinates, text):
#     for i, bbox in enumerate(coordinates):
#         # Convert coordinates to numpy array
#         bbox = np.array(bbox)
#         # Draw bounding box
#         cv2.polylines(image, [bbox], isClosed=True, color=(0, 255, 0), thickness=2)
#         # Draw text
#         if i < len(text):
#             cv2.putText(image, text[i], (bbox[0][0], bbox[0][1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
#     return image

# # Load input image
# input_image_path = "haldiram.jpeg"  # Replace with your image path
# input_image = cv2.imread(input_image_path)

# # Check if image is loaded successfully
# if input_image is None:
#     print("Error: Image not found or unable to load.")
# else:
#     # Draw bounding boxes and text on input image
#     for key, value in combined_dict.items():
#         coordinates = value['coordinates']
#         text = value['text']
#         input_image = draw_boxes(input_image, coordinates, text)

#     cv2.imwrite('detected_image.jpg', input_image)
#     # Display the image with OpenCV
#     cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
#     cv2.imshow('Image', input_image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

# # //////////////////////////////////////////////////////////////////////////////
    
def calculate_centroid(points):
    x = sum(point[0] for point in points) / len(points)
    y = sum(point[1] for point in points) / len(points)
    return int(x), int(y)

# Define a function to create centroid dictionary
def create_centroid_dict(data):
    new_data = {}
    for key, value in data.items():
        centroids = []
        for coords in value['coordinates']:
            centroid = calculate_centroid(coords)
            centroids.append(centroid)
        new_data[key] = {'centroid': centroids, 'text': value['text']}
    return new_data

# Define a function to draw centroids on the image
def draw_centroids(image, centroids, texts):
    for centroid, text in zip(centroids, texts):
        x, y = centroid
        cv2.circle(image, (x, y), 5, (0, 255, 0), -1)  # Draw a green circle at the centroid
        cv2.putText(image, f"{text} ({x},{y})", (x + 10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)  # Write text and centroid coordinates

# Load the image
image = cv2.imread("haldiram.jpg")

# Create centroid dictionary
new_data = create_centroid_dict(combined_dict)

# Extract texts and centroids
texts_centroids = [(text, centroid) for key, value in new_data.items() for text, centroid in zip(value['text'], value['centroid'])]
sorted_texts_centroids = sorted(texts_centroids, key=lambda x: (x[1][1], x[1][0]))
# Draw centroids on the image
texts = [text for text, _ in sorted_texts_centroids]
centroids = [centroid for _, centroid in sorted_texts_centroids]
draw_centroids(image, centroids, texts)
cv2.imwrite('finale_inference.jpg',image)
# Display the image

# Concatenate the texts in sorted order
concatenated_string = ' '.join([text for text, _ in sorted_texts_centroids])
print(concatenated_string)
