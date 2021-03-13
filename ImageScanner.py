import cv2
import imutils
import logging
import numpy as np
import os

from skimage.filters import threshold_local


logger = logging.getLogger("SCANNER")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s | [%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


class ImageScanner:
    """ Scanner that applies edge detection in order to scan an ordinary image into a grayscale scan
        while positioning the point of view accordingly if needed. """

    def __init__(self, image, destination, show_results):
        """
        :param image: Path to the image to scan
        :param show_results: Specifies whether to show intermediate results in GUI windows or not
        """
        self.image = image
        self.destination = destination
        self.show_results = show_results

    def scan(self):
        """ Scans the document in the given image and saves the result in the destination directory """
        screenContours = self.__analyze_contours()
        scan_img = self.__transform_and_scan(screenContours)

        logger.info("Saving Scan in {}".format(self.destination))
        destination_path = os.path.join(self.destination, "scanresult.jpg")

        cv2.imwrite(destination_path, scan_img)

    def __analyze_contours(self):
        """ Transforms the image to black and white in a way so that only the edges become clearly visible. """
        cv2_image = cv2.imread(self.image)
        cv2_image = imutils.resize(cv2_image, height=500)

        # Gray the image and detect edges
        grayscaled = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(grayscaled, (5, 5), 0)
        edged = cv2.Canny(blurred, 75, 200)

        if self.show_results:
            self.__show_intermediate_result("Original Image", cv2_image)
            self.__show_intermediate_result("Image transformed to edges", edged)

        contours = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        grabbed = imutils.grab_contours(contours)
        sortedContours = sorted(grabbed, key=cv2.contourArea, reverse=True)[:5]

        screenCnt = None
        for contour in sortedContours:
            peri = cv2.arcLength(contour, True)
            approximation = cv2.approxPolyDP(contour, 0.02 * peri, True)

            # If approx. contour has four points, then we can assume that we have found the document
            if len(approximation) == 4:
                screenCnt = approximation
                break

        if screenCnt is None:
            logger.error("No rectangular object could be detected on the given image.")
            raise SystemExit(1)

        elif self.show_results:
            cv2.drawContours(cv2_image, [screenCnt], -1, (0, 255, 0), 2)
            self.__show_intermediate_result("Outlined Image", cv2_image)

        return screenCnt

    def __transform_and_scan(self, screenCnt):
        cv2_image = cv2.imread(self.image)
        ratio = cv2_image.shape[0] / 500.0
        transformed = self.__four_point_transform(cv2_image, screenCnt.reshape(4, 2) * ratio)

        transformed_grayscaled = cv2.cvtColor(transformed, cv2.COLOR_BGR2GRAY)
        threshold = threshold_local(transformed_grayscaled, 11, offset=10, method="gaussian")
        transformed_grayscaled = (transformed_grayscaled > threshold).astype("uint8") * 255

        if self.show_results:
            self.__show_intermediate_result("Original Image", imutils.resize(cv2_image, height=650))
            self.__show_intermediate_result("Scanning Result", imutils.resize(transformed_grayscaled, height=650))

        return transformed_grayscaled

    def __order_points(self, pts):
        # initialzie a list of coordinates that will be ordered such that the first entry in the list is the top-left,
        # the second entry is the top-right, the third is the bottom-right, and the fourth is the bottom-left
        rect = np.zeros((4, 2), dtype="float32")

        # the top-left point will have the smallest sum, whereas the bottom-right point will have the largest sum
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        # now, compute the difference between the points, the top-right point will have the smallest difference,
        # whereas the bottom-left will have the largest difference
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        # return the ordered coordinates
        return rect

    def __four_point_transform(self, image, pts):
        # obtain a consistent order of the points and unpack them individually
        rect = self.__order_points(pts)
        (tl, tr, br, bl) = rect

        # compute the width of the new image, which will be the maximum distance between bottom-right and bottom-left
        # x-coordiates or the top-right and top-left x-coordinates
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))

        # compute the height of the new image, which will be the maximum distance between the top-right and bottom-right
        # y-coordinates or the top-left and bottom-left y-coordinates
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))

        # now that we have the dimensions of the new image, construct the set of destination points to obtain a
        # "birds eye view",(i.e. top-down view) of the image, again specifying points in the top-left, top-right,
        # bottom-right, and bottom-left order
        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype="float32")

        # compute the perspective transform matrix and then apply it
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

        # return the warped image
        return warped

    def __show_intermediate_result(self, title, image):
        """ Shows an intermediate image processing step using a GUI window.
        :param title:  The title to use for the GUI window
        :param image:  The image object to display in the GUI window
        """
        cv2.imshow(title, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
