#!/usr/bin/env python3

"""
# Author: Noman Akbar
# Data: 18 August 2019
##############################################################################
Usage: count-areas <filename.bin> --shape <width>,<height>
Input: Input is a binary image with extension .bin
Output: unit8 array with the count of objects corresponding to the greyscale
value.
#############################################################################
Explanation:
Load image from .bin file as a 2D matrix then create a greylevel mask
for each value in the image. Then use connected component labelling to find
the total number of objects corresponding to the current value. Then, repeat
the process for all the unique greyscale values in the image.
#############################################################################
References:
https://www.youtube.com/watch?v=ticZclUYy88
"""

from PIL import Image
import numpy as np
import sys
import time


def LoadImage(filename, ImageRows, ImageCols):
    """This function loads an image file as numpy array and displays the
    image"""
    data = np.fromfile(filename, dtype='uint8', sep="")
    data = data.reshape([ImageRows, ImageCols])
    Image.fromarray(data).show()
    return data


def Mask2Img(ImgCpy):
    "This function displays an binary image mask for a specific grey value"
    Mask = Image.fromarray(255*ImgCpy)
    Mask.show()


def ConnectedComponets(ImgCpy, ImageRows, ImageCols):
    "This function finds the number of objects with a specific grey value"
    ImgCpy = np.pad(ImgCpy, ((1, 1), (1, 1)), 'constant')  # extend array
    label = 1
    nonzidx = np.where(ImgCpy != 0)
    coord = list(zip(nonzidx[0], nonzidx[1]))
    EqList = np.array([0, 0])
    for a in coord:
        m, n = a[0], a[1]
        if ImgCpy[m, n-1] == 0 and ImgCpy[m-1, n] == 0:
            EqList = np.vstack((EqList, [label, label]))
            ImgCpy[m, n] = label
            label = label+1
        elif ImgCpy[m, n-1] == 0 and ImgCpy[m-1, n] != 0:
            ImgCpy[m, n] = ImgCpy[m-1, n]
        elif ImgCpy[m, n-1] != 0 and ImgCpy[m-1, n] == 0:
            ImgCpy[m, n] = ImgCpy[m, n-1]
        elif ImgCpy[m, n-1] != 0 and ImgCpy[m-1, n] != 0 and ImgCpy[m, n-1] == ImgCpy[m-1, n]:
            ImgCpy[m, n] = ImgCpy[m, n-1]
        elif ImgCpy[m, n-1] != 0 and ImgCpy[m-1, n] != 0 and ImgCpy[m, n-1] != ImgCpy[m-1, n]:
            ImgCpy[m, n] = min(ImgCpy[m, n-1], ImgCpy[m-1, n])
            EqList = np.vstack((EqList, [min(ImgCpy[m, n-1], ImgCpy[m-1, n]), max(ImgCpy[m, n-1], ImgCpy[m-1, n])]))
    EqList = np.unique(EqList, axis=0)
    EqList = np.flipud(EqList)
    for m in range(EqList.shape[0]):
        ImgCpy[ImgCpy == EqList[m, 1]] = EqList[m, 0]
    xx = np.unique(ImgCpy)
    xx = xx[xx > 0].shape[0]
    return xx


if __name__ == '__main__':
    # Load the image and convert it into Greyscale Image
    start_time = time.time()
    file = sys.argv[1]       # Input file
    if sys.argv[2] == "--shape":
        DimStr = sys.argv[3]
        MatDim = [int(x) for x in DimStr.split(',')]
        if len(MatDim) > 2:
            print("Inavlid arguments, Please check the imputs")
            print("Usage: count-areas <filename> --shape <width>,<height>")
            sys.exit(2)
        else:
            ImageRows = MatDim[0]
            ImageCols = MatDim[1]
    else:
        print("Inavlid arguments, Please check the imputs")
        print("Usage: count-areas <filename> --shape <width>,<height>")
        sys.exit(2)

    A = np.uint8(np.zeros(256))  # Prepare the output array
    GreyImg = LoadImage(file, ImageRows, ImageCols)

    # Create grey level mask
    ImageUnique = np.unique(GreyImg)
    # Now process each unique value
    for CurrColor in ImageUnique:
        ImCpy = np.copy(GreyImg)
        ImCpy[ImCpy == CurrColor] = 1  # Create color mask
        ImCpy[ImCpy != 1] = 0
        NumObj = ConnectedComponets(ImCpy, ImageRows, ImageCols)
        print(CurrColor, "--- %s seconds ---" % (time.time() - start_time))
        A[np.uint8(CurrColor)] = np.uint8(NumObj)
    print(A)
