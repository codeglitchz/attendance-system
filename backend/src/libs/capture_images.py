import os
import csv
import cv2
import unicodedata  # to check if entered in different unicode format


# helper function ->  to check whether student_id is a number
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
def capture(input_video):
    student_id = input("Enter Your ID (numbers only): ")
    name = input("Enter Your Name (alphabets only): ")

    # if "student_id is a number" and "name consists of alphabetic chars only" then
    if is_number(student_id) and name.isalpha():
        # store input video stream in cap variable
        cap = cv2.VideoCapture(input_video)

        # using haar cascade
        haar_cascade_path = "files" + os.sep + "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(haar_cascade_path)

        increment_num = 0

        while True:
            # capture frame-by-frame
            ret, img = cap.read()
            if ret is True:  # video is detected
                # convert frame to grayscale
                gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # detect faces using haar cascade detector
                faces = detector.detectMultiScale(gray_frame, 1.3, 5)
                for(x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)  # ##gray

                    # incrementing number
                    increment_num += 1

                    # saving the captured face in the data-set folder training_images
                    cv2.imwrite(
                        "static" + os.sep + "images" + os.sep + "known" + os.sep +
                        name + "." + student_id + '.' + str(increment_num) + ".jpg", img[y:y+h, x:x+w]
                    )  # ##gray[y:y+h, x:x+w]

                    # display the resulting frame
                    cv2.imshow('Capturing Face - Attendance System', img)  # ##gray

                # wait for 100 milliseconds
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                # break if the sample number is more than 100
                elif increment_num > 60:
                    break
            else:  # video not detected
                break

        # when everything is done
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
