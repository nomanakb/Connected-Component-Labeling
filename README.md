# Connected Component Labeling for a Grey-scale Image (4 Conectivity) 

This script takes a .bin file as an input. The .bin file contains the greyscale values of a (width),(height) 2D greyscale image. The script counts the number of areas corresponding to a grescale value and print the number of objects detected for these values. For example, an image may contain 3 black objects (greyscale value 0) and 5 white objects (greyscale value 255). For this case, the script prints a unit8 vector of length 256, e.g., with all values equal to zeros except 2 with A[0] = 3 and A[255] = 5.
  
More details on the connected component labelling algorithm can be found here https://www.youtube.com/watch?v=ticZclUYy88

Usage: count-areas <filename.bin> --shape (width),(height)
