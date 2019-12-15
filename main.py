import os  # accessing the os functions
from modules import capture_video
from modules import capture_images
from modules import train_images
from modules import recognize
import pyfiglet


# input live stream from a recorder
INPUT_VIDEO = "http://192.168.1.100:8080/video"

# input from saved video
# INPUT_VIDEO = "video.avi"

# input from a device attached to computer
# INPUT_VIDEO = 0  # or -1 if 0 doesn't work


# creating the title bar function
def title_bar():
    # os.system('cls')  # for windows

    # title of the program
    title = pyfiglet.figlet_format("Attendance using Face Recognition")
    print(title)


# creating the user main menu function
def main_menu():
    title_bar()
    print()
    print(10*"*", "WELCOME", 10*"*")
    print("[1] Check Camera")
    print("[2] Capture Faces")
    print("[3] Train Images")
    print("[4] Recognize & Attendance")
    print("[5] Quit")

    while True:
        try:
            choice = int(input("Enter Choice: "))

            if choice == 1:
                check_camera(INPUT_VIDEO)
                break
            elif choice == 2:
                capture_face(INPUT_VIDEO)
                break
            elif choice == 3:
                train_face()
                break
            elif choice == 4:
                recognize_face(INPUT_VIDEO)
                break
            elif choice == 5:
                print("Thank You =)")
                break
            else:
                print("Invalid Choice. Enter 1-4")
                main_menu()
        except ValueError:
            print("Invalid Choice. Enter 1-4\n Try Again")
        finally:
            # key = input("Enter any key to return main menu")
            pass


# ---------------------------------------------------------
# calling the camera test function from check camera.py file
def check_camera(input_video):
    capture_video.start(input_video)
    main_menu()


# --------------------------------------------------------------
# calling the take image function form capture image.py file
def capture_face(input_video):
    capture_images.capture(input_video)
    main_menu()


# -----------------------------------------------------------------
# calling the train images from train_images.py file
def train_face():
    train_images.train()
    main_menu()


# --------------------------------------------------------------------
# calling the recognize_attendance from recognize.py file
def recognize_face(input_video):
    recognize.mark_attendance(input_video)
    main_menu()


# --------------- run the main function ------------------
if __name__ == "__main__":
    main_menu()
