import os  # accessing the os functions
from modules import capture_video
from modules import capture_images
from modules import train_images
from modules import recognize
import pyfiglet


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
                check_camera()
                break
            elif choice == 2:
                capture_face()
                break
            elif choice == 3:
                train_face()
                break
            elif choice == 4:
                recognize_face()
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
def check_camera():
    capture_video.start()
    main_menu()


# --------------------------------------------------------------
# calling the take image function form capture image.py file
def capture_face():
    capture_images.capture()
    main_menu()


# -----------------------------------------------------------------
# calling the train images from train_images.py file
def train_face():
    train_images.train()
    main_menu()


# --------------------------------------------------------------------
# calling the recognize_attendance from recognize.py file
def recognize_face():
    recognize.mark_attendance()
    main_menu()


# --------------- run the main function ------------------
if __name__ == "__main__":
    main_menu()
