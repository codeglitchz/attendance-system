import os
import csv
import cv2
import unicodedata  # to check if entered in different unicode format

# input live stream from a recorder
# URL = "http://192.168.1.103:8080/video"

# input from saved video
# URL = "video.avi"

# input from a device attached to computer
URL = 0  # or -1


# check if student_id is a number
def is_number(_id):
    try:
        float(_id)
        return True
    except ValueError:
        pass

    try:
        unicodedata.numeric(_id)
        return True
    except (TypeError, ValueError):
        pass

    return False


# Capture Image function definition
def capture():
    student_id = input("Enter Your ID (numbers only): ")
    name = input("Enter Your Name (alphabets only): ")

    # if "student_id is a number" and "name consists of alphabetic chars only" then
    if is_number(student_id) and name.isalpha():
        cap = cv2.VideoCapture(URL)

        # using haar cascade
        haar_cascade_path = "files" + os.sep + "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(haar_cascade_path)

        increment_num = 0

        while True:
            # capture frame-by-frame
            ret, img = cap.read()

            if ret is True:
                # operations on the frame come here
                gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                faces = detector.detectMultiScale(gray_frame, 1.3, 5)
                for(x, y, w, h) in faces:
                    cv2.rectangle(gray_frame, (x, y), (x+w, y+h), (255, 0, 0), 2)  # ##gray

                    # incrementing number
                    increment_num += 1

                    # saving the captured face in the data-set folder training_images
                    cv2.imwrite("training_images" + os.sep + name + "." + student_id + '.' +
                                str(increment_num) + ".jpg", gray_frame[y:y+h, x:x+w])  # ##gray[y:y+h, x:x+w]

                    # display the resulting frame
                    cv2.imshow('frame', gray_frame)  # ##gray

                # wait for 100 milliseconds
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                # break if the sample number is more than 100
                elif increment_num > 60:
                    break
            else:
                break
        cap.release()
        cv2.destroyAllWindows()
        # res = "Images Saved for ID : " + student_id + " Name : " + name
        row = [student_id, name]
        with open("files" + os.sep + "student_details.csv", 'a+') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(row)
        csv_file.close()

    # else Invalid Input ("student_id is not a number" or "name doesn't contain only alphabetic chars")
    else:
        # if student_id input is correct then
        if is_number(student_id):
            # ask to input correct alphabetic name
            print("Enter Alphabetical Name: ")

        # if name input is correct then
        if name.isalpha():
            # ask to input correct numeric ID
            print("Enter Numeric ID: ")
