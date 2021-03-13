# image2scan

### Purpose
image2scan is a python program that can be applied on an image in order to get a scan of it back.
For this purpose, it searches for an rectangular object inside the image which is then processed and scanned.
It even works on images where the angle of the document inside the image is oblique. 

### Usage
The program itself can be applied on an image:
 
 `$ py scan.py --image <path_to_your_image>`.
 
 
If you want to check what its doing, you can also tell it to visualize the intermediate results in a GUI:
 
 `$ py scan.py --image <path_to_your_image> --show-results`.

### Installation
`$ pip install -r requirements.txt`