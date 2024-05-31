# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 08:22:25 2023

@author: USer
"""
import os
import sys
import cv2
import numpy as np
import re
import json
from google.cloud import vision_v1
import matplotlib.pyplot as plt
from pdf2image import convert_from_path
from flask import jsonify


# Load the answer sheet image from server
with open(sys.argv[1], 'r') as file:
    # 파일 내용을 JSON 파싱하여 데이터 읽기
    answers= json.load(file)


pdf_path= sys.argv[2]


answer_sheet_images = convert_from_path(pdf_path)

answer_sheet_image = np.array(answer_sheet_images[0])
# Define the kernel for dilation
kernel = np.ones((2, 2), np.uint8)  # You can adjust the kernel size

# Apply dilation to the image
dilated_image = cv2.dilate(answer_sheet_image, kernel, iterations=1)

# Convert the image to grayscale
gray_image = cv2.cvtColor(dilated_image, cv2.COLOR_BGR2GRAY)

# Threshold the image to create a binary image
canny = cv2.Canny(gray_image, 100, 200)

# Find contours in the binary image
contours, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Initialize variables to keep track of the largest area and its index
largest_area = 0
largest_contour_index = -1

# Iterate through each contour and find the largest area
for i, contour in enumerate(contours):
    area = cv2.contourArea(contour)
    if area > largest_area:
        largest_area = area
        largest_contour_index = i

# Extract the largest bounding rectangle
if largest_contour_index != -1:
    x, y, w, h = cv2.boundingRect(contours[largest_contour_index])
    largest_answer_image = answer_sheet_image[y:y+h, x:x+w]

# Find the longest horizontal line and its y coordinate
longest_horizontal_line_length = 0
longest_horizontal_line_y = 0

for contour in contours:
    _, _, w, _ = cv2.boundingRect(contour)
    if w > longest_horizontal_line_length:
        longest_horizontal_line_length = w
        longest_horizontal_line_y = contour[0][0][1]

gray_answer = cv2.cvtColor(largest_answer_image, cv2.COLOR_BGR2GRAY)
new_canny = cv2.Canny(gray_answer, 100, 200)

# Calculate the horizontal projection (sum of pixel values in each row)
horizontal_projection = np.sum(new_canny, axis=1)

# Set a threshold to determine where to split the image based on horizontal projection
threshold = 0.8 * np.max(horizontal_projection)  # Adjust the threshold as needed

# Find the positions where the projection exceeds the threshold, indicating presence of a horizontal line
line_positions = np.where(horizontal_projection > threshold)[0]

# Divide the image based on the detected lines
divided_images = []
prev_pos = 0

for pos in line_positions:
    # Divide the image at the detected line positions
    divided_image = gray_answer[prev_pos:pos, :]

    # Skip small fragments (you can adjust the threshold as needed)
    if pos - prev_pos > 10:
        divided_images.append(divided_image)

    prev_pos = pos

# Bottom of answer sheet (may have contain more answer area)
if line_positions[-1] < gray_answer.shape[0] - 1:
    last_line_to_bottom_region = gray_answer[line_positions[-1]:, :]
    divided_images.append(last_line_to_bottom_region)

# Measure y-axis lengths for each divided image
y_lengths = [image.shape[0] for image in divided_images]

# Calculate the histogram
hist, bin_edges = np.histogram(y_lengths, bins=20)

# Find the bin with the highest count (most frequent y length)
most_frequent_bin = np.argmax(hist)

# Get the bin edges for the most frequent bin
most_frequent_bin_edges = [bin_edges[most_frequent_bin], bin_edges[most_frequent_bin + 1]]

# Find y lengths within the most frequent bin's range
y_lengths_most_frequent_bin = [length for length in y_lengths if most_frequent_bin_edges[0] <= length < most_frequent_bin_edges[1]]

# Calculate the mean of y lengths in the most frequent bin
mean_y_length_most_frequent_bin = np.mean(y_lengths_most_frequent_bin)

new_divided_images = []
for i, divided_image in enumerate(divided_images):
    factor = round(divided_image.shape[0] / mean_y_length_most_frequent_bin)
    if factor == 1:
        new_divided_images.append(divided_image)
    else:
        for j in range(factor):
            start_y = j * (divided_image.shape[0] // factor)
            end_y = (j + 1) * (divided_image.shape[0] // factor)
            divided_part = divided_image[start_y:end_y, :]
            new_divided_images.append(divided_part)

collected_divided_images = []

# Add the specified portion of gray_image to the beginning
collected_divided_images.append(gray_image[0:longest_horizontal_line_y, :])

# Add all elements from new_divided_images to collected_divided_images
collected_divided_images.extend(new_divided_images)

# Google Cloud Vision client creation
key_path = "C:/Users/dmlwl/source/repos/capstone/src/service_account_key.json"
client = vision_v1.ImageAnnotatorClient.from_service_account_file(key_path)

# Initialize an empty 2D array to store the recognized text
dapan = []

# Loop through each divided image for text recognition, starting from index 3
for i in range(2, len(collected_divided_images)):
    divided_image = collected_divided_images[i]

    # Create an array to store the text for the current image
    image_texts = []

    # Define the x-ranges for text extraction  
    x_ranges = [(0, 207), (208, 1032), (1033, 1270)]

    for x_start, x_end in x_ranges:
        # Crop the image based on the x-ranges
        cropped_image = divided_image[:, x_start:x_end]

        # Convert the OpenCV image to a format that Vision API expects
        _, img_encoded = cv2.imencode('.jpg', cropped_image)
        image_data = img_encoded.tobytes()

        # Perform text detection on the cropped image
        image = vision_v1.Image(content=image_data)
        response = client.text_detection(image=image)

        # Extract the recognized text and add it to the array for the current image
        recognized_text = response.text_annotations[0].description if response.text_annotations else ""
        image_texts.append(recognized_text)

    # Add the array of extracted texts for the current image to the dapan array
    dapan.append(image_texts)

# Process the first image (collected_divided_images[0])
first_image = collected_divided_images[0]
# print(type(first_image))
# print(first_image) 
# Convert the OpenCV image to a format that Vision API expects
_, img_encoded = cv2.imencode('.jpg', first_image)
image_data = img_encoded.tobytes()

# Perform text detection on the image
image = vision_v1.Image(content=image_data)
response = client.text_detection(image=image)

# Extract the recognized text
recognized_text = response.text_annotations[0].description if response.text_annotations else ""

# Use regular expressions to extract text within parentheses and brackets
student_id = re.findall(r'\((.*?)\)', recognized_text)
student_name = re.findall(r'\[(.*?)\]', recognized_text)

# Output the extracted student ID and student name
# print("Student ID:", student_id)
# print("Student Name:", student_name)

# Initialize test_score
test_score = 0

# Calculate test_score
for i in range(len(dapan)):
    real_answer_text = answers[i]
    student_answer = dapan[i][1]
    student_score = dapan[i][2]

    if real_answer_text == student_answer:
        # Extract the numeric part of student_score (assuming it starts with #)
        score = int(student_score[1:]) if student_score.startswith("#") else 0
        test_score += score

# print("[", student_id[0], student_name[0], "]", "Test Score:", test_score)
# print(dapan)

student_info = {
    "student_id": student_id[0] if student_id else "",
    "student_name": student_name[0] if student_name else "",
    "test_score": str(test_score)
}
# student_info를 JSON 문자열로 변환
student_info_json = json.dumps(student_info)

# 결과를 표준 출력에 기록
print(student_info_json)