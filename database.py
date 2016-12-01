import tkinter
from tkinter import *
import os
import sqlite3
import client

notesHeight = 8
notesWidth = 35

connection = sqlite3.connect("clientDB.db")
c= connection.cursor()



#Make sure that all temporary files are deleted
#in case program didn't close properly
#i.e. power failure
if(os.path.isfile("tempClientID.txt")):
    os.remove("tempClientID.txt")
if(os.path.isfile("temp_clientID.txt")):
    os.remove("temp_clientID.txt")
if(os.path.isfile("temp_clientList.txt")):
    os.remove("temp_clientList.txt")




def protocolhandler():
    tkinter.messagebox.showinfo("Redirect",\
                                "Please exit using the 'FILE -- EXIT' command.\nThank you!")
class realestate:
    def __init__(self):
        
        
        location = "master"
        infile = open("_location_.txt","w")
        infile.write(location)
        infile.close()

        

        self.master = tkinter.Tk()

        self.master.protocol("WM_DELETE_WINDOW", protocolhandler)

        self.setTitle()

        #Centers the window with in the screen
        x = (self.master.winfo_screenwidth() -self.master.winfo_reqwidth())/2
        y = (self.master.winfo_screenheight()-self.master.winfo_reqheight())/2
        self.master.geometry("+%d+%d" % (x,y))

        #Create a menu bar
        menuBar = Menu(self.master)
        self.master.config(menu = menuBar)

        global fileMenu
        fileMenu = Menu(menuBar)
        menuBar.add_cascade(label = "File", menu = fileMenu)
        fileMenu.add_command(label = "New Client", command =self.newclient)
        fileMenu.add_command(label = "Exit", command = self.exitHandler)

        searchMenu = Menu(menuBar)
        menuBar.add_cascade(label = "Search", menu = searchMenu)
        searchMenu.add_command(label = "Alternate Search", command = self.altSearch)

        helpMenu = Menu(menuBar)
        menuBar.add_cascade(label = "Help", menu = helpMenu)
        helpMenu.add_command(label = "Instructions", command = self.mainInstruct)

        #End menu bar creation

        #Create main screen

        self.mainFrame = tkinter.Frame(self.master)
        self.firstFrame = tkinter.Frame(self.master)
        self.middleFrame = tkinter.Frame(self.master)
        self.lastFrame = tkinter.Frame(self.master)
        self.buttonFrame = tkinter.Frame(self.master);

        self.titleLabel = tkinter.Label(self.mainFrame,\
                                        text="\nSearch Screen\n",\
                                        font="Helvetica, 12 bold")

        self.mainFrame.pack()
        self.titleLabel.pack()

        self.fnamePrompt = tkinter.Label(self.firstFrame,\
                                         text="First Name",\
                                         width = 12,\
                                         font= "Helvetica, 12")

        self.fnameentry=tkinter.Entry(self.firstFrame,\
                                      width=12,\
                                      justify="center")
        
        self.firstFrame.pack()
        self.fnamePrompt.pack(side='left')
        self.fnameentry.pack(side='right')

        

        #Define middleFrame
        self.middleprompt=tkinter.Label(self.middleFrame,\
                                        text="M.I.",\
                                        width = 12,\
                                        font="Helvetica, 12")
        self.middleentry=tkinter.Entry(self.middleFrame,\
                                       width=12,\
                                       justify="center")

        self.middleFrame.pack()
        self.middleprompt.pack(side='left')
        self.middleentry.pack(side='right')

        #Define lastFrame
        self.lnameprompt=tkinter.Label(self.lastFrame,\
                                       text="Last Name",\
                                       width = 12,\
                                       font="Helvetica, 12")
        self.lnameentry=tkinter.Entry(self.lastFrame,\
                                      width=12,\
                                      justify="center")

        self.lastFrame.pack()
        self.lnameprompt.pack(side='left')
        self.lnameentry.pack(side='right')

        #Define buttonFrame
        self.newButton=tkinter.Button(self.buttonFrame,\
                                      text="New Client",\
                                      font="Helvetica, 11",\
                                      command=self.newclient)
        self.searchButton=tkinter.Button(self.buttonFrame,\
                                         text="Search",\
                                         font="Helvetica, 11",\
                                         command=self.search)
        self.altSearchButton=tkinter.Button(self.buttonFrame,\
                                            text="Advanced Search",\
                                            font="Helvetica, 11",\
                                            command=self.altSearch)

        self.buttonFrame.pack()
        self.newButton.pack(side='left')
        self.searchButton.pack(side='left')
        self.altSearchButton.pack(side='left')

        #Create a decorative image to make application attractive

        self.canvas=Canvas(width=110, height=115)
        self.canvas.pack(expand=NO, fill=X)
        global pic
        pic=PhotoImage(file="smallhouse.png")
        self.canvas.create_image(150,100, image=pic, anchor=S)

        tkinter.mainloop()

    
    def exitHandler(self):
        connection.close()
        try:
            if(os.path.isfile("tempClientID.txt")):
                os.remove("tempClientID.txt")
            if(os.path.isfile("temp_clientID.txt")):
                os.remove("temp_clientID.txt")
            if(os.path.isfile("temp_clientList.txt")):
                os.remove("temp_clientList.txt")
        except PermissionError:
            infile = open("errorLog.txt", "a")
            infile.write("Permission_Error_exitHandler\n")
            infile.close()
            
            self.master.destroy()
            sys.exit(0)

        self.master.destroy()
        sys.exit(0)

    def newClientSubmit(self):
        fname = self.fNameEntry.get()
        mname = self.mNameEntry.get()
        lname = self.lNameEntry.get()
        pnumber=self.pNumberEntry.get()
        anumber = self.aNumberEntry.get()

        buying = self.cb_isBuying.get()
        selling = self.cb_isSelling.get()

        if(buying == 1 and selling ==1):
            status = 3
        elif (buying ==1 and selling ==0 ):
            status = 2
        elif (buying == 0 and selling == 1):
            status = 1
        else:
            status = 0


        numClients = client.getClientInfo.numClients()
        numClients+=1

        c.execute("INSERT INTO clientInfo(cliNum, firstName, middleName, lastName, phone, altPhone, status) VALUES(?,?, ?, ?, ?, ?, ?)",(numClients, fname.lower(), mname.lower(), lname.lower(), pnumber, anumber, status))
        connection.commit()
        
        #Keep saving the notes to a txt file.  Save everything else to db though it would be nice in a db or a table
        #Trying to figure out how to get the notes to save to txt file
        count = 1.0
        for lines in str(self.notesText):
            text=self.notesText.get(1.0, "end")
            text=text+'/'
        
        infile=open(fname.lower()+mname.lower()+lname.lower()+"notes.txt",'w')
        infile.write(text)
        infile.close()





        tkinter.messagebox.showinfo("Confirmation",\
                                    fname+" "+mname+" "+lname+" has been added.")
        

        self.master.destroy()
        self.__init__()
        

    def altSearch(self):
        infile = open("_location_.txt", "w")
        infile.write("master")
        infile.close()
        
        self.unpack()
        
        location = "alternateSearch"
        infile = open("_location_.txt", "w")
        infile.write(location)
        infile.close()

        self.setTitle()

        self.setScreen(location)

        

    
            
        

    def unpack(self):
        infile = open("_location_.txt","r")
        location = infile.read()
        infile.close()
        if(location == "new" or location == "alternateSearch" or location == "managerial"):
            self.master.destroy()
            self.__init__()

            

        elif(location == "clientinfo"):
            self.master.destroy()
            self.__init__()
        elif(location == "master"):
            self.mainFrame.pack_forget()
            self.firstFrame.pack_forget()
            self.middleFrame.pack_forget()
            self.lastFrame.pack_forget()
            self.buttonFrame.pack_forget()
            self.canvas.pack_forget()
            
        

    def setTitle(self):
        infile = open("_location_.txt", "r")
        location = infile.read()
        infile.close()
        if(location == "master"):
            self.master.title("ClientDB")
        elif(location == "new"):
            self.master.title("New Client")
        elif(location == "clientinfo"):
            self.master.title("View Client Information")
        elif(location == "alternateSearch"):
            self.master.title("Alternate Search")
    
        

    def mainInstruct(self):

        #This function takes the current location from a text file
        # when the user clicks HELP -- INSTRUCTIONS from the menu bar
        # and gives them some instructions about that particular screen.

        infile = open("_location_.txt", "r")
        location = infile.read()
        infile.close()
        
        if location=="master":
            tkinter.messagebox.showinfo("Help",\
                                        "Enter name information"+
                                        "\nto search for client information."+
                                        "\nClick 'New Client' to enter new"+
                                        "\nclient information."+
                                        "\nClick 'Advanced Search' to search"+
                                        "\nfor alternative parameters.")
           
        elif location=="new":
            tkinter.messagebox.showinfo("Help",\
                                        "Fill out the information for"+
                                        "\nthe new Property Client and"+
                                        "\nclick 'Submit' to save information."+
                                        "\nClick 'Cancel' to return to Main Search.")
        elif location=="managerial":
            tkinter.messagebox.showinfo("Help",\
                                        "'Reset All' button will reset"+
                                        "\nprogram to original default settings.")
        elif location=="clientinfo":
            tkinter.messagebox.showinfo("Help",\
                                        "View client info"+
                                        "\nChange information and click update"+
                                        "\nto save information")
        elif location=="alternateSearch":
            tkinter.messagebox.showinfo("Help",\
                                        "Enter a telephone number to search\n"+
                                        "for all clients with that telephone number.")
    def clear(self):
        #Clear out all fields within a new client
        #setup
        self.fNameEntry.delete(0, END)
        self.mNameEntry.delete(0, END)
        self.lNameEntry.delete(0, END)
        self.pNumberEntry.delete(0, END)
        self.aNumberEntry.delete(0, END)
        self.cb_isBuying.set(0)
        self.cb_isSelling.set(0)
        self.notesText.delete(1.0, END)

    def printNotes(self):
        import subprocess

        #Make sure client_notes.txt doesn't exist
        if(os.path.isfile("client_notes.txt")):
           os.remove("client_notes.txt")
        
        fname = self.fNameEntry.get()
        fname = fname.lower()

        mname = self.mNameEntry.get()
        mname = mname.lower()

        lname = self.lNameEntry.get()
        lname = lname.lower()

        fileName = fname+mname+lname+"notes.txt"
        phone = self.pNumberEntry.get()
        if(phone == "" or phone == " "):
            phone = "None Listed"
        altphone = self.aNumberEntry.get()
        if(altphone == "" or altphone == " "):
            altphone = "None Listed"


        for lines in str(self.notesText):
            notes = self.notesText.get(1.0, "end")
        


        
        infile = open("client_notes.txt","a")
        infile.write("Notes for: "+fname.title()+" "+mname.title()+" "+lname.title()+"\n")
        infile.write("Main Telephone:       "+phone+"\n")
        infile.write("Alternate Telephone:  "+altphone+"\n")
        infile.write("\n\nClient Notes:\n\n")

        infile.write(notes)
        infile.close()

        subprocess.call(["notepad.exe","/p","client_notes.txt"])

        os.remove("client_notes.txt")
    
            
    def reset(self):
        import os
        try:
            infile = open("allFiles.txt","r")
            readfile = infile.read()
            readfile = readfile.split("/")
            count = 0
            for files in readfile:
                file = readfile[count]
                file = file.replace(".txt", "notes.txt")
                os.remove(file)
                os.remove(readfile[count])
                count+=1
            infile.close()

            infile = open("allFiles.txt", "w")
            infile.write("")
            infile.close()

            tkinter.messagebox.showinfo("Confirmation",\
                                        "All files have been erased.\nProgram reset to inital settings.")
        except FileNotFoundError:
            tkinter.messagebox.showinfo("Files Do Not Exist",\
                                        "There are not any files to delete")
    
    def phone(self):
        
        phone = self.phoneEntry.get()

        getClientList = []
        getClientIDList = []

        for clients in c.execute("SELECT firstName, middleName, lastName, cliNum FROM clientInfo WHERE phone LIKE ?", ("%"+phone+"%",)):
            name = clients[0].title()+" "+ clients[1].title() + " " + clients[2].title()
            clientID = clients[3]

            getClientList.append(name)
            getClientIDList.append(clientID)

        if(os.path.isfile("temp_clientList.txt")):
            os.remove("temp_clientList.txt")
        if(os.path.isfile("temp_clientID.txt")):
            os.remove("temp_clientID.txt")

        
        
        infile = open("temp_clientID.txt", "w")
        
        for ID in getClientIDList:
            infile.write(str(ID)+"/")
        infile.close()

        infile = open("tempClientID.txt", "w")
        for ID in getClientIDList:
            infile.write(str(ID)+"/")
        infile.close()
        
        #######################################################################################
        self.titleFrame.pack_forget()
        self.phoneSearch.pack_forget()
        self.altPhoneSearch.pack_forget()
        self.cancelFrame.pack_forget()
        self.canvas.pack_forget()

        if(len(getClientList)>1):
            
            self.master.title("Multiple Clients Found")
            self.multiFrame = tkinter.Frame(self.master)
            self.title = tkinter.Label(self.multiFrame, text = "Multiple Clients. Choose Desired Client.")

            self.multiFrame.pack()
            self.title.pack()

            count = 0
            for person in getClientList:
                disp = count+1
                label = str(disp)+". "+getClientList[count]
                self.listLabel = tkinter.Label(self.multiFrame, text = label)
                self.listLabel.pack()

                count+=1

            self.choice = tkinter.Entry(self.multiFrame, width = 15, justify = CENTER)
            self.button = tkinter.Button(self.multiFrame, text = "Submit", command = self.save)

            self.choice.pack(side="left")
            self.button.pack(side="left")
        elif(len(getClientList) == 0):
            tkinter.messagebox.showinfo("Alert",\
                                        "There are zero clients with"+
                                        "\nthat main contact number.")
            self.master.destroy()
            self.__init__()
        else:
            self.setScreen("clientinfo")

    

    def altPhone(self):
        altPhone = self.altPhoneEntry.get()

        getClientList = []
        getClientIDList = []

        for clients in c.execute("SELECT firstName, middleName, lastName, cliNum FROM clientInfo WHERE altPhone LIKE ?", ("%"+altPhone+"%",)):
            name = clients[0].title()+" "+ clients[1].title() + " " + clients[2].title()
            clientID = clients[3]

            getClientList.append(name)
            getClientIDList.append(clientID)

        if(os.path.isfile("temp_clientList.txt")):
            os.remove("temp_clientList.txt")
        if(os.path.isfile("temp_clientID.txt")):
            os.remove("temp_clientID.txt")

        
        
        infile = open("temp_clientID.txt", "w")
        for ID in getClientIDList:
            infile.write(str(ID)+"/")
        infile.close()

        infile = open("tempClientID.txt", "w")
        for ID in getClientIDList:
            infile.write(str(ID)+"/")
        infile.close()
        
        
        self.titleFrame.pack_forget()
        self.phoneSearch.pack_forget()
        self.altPhoneSearch.pack_forget()
        self.cancelFrame.pack_forget()
        self.canvas.pack_forget()

        if(len(getClientList)>1):
            self.master.title("Multiple Clients Found")
            self.multiFrame = tkinter.Frame(self.master)
            self.title = tkinter.Label(self.multiFrame, text = "Multiple Clients. Choose Desired Client.")

            self.multiFrame.pack()
            self.title.pack()

            count = 0
            for person in getClientList:
                disp = count+1
                label = str(disp)+". "+getClientList[count]
                self.listLabel = tkinter.Label(self.multiFrame, text = label)
                self.listLabel.pack()

                count+=1

            self.choice = tkinter.Entry(self.multiFrame, width = 5)
            self.button = tkinter.Button(self.multiFrame, text = "Submit", command = self.save)

            self.choice.pack(side="left")
            self.button.pack(side="left")
        elif(len(getClientList) == 0):
            tkinter.messagebox.showinfo("Alert",\
                                        "There are zero clients with"+
                                        "\nthat alternate contact number.")
            self.master.destroy()
            self.__init__()
        else:
            self.setScreen("clientinfo")


        
    def save(self):
        try:
            choice = int(self.choice.get())

            choice-=1

            infile = open("temp_clientID.txt", "r")
            clientIDList = infile.read()
            clientIDList = clientIDList.split("/")
            infile.close()

            infile = open("tempClientID.txt", "w")
            infile.write(clientIDList[choice])
            infile.close()

            self.multiFrame.pack_forget()

            infile = open("_location_.txt", "w")
            infile.write("clientinfo")
            infile.close()

            self.setScreen("clientinfo")
        except NameError:
            tkinter.messagebox.showinfo("Error",\
                                    "Enter an integer number.\nDo not enter a name.")
        except ValueError:
            tkinter.messagebox.showinfo("Error",\
                                        "Please enter an integer number.\nDo not leave blank.")
        except IndexError:
            tkinter.messagebox.showinfo("Error",\
                                        "Invalid Choice.  Choose again.")
    def saveChangesToDB(self):

        #Update database here
        
        infile = open("tempClientID.txt", "r")
        readfile = int(infile.read())
        infile.close()

        if(os.path.isfile("tempClientID.txt")):
           os.remove("tempClientID.txt")
        
        fName = self.fNameEntry.get()
        fName = fName.lower()
        mName = self.mNameEntry.get()
        mName = mName.lower()
        lName = self.lNameEntry.get()
        lName = lName.lower()
        pNumber = self.pNumberEntry.get()
        aNumber = self.aNumberEntry.get()


        buying = self.cb_isBuying.get()
        selling = self.cb_isSelling.get()
        

        if(buying == 1 and selling ==1):
            status = 3
        elif (buying ==1 and selling ==0 ):
            status = 2
        elif (buying == 0 and selling == 1):
            status = 1
        else:
            status = 0

        if(tkinter.messagebox.askokcancel("Warning", "Are you sure you wish to save changes?\nThis is irreversible")):
            

            c.execute("UPDATE clientInfo SET firstName = ?, middleName = ?, lastName = ?, phone = ?, altPhone = ?, status = ? WHERE cliNum = ?", (fName, mName, lName, pNumber, aNumber, status, readfile))

            connection.commit()

            infile = open(superFileName+"notes.txt", "w")

            for lines in str(self.notesText.get(1.0, "end")):
                notes = self.notesText.get(1.0, "end")
                notes = notes+"/"

            infile.write(notes)                
            
            infile.close()

            tkinter.messagebox.showinfo("Confirmation", "Changes have been saved.")
            
        else:
            tkinter.messagebox.showinfO("Confirmation", "Changes have been discarded.")

        
        
    def setScreen(self, location):
        if(location == "alternateSearch"):
            self.titleFrame=tkinter.Frame(self.master)
            self.phoneSearch = tkinter.Frame(self.master)
            self.altPhoneSearch = tkinter.Frame(self.master)
            self.cancelFrame = tkinter.Frame(self.master)

            self.advtitlelabel = tkinter.Label(self.titleFrame,\
                                               text = "Advanced Search",\
                                               font = "Helvetica, 12 bold")
            self.titleFrame.pack()
            self.advtitlelabel.pack()

            self.phonePrompt = tkinter.Label(self.phoneSearch,\
                                             text = "Telephone",\
                                             font = "Helvetica, 12")
            self.phoneEntry = tkinter.Entry(self.phoneSearch,\
                                            width = 15,\
                                            justify = "center")
            self.phoneSearchButton = tkinter.Button(self.phoneSearch,\
                                                    text = "Search",\
                                                    command = self.phone)

            self.phoneSearch.pack()
            self.phonePrompt.pack(side="left")
            self.phoneEntry.pack(side="left")
            self.phoneSearchButton.pack(side="left")

            self.altPhonePrompt = tkinter.Label(self.altPhoneSearch,\
                                                text = "Alt. Phone",\
                                                font = "Helvetica, 12")
            self.altPhoneEntry=tkinter.Entry(self.altPhoneSearch,\
                                         width=15,\
                                         justify='center')
            self.altPhoneSearchButton=tkinter.Button(self.altPhoneSearch,\
                                               text="Search",\
                                               command=self.altPhone)

            self.altPhoneSearch.pack()
            self.altPhonePrompt.pack(side='left')
            self.altPhoneEntry.pack(side='left')
            self.altPhoneSearchButton.pack(side='left')

            self.cancelButton=tkinter.Button(self.cancelFrame,\
                                             text="Back To Search",\
                                             command=self.unpack)

            self.cancelFrame.pack()
            self.cancelButton.pack()

            
            

        elif(location == "new" or location == "clientinfo"):
            #at the end of this block use if else statement
            #for buttons to send to different functions
            if(location == "new"):
                self.titleFrame = tkinter.Frame(self.master)
            self.firstFrame = tkinter.Frame(self.master)
            self.middleFrame= tkinter.Frame(self.master)
            self.lastFrame = tkinter.Frame(self.master)
            self.pNumberFrame = tkinter.Frame(self.master)
            self.aNumberFrame = tkinter.Frame(self.master)
            self.statusFrame = tkinter.Frame(self.master)
            self.notesFrame = tkinter.Frame(self.master)
            self.buttonFrame = tkinter.Frame(self.master)

            #Display title
            if(location == "new"):
                self.newClientTitle = tkinter.Label(self.titleFrame,\
                                                    text = "Create New Client\n",\
                                                    font = "Helvetica, 14 bold")
                self.titleFrame.pack()
                self.newClientTitle.pack()

            
            #Display first name
            self.fName = tkinter.Label(self.firstFrame,\
                                       text = "First Name",\
                                       width = 15,\
                                       justify = "center",\
                                       relief = SUNKEN,\
                                       font = "Helvetica, 12")
            self.fNameEntry = tkinter.Entry(self.firstFrame,\
                                            width = 15,\
                                            justify = "center")

            self.firstFrame.pack()
            self.fName.pack(side="left")
            self.fNameEntry.pack(side="right")

            #Display middle name
            self.mName = tkinter.Label(self.middleFrame,\
                                       text = "M.I.",\
                                       width = 15,\
                                       relief = SUNKEN,\
                                       font = "Helvetica, 12")
            self.mNameEntry = tkinter.Entry(self.middleFrame,\
                                            width = 15,\
                                            justify = "center")
            self.middleFrame.pack()
            self.mName.pack(side = "left")
            self.mNameEntry.pack(side = "right")

            #Display last name
            self.lName = tkinter.Label(self.lastFrame,\
                                       text = "Last Name",\
                                       width = 15,\
                                       relief = SUNKEN,\
                                       font = "Helvetica, 12")
            self.lNameEntry = tkinter.Entry(self.lastFrame,\
                                            width = 15,\
                                            justify = "center")

            self.lastFrame.pack()
            self.lName.pack(side = "left")
            self.lNameEntry.pack(side = "right")

            #display primary number
            self.pNumber = tkinter.Label(self.pNumberFrame,\
                                         text = "Phone Number",\
                                         font = "Helvetica, 12",\
                                         width = 15,\
                                         relief = SUNKEN)
            self.pNumberEntry = tkinter.Entry(self.pNumberFrame,\
                                              width = 15, \
                                              justify = "center")
            self.pNumberFrame.pack()
            self.pNumber.pack(side="left")
            self.pNumberEntry.pack(side = "right")

            #display alternate number
            self.aNumber = tkinter.Label(self.aNumberFrame,\
                                         text = "Alt. Phone",\
                                         relief = SUNKEN,\
                                         width = 15,\
                                         font = "Helvetica, 12")
            self.aNumberEntry = tkinter.Entry(self.aNumberFrame,\
                                              width = 15,\
                                              justify = "center")
            self.aNumberFrame.pack()
            self.aNumber.pack(side="left")
            self.aNumberEntry.pack(side="right")


            self.cb_isBuying = tkinter.IntVar()
            self.cb_isSelling = tkinter.IntVar()

            #Clear the intVar objects to not initially
            #auto select
            self.cb_isBuying.set(0)
            self.cb_isSelling.set(0)

            self.cbBuying = tkinter.Checkbutton(self.statusFrame,\
                                                text = "Looking to Buy",\
                                                font = "Helvetica, 12",\
                                                variable = self.cb_isBuying)
            self.cbSelling = tkinter.Checkbutton(self.statusFrame,\
                                                 text = "Looking to Sell",\
                                                 font = "Helvetica, 12",\
                                                 variable = self.cb_isSelling)
            self.statusFrame.pack()
            self.cbBuying.pack()
            self.cbSelling.pack()

            #Create a textarea for a notes box
            #using variables created as fields for size
            self.notes = tkinter.Label(self.notesFrame,\
                                               text = "Notes",\
                                               font = "Helvetica, 12")
            self.notesText = tkinter.Text(self.notesFrame,\
                                             height = notesHeight,\
                                             width = notesWidth)
            self.notesFrame.pack()
            self.notes.pack(side="left")
            self.notesText.pack(side="right")

            
            if(location == "new"):
                self.submit = tkinter.Button(self.buttonFrame,\
                                             text = "Submit",\
                                             font = "Helvetica, 12",\
                                             command = self.newClientSubmit)
                self.clear = tkinter.Button(self.buttonFrame,\
                                        text = "Clear",\
                                        font = "Helvetica, 12",\
                                        command = self.clear)
                
                
            else:

                

                
                self.submit = tkinter.Button(self.buttonFrame,\
                                             text = "Save",\
                                             font = "Helvetica, 12",\
                                             command = self.saveChangesToDB)
                self.mls = tkinter.Button(self.buttonFrame,\
                                          text = "Go to MLS",\
                                          state = DISABLED,\
                                          font = "Helvetica, 12",\
                                          command = self.mls)
                self.print = tkinter.Button(self.buttonFrame,\
                                            text = "Print Client Info",\
                                            font = "Helvetica, 12",\
                                            command = self.printNotes)
            
            
            self.cancel = tkinter.Button(self.buttonFrame,\
                                            text = "Cancel",\
                                            font = "Helvetica, 12",\
                                            command = self.unpack)
            self.buttonFrame.pack()
            self.submit.pack(side="left")
            if(location == "new"):
                self.clear.pack(side ="left")
            if(location != "new"):
                self.mls.pack(side="left")
                self.print.pack(side="left")
            self.cancel.pack(side="left")

            if(location == "clientinfo"):
                try:
                    fname = self.fnameentry.get()
                    fname = fname.lower()
                    mname = self.middleentry.get()
                    mname = mname.lower()
                    lname = self.lnameentry.get()
                    lname = lname.lower()

                    
                    #Get the client id to allow user to change all info including
                    #that which program originally uses to grab client from database

                    try:
                        if not(os.path.isfile("tempClientID.txt")):
                            
                            clientID = client.getClientInfo.getClientID(fname, mname, lname)
                        else:
                            infile = open("tempClientID.txt", "r")
                            readfile = infile.read()
                            readfile = readfile.split("/")
                            infile.close()
                            clientID = readfile[0]
                        
                    except UnboundLocalError:
                        if(tkinter.messagebox.askokcancel("Error", fname.title()+" "+mname.title()+" "+lname.title()+" does not exist. Create new client?")):
                            infile = open("temp_client_name.txt", "w")
                            infile.write(fname+"/"+mname+"/"+lname)
                            infile.close()
                            self.setScreen("new")
                        else:
                            self.master.destroy()
                            self.__init__()

                    infile = open("tempClientID.txt", "w")
                    infile.write(str(clientID))
                    infile.close()

                    

                    count = 0

                    for row in c.execute("SELECT firstName, middleName, lastName, phone, altPhone, status FROM clientInfo WHERE cliNum = ?", (clientID,)):
                        clientInformation = row
                        count+=1

                    DBfname = clientInformation[0].title()
                    DBmname = clientInformation[1].title()
                    DBlname = clientInformation[2].title()
                    DBphone = clientInformation[3]
                    DBaltPhone = clientInformation[4]
                    DBstatus = clientInformation[5]




                    self.fNameEntry.insert(0, DBfname)
                    self.mNameEntry.insert(0, DBmname)
                    self.lNameEntry.insert(0, DBlname)
                    self.pNumberEntry.insert(0, DBphone)
                    self.aNumberEntry.insert(0, DBaltPhone)

                    if(DBstatus == 3):
                        self.cb_isBuying.set(1)
                        self.cb_isSelling.set(1)
                    elif(DBstatus == 2):
                        self.cb_isBuying.set(1)
                        self.cb_isSelling.set(0)
                    elif(DBstatus == 1):
                        self.cb_isBuying.set(0)
                        self.cb_isSelling.set(1)
                    else:
                        self.cb_isBuying.set(0)
                        self.cb_isSelling.set(0)

                    
                    
                    
                    #Read and insert notes from temp text file
                    if not(os.path.isfile("tempClientID.txt")):
                        infile=open(superFileName+'notes.txt','r')
                    else:
                        sql = c.execute("SELECT firstName, middleName, lastName FROM clientInfo WHERE cliNum = ?", (clientID,))
                        for name in sql:
                            firstName = name[0]
                            middleName = name[1]
                            lastName = name[2]

                        Name = firstName+middleName+lastName
                        
                        infile = open(Name+"notes.txt", 'r')
                            
                    readfile=infile.read()
                    readfile=readfile.split('/')
                    count=0
                    for lines in readfile:
                        self.notesText.insert(END, readfile[count])
                        self.notesText.insert(END, "\n")
                        count+=1
                    infile.close()
                    
                except FileNotFoundError:
                    try:
                        infile = open("errorLog.txt", "a")
                        infile.write("FileNotFound___Func_is_setScreen___location_is_new_OR_clientinfo\n")
                        infile.close()
                        print("fnfe within setScreen")
                    except FileNotFoundError:
                        infile = open("errorLog.txt", "w")
                        infile.write("errorLog_fnfe_file_created\n")
                        infile.close()
            else:
                if(os.path.isfile("temp_client_name.txt")):
                    infile = open("temp_client_name.txt", "r")
                    readfile = infile.read()
                    readfile = readfile.split("/")
                    infile.close()

                    self.fNameEntry.insert(0, readfile[0])
                    self.mNameEntry.insert(0, readfile[1])
                    self.lNameEntry.insert(0, readfile[2])

                    os.remove("temp_client_name.txt")
                        
     

    def mls(self):
        import webbrowser
        status =tkinter.messagebox.askokcancel("Accessing Browser",\
                                          "You are now accessing the MLS website.\n",\
                                          "Are you sure you wish to continue?")
        if(status):
           webbrowser.open("nwla.fusionmls.com")
        else:
            tkinter.messagebox.showinfo("Declined",\
                                        "Browser closed. MLS website not accessed.")
    def newclient(self):
        #declare old location
        infile = open("_location_.txt", "w")
        infile.write("master")
        infile.close()

        
        self.unpack()

        #set new location
        location = "new"

        infile = open("_location_.txt", "w")
        infile.write(location)
        infile.close()

        self.master.geometry("430x485")

        self.setTitle()

        self.setScreen(location)


    def search(self):
        

        infile = open("_location_.txt", "w")
        infile.write("master")
        infile.close()

        #unpack master screen
        self.unpack()

        #set new location
        location = "clientinfo"

        infile = open("_location_.txt", "w")
        infile.write(location)
        infile.close()
        
        

        fname = self.fnameentry.get()

        mname = self.middleentry.get()

        lname = self.lnameentry.get()

        if(fname == "" and lname != ""):
            #multiple search based on last name only
            #if only one person with search parameter
            #automatically display person
            #same for the elif statement only with first name
            getClientList = []
            getClientIDList = []

            

            for clients in c.execute("SELECT firstName, middleName, lastName, cliNum FROM clientInfo WHERE lastName LIKE ? ORDER BY lastName", (lname+"%",)):
                name = clients[0].title() + " " + clients[1].title() + " " + clients[2].title()
                clientID = clients[3]

                getClientList.append(name)
                getClientIDList.append(clientID)

            if(os.path.isfile("temp_clientList.txt")):
                os.remove("temp_clientList.txt")
            if(os.path.isfile("temp_clientID.txt")):
                os.remove("temp_clientID.txt")

            infile = open("temp_clientID.txt", "w")
        
            for ID in getClientIDList:
                infile.write(str(ID)+"/")
            infile.close()

            infile = open("tempClientID.txt", "w")
            for ID in getClientIDList:
                infile.write(str(ID)+"/")
            infile.close()

            #clear the main window
            self.mainFrame.pack_forget()
            self.firstFrame.pack_forget()
            self.middleFrame.pack_forget()
            self.lastFrame.pack_forget()
            self.buttonFrame.pack_forget()
            self.canvas.pack_forget()
            ################################

            if(len(getClientList)>1):
            
                self.master.title("Multiple Clients Found")
                self.multiFrame = tkinter.Frame(self.master)
                self.title = tkinter.Label(self.multiFrame, text = "Multiple Clients. Choose Desired Client.")

                self.multiFrame.pack()
                self.title.pack()

                count = 0
                for person in getClientList:
                    disp = count+1
                    label = str(disp)+". "+getClientList[count]
                    self.listLabel = tkinter.Label(self.multiFrame, text = label)
                    self.listLabel.pack()

                    count+=1

                self.choice = tkinter.Entry(self.multiFrame, width = 15, justify = CENTER)
                self.button = tkinter.Button(self.multiFrame, text = "Submit", command = self.save)

                self.choice.pack(side="left")
                self.button.pack(side="left")
            elif(len(getClientList) == 0):
                tkinter.messagebox.showinfo("Alert",\
                                            "There are zero clients with"+
                                            "\nthat last name.")
                self.master.destroy()
                self.__init__()
            else:
                self.setScreen("clientinfo")
            

        elif(fname!= "" and lname == ""):
            getClientList = []
            getClientIDList = []

            for clients in c.execute("SELECT firstName, middleName, lastName, cliNum FROM clientInfo WHERE firstName LIKE ? ORDER BY lastName", (fname+"%",)):
                name = clients[0].title() + " " + clients[1].title() + " " + clients[2].title()
                clientID = clients[3]

                getClientList.append(name)
                getClientIDList.append(clientID)

            if(os.path.isfile("temp_clientList.txt")):
                os.remove("temp_clientList.txt")
            if(os.path.isfile("temp_clientID.txt")):
                os.remove("temp_clientID.txt")

            infile = open("temp_clientID.txt", "w")
        
            for ID in getClientIDList:
                infile.write(str(ID)+"/")
            infile.close()

            infile = open("tempClientID.txt", "w")
            for ID in getClientIDList:
                infile.write(str(ID)+"/")
            infile.close()

            #clear the main window
            self.mainFrame.pack_forget()
            self.firstFrame.pack_forget()
            self.middleFrame.pack_forget()
            self.lastFrame.pack_forget()
            self.buttonFrame.pack_forget()
            self.canvas.pack_forget()
            ################################

            if(len(getClientList)>1):
            
                self.master.title("Multiple Clients Found")
                self.multiFrame = tkinter.Frame(self.master)
                self.title = tkinter.Label(self.multiFrame, text = "Multiple Clients. Choose Desired Client.")

                self.multiFrame.pack()
                self.title.pack()

                count = 0
                for person in getClientList:
                    disp = count+1
                    label = str(disp)+". "+getClientList[count]
                    self.listLabel = tkinter.Label(self.multiFrame, text = label)
                    self.listLabel.pack()

                    count+=1

                self.choice = tkinter.Entry(self.multiFrame, width = 15, justify = CENTER)
                self.button = tkinter.Button(self.multiFrame, text = "Submit", command = self.save)

                self.choice.pack(side="left")
                self.button.pack(side="left")
            elif(len(getClientList) == 0):
                tkinter.messagebox.showinfo("Alert",\
                                            "There are zero clients with"+
                                            "\nthat first name.")
                self.master.destroy()
                self.__init__()
            else:
                self.setScreen("clientinfo")
        else:

            

            global superFileName
            superFileName = fname.lower()+mname.lower()+lname.lower()

            
            
            #Convert input to all lower case
            fileMenu.add_command(label = "Print Notes", command =self.printNotes)
                        

            if (fname == "" or lname == ""):
                tkinter.messagebox.showinfo("Error",\
                                            "Please verify search parameters.")
                self.master.destroy()
                self.__init__()
            else:
                            
                fileName=superFileName
                fullFileName = superFileName+".txt"
                                
                self.master.geometry("440x425")

                self.setTitle()

                #set screen up here
                self.setScreen(location)

    


realestate = realestate()

            

        
