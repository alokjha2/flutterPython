


# import cv2
# import dlib
# import faceBlendCommon as face
# import numpy as np

# # Load Image
# im = cv2.imread("cv2/images/girl.jpg")

# # Detect face landmarks
# PREDICTOR_PATH = r"C:\Users\felipe.cunha\Documents\venv\cv2\week1-pyton\data\models\shape_predictor_68_face_landmarks.dat"
# faceDetector = dlib.get_frontal_face_detector()
# landmarkDetector = dlib.shape_predictor(PREDICTOR_PATH)
# landmarks = face.getLandmarks(faceDetector, landmarkDetector, im)

# def createEyeMask(eyeLandmarks, im):
#     leftEyePoints = eyeLandmarks
#     eyeMask = np.zeros_like(im)
#     cv2.fillConvexPoly(eyeMask, np.int32(leftEyePoints), (255, 255, 255))
#     eyeMask = np.uint8(eyeMask)
#     return eyeMask

# def findIris(eyeMask, im, thresh):
#     r = im[:,:,2]
#     _, binaryIm = cv2.threshold(r, thresh, 255, cv2.THRESH_BINARY_INV)
#     kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4,4))
#     morph = cv2.dilate(binaryIm, kernel, 1)
#     morph = cv2.merge((morph, morph, morph))
#     morph = morph.astype(float)/255
#     eyeMask = eyeMask.astype(float)/255
#     iris = cv2.multiply(eyeMask, morph)
#     return iris

# def findCentroid(iris):
#     M = cv2.moments(iris[:,:,0])
#     cX = int(M["m10"] / M["m00"])
#     cY = int(M["m01"] / M["m00"])
#     centroid = (cX,cY)
#     return centroid

# def createIrisMask(iris, centroid):
#     cnts, _ = cv2.findContours(np.uint8(iris[:,:,0]), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     flag = 10000
#     final_cnt = None
#     for cnt in cnts:
#         (x,y),radius = cv2.minEnclosingCircle(cnt)
#         distance = abs(centroid[0]-x)+abs(centroid[1]-y)
#         if distance < flag :
#             flag = distance
#             final_cnt = cnt
#         else:
#             continue
#     (x,y),radius = cv2.minEnclosingCircle(final_cnt)
#     center = (int(x),int(y))
#     radius = int(radius) - 2

#     irisMask = np.zeros_like(iris)
#     inverseIrisMask = np.ones_like(iris)*255
#     cv2.circle(irisMask,center,radius,(255, 255, 255),-1)
#     cv2.circle(inverseIrisMask,center,radius,(0, 0, 0),-1)
#     irisMask = cv2.GaussianBlur(irisMask, (5,5), cv2.BORDER_DEFAULT)
#     inverseIrisMask = cv2.GaussianBlur(inverseIrisMask, (5,5), cv2.BORDER_DEFAULT)

#     return irisMask, inverseIrisMask

# def changeEyeColor(im, irisMask, inverseIrisMask):
#     imCopy = cv2.applyColorMap(im, cv2.COLORMAP_TWILIGHT_SHIFTED)
#     imCopy = imCopy.astype(float)/255
#     irisMask = irisMask.astype(float)/255
#     inverseIrisMask = inverseIrisMask.astype(float)/255
#     im = im.astype(float)/255
#     faceWithoutEye = cv2.multiply(inverseIrisMask, im)
#     newIris = cv2.multiply(irisMask, imCopy)
#     result = faceWithoutEye + newIris
#     return result

# def float642Uint8(im):
#     im2Convert = im.astype(np.float64) / np.amax(im)
#     im2Convert = 255 * im2Convert 
#     convertedIm = im2Convert.astype(np.uint8)
#     return convertedIm

# # Create eye mask using eye landmarks from facial landmark detection
# leftEyeMask = createEyeMask(landmarks[36:42], im)
# rightEyeMask = createEyeMask(landmarks[43:49], im)

# # Find the iris by thresholding the red channel of the image within the boundaries of the eye mask
# leftIris = findIris(leftEyeMask, im, 40)
# rightIris = findIris(rightEyeMask, im, 50)

# # Find the centroid of the binary image of the eye
# leftIrisCentroid = findCentroid(leftIris)
# rightIrisCentroid = findCentroid(rightIris)

# # Generate the iris mask and its inverse mask
# leftIrisMask, leftInverseIrisMask = createIrisMask(leftIris, leftIrisCentroid)
# rightIrisMask, rightInverseIrisMask = createIrisMask(rightIris, rightIrisCentroid)

# # Change the eye color and merge it to the original image
# coloredEyesLady = changeEyeColor(im, rightIrisMask, rightInverseIrisMask)
# coloredEyesLady = float642Uint8(coloredEyesLady)
# coloredEyesLady = changeEyeColor(coloredEyesLady, leftIrisMask, leftInverseIrisMask)

# # Present results
# cv2.imshow("", coloredEyesLady)
# cv2.waitKey(0)