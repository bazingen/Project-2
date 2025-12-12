from tkinter import *
from gui import GUI


def main():
    window = Tk()
    window.title("Bank")          
    window.geometry("380x400")      
    window.resizable(False, False) 

    GUI(window)

    window.mainloop()


if __name__ == "__main__":
    main()
