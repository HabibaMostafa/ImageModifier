########################################################
import time
import datetime
import os
import numpy as np
import cv2
import errno
import os
from datetime import datetime
from skimage.util import view_as_windows

########################################################
import tkinter as tk
from tkinter import filedialog
from tkinter import Menu
from PIL import Image, ImageTk

########################################################

######////////////////////////////////////////////////////////////////////////////////////////////##########

################### Program Classes ####################


class GUI:

    def __init__(self, master=None):
        
        ############# Variables ##############
        self.root = master
        self.img = None
        self.display_img = None
        self.resized_img = None
        self.tile_counter = 1

        ########### Canvas set up ############
        self.canvas = tk.Canvas(self.root, height=600, width=800)
        self.canvas.pack()

        self.frame = tk.Frame(self.root, bg='#000000', bd=5)
        self.frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

        self.display = tk.Frame(self.frame, bg='#A9A9A9', bd=5)
        self.display.place(relx=0.12, rely=0.08, relwidth=0.75, relheight=0.7)

        self.load_label = tk.Label(self.display, text="Waiting for Image to be loaded.", font="Helvetica 12 bold")
        self.load_label.place(relx=0.05, rely=0.85, relwidth=0.9, relheight=0.12)

        self.img_label = tk.Label(self.display, bg='#000000')
        self.img_label.place(relx=0.05, rely=0.085, relwidth=0.9, relheight=0.7)

        self.tiles_path()


####################################

    def tiles_path(self):

        self.tiles_dir_path = os.path.realpath(__file__)
        self.tiles_dir = os.path.dirname(self.tiles_dir_path) + '/Tiles'


####################################

    def load_image(self):

        self.img_location = filedialog.askopenfilename(initialdir='/Image Tiler/Images to Tile',
                                                       filetypes=(("JPG File", "*.jpg"), ("All Files", "*.*")),
                                                       title="Choose an Image"
                                                       )
        self.tile_image()


####################################

    def tile_image(self):

        time_stamp = time.time()
        self.set_tile_counter()
        self.make_dir()

        self.img = cv2.imread(self.img_location)
        scanner_location_x = 0
        scanner_location_y = 0
        stride = 50
        scanner = (80, 80, 3)
        img_height = 350
        img_width = 2000

        windows = view_as_windows(self.img, scanner)

        num_of_height_images = int((img_height) / stride)
        num_of_width_images = int(img_width / stride)
        tiles = range(int(img_height / stride) * int(img_width / stride))

        for x in range(num_of_height_images):
            for y in range(num_of_width_images):
                self.tile_location = os.path.join('Tiles/' + self.dir_name, "IMG")
                cv2.imwrite(self.tile_location + str(x) + '_' + str(y) + '.jpg', windows[scanner_location_x, scanner_location_y, 0])
                scanner_location_y = scanner_location_y + stride
            scanner_location_x = scanner_location_x + stride
            if scanner_location_x > img_height - 80:
                scanner_location_x = img_height - 80
            else:
                pass
            scanner_location_y = 0

        self.display_image()


#####################################

    def display_image(self):

        self.img = cv2.resize(self.img, (80, 80))
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.display_img = Image.fromarray(self.img)
        self.resized_img = self.display_img.resize((460, 81), Image.ANTIALIAS)
        self.resized_img = ImageTk.PhotoImage(image=self.resized_img)
        self.img_label.resized_img = self.resized_img
        self.img_label.configure(image=self.resized_img)
        self.load_label.config(text="Image has been tiled")


#####################################

    def make_dir(self):

        self.my_dir = 'Tiled_Image'
        self.dir_name = self.my_dir + '_' + "%03d" % self.tile_counter
        try:
            os.makedirs('Tiles/' + self.dir_name)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise


###########################################################

    def set_tile_counter(self):

        if not os.path.exists(self.tiles_dir):
            os.makedirs(self.tiles_dir)
        self.list_of_dirs = os.listdir(self.tiles_dir)
        self.tile_counter = len(self.list_of_dirs) + 1


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
    root.title("Image Tiling")
    file_menu(root, b)
    root.mainloop()

###########################################


def file_menu(root, b):
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Load Image", command=b.load_image)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)

############### Program Functions END ##################

######////////////////////////////////////////////////////////////////////////////////////////////##########


########################################################
if __name__ == '__main__':
    main()
