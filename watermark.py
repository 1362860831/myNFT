import numpy as np
import qftpy.io
import qftpy.fft
import matplotlib.pyplot as plt
from PIL import Image
import skimage
import cv2
import os

var_3 = np.sqrt(1 / 3)
var_unit = np.quaternion(0, var_3, var_3, var_3)
var_zero = np.quaternion(0, 0, 0, 0)




def shift_to_3channels(shift):
    shift_final = np.zeros([shift.shape[2], shift.shape[0], shift.shape[1]])
    for i in range(0, shift.shape[0]):
        for j in range(0, shift.shape[1]):
            for k in range(0, shift.shape[2]):
                shift_final[k][i][j] = shift[i][j][k]
    return shift_final


def normalized_correlation(imgA, imgB):
    rows, cols = imgA.shape
    sqrSumA = 0
    sqrSumB = 0
    productSum = 0

    # flag = np.zeros((rows, cols), dtype=int)
    #
    # center = (rows - 1) / 2
    #
    # for i in range(rows):
    #     for j in range(cols):
    #         if (np.absolute(i - center) + np.absolute(j - center)) < center:
    #             flag[i][j] = 1
    #
    # sumA = 0;
    # sumB = 0;
    # count = 0;
    # err = 0
    # for i in range(rows):
    #     for j in range(cols):
    #         if flag[i][j] == 0:
    #             sumA += imgA[i][j]
    #             sumB += imgB[i][j]
    #             count += 1
    #             if (imgA[i][j] != imgB[i][j]):
    #                 err += 1
    #
    # meanA = sumA / count
    # meanB = sumB / count
    # for i in range(rows):
    #     for j in range(cols):
    #         if flag[i][j] == 0:
    #             productSum += (float(imgA[i][j]) - meanA) * (float(imgB[i][j]) - meanB)
    #             sqrSumA += (imgA[i][j] - meanA) ** 2
    #             sqrSumB += (imgB[i][j] - meanB) ** 2
    # NC = productSum / ((sqrSumA * sqrSumB) ** 0.5)
    # ber = err / count
    # return NC, ber

    meanA=imgA.mean()
    meanB=imgB.mean()
    for i in range(rows):
        for j in range(cols):
            productSum+=(float(imgA[i][j])-meanA)*(float(imgB[i][j])-meanB)
            sqrSumA+=(imgA[i][j]-meanA)**2
            sqrSumB+=(imgB[i][j]-meanB)**2
    NC =productSum /((sqrSumA*sqrSumB)**0.5)
    return NC


def test_gaussian_noise():
    origin = skimage.img_as_float(skimage.io.imread("./monai.jpg"))
    # 测试高斯噪声
    noisy = skimage.util.random_noise(origin, mode='gaussian', var=0.05)
    noisy = shift_to_3channels(noisy)
    return noisy


###############################################################
# cat transform


def run(img, round):
    cv2.imshow('image', img)
    cv2.waitKey(-1)

    for i in range(round):
        img = cat_transform(img)
    return img


def reverse_run(img, round):
    for i in range(round):
        img = cat_reverse_transform(img)
    return img


def cat_transform(img):
    rows, cols = img.shape
    n = rows
    img2 = np.zeros([rows, cols])

    for x in range(0, rows):
        for y in range(0, cols):
            img2[x][y] = img[(x + y) % n][(x + 2 * y) % n]
    return img2


def cat_reverse_transform(img):
    rows, cols = img.shape
    n = rows
    img2 = np.zeros([rows, cols])

    for x in range(0, rows):
        for y in range(0, cols):
            img2[x][y] = img[(2 * x - y) % n][((-1) * x + y) % n]
    return img2


###############################################################

