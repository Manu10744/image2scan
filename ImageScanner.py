import cv2
import imutils
from skimage.filters import threshold_local


class ImageScanner:
    """ Scanner that applies edge detection in order to scan an ordinary image into a grayscale scan
        while positioning the point of view accordingly if needed. """

    def __init__(self, image, show_results):
        """
        :param image: Path to the image to scan
        :param show_results: Specifies whether to show intermediate results in GUI windows or not
        """
        self.image = image
        self.show_results = show_results

    def scan(self):
        self.__analyze_contours()

    def __analyze_contours(self):
        """ Transforms the image to black and white in a way so that only the edges become clearly visible. """
        cv2_image = cv2.imread(self.image)
        ratio = cv2_image[0] / 500.0
        original = cv2_image.copy()
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

        for contour in sortedContours:
            peri = cv2.arcLength(contour, True)
            approximation = cv2.approxPolyDP(contour, 0.02 * peri, True)

            # If approx. contour has four points, then we can assume that we have found the document
            if len(approximation) == 4:
                screenCnt = approximation
                break

        if self.show_results:
            cv2.drawContours(cv2_image, [screenCnt], -1, (0, 255, 0), 2)
            self.__show_intermediate_result("Outlined Image", cv2_image)

    def __show_intermediate_result(self, title, image):
        """ Shows an intermediate image processing step using a GUI window.
        :param title:  The title to use for the GUI window
        :param image:  The image object to display in the GUI window
        """
        cv2.imshow(title, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
