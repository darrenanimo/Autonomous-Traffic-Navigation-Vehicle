import cv2 as cv
import RPi.GPIO as GPIO

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1280,
    capture_height=720,
    display_width=960,
    display_height=540,
    framerate=60,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d !"
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

#def show_camera():
    #red_led = 31
    #green_led = 35
    #blue_led = 33

    #GPIO.setmode(GPIO.BOARD)
    #GPIO.setup(red_led, GPIO.OUT, initial=GPIO.LOW)
    #GPIO.setup(green_led, GPIO.OUT, initial=GPIO.LOW)
    #GPIO.setup(blue_led, GPIO.OUT, initial=GPIO.LOW)

    # Create the Camera instance for 640 by 480
    #camera = nano.Camera()

def show_camera():

    print('Started')
    #print(gstreamer_pipeline(flip_method=0))
    window_title = "camera"
    video_capture = cv.VideoCapture(gstreamer_pipeline(flip_method=0), cv.CAP_GSTREAMER)
    #video_capture = cv.VideoCapture(0)
    #video_capture.set(cv.CAP_PROP_FPS, 60)
    #sign_Cascade = cv.CascadeClassifier("stopsign_classifier_haar.xml")
    #sign_Cascade = cv.CascadeClassifier("stop.xml")
    #sign_Cascade = cv.CascadeClassifier("stop2.xml")
    sign_Cascade = cv.CascadeClassifier("stop3.xml")
    
    if video_capture.isOpened():
        try:
            window_handle = cv.namedWindow(window_title, cv.WINDOW_AUTOSIZE)
            while True:
                ret_val, frame = video_capture.read()
                gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                signs = sign_Cascade.detectMultiScale(gray, 1.1, 4)
                for (x, y, w, h) in signs:
                    cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                if cv.getWindowProperty(window_title, cv.WND_PROP_AUTOSIZE) >= 0:
                    cv.imshow(window_title, frame)
                else:
                    break
                keyboard = cv.waitKey(30)
                if keyboard == 'q' or keyboard == 27:
                    break
        finally:
            GPIO.cleanup()
            video_capture.release()
            cv.destroyAllWindows()

        print('Stopped')
    else:
        print("Error Opening Camera")
if __name__ == "__main__":
    show_camera()
