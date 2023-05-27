import pyrealsense2 as rs
import numpy as np

def pixel_to_3d_point(image, pixel_x, pixel_y):
    # Define the camera intrinsics (fx, fy, cx, cy)
    fx = 616.582
    fy = 616.783
    cx = 327.194
    cy = 239.961

    # Define the depth scale (millimeters to meters)
    depth_scale = 0.001

    # Get the depth value at the specified pixel
    depth = image[pixel_y, pixel_x] * depth_scale

    # Convert the pixel to a 3D point
    point_3d = rs.rs2_deproject_pixel_to_point(
        [fx, fy],
        [cx, cy],
        [pixel_x, pixel_y],
        depth
    )

    return point_3d

# Example usage:
image = ...  # Your RGBD image
pixel_x = 320
pixel_y = 240

# Convert the pixel to a 3D point
point_3d = pixel_to_3d_point(image, pixel_x, pixel_y)

# Print the 3D point relative to the camera
print("3D Point (Camera Coordinates):", point_3d)