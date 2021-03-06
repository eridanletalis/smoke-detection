import cv2
import matplotlib.pyplot as plt
import numpy as np
np.seterr(divide='ignore', invalid='ignore')


# to simply segment all the gray pixels in hsv
def simple_gray(bgr):
    hsv_image = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    light_white = (0, 0, 200)
    dark_white = (145, 60, 255)
    mask_white = cv2.inRange(hsv_image, light_white, dark_white)
    rgb_image = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    result_white = cv2.bitwise_and(rgb_image, rgb_image, mask=mask_white)
    cv2.imwrite("outputs/hsvGray.jpg", mask_white)

    plt.subplot(1, 2, 1)
    plt.imshow(mask_white, cmap="gray")
    plt.subplot(1, 2, 2)

    blur = cv2.GaussianBlur(result_white, (7, 7), 0)
    plt.imshow(blur)
    plt.show()


# from Yu C., A real-time video fire flame and smoke detection algorithm
def gray_plus_intensity(bgr):
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    hls_image = cv2.cvtColor(bgr, cv2.COLOR_BGR2HLS)  # or intensity?
    i = hls_image[:, :, 1]
    mask_white = np.ones(gray.shape[:2], dtype="uint8")
    m = np.ones(gray.shape[:2], dtype="uint8")
    n = np.ones(gray.shape[:2], dtype="uint8")
    # i = np.ones(gray.shape[:2], dtype="uint8")

    m = rgb.max(axis=2)
    n = rgb.min(axis=2)

    # This is 0 or 1 depending on whether it is == 0
    mask_white[:, :] = (i > 190) & (m - n < 20)

    # So scale the values up with a simple multiplcation
    mask_white = mask_white*255
    cv2.imwrite("outputs/gray_plus_intensity.jpg", mask_white)
    rgb_image = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    result_white = cv2.bitwise_and(rgb_image, rgb_image, mask=mask_white)

    plt.subplot(1, 2, 1)
    plt.imshow(mask_white, cmap="gray")
    plt.subplot(1, 2, 2)

    blur = cv2.GaussianBlur(result_white, (7, 7), 0)
    plt.imshow(blur)
    plt.show()


# from Shafar, Early Smoke Detection on Video Using Wavelet Energy
def saturation_plus_value(bgr):
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    mask_white = np.ones(gray.shape[:2], dtype="uint8")
    value = np.ones(gray.shape[:2], dtype="uint8")
    value = bgr.max(axis=2)
    minimum = bgr.min(axis=2)
    dif = value-minimum
    saturation = np.ones(gray.shape[:2], dtype="uint8")

    saturation = np.nan_to_num(dif/value)

    mask_white[:, :] = (value > 163) & (saturation < 0.37)
    mask_white = mask_white*255
    cv2.imwrite("outputs/saturation_plus_value.jpg", mask_white)
    rgb_image = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    result_white = cv2.bitwise_and(rgb_image, rgb_image, mask=mask_white)

    plt.subplot(1, 2, 1)
    plt.imshow(mask_white, cmap="gray")
    plt.subplot(1, 2, 2)

    blur = cv2.GaussianBlur(result_white, (7, 7), 0)
    plt.imshow(blur)
    plt.show()


# from Wang, Video smoke detection using shape, color, and dynamic features
def inYCbCrColourSpace(bgr):
    mask_white = np.ones(bgr.shape[:2], dtype="uint8")
    image_ycrcb = cv2.cvtColor(bgr, cv2.COLOR_BGR2YCR_CB)

    mask_white[:, :] = (image_ycrcb[:, :, 1] > 115) & (
        image_ycrcb[:, :, 1] < 141) & (
        image_ycrcb[:, :, 2] > 115) & (image_ycrcb[:, :, 2] < 141) & (
            image_ycrcb[:, :, 0] > 190)
    mask_white = mask_white*255
    cv2.imwrite("outputs/inYCbCrColourSpace.jpg", mask_white)
    rgb_image = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    result_white = cv2.bitwise_and(rgb_image, rgb_image, mask=mask_white)

    plt.subplot(1, 2, 1)
    plt.imshow(mask_white, cmap="gray")
    plt.subplot(1, 2, 2)

    blur = cv2.GaussianBlur(result_white, (7, 7), 0)
    plt.imshow(blur)
    plt.show()