def watermark_gen(original, watermark):
    resized = original.resize((watermark.size[0], watermark.size[1]), Image.Resampling.LANCZOS)

    matrix = qftpy.io.im2q(resized)
    print(matrix)
    matrix = qftpy.fft.qfft2(matrix, axis=np.quaternion(0, 1, 1, 1), side='L')

    for i in range(0, matrix.shape[0]):
        for j in range(0, matrix.shape[1]):
            matrix[i][j] = np.absolute(matrix[i][j])

    mid = np.mean(matrix)
    eigenMatrix = np.zeros([matrix.shape[0], matrix.shape[1]])
    for i in range(0, matrix.shape[0]):
        for j in range(0, matrix.shape[1]):
            if matrix[i][j] >= mid:
                eigenMatrix[i][j] = 1
    for i in range(5):
        eigenMatrix = cat_transform(eigenMatrix)
    # plt.imshow(eigenMatrix)
    # plt.show()

    watermark_matrix = qftpy.io.im2q(watermark)
    watermark_01 = np.zeros([matrix.shape[0], matrix.shape[1]])
    for i in range(0, matrix.shape[0]):
        for j in range(0, matrix.shape[1]):
            if (watermark_matrix[i][j]) != var_zero:
                watermark_01[i][j] = 1

    # plt.imshow(watermark_01)
    # plt.show()
    for i in range(5):
        watermark_01 = cat_transform(watermark_01)

    final = np.zeros([matrix.shape[0], matrix.shape[1]])
    for i in range(0, matrix.shape[0]):
        for j in range(0, matrix.shape[1]):
            if (((eigenMatrix[i][j] == 1) & (watermark_matrix[i][j] == var_zero)) | (
                    (eigenMatrix[i][j] == 0) & (watermark_matrix[i][j] != var_zero))):
                final[i][j] = 1

    return final, watermark_01


def watermark_verify(veriImg, final, watermark_01):
    veriImg = veriImg.resize((watermark_01.shape[0], watermark_01.shape[1]), Image.Resampling.LANCZOS)

    # 不做测试
    matrix = qftpy.io.im2q(veriImg)

    # 测试高斯噪声
    # noisy = test_gaussian_noise()
    # plt.imshow(noisy)
    # plt.show()
    # matrix = qftpy.io.im2q(noisy)

    # 测试椒盐噪声
    # noisy = test_salt_and_pepper_noise()
    # matrix = qftpy.io.im2q(noisy)

    # 测试运动模糊
    # blur_final = test_motion_blur(veriImg)
    # matrix = qftpy.io.im2q(blur_final)

    # 测试方框模糊
    # blur=test_box_blur(veriImg)
    # matrix = qftpy.io.im2q(blur)

    # 测试高斯模糊
    # blur = test_gaussian_blur(veriImg)
    # matrix = qftpy.io.im2q(blur)

    # 测试jpeg压缩
    # compressed = test_JPEG_compression(veriImg)
    # matrix = qftpy.io.im2q(compressed)

    matrix = qftpy.fft.qfft2(matrix, axis=np.quaternion(0, 1, 1, 1), side='L')

    for i in range(0, matrix.shape[0]):
        for j in range(0, matrix.shape[1]):
            matrix[i][j] = np.absolute(matrix[i][j])

    mid = np.mean(matrix)

    eigenMatrix = np.zeros([matrix.shape[0], matrix.shape[1]])

    for i in range(0, matrix.shape[0]):
        for j in range(0, matrix.shape[1]):
            if matrix[i][j] >= mid:
                eigenMatrix[i][j] = 1
    for i in range(5):
        eigenMatrix = cat_transform(eigenMatrix)
    # plt.imshow(eigenMatrix)
    # plt.show()

    watermark_retrieved = np.zeros([matrix.shape[0], matrix.shape[1]])
    for i in range(0, matrix.shape[0]):
        for j in range(0, matrix.shape[1]):
            if eigenMatrix[i][j] != final[i][j]:
                watermark_retrieved[i][j] = 1
    for i in range(5):
        watermark_01 = cat_reverse_transform(watermark_01)
    # plt.imshow(watermark_retrieved)
    # plt.show()

    count = 0
    for i in range(0, matrix.shape[0]):
        for j in range(0, matrix.shape[1]):
            if watermark_retrieved[i][j] != watermark_01[i][j]:
                count += 1
    ber = count / (matrix.shape[0] * matrix.shape[1])


    NC = normalized_correlation(watermark_retrieved, watermark_01)
    # NC, ber = normalized_correlation(watermark_retrieved, watermark_01)

    return NC, ber, watermark_retrieved


if __name__ == '__main__':
    original_img = Image.open(open("./monai.jpg", 'rb'))
    watermark_img = Image.open(open("./watermark_256x256.png", 'rb'))
    zero_watermark, watermark_01 = watermark_gen(original_img, watermark_img)

    plt.figure(1)
    plt.imshow(zero_watermark)
    plt.figure(2)
    plt.imshow(watermark_01)

    suspected_img = Image.open(open("./monai_corp.jpg", 'rb'))
    NC, ber, watermark_retrieved = watermark_verify(suspected_img, zero_watermark, watermark_01)
    plt.figure(3)
    plt.imshow(watermark_retrieved)

    print("normalized correlation=", NC)
    print("bit error ratio=", ber)

    plt.show()

