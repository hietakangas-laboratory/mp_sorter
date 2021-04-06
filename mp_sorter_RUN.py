'''
Author: Jack Morikka.
A programme to save MP coordinates from tiffs with imageJ MP selection
and then to place these in the corresponding output directories
'''

import os
from tkinter import *
from tkinter import filedialog
import logging
import subprocess


class MP_sort:
    '''
    Creates a GUI window to derive from the user the input folder with tiffs
    and output folder with LAM files which the vector.txt files will be moved into
    '''
    def __init__(self):

        self.__py_file_dir = os.path.dirname(os.path.realpath(__file__))
        self.__py_file = r"\mp_sorter.py"
        self.__py_file_loc = self.__py_file_dir + self.__py_file

        # Creates the structure for the GUI with the title
        self.__window = Tk()
        self.__window.title('MP_sorter')


        # Creates label for select ImageJ.exe prompt
        self.__s_ij_prompt = Label(self.__window,
                                   text='Select ImageJ.exe file:') \
            .grid(row=3, column=1, sticky=E)

        # Creates the browse button for getting the ImageJ.exe path
        Button(self.__window, text='Browse', command=self.retrieve_ifolder) \
            .grid(row=3, column=2)

        # Creates the variable label for ImageJ path text
        self.__imgj_path = StringVar()
        self.__selectij = Label(self.__window, text=self.__imgj_path.get(),
                                bg='white', bd=2,
                                textvariable=self.__imgj_path, relief='sunken')
        self.__selectij.grid(row=3, column=3, columnspan=3, sticky=W)

        # Creates label for select root folder prompt
        self.__r_dir_prompt = Label(self.__window,
                                    text='Select tiff folder (tiffs '
                                         'contain manually drawn MPs):') \
            .grid(row=5, column=1, sticky=E)

        # Creates the browse button for getting the root folder
        Button(self.__window, text='Browse', command=self.retrieve_rfolder) \
            .grid(row=5, column=2)

        # Creates the variable label for root folder text
        self.__rfolder = StringVar()
        self.__selectDir = Label(self.__window, text=self.__rfolder.get(),
                                 bg='white', bd=2,
                                 textvariable=self.__rfolder, relief='sunken')
        self.__selectDir.grid(row=5, column=3, columnspan=3, sticky=W)

        # Creates label for select analysis folder prompt
        self.__a_dir_prompt = Label(self.__window,
                                    text='Select LAM analysis folder to place MP data:') \
            .grid(row=6, column=1, sticky=E)
        # Creates the browse button for getting the analysis folder
        Button(self.__window, text='Browse', command=self.retrieve_afolder) \
            .grid(row=6, column=2)

        # Creates the variable label for analysis folder text
        self.__afolder = StringVar()
        self.__selectDir = Label(self.__window, text=self.__afolder.get(),
                                 bg='white', bd=2,
                                 textvariable=self.__afolder, relief='sunken')
        self.__selectDir.grid(row=6, column=3, columnspan=3, sticky=W)

        # Creates the run button for running the simulator
        Button(self.__window, text='Run', command=self.go) \
            .grid(row=11, column=1, sticky=E)

        # Creates button for quitting the stitcher
        Button(self.__window, text='Quit', command=self.quit_func) \
            .grid(row=11, column=2, sticky=W)

    def retrieve_ifolder(self):
        ''' Retrieves imageJ path with file selection prompt'''
        selected_path = filedialog.askopenfilename()
        self.__imgj_path.set(selected_path)

    def retrieve_rfolder(self):
        ''' Retrieves directory with tiffs path with directory selection prompt
        '''

        selected_directory = filedialog.askdirectory()
        self.__rfolder.set(selected_directory)


    def retrieve_afolder(self):
        ''' Retrieves LAM analysis directory with directory selection
        prompt'''

        selected_directory = filedialog.askdirectory()
        self.__afolder.set(selected_directory)

    def prompt_creator(self):
        '''Creates prompt for subprocess that will call imageJ in headless
        mode to run the macro for saving the vector.txt files'''
        prompt_items = [str(self.__rfolder.get()),
                        str(self.__afolder.get())]

        prompt = ' "tiff_dir=\'{p[0]}\',analysis_dir=\'{p[1]}\'"'\
            .format(p=prompt_items)

        lab_prompt = self.__imgj_path.get() + " --ij2 --headless --console --run " + \
                     self.__py_file_loc + prompt

        return lab_prompt

    def go(self):

        if self.__rfolder.get() == '' or self.__imgj_path.get() == '' or self.__afolder.get() == '':
            from tkinter import messagebox

            messagebox.showinfo("Warning", "ImageJ path or a folder not"
                                           " selected!")
        else:
            logging.basicConfig(
                filename='%s/MP_sorter.log' % self.__rfolder.get(),
                format='%(asctime)s %(levelname)-8s %(message)s',
                level=logging.INFO,
                datefmt='%d-%m-%Y %H:%M:%S')

            lab_prompt = self.prompt_creator()
            logging.info('Prompt: %s' % lab_prompt)
            try:
                self.__window.destroy()
                subprocess.call(lab_prompt, shell=True)
            except Exception as e:
                logging.exception(str(e))

    def quit_func(self):

        self.__window.destroy()

    def start(self):

        self.__window.mainloop()


def main():
    ui = MP_sort()
    ui.start()


main()
