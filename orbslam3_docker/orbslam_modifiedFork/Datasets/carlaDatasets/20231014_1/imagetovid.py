#!/usr/bin/env python
import cv2
import os

def create_video_from_images(image_folder, output_video_path, fps=20):
    images = [img for img in os.listdir(image_folder) if img.endswith(".png") or img.endswith(".jpg")]
    images.sort()  # Sort by filename to keep the order

    if len(images) == 0:
        print(f"No images found in {image_folder}")
        return

    # Get the size of the images
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    # Create a video writer object
    video = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    for image in images:
        img_path = os.path.join(image_folder, image)
        frame = cv2.imread(img_path)
        video.write(frame)

    video.release()

def create_side_by_side_video(left_folder, right_folder, output_video_path, fps=20):
    left_images = [img for img in os.listdir(left_folder) if img.endswith(".png") or img.endswith(".jpg")]
    right_images = [img for img in os.listdir(right_folder) if img.endswith(".png") or img.endswith(".jpg")]
    
    left_images.sort()
    right_images.sort()

    if len(left_images) != len(right_images):
        print("The number of images in the left and right folders don't match.")
        return

    # Get the size of the images
    frame_left = cv2.imread(os.path.join(left_folder, left_images[0]))
    frame_right = cv2.imread(os.path.join(right_folder, right_images[0]))
    height, width, layers = frame_left.shape

    # Create a video writer object with double the width (for side-by-side)
    video = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width*2, height))

    for left_image, right_image in zip(left_images, right_images):
        img_left = cv2.imread(os.path.join(left_folder, left_image))
        img_right = cv2.imread(os.path.join(right_folder, right_image))
        
        # Concatenate images side by side
        combined_frame = cv2.hconcat([img_left, img_right])
        video.write(combined_frame)

    video.release()

# Example usage:
left_folder = "left"
right_folder = "right"
output_video_single_left = "."
output_video_side_by_side = "."

# Create the video with only left images
create_video_from_images(left_folder, output_video_single_left)

# Create the side-by-side video
create_side_by_side_video(left_folder, right_folder, output_video_side_by_side)

