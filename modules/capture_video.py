import cv2


def start(input_video):
    # store input video stream capture in cap variable
    cap = cv2.VideoCapture(input_video)

    while cap.isOpened():
        # capture frame-by-frame
        ret, frame = cap.read()
        if ret is True:  # video is detected
            # convert frame to grayscale
            # gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # display the resulting frame
            cv2.imshow('Checking Video - Attendance using Face Recognition', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:  # video not detected
            break

    # when everything is done
    cap.release()
    cv2.destroyAllWindows()
