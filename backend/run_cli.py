import os

import pyfiglet

from src.db import engine
from src.models import Base
from src.libs.face_util import FaceUtil

# create database tables
Base.metadata.create_all(engine)

# input live stream from a recorder
# INPUT_VIDEO = "http://192.168.1.100:8080/video"

# input from saved video
# INPUT_VIDEO = "files" + os.sep + "video.avi"

# input from a device attached to computer
INPUT_VIDEO = 0  # or -1 if 0 doesn't work


# creating the title bar function
def title_bar():
    # os.system('cls')  # for windows

    # title of the program
    title = pyfiglet.figlet_format("Attendance System")
    print(title)


# creating the user main menu function
def main_menu():
    title_bar()
    # print()
    print(10*"*", "WELCOME", 10*"*")
    print("[1] Check Camera")
    print("[2] Capture Face")
    print("[3] Train Classifier")
    print("[4] Recognize & Attendance")
    print("[5] Quit")

    while True:
        face_util = FaceUtil(INPUT_VIDEO)
        choice = 0
        try:
            choice = int(input("Enter Choice: "))

            if choice == 1:
                face_util.check()
                break
            elif choice == 2:
                face_util.detect_n_capture()
                break
            elif choice == 3:
                face_util.train_classifier()
                break
            elif choice == 4:
                face_util.recognize_n_attendance()
                break
            elif choice == 5:
                print("Thank You =)")
            else:
                choice = 0
        except ValueError:
            choice = 0
        finally:
            if choice == 0:
                print("Invalid Choice. Enter 1-5")
            elif choice == 5:
                exit()
            else:
                main_menu()


# --------------- run the main function ------------------
if __name__ == "__main__":
    main_menu()
