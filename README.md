# image2scan

### Purpose
image2scan is a python program that can be applied on an image in order to get a scan of it back.
For this purpose, it searches for an rectangular object inside the image which is then processed and scanned.
It even works on images where the angle of the document inside the image is oblique. 

Generally, it performs good on images with enough contrast regarding the image and the rectangular object inside the image. 
It fails on images where the contrast is not sufficient to detect the edges or when there is no rectangular object (like a piece of paper) at all.

If it fails to detect 4 edges, the user is asked to define 4 points in order to determine the object to be scanned.

### Usage
The program can be applied on an image:
 
 ```bash
$ py scan.py --image <PATH_TO_IMAGE>
```

The directory for saving the scan PDF can be specified as well:
```bash
$ py scan.py --image <PATH_TO_IMAGE> --dest <PATH_TO_DIR>
```
 
If you want to check what its doing, you can also tell it to visualize the intermediate results in a GUI:
 
 ```
 $ py scan.py --image <PATH_TO_IMAGE> --show-results
```

### Installation
`$ pip install -r requirements.txt`