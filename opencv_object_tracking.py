# USAGE
# python opencv_object_tracking.py
# python opencv_object_tracking.py --video dashcam_boston.mp4 --tracker csrt

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import requests
import cv2
oldz = 0
#
print(cv2.__version__)
orig_img = cv2.imread('DonaldTrumpHead.jpg')
img = orig_img.copy()
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
                help="path to input video file")
ap.add_argument("-ht", "--HeadTracker", type=str, default="medianflow",
                help="OpenCV object tracker type")
ap.add_argument("-lht", "--LeftHandTracker", type=str, default="kcf",
                help="OpenCV object tracker type")
args = vars(ap.parse_args())

# extract the OpenCV version info
(major, minor) = cv2.__version__.split(".")[:2]

# if we are using OpenCV 3.2 OR BEFORE, we can use a special factory
# function to create our object tracker
LeftHandTracker = None
HeadTracker = None
# initialize a dictionary that maps strings to their corresponding
# OpenCV object tracker implementations
OPENCV_OBJECT_TRACKERS = {
    "csrt": cv2.TrackerCSRT_create,
    "kcf": cv2.TrackerKCF_create,
    "boosting": cv2.TrackerBoosting_create,
    "mil": cv2.TrackerMIL_create,
    "tld": cv2.TrackerTLD_create,
    "medianflow": cv2.TrackerMedianFlow_create,
    "mosse": cv2.TrackerMOSSE_create
}

    # grab the appropriate object tracker using our dictionary of
    # OpenCV object tracker objects

# initialize the bounding box coordinates of the object we are going
# to track
initHeadBB = None
initLeftHandBB = None
# if a video path was not supplied, grab the reference to the web cam
if not args.get("video", False):
    print("[INFO] starting video stream...")
    vs = VideoStream(src=1).start()
    time.sleep(1.0)

# otherwise, grab a reference to the video file
else:
    vs = cv2.VideoCapture(args["video"])

# initialize the FPS throughput estimator
fps = None

# loop over frames from the video stream
while True:
    # grab the current frame, then handle if we are using a
    # VideoStream or VideoCapture object
    frame = vs.read()
    frame = frame[1] if args.get("video", False) else frame

    # check to see if we have reached the end of the stream
    if frame is None:
        break

    # resize the frame (so we can process it faster) and grab the
    # frame dimensionss
    frame = imutils.resize(frame, width=1300)
    (H, W) = frame.shape[:2]

    # check to see if we are currently tracking an object
    if initHeadBB is not None:
        # grab the new bounding box coordinates of the object
        (Headsuccess, box) = HeadTracker.update(frame)
        #currentz = box[2]
        #currenty = box[1]
        #ccurrentx = box[0]
        # check to see if the tracking was a success
        if Headsuccess:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            #requests.get(url = "https://opencvroblox.glitch.me/setx?x=" + str(currentx))
            #if oldz != 0:
                #width = orig_img.shape[0]
                #height = orig_img.shape[1]
                #img = cv2.resize(orig_img, (int(width + currentz - oldz), int(height + currentz-oldz)))
            #else:
               # img = orig_img.copy()

       # oldz = box[2]

        # update the FPS counter
        fps.update()
        fps.stop()

        # initialize the set of information we'll be displaying on
        # the frame
        info = [
            ("HeadTracker", args["HeadTracker"]),
            ("HeadSuccess", "Yes" if Headsuccess else "No"),
            ("FPS", "{:.2f}".format(fps.fps())),
        ]

        # loop over the info tuples and draw them on our frame
        for (i, (k, v)) in enumerate(info):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    if initLeftHandBB is not None:
        # grab the new bounding box coordinates of the object
        (LeftHandsuccess, box) = LeftHandTracker.update(frame)
        #currentz = box[2]
        #currenty = box[1]
        #ccurrentx = box[0]
        # check to see if the tracking was a success
        if LeftHandsuccess:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            #requests.get(url = "https://opencvroblox.glitch.me/setx?x=" + str(currentx))
            #if oldz != 0:
                #width = orig_img.shape[0]
                #height = orig_img.shape[1]
                #img = cv2.resize(orig_img, (int(width + currentz - oldz), int(height + currentz-oldz)))
            #else:
               # img = orig_img.copy()

       # oldz = box[2]

        # update the FPS counter
        fps.update()
        fps.stop()

        # initialize the set of information we'll be displaying on
        # the frame
        

        # loop over the info tuples and draw them on our frame
        #for (i, (k, v)) in enumerate(info):
           # text = "{}: {}".format(k, v)
            #cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
                        #cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # show the output frame
    cv2.imshow("Frame", frame)
    #cv2.imshow("Video", img)

    key = cv2.waitKey(1) & 0xFF

    # if the 's' key is selected, we are going to "select" a bounding
    # box to track
    if key == ord("s"):
        # select the bounding box of the object we want to track (make
        # sure you press ENTER or SPACE after selecting the ROI)
        initHeadBB = cv2.selectROI("Frame", frame, fromCenter=False,
                               showCrosshair=False)
        HeadTracker = OPENCV_OBJECT_TRACKERS[args["HeadTracker"]]()
        # start OpenCV object tracker using the supplied bounding box
        # coordinates, then start the FPS throughput estimator as well
        HeadTracker.init(frame, initHeadBB)

        initLeftHandBB = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=False)
        LeftHandTracker = OPENCV_OBJECT_TRACKERS[args["LeftHandTracker"]]()
        LeftHandTracker.init(frame, initLeftHandBB)

        fps = FPS().start()
    if key == ord("l"):
        
        fps = FPS().start()
    # if the `q` key was pressed, break from the loop
    elif key == ord("q"):
        break

# if we are using a webcam, release the pointer
if not args.get("video", False):
    vs.stop()

# otherwise, release the file pointer
else:
    vs.release()

# close all windows
cv2.destroyAllWindows()
