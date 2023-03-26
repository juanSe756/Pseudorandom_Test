import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

class Frame:
    def __init__(self, control):
        self.control = control
        self.mywindow = tk.Tk()
        self.mywindow.geometry("900x600")
        self.mywindow.title("Testing Pseudorandom Numbers ")
        self.mywindow.resizable(False,False)
        self.mywindow.config(background = "#213141")
        main_title = tk.Label(text = "Pseudorandom Number Tests", font = ("Gotham", 26), bg = "#56CD63", fg = "black", width = "500", height = "2")
        main_title.pack()
        self.selected_option = tk.StringVar()
        self.selected_file = tk.StringVar()
        self.x1=22
        self.y1=190
        self.labels = []
        self.initComponents()
    
    def initComponents(self):
        select_file_lbl = tk.Label(text = "Select file: ", bg = "#FFEEDD")
        select_file_lbl.place(x = 22, y = 100)

        self.path_lbl = tk.Label(text = "...", bg = "#FFEEDD")
        self.path_lbl.place(x = 230, y = 100)

        self.graphic_lbl = tk.Label(text = "NUMBERS DISTRIBUTION", bg = "#FFEEDD")
        self.graphic_lbl.place(x = 520, y = 155)

        browse_button = tk.Button(self.mywindow, text="File Explorer", command=self.browseFiles)
        browse_button.place(x=120, y=100)

        select_test = tk.Label(text = "Select test: ", bg = "#FFEEDD")
        select_test.place(x = 22, y = 160)

        self.createMenu()

        button_to_do = tk.Button(self.mywindow, text="MAKE TEST", command=self.control.makeTest)
        button_to_do.place(x=280,y=160)

    #Creates the dropdown menu
    def createMenu(self):
        options = ["Mean Test", "Mean Test","Variance Test", "KS Test", "Chi2 Test", "Poker Test"]
        self.selected_option.set(options[0])
        menu = ttk.OptionMenu(self.mywindow,self.selected_option, *options)
        menu.place(x = 120, y = 160)

    #Creates a label to describe a graphic
    def generateLblToDescribeGraph(self, description):
        new_lbl = tk.Label(text = self.cutString(description), bg = "#FFEEDD")
        new_lbl.place(x=520,y=500)
        self.labels.append(new_lbl)
        self.mywindow.update()
        
    #Allows open file explorer and choose a file
    def browseFiles(self):
        file = filedialog.askopenfilename()
        self.selected_file = file
        self.path_lbl = tk.Label(text = file, bg = "#FFEEDD")
        self.path_lbl.place(x = 230, y = 100)

    #get the selected file path
    def getFilePath(self):
        return self.selected_file
    
    #gets the selected option
    def getSelectedOption(self):
        return self.selected_option.get()

    #Allows clean the frame to show other labels 
    def destroyAlllbls(self):
        for label in self.labels:
            label.destroy()
        self.x1 = 22
        self.y1 = 190
        self.mywindow.update()
    
    #Cuts the string if it is too long
    def cutString(self,cadena):
        # If the string is shorter than 200 characters, it is returned as-is.
        if len(cadena) <= 60:
            return cadena
        # If the string is longer than 200 characters, it is split into 200-character parts with newlines
        partes = []
        i = 0
        while i < len(cadena):
            partes.append(cadena[i:i+60])
            i += 60
        return '\n'.join(partes) #finally join the parts with a line break

    #Allows create a new label to show information
    def generateLbl(self, labelname, extraHeight=0):
        new_lbl = tk.Label(text = self.cutString(labelname), bg = "#FFEEDD")
        new_lbl.place(x=self.x1,y=self.y1)
        self.labels.append(new_lbl)
        self.y1+=60+extraHeight
        self.mywindow.update()

