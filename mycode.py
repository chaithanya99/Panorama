# %%
#importing all the required libraries
import numpy as np
import cv2
import matplotlib.pyplot as plt

# %%
#detecting the key points of the images using the SIFT
def detectkeypoints(image):
    SIFT = cv2.SIFT_create()
    (key_points, features) = SIFT.detectAndCompute(image, None)
    return (key_points, features)

# %%
#matching the keypoints on the left and right images using the BFMatcher
def matchkeypoints(features1, features2):
    matcher = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
    matches = matcher.match(features1, features2)

    sorted_matches = sorted(matches, key=lambda x: x.distance)
    return sorted_matches
# %%
#finding the hormography matrix for the given set of images
def get_homography_matrix(keypoint1, keypoint2,matches, threshold):
    keypoint1 = np.float32([kps.pt for kps in keypoint1])
    keypoint2 = np.float32([kps.pt for kps in keypoint2])
    points1 = np.float32([keypoint1[mat.queryIdx] for mat in matches])
    points2 = np.float32([keypoint2[mat.trainIdx] for mat in matches])
    (H, status) = cv2.findHomography(points2, points1, cv2.RANSAC, threshold)
    return(matches, H, status)
def join_images(left_path,right_path,out_path):
    
# %%
#loading the two images
    image1 = cv2.imread(left_path)
    image2 = cv2.imread(right_path)




# %%
#reshaping the images if the size of images are greater than the 1000 pixels
    if image1.shape[0] > 1000 or image1.shape[1] > 1000:
        image1 = cv2.resize(image1, (1000, 1000))
    if image2.shape[0] > 1000 or image1.shape[1] > 1000:
        image2 = cv2.resize(image2, (1000, 1000))


# %%
#converting the color of images into gray color
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # %%
    kps1, features1 = detectkeypoints(gray1)
    kps2, features2 = detectkeypoints(gray2)

    # %%
    matches = matchkeypoints(features1, features2)
    image3 = cv2.drawMatches(image1, kps1, image2, kps2,
                             matches[:100], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    
    # %%
    (matches, H, status) = get_homography_matrix(
        kps1, kps2, matches, 4)

    # %%
#finally printing the panarama image by using the warpPerspective by combing the both images.
    width = image1.shape[1]+image2.shape[1]
    height = image1.shape[0]+image2.shape[0]
    result = cv2.warpPerspective(image2, H, (width, height))
    result[0:image1.shape[0], 0:image1.shape[1]] = image1
    cv2.imwrite(out_path,result)
    























