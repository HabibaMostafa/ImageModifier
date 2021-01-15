# python version 3
# Importing the Keras libraries and packages
import h5py
import cv2

from keras.models import Sequential
from keras.models import load_model
from keras.optimizers import Adam
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.preprocessing.image import ImageDataGenerator

########################################################
#from matplotlib import pyplot as plt
#from sklearn.matrics import confusion_matrix

from os import listdir
from os.path import isfile, join
import numpy
import time

########################################################
# Importing Tkinter libraries to setup GUI
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import Menu

########################################################

######////////////////////////////////////////////////////////////////////////////////////////////##########

################### Program Classes ####################


class GUI:

    def __init__(self, master=None):

        ############# Variables ##############
        self.pred = None
        self.indicator = 'yellow'
        self.img = None
        self.displayImg = None
        self.resizedImg = None
        self.root = master

        ########### Canvas set up ############
        self.canvas = tk.Canvas(self.root, height=600, width=800)
        self.canvas.pack()

        self.frame = tk.Frame(self.root, bg='#000000', bd=5)
        self.frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

        self.display = tk.Frame(self.frame, bg='#A9A9A9', bd=5)
        self.display.place(relx=0.08, rely=0.08, relwidth=0.55, relheight=0.5)

        self.terminalLabel = tk.Label(self.frame, text="TERMINAL TO COME", font="Helvetica 19 bold")
        self.terminalLabel.place(relx=0.08, rely=0.75, relwidth=0.85, relheight=0.2)

        self.imgLabel = tk.Label(self.display, text="Waiting for image to be uploaded", font="Helvetica 11 bold")
        self.imgLabel.place(relx=0.065, rely=0.85, relwidth=0.88, relheight=0.15)

        self.indicatorButton = tk.Label(self.frame, text="Indicator", bg=self.indicator)
        self.indicatorButton.place(relx=0.08, rely=0.62, relwidth=0.2, relheight=0.1)

        self.lmain = tk.Label(self.display)
        self.lmain.place(relx=0.065, rely=0.065, relwidth=0.88, relheight=0.75)


####################################

    def import_model(self):

        self.model_location = filedialog.askopenfilename(initialdir="/Training Models",
                                                         filetypes=(("h5 File", "*.h5"), ("All Files", "*.*")),
                                                         title="Choose a Model")
        self.model = load_model(self.model_location)


####################################

    def load_image(self):
        
        self.image_location = filedialog.askopenfilename(initialdir="/Datasets",
                                                         filetypes=(("JPG File", "*.jpg"), ("All Files", "*.*")),
                                                         title="Choose an Image")
        self.display_image()


####################################

    def display_image(self):
        self.img = cv2.imread(self.image_location)
        self.img = cv2.resize(self.img, (80, 80))
        self.displayImg = Image.fromarray(self.img)
        self.resizedImg = self.displayImg.resize((340, 205), Image.ANTIALIAS)
        self.resizedImg = ImageTk.PhotoImage(image=self.resizedImg)
        self.lmain.resizedImg = self.resizedImg
        self.lmain.configure(image=self.resizedImg)
        self.imgLabel.config(text="Image successfully loaded")

        self.set_predictions()


####################################

    def set_predictions(self):
        self.pred = self.model.predict(self.img[None, ...])
        self.pre = numpy.array(self.pred)
        self.rpre = numpy.matrix.round(self.pred, 0)
        self.rpre = numpy.array(self.rpre[:, 0])
        print('Here are your Prediciton:')
        print(self.rpre[:, None])
        print(self.pred)
        self.rpre = self.rpre[:, None]

        self.set_indicator()


####################################

    def set_indicator(self):
        if self.rpre == 1:
            self.indicator = 'red'
            self.indicatorButton = tk.Label(self.frame, text="Crator", bg=self.indicator)
            self.indicatorButton.place(relx=0.08, rely=0.62, relwidth=0.2, relheight=0.1)

        else:
            self.indicator = 'green'
            self.indicatorButton = tk.Label(self.frame, text="Pass", bg=self.indicator)
            self.indicatorButton.place(relx=0.08, rely=0.62, relwidth=0.2, relheight=0.1)

################ Program Classes END ###################

######////////////////////////////////////////////////////////////////////////////////////////////##########

################## Program Main Loop ###################


def main():
    initial_gui()

############### Program Main Loop END ##################

######////////////////////////////////////////////////////////////////////////////////////////////##########

################# Program Functions ####################


def initial_gui():
    root = tk.Tk()
    b = GUI(root)
    root.title("Model Testing")
    file_menu(root, b)
    root.mainloop()

###########################################


def file_menu(root, b):
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Pick a Model", command=b.import_model)
    filemenu.add_command(label="Load an Image", command=b.load_image)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)

############### Program Functions END ##################

######////////////////////////////////////////////////////////////////////////////////////////////##########


########################################################
if __name__ == '__main__':
    main()
