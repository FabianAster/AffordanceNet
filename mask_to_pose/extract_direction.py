import numpy as np
from os import walk
import cv2
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

def convert_nonzero_pixels_to_points(image):
    # Get non-zero pixel coordinates
    nonzero_pixels = np.transpose(np.nonzero(image))

    # Create array of points with x and y coordinates
    points = np.zeros((nonzero_pixels.shape[0], 2))
    points[:, 0] = nonzero_pixels[:, 1]  # x-coordinate
    points[:, 1] = nonzero_pixels[:, 0]  # y-coordinate

    return points

def apply_pca(points):
    # Perform PCA
    pca = PCA(n_components=1)
    pca.fit(points)

    # Transform points to the principal component space
    transformed_points = pca.transform(points)
    transformed_points = pca.inverse_transform(transformed_points)

    # Return the transformed points and the explained variance ratios
    return transformed_points

def plot_points(points):
    # Extract x and y coordinates
    x = points[:, 0]
    y = points[:, 1]

    # Create a scatter plot
    plt.scatter(x, y)
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.title('Points After PCA')
    plt.show()



def extract_and_plot_direction(image):
    # Step 2: Convert to grayscale if necessary
    if len(image.shape) == 3:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray_image = image

    points = convert_nonzero_pixels_to_points(image)
#plot_points(points)


    plt.imshow(cv2.cvtColor(image * 20, cv2.COLOR_BGR2RGB))
    plt.axis('off')


    # plot_points(points)

    print(points)
    pca = apply_pca(points)
    print(pca)
    print(points.shape)
    print(pca)
    # plot_points(pca)
    pca = np.rint(pca).astype(int)

    sorted_points = sorted(pca, key=lambda p: (p[0], p[1]))
    # Get the starting and endpoint of the line
    start_point = sorted_points[0]
    end_point = sorted_points[-1]
    
    
    median_x = np.median(pca[:, 0])
    median_y = np.median(pca[:, 1])
    
    grasp_point = (median_x, median_y)
    orientation_point = (start_point)

    line_image = cv2.line(image.copy()*15, start_point, end_point, (255), 1)
    
    cv2.circle(line_image, (int(median_x), int(median_y)), 3, 255, -1)

    # Display the image with the line
    plt.imshow(cv2.cvtColor(line_image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()
    
    return grasp_point, orientation_point


# Step 1: Load the image
if __name__ == '__main__':
    src_dir = '/home/fabian/31_TrainingImages/training_set/masks'


    filenames = next(walk(src_dir), (None, None, []))[2]  # [] if no file
    print(filenames)

    counter = 0
    for filename in filenames:
        print(filename)
        image = cv2.imread(src_dir + "/" + filename, cv2.IMREAD_GRAYSCALE)
        extract_and_plot_direction(image)
