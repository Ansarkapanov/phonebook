from Tkinter import *
import json
import re

class PhoneBook:
    """Stores the collection of contacts.

    It's responsible for pulling and pushing the contacts to permanent local storage.

    Attributes:
        contacts (list): a list containing Contacts
    """
    contacts = []

    def __init__(self):
        '''Initializer for a PhoneBook; draws local storage from phonebook.json'''

        self.pull()

    def toJSON(self):
        jsonContacts = []
        for c in self.contacts:
            jsonContacts.append(c.toJSON())
        return {'contents': jsonContacts}

    def pull(self):
        '''Pulls contacts from local storage

        Looks at phonebook.json and converts the JSON string to a dict.
        '''
        with open('phonebook.json') as data_file:  
            data = json.load(data_file)['contents']

        for contactDict in data:
            c = Contact(contactDict)
            self.contacts.append(c)

    def push(self):
        '''Pushes self.contacts to phonebook.json'''
        with open('phonebook.json', 'w') as data_file:
            json.dump(self.toJSON(), data_file) # convert from list of dicts to JSON string and save file

    def add(self, contact):
        ''' Adds a Contact object to self.contacts'''

        self.contacts.append(contact)
        self.push()

    def restoreLocalStorage(self):
        with open('phonebook copy.json') as data_file:
            data = json.load(data_file)

        with open('phonebook.json', 'w') as data_file:
            json.dump(data, data_file)

    def deleteLocalStorage(self):
         with open('phonebook.json', 'w') as data_file:
            json.dump({"contents":[]}, data_file)       

class Contact:
    """Representation of a contact in the Phonebook.

    Attributes:
        first_name (str): contact's first name
        last_name (str): contact's first name
        addr1 (str): First line of contact's address
        addr2 (str): Second line of contac's address
        homePh (str): Home phone number
        workPh (str): Work phone number
        cellPh (str): Cell phone number
        fax (str): Fax number
        email (Str): Email address
    """
    dataFields = {'first_name':'First Name', 'last_name':'Last Name', 'addr1':'Address Line 1',
        'addr2':'Address Line 2', 'homePh':'Home Phone', 'workPh':'Work Phone', 
        'cellPh':'Cell Phone', 'fax':'Fax', 'email':'Email Address'}

    def __init__(self, obj):
        '''Init method for contact.

        Args:
            **kwargs: These will be the info fields for a contact

        '''
        # Set default values
        for f in self.dataFields:
            setattr(self, f, None)

        for field, value in obj.items():
            setattr(self, field, value)

    def toJSON(self):
        json = {}
        for f in self.dataFields:
            attr = getattr(self, f)
            if attr != None:
                json[f] = attr
        return json

    def queryString(self):
        string = ''
        for f in self.dataFields:
            attr = getattr(self, f)
            if attr != None:
                string = ' '.join([string, attr])
        return string

    def __str__(self):
        return ' '.join([self.first_name, self.last_name, ',', self.addr2])

class App:
    """Representation of a Tkinter PhoneBook application"""
    tracers = []

    def __init__(self, root):
        """Initializer for PhoneBook application.

        Args:
            root (Tkinter root widget): the main root widget
        """
        # pull contacts into python
        self.pb = PhoneBook()

        # construct the Frame
        Grid.rowconfigure(root, 0, weight=1)
        Grid.columnconfigure(root, 0, weight=1)
        self.frame = Frame(root, width=100, height=150, padx=10, pady=10) # preliminary structure
        root.title('Phonebook')
        self.frame.pack()

        addButton = Button(self.frame, text='Add Contact', command=self.showCreationForm).grid(row=0, column=0)
        listButton = Button(self.frame, text='View Contacts', command=self.showContactList).grid(row=0, column=1)
        printButton = Button(self.frame, text='Print', command=self.toPDF).grid(row=0, column=2)

        self.showCreationForm()
        # self.showContactList()

        # after all elements added to frame center the window
        root.update()
        screenWidth = self.frame.winfo_screenwidth()
        screenHeight = self.frame.winfo_screenheight()
        frameWidth = self.frame.winfo_width()
        frameHeight = self.frame.winfo_height()
        xoffset = (screenWidth - frameWidth) / 2 # determine offsets via widths
        yoffset = (screenHeight - frameHeight) / 2
        root.geometry("%dx%d%+d%+d" % (frameWidth, frameHeight, xoffset, yoffset)) # move window

    def clearSearch(self, *args):
        self.searchQuery.set('')

    def searchPhonebook(self, *args):
        #search for contact
        query = self.searchQuery.get()
        results = []
        if query == '':
            self.filterContactList(self.pb.contacts)
        elif query != 'Search for contacts...':
            for c in self.pb.contacts:
                regexp = '(?i)' + query
                match = re.search(regexp, c.queryString())
                if match != None:
                    results.append(c)

            self.filterContactList(results)

    def resetActionPane(self):
        if hasattr(self, 'actionPane'):
            self.actionPane.destroy()

        self.actionPane = Frame(self.frame)
        self.actionPane.grid(row=1, column=0, columnspan=3, sticky=W+E+N+S)

    def showContactList(self):
        self.resetActionPane()
        self.activeView = {} #namespace

        self.searchQuery = StringVar()
        search = Entry(self.actionPane, textvariable=self.searchQuery, width=40)
        search.grid(row=0, column=0, columnspan=2)
        search.insert(0, 'Search for contacts...')
        search.bind('<Button-1>', self.clearSearch)

        scrollbar = Scrollbar(self.actionPane, orient=VERTICAL)
        self.activeView['contactList'] = Listbox(self.actionPane, yscrollcommand=scrollbar.set, width=40)
        self.activeView['contactList'].grid(row=1, column=0, columnspan=2)
        scrollbar.config(command=self.activeView['contactList'].yview)

        for contact in self.pb.contacts:
            self.activeView['contactList'].insert(END, str(contact))

        self.searchQuery.trace('w', self.searchPhonebook)

    def filterContactList(self, filtered):
        self.activeView['contactList'].delete(0, END)

        for contact in filtered:
            self.activeView['contactList'].insert(END, str(contact))

    def showCreationForm(self):
        self.resetActionPane()
        self.activeView = {} #namespace

        n = 0
        for field, longField in Contact.dataFields.items():
            self.activeView[field] = StringVar()
            Label(self.actionPane, text=longField).grid(row=n, column=0, sticky=E)
            Entry(self.actionPane, textvariable=self.activeView[field]).grid(row=n, column=1)
            n += 1

        Button(self.actionPane, text="Save Contact", command=self.submitCreationForm).grid(row=n, column=1)

    def submitCreationForm(self):
        data = {}
        for field, textvariable in self.activeView.items():
            value = textvariable.get()
            if value != '':
                data[field] = textvariable.get()

        contact = Contact(data)
        self.pb.add(contact)
        self.showContactList()

    def toPDF(self):
        pass


root = Tk()

app = App(root)

root.mainloop()
