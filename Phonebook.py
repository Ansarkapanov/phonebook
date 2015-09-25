from Tkinter import *
import json

class PhoneBook:
    '''Stores the collection of contacts.

    It's responsible for pulling and pushing the contacts to permanent local storage.

    Attributes:
        contacts (list): a list containing Contacts
    '''

    def __init__(self):
        '''Initializer for a PhoneBook; draws local storage from phonebook.json'''

        self.pull()

    def pull(self):
        '''Pulls contacts from local storage

        Looks at phonebook.json and converts the JSON string to a dict.
        '''

        with open('phonebook.json') as data_file:  
            self.contacts = json.load(data_file)['contents'] # convert from JSON string to dict

    def push(self, contact):
        '''Pushes self.contacts to phonebook.json'''

        with open('phonebook.json') as data_file:
            json.dumps(self.contacts, data_file) # convert from list of dicts to JSON string and save file

    def add(self, contact):
        ''' Adds a Contact object to self.contacts'''

        self.contacts.append(contact)
        self.push()

class Contact:
    '''Representation of a contact in the Phonebook.

    Attributes:
        first_name (str): contact's first name
        last_name (str): contact's first name
        addr1 (str): First line of contact's address
        addr2 (str): Second line of contac's address
        homePh (str): Home phone number
        workPh (str): Work phone number
        cellPh (str): Cell phone number
        fax (str): Fax number
    '''

    def __init__(self, **kwargs):
        '''Init method for contact.

        Args:
            **kwargs: These will be the info fields for a contact

        '''

        # Set default values
        self.first_name = ''
        self.last_name = ''
        self.addr1 = ''
        self.addr2 = ''
        self.homePh = ''
        self.workPh = ''
        self.cellPh = ''
        self.fax = ''

        # Set given values from kwargs
        if kwargs is not None:
            for field, value in kwargs.items():
                setattr(self, field, value)

class App:
    '''Representation of a Tkinter PhoneBook application'''

    def __init__(self, root):
        '''Initializer for PhoneBook application.

        Args:
            root (Tkinter root widget): the main root widget
        '''

        # pull contacts into python
        pb = PhoneBook()

        # construct the Frame
        frame = Frame(root, padx=10, pady=10) # preliminary structure
        root.title('Phonebook')
        frame.pack()
        searchLabel = Label(frame, text='Search names:').grid(row=0, column=0)
        search = Entry(frame).grid(row=0, column=1)
        addButton = Button(frame, '+add', command=pb.add).grid(row=0, column=3)

        # after all elements added to frame center the window
        root.update()
        screenWidth = frame.winfo_screenwidth()
        screenHeight = frame.winfo_screenheight()
        frameWidth = frame.winfo_width()
        frameHeight = frame.winfo_height()
        xoffset = (screenWidth - frameWidth) / 2 # determine offsets via widths
        yoffset = (screenHeight - frameHeight) / 2
        root.geometry("%dx%d%+d%+d" % (frameWidth, frameHeight, xoffset, yoffset)) # move window

root = Tk()

app = App(root)

root.mainloop()
