import cv2

# input live stream from a recorder
# URL = "http://192.168.1.103:8080/video"

# input from saved video
# URL = "video.avi"

# input from a device attached to computer
URL = 0  # or -1


def start():
    cap = cv2.VideoCapture(URL)
    while cap.isOpened():
        # capture frame-by-frame
        ret, frame = cap.read()
        if ret is True:  # video is detected
            # gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # display the resulting frame
            cv2.imshow('frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:  # video not detected
            break
    # when everything is done
    cap.release()
    cv2.destroyAllWindows()
