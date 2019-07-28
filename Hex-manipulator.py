#!/usr/bin/python3
# ------------------- Hex file tool -----------------------------#
# Creates a new Hex file(s) from a source HEX file, replaces     #
# the device serial and MAC addresses then generates a checksum  #
# and saves the new HEX file as newSERIAL_newMAC.HEX             #
#--------------------------------------------------------------- #
from tkinter import *
import tkinter as tk
from tkinter import filedialog    # needed for linux
import tkinter.font as tkFont
import tkinter.ttk as ttk
import tkinter.messagebox
import os
import hexAnalyzer

class McListBox(object):
    """use a ttk.TreeView as a multicolumn ListBox"""
    def __init__(self):
        self.tree = None
        self._setup_widgets()
        self._build_tree()
    def _setup_widgets(self):
        container = ttk.Frame(f1)
        #container.pack()#fill='both', expand=True)
        container.grid(row=10, column=root.a, columnspan=6, sticky='wens', padx=0, pady=0)
        # create a treeview with dual scrollbars
        self.tree = ttk.Treeview(columns=tbl_header, show="headings")
        vsb = ttk.Scrollbar(orient="vertical",
            command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal",
            command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,
            xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        hsb.grid(column=0, row=1, sticky='ew', in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
    def _build_tree(self):
        for col in tbl_header:
            self.tree.heading(col, text=col.title())
            # adjust the column's width to the header string
            self.tree.column(col,
                width=tkFont.Font().measure(col.title()))
        for item in tbl_list:
            self.tree.insert('', 'end', values=item)
            # adjust column's width if necessary to fit each value
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(tbl_header[ix],width=None)<col_w:
                    self.tree.column(tbl_header[ix], width=col_w)

#-------------------- the test data --------------------#
tbl_header1 = ['First part', 'Data', 'Checksum']
tbl_list1 = [
('','', ''),
('','', '')
]

tbl_header2 = ['First part', 'Data', 'Checksum']
tbl_list2 = [
('','', ''),
('','', '')
]

#-------------------- Main window --------------------#
root = tk.Tk()
root.wm_title("Hex files tool")
root.geometry("1400x600")

root.Flines = ""    # Loads Source file
#-------------------- Functions --------------------#
def quitfunc():
    quit()
def popAbout():
    tkinter.messagebox.showinfo("About Hex-Manipulator", "Hex-Manipulator v1.0\n contact: karimlakra@hotmail.com")
def dirDialog():
    currdir = os.getcwd()
    tempdir = filedialog.askdirectory(parent=root, initialdir=currdir, title= 'Please select a directory where the new files will be saved')
    if len(tempdir) > 0:
        if tempdir != '':
            pathNewHx.delete(0,END)
            pathNewHx.insert(0,tempdir)
def fileDialog():
    filename = filedialog.askopenfilename()
    if filename != '':
        pathSource.delete(0,END)
        pathSource.insert(0,filename)

def loadLines():
    x = serialSource.get()
    a = "".join([hex(ord(c))[2:].zfill(2) for c in x])
    label_var_HOS.set(a)

    fp=open(pathSource.get())
    root.Flines=fp.readlines()

    a = root.Flines[14009].strip()    #get lines to modify and remove whitespaces
    b = root.Flines[28907].strip()

    def prepareLine(va):
        L1L = len(va)
        dt = (va[:9], va[9:(L1L-11)+9],va[-2:])
        return dt

    L1 = prepareLine(a)
    L2 = prepareLine(b)
    modiflines = (L1, L2)

    rwsList1 = SH_listbox.tree.get_children()
    for i in rwsList1:
        SH_listbox.tree.delete(i)
    for x in range(3):
        SH_listbox.tree.column(x,width=99)

    count = 1
    for item in modiflines:
        SH_listbox.tree.insert('', '0', values=(modiflines[count][0],modiflines[count][1],modiflines[count][2]))

        for ix, val in enumerate(item):
            col_w = tkFont.Font().measure(val)
            if SH_listbox.tree.column(tbl_header1[ix],width=None)<col_w:
                SH_listbox.tree.column(tbl_header1[ix], width=col_w)
        count -= 1
def generatHex():
    print('generated!')
def SaveToHex():
    if root.Flines != "":
        SaveToHex = os.path.join(pathNewHx.get(), serialDestination.get()+".hex")
        fo = open(SaveToHex, "w+")
        for i in range(len(root.Flines)):
            if i == 14009 :
                print(root.Flines[i])
                fo.write(root.Flines[i])
            elif i == 28907:
                print(root.Flines[i])
                fo.write(root.Flines[i])
            else:
                fo.write(root.Flines[i])
        fo.close()


    else:
        print("Please load the source Hex file first")

#def StringToHex():
def analyzerHEX():
    print('Nothing')

#-------------------- Menu --------------------#
menu = Menu(root)
root.config(menu=menu)

subMenu = Menu(menu, tearoff=False)
menu.add_cascade(label="File", menu = subMenu)
subMenu.add_command(label="Exit",command = quitfunc)

helpMenu = Menu(menu, tearoff=False)
menu.add_cascade(label="Help", menu = helpMenu)
helpMenu.add_command(label="About", command = popAbout)
#-------------------- Toolbar --------------------#
#-------------------- Page Header --------------------#
label_var = tk.StringVar() #update label text holder
label_var.set("Enter some characters and press convert..")
lbl1 = tk.Label(root, textvariable = label_var)
lbl1.pack()

#-------------------- Tabs --------------------#
n = ttk.Notebook(root)              # add tab holder (notebook) to root
f1 = ttk.Frame(n)                   # add first tab to notebook
f2 = ttk.Frame(n)
f1.configure(padding=20)            # add a padding inside the tab
f2.configure(padding=20)
n.add(f1, text='Generator')
n.add(f2, text ='Verificator')

#----------- Labels/Buttons Source -----------#
folderpic = PhotoImage(file="folder.png")
mhfp = Label(f1, text='Source hex file path', bg='#a89999', fg='white')
mhfp.grid(row=0, sticky=W)

pathSource = Entry(f1, width=55)
pathSource.grid(row=1, columnspan=5, sticky=W)
# pathSource.delete(0,END)
pathSource.insert(0,'/home/kardes/Tests/Python/hex/CE13007 MAC 1e306ca24747 MASTER.hex')
ButtonLMF = Button(f1, compound=TOP, width=30, height=20, image=folderpic, command=fileDialog)   #Load master file button
ButtonLMF.grid(row=1, column=5, sticky=E)

HOS = Label(f1, text='Source serial')
HOS.grid(row=2, column=0, sticky=W)

f1.grid_columnconfigure(1, minsize=3)

SoS = Label(f1, text='Hex of serial Source')
SoS.grid(row=2, column=2, sticky=W)

#f1.grid_columnconfigure(3, minsize=3)
serialSource = Entry(f1)#, width=55)
serialSource.grid(row=3, sticky=W)
serialSource.insert(0, 'CE13007')
label_var_HOS = tk.StringVar() #update label text holder
label_var_HOS.set("")
HOS = Label(f1, text='HexSourceHolder', relief=SUNKEN, width=30, textvariable = label_var_HOS)
HOS.grid(row=3, column=2, sticky=W)

SMA = Label(f1, text='Source MAC address')
SMA.grid(row=4, column=0, sticky=W)
MACSource = Entry(f1)#, width=55)
MACSource.grid(row=5, sticky=W)
MACSource.insert(0, '1E306CA24747')

f1.grid_rowconfigure(6, minsize=15)

ButtonLS = Button(f1, text="Load Source HEX", width=15, height=2, command=lambda:loadLines())
ButtonLS.grid(row=7, column=0, sticky=W)

f1.grid_rowconfigure(8, minsize=15)
#----------- Labels/Buttons Destination -----------#
f1.grid_columnconfigure(6, minsize=60)
FNH = Label(f1, text='Destination Hex file', bg='#5e5', fg='#000')
FNH.grid(row=0, column=7, sticky=W)
pathNewHx = Entry(f1, width=55)
pathNewHx.grid(row=1, column=7, columnspan=5, sticky=W)
pathNewHx.insert(0,'/home/kardes/Tests/Python/hex/HexFilesTest')
ButtonST = Button(f1, text="Save to Folder", fg='red', width=30, height=20, image=folderpic, command=dirDialog)   #Genarate new button

DS = Label(f1, text='Destination serial')
DS.grid(row=2, column=7, sticky=W)

f1.grid_columnconfigure(8, minsize=3)

SoS = Label(f1, text='Hex of serial Destination')
SoS.grid(row=2, column=9, sticky=W)

serialDestination = Entry(f1)
serialDestination.grid(row=3, column=7, sticky=W)
serialDestination.insert(0, 'CE16937')
HOS = Label(f1, text='HexDestinationHolder', relief=SUNKEN, width=30)
HOS.grid(row=3, column=9, sticky=W)

DMA = Label(f1, text='Destination MAC address')
DMA.grid(row=4, column=7, sticky=W)
MACDestination = Entry(f1)#, width=55)
MACDestination.grid(row=5, column=7, sticky=W)
MACDestination.insert(0, '1E306CA26097')

ButtonGN = Button(f1, text="Generate New", fg='red', width=15, height=2, command=generatHex)   #Genarate new button
ButtonSV = Button(f1, text="Save", fg='#62674b', command=SaveToHex, width=15, height=2)   #Save genarated file

ButtonST.grid(row=1, column=12, sticky=E)
ButtonGN.grid(row=7, column=7, sticky=W)
ButtonSV.grid(row=7, column=9)

#----------- Table data -----------#
root.a = 0                             # variable to pass to the class for positioning the table
tbl_list = tbl_list1
tbl_header = tbl_header1
SH_listbox = McListBox()               # Create a table for the source HEX

tbl_list = tbl_list2
tbl_header = tbl_header2
root.a = 7
DH_listbox = McListBox()               # Create a table for the source HEX


n.pack(expand=1, fill='both')          # add tabs

def handle_tab_changed(event):                           # return which tab is activated
    selection = event.widget.select()
    tab = event.widget.tab(selection, "text")
    #print("text:", tab)
    if tab == "Generator":
        label_var.set('Modified lines from files')
    else:
        label_var.set('Verificator')

n.bind("<<NotebookTabChanged>>", handle_tab_changed)    # detects the active tab

#-------------------- Status bar --------------------#
statusFrame = Frame(root)
statusFrame.pack(side=BOTTOM, fill=X)
status = Label(statusFrame, text="status bar", relief=SUNKEN, anchor=W)
status.pack(fill=X)

root.mainloop()
