from Tkinter import *

class Contact:
    '''Representation of a contact in the Phonebook.

    Attributes:
        data (dict): dictionary of contact fields
    '''
    def __init__(self, data):
        '''Init method for contact.

        Args:
            data (dict): A dictionary containing the default values to set
        '''
        # Set default (given) values
        if kwargs is not None:
            for field, value in kwargs:
                self.field = value

    def save(self):
        # make file if DNE
        # get contact list and append
        # overwrite old file
        pass

    def __str__(self):
        pass


class App:
    def __init__(self, root):
        frame = Frame(root, padx=10, pady=10)
        root.title('Phonebook')
        frame.pack()
        l1 = Label(frame, text="Hello, world!")
        l1.grid(row=0)

        # After all elements added to frame center the window
        root.update()
        screenWidth = frame.winfo_screenwidth()
        screenHeight = frame.winfo_screenheight()

        frameWidth = frame.winfo_width()
        frameHeight = frame.winfo_height()

        print frameWidth

        xoffset = (screenWidth - frameWidth) / 2
        yoffset = (screenHeight - frameHeight) / 2

        # root.geometry("%dx%d%+d%+d" % (frameWidth, frameHeight, xoffset, yoffset))

root = Tk()

app = App(root)

root.mainloop()