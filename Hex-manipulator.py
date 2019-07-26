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
#test git26-jul-2019 23:48
#test2 git27-jul-19 0:51

class McListBox(object):
    """use a ttk.TreeView as a multicolumn ListBox"""
    def __init__(self):
        self.tree = None
        self._setup_widgets()
        self._build_tree()
    def _setup_widgets(self):
        container = ttk.Frame(f1)
        #container.pack()#fill='both', expand=True)
        container.grid(row=10, column=root.a, columnspan=2, sticky='wens', padx=0, pady=0)
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
(':02000004', '0000', 'FA') ,
(':10000000','18F09FE518F09FE518F09FE518F09FE5', 'C0'),
(':10001000','18F09FE50000A0E120F11FE518F09FE5', '32')
]

tbl_header2 = ['First part', 'Data', 'Checksum']
tbl_list2 = [
(':02000005', '0000', 'FB') ,
(':10000000','18F09FE518F09FE518F09FE518F09FE5', 'C02'),
(':10001000','18F09FE50000A0E120F11FE518F09FE5', '32B')
]

#-------------------- Main window --------------------#
root = tk.Tk()
root.wm_title("Hex files tool")
root.geometry("1400x600")

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
        pathMaster.delete(0,END)
        pathMaster.insert(0,filename)
def popmsg():
    print("file saved!")
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
mhfp = Label(f1, text='Master hex file path', bg='#a89999', fg='white')
mhfp.grid(row=0, sticky=W)
pathMaster = Entry(f1, width=55)
pathMaster.grid(row=1, sticky=W)
ButtonLMF = Button(f1, compound=TOP, width=30, height=20, image=folderpic, command=fileDialog)   #Load master file button
ButtonLMF.grid(row=1, column=1, sticky=E)
#----------- Labels/Buttons Destination -----------#
f1.grid_columnconfigure(2, minsize=40)
FNH = Label(f1, text='Folder for new hex file', bg='#5e5', fg='#000')
FNH.grid(row=0, column=3, sticky=W)
pathNewHx = Entry(f1, width=55)
pathNewHx.grid(row=1, column=3, sticky=W)
ButtonST = Button(f1, text="Save to Folder", fg='red', width=30, height=20, image=folderpic, command=dirDialog)   #Genarate new button
ButtonGN = Button(f1, text="Generate New", fg='red')   #Genarate new button
ButtonSV = Button(f1, text="Save", fg='#62674b', command=popmsg)   #Save genarated file

ButtonST.grid(row=1, column=4, sticky=E)
ButtonGN.grid(row=2, column=3)
ButtonSV.grid(row=2, column=4)

#----------- Table data -----------#
root.a = 0
tbl_list = tbl_list1
tbl_header = tbl_header1
mc_listbox = McListBox()               # Create a table for the source HEX

tbl_list = tbl_list2
tbl_header = tbl_header2
root.a = 3
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
