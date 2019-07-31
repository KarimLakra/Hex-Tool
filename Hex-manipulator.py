#!/usr/bin/env python
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
import hexLineAnalyzer
import random
import tooltip

#-------------------- Main window --------------------#
root = tk.Tk()
root.wm_title("Hex files tool")
root.geometry("1450x700")

label_tool_var = tk.StringVar() #update label tool bar

root.Flines = ""    # Loads Source file
label_var_InfoLines = tk.StringVar() #update label text holder

label_status = tk.StringVar() # Variable for a dynamic status label
label_status.set("status bar")

ConfigData = ['','','','','','']                # global variable to hold the config data

Separator = os.sep                              # Check operating system windows uses \ separator linux uses /
#----------------------------------------------------------#

label_var_InfoLines.set("Double Click a line \n to analyze")

class McListBox(object):
    """use a ttk.TreeView as a multicolumn ListBox"""
    def __init__(self):
        self.tree = None
        self._setup_widgets()
        self._build_tree()
    def _setup_widgets(self):
        container = ttk.Frame(f1)
        #container.pack()#fill='both', expand=True)
        container.grid(row=12, column=root.a, columnspan=6, sticky='wens', padx=0, pady=0)
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
            self.tree.bind("<Double-1>", self.OnDoubleClick)
            # adjust column's width if necessary to fit each value
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(tbl_header[ix],width=None)<col_w:
                    self.tree.column(tbl_header[ix], width=col_w)
    def OnDoubleClick(self, event):
        item = self.tree.identify('item', event.x, event.y)
        global label_var_InfoLines
        a = self.tree.item(item,"values")
        if a[0] != '':
            b = hexLineAnalyzer.checLine(a[0]+a[1]+a[2])
            if b[0] == '':
                err = 'No Error'
            c = "Byte count: "+b[2] +"\nAddress: "+b[1]+"\nRecord type: "+b[3]+"\nChecksum from line:" \
            +b[5]+"\nCalculated Checksum: "+b[6]+"\n\n"+ err
            label_var_InfoLines.set(c)



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


#-------------------- Functions --------------------#
def loadSetting():
    global ConfigData

    currdir = os.getcwd()
    LoadConfiguration = os.path.join(currdir+Separator+"setting")

    checkConfig = 0
    fo = open(LoadConfiguration, "r")
    conf = fo.readlines()
    fo.close()
    for i, val in enumerate(conf):
        ConfigData[i] = conf[i].replace("\n", "")
    for i in ConfigData:
        if i == '':
            checkConfig += 1
    if checkConfig == 6:
        label_tool_var.set('No Setting data found')

def saveSetting():
    ConfigData = [pathSource.get(), pathNewHx.get(), serialSource.get(), \
        serialDestination.get(), MACSource.get(), MACDestination.get()]
    currdir = os.getcwd()
    SaveConfiguration = os.path.join(currdir+Separator+"setting")
    fo = open(SaveConfiguration, "w")
    for i in range(6):
        fo.write(ConfigData[i]+"\n")
    fo.close()
    label_toolBar.config(bg=randomizCor())
    label_tool_var.set('Setting saved')

loadSetting()     # Load the setting from setting file

def reloadSetting():
    ClearAllFields()
    loadSetting()
    pathSource.insert(0,ConfigData[0])                        # Source file path
    serialSource.insert(0, ConfigData[2])                     # serial source
    MACSource.insert(0, ConfigData[4])                        # Mac addr source

    pathNewHx.insert(0,ConfigData[1])                         # path where the generated hex file will be saved
    serialDestination.insert(0, ConfigData[3])                # Serial destination
    MACDestination.insert(0, ConfigData[5])                 # Mac addr destination

    label_toolBar.config(bg=randomizCor())
    label_tool_var.set('Setting reloaded')

def ClearAllFields():
    pathSource.delete(0,END)                        # Source file path
    serialSource.delete(0,END)                     # serial source
    MACSource.delete(0,END)                        # Mac addr source

    pathNewHx.delete(0,END)                         # path where the generated hex file will be saved
    serialDestination.delete(0,END)                # Serial destination
    MACDestination.delete(0,END)                 # Mac addr destination

    label_toolBar.config(bg=randomizCor())
    label_tool_var.set('Fields cleared')

def deleteSetting():
    PathConfiguration = os.path.join(os.getcwd()+Separator+"setting")
    open(PathConfiguration, 'w').close()

    label_toolBar.config(bg=randomizCor())
    label_tool_var.set('Setting deleted')

def quitfunc():
    quit()
def MsgBox(a,b):
    tkinter.messagebox.showinfo(a,b)
def dirDialog():
    currdir = os.getcwd()
    tempdir = filedialog.askdirectory(parent=root, initialdir=currdir, \
        title= 'Please select a directory where the new files will be saved')
    if len(tempdir) > 0:
        if tempdir != '':
            pathNewHx.delete(0,END)
            pathNewHx.insert(0,tempdir)
def fileDialog():
    filename = filedialog.askopenfilename()
    if filename != '':
        pathSource.delete(0,END)
        pathSource.insert(0,filename)

def loadLines(s,l,fo,lb, rw):
                                                # s=serial, l=label,fo=file path,lb=listbox,
    HFS = "".join([hex(ord(c))[2:].zfill(2) for c in s])  # hex from serial string
    l.set(HFS)

    if rw == "R":                               # read hex source
        fp=open(fo.get())
        root.Flines=fp.readlines()
        fp.close()

    a = root.Flines[14009].strip()              #get lines to modify and remove whitespaces
    b = root.Flines[28907].strip()


    def prepareLine(va, ln, rw):
        # va = line number, ln = line 1 or 2, rw= operation read or write(read to generate hex, write to create the hex file)
        L1L = len(va)                           # prepare the lines to insert to table
        if rw == "R":
            dt = (va[:9], va[9:(L1L-11)+9],va[-2:])     # prepare line from source hex file
            # print(dt)
        elif rw == "W":
            if ln == 1:
                SHx = "".join([hex(ord(c))[2:].zfill(2) for c in serialSource.get()])               # convert string to hex
                DHx = "".join([hex(ord(c))[2:].zfill(2) for c in serialDestination.get()])
                cksum = hexLineAnalyzer.checLine(va[:9]+va[9:(L1L-11)+9].replace(SHx,DHx))        # Generate checksum for line1
                dt = (va[:9], va[9:(L1L-11)+9].replace(SHx,DHx),cksum[6])
            elif ln == 2:
                SouRc = MACSource.get() + "".join([hex(ord(c))[2:].zfill(2) for c in serialSource.get()])
                DesT = MACDestination.get() + "".join([hex(ord(c))[2:].zfill(2) for c in serialDestination.get()])
                cksum = hexLineAnalyzer.checLine(va[:9]+va[9:(L1L-11)+9].replace(SouRc,DesT))        # Generate checksum for line2
                dt = (va[:9], va[9:(L1L-11)+9].replace(SouRc,DesT),cksum[6])

        return dt

    L1 = prepareLine(a, 1, rw)
    L2 = prepareLine(b, 2, rw)

    modiflines = (L1, L2)                      # tuple from data

    rwsList1 = lb.tree.get_children()          # get treeView children to empty
    for i in rwsList1:
        lb.tree.delete(i)
    for x in range(3):                         # shrink columns width
        lb.tree.column(x,width=99)

    count = 1                                  # counter to decrement to insert rows in treeView
    for item in modiflines:
        lb.tree.insert('', '0', values=(modiflines[count][0],modiflines[count][1],modiflines[count][2]))
        for ix, val in enumerate(item):        # adjust columns width to fit new data
            col_w = tkFont.Font().measure(val)
            if lb.tree.column(tbl_header1[ix],width=None)<col_w:
                lb.tree.column(tbl_header1[ix], width=col_w)
        count -= 1

    rslt = (L1,L2)
    return  rslt                               # return Lines to modify
def NextPrevSerial(op):
    if op == "N":
        op = 1
    elif op == "P":
        op = -1
    a = serialDestination.get()
    b = str(int(a[2:])+op)
    c = a[:-5]+b
    serialDestination.delete(0,END)
    serialDestination.insert(0,c)

    a = MACDestination.get()
    b = str(int(a[7:])+op)
    c = a[:-5]+b
    MACDestination.delete(0,END)
    MACDestination.insert(0,c)
    generatHex()

def generatHex():
    fo = pathSource.get()
    if not os.path.exists(fo):
        missingEntry("The location to the Source file is not available or the file does not exist!")
        err = True
        pathSource.focus_set()
    elif serialSource.get() == "":
        missingEntry("The Source Serial is needed. No file generated")
        serialSource.focus_set()
    elif serialDestination.get() == "":
        missingEntry("The Destination Serial is needed. No file generated")
        serialDestination.focus_set()
    elif MACSource.get() == "":
        missingEntry("The MAC Source is needed. No file generated")
        MACSource.focus_set()
    elif MACDestination.get() == "":
        missingEntry("The MAC Destination is needed. No file generated")
        MACDestination.focus_set()
    else:
        #if len(root.Flines)<14009:              # if lines are not loaded by Load Source Button
                                                # TODO: reset .root.Flines if some entry changed
                                                # this execute only once for the moment
        root.Sourc = loadLines(serialSource.get(),label_var_HOS, pathSource, SH_listbox, "R")
        root.Destin = loadLines(serialDestination.get(),label_var_HOD, pathNewHx, DH_listbox, "W")

        # root.Flines[14009]
        status.config(bg=randomizCor())
        label_status.set("Hex File generated successfully")
    # print(root.Sourc,"\n",root.Destin)



def missingEntry(m):
    status.config(bg=randomizCor())             # Generat random background for the status bar
    label_status.set(m)
def randomizCor():                              # random hex color generator
    r = lambda:random.randint(0,255)
    co = '#%02X%02X%02X' % (r(),r(),r())
    co = co.replace('-','')
    return co

def SaveToHex():
    if root.Flines != "":
        fiP = pathNewHx.get()
        if not os.path.exists(fiP):
            missingEntry("The location to the Destination file is not available. Use the button to select a correct Location.")
            pathNewHx.focus_set()
        else:
            SaveToHex = os.path.join(pathNewHx.get(), serialDestination.get()+".hex")
            # LAR = (err ,addressCode, byteCount, recordType, typeString, checksum, checksumVerifyResult)
            # Generate checksum for lines
            cs1 = hexLineAnalyzer.checLine(root.Destin[0][0]+root.Destin[0][1]+root.Destin[0][2])
            cs2 = hexLineAnalyzer.checLine(root.Destin[1][0]+root.Destin[1][1]+root.Destin[1][2])

            fo = open(SaveToHex, "w+")
            for i in range(len(root.Flines)):
                if i == 14009 :
                    fo.write(root.Destin[0][0]+root.Destin[0][1]+cs1[6]+"\n")
                elif i == 28907:
                    fo.write(root.Destin[1][0]+root.Destin[1][1]+cs2[6]+"\n")
                else:
                    fo.write(root.Flines[i])
            fo.close()
            status.config(bg=randomizCor())
            label_status.set("A new Hex file was successfully generated")


    else:
        status.config(bg=randomizCor())
        label_status.set("Please Generate New Hex file first")
def Nothingfunc():
    print('Nothing')
def DebugToolBar():
    print('Debuged')
#-------------------- Menu --------------------#
menu = Menu(root)
root.config(menu=menu)

subMenu = Menu(menu, tearoff=False)
menu.add_cascade(label="File", menu = subMenu)
subMenu.add_command(label="Exit",command = quitfunc)

helpMenu = Menu(menu, tearoff=False)
menu.add_cascade(label="Help", menu = helpMenu)
helpMenu.add_command(label="About", command = lambda: MsgBox("About Hex-Manipulator", "Hex-Manipulator v1.0\n contact: karimlakra@hotmail.com"))
#-------------------- Toolbar --------------------#
Ssett = PhotoImage(file="saveSett.png")
Dsett = PhotoImage(file="delSett.png")
CFields = PhotoImage(file="clear.png")
Loadsett = PhotoImage(file="load.png")


toolbar = Frame(root, width="500", pady=4, bg="#6bb2c6")
# toolbar.configure(pady=(0,10))
saveSett = Button(toolbar, image=Ssett, command=saveSetting)
saveSett.grid(row=0, padx=5)
SaveConfigTooltip = tooltip.CreateToolTip(saveSett, "Save current settings")

reloadSett = Button(toolbar, image=Loadsett, command=reloadSetting)
reloadSett.grid(row=0, column=1, padx=5)
reloadConfigTooltip = tooltip.CreateToolTip(reloadSett, "Load/reload settings")

delSett = Button(toolbar, image=Dsett, command=deleteSetting)
delSett.grid(row=0, column=2, padx=5)
DeleteConfigTooltip = tooltip.CreateToolTip(delSett, "Delete current settings")

SeparatorSettField = ttk.Separator(toolbar, orient=VERTICAL)
SeparatorSettField.grid(row=0, column=3, padx=5, sticky=N+S)

ClearFields = Button(toolbar, image=CFields, command=ClearAllFields)
ClearFields.grid(row=0, column=4, padx=5)
ClearFieldsTooltip = tooltip.CreateToolTip(ClearFields, "Clear Fields")

# toolbar.grid_columnconfigure(, minsize=3)

label_toolBar = tk.Label(toolbar, textvariable = label_tool_var, bg="#6bb2c6", width=25, padx=3)
label_toolBar.grid(row=0, column=5)

# ---------------------------- # DEBUG BUTTON # --------------------------
debugimg =  PhotoImage(file="debug.png")
Debug = Button(toolbar, image=debugimg, command=DebugToolBar)
Debug.grid(row=0, column=12, padx=50, sticky=W)
DebugTooltip = tooltip.CreateToolTip(Debug, "You don't need this it is for debuging purpose ;)")
# -----------------------------------------------------------------

toolbar.pack(side=TOP, fill=X)
#-------------------- Page Header --------------------#
label_var = tk.StringVar() #update label text holder
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

SB_PS = Scrollbar(f1, orient=HORIZONTAL)            # Scroll bar for path source
SB_PS.grid(row=2, columnspan=5, sticky=W+N+E)

pathSource = Entry(f1, width=55, xscrollcommand=SB_PS.set)
pathSource.grid(row=1, columnspan=5, sticky=W)
pathSource.insert(0,ConfigData[0])                        # Source file path

SB_PS.config(command=pathSource.xview)

ButtonLMF = Button(f1, compound=TOP, width=30, height=20, image=folderpic, command=fileDialog)   #Load master file button
ButtonLMF.grid(row=1, column=5, sticky=E)

HOS = Label(f1, text='Source serial')
HOS.grid(row=3, column=0, sticky=W)

f1.grid_columnconfigure(1, minsize=3)

SoS = Label(f1, text='Hex of serial Source')
SoS.grid(row=3, column=2, sticky=W)

#f1.grid_columnconfigure(3, minsize=3)
serialSource = Entry(f1)#, width=55)
serialSource.grid(row=4, sticky=W)
serialSource.insert(0, ConfigData[2])                     # serial source
label_var_HOS = tk.StringVar() #update label text holder
label_var_HOS.set("")
HOS = Label(f1, text='HexSourceHolder', relief=SUNKEN, width=30, textvariable = label_var_HOS)
HOS.grid(row=4, column=2, sticky=W)

SMA = Label(f1, text='Source MAC address')
SMA.grid(row=5, column=0, sticky=W)
MACSource = Entry(f1)#, width=55)
MACSource.grid(row=6, sticky=W)
MACSource.insert(0, ConfigData[4])                        # Mac addr source

f1.grid_rowconfigure(7, minsize=15)

# ButtonLS = Button(f1, text="Load Source HEX", width=15, height=2,
#     command=lambda:loadLines(serialSource.get(),label_var_HOS, pathSource, SH_listbox, "R"))
# ButtonLS.grid(row=7, column=0, sticky=W)

f1.grid_rowconfigure(9, minsize=15)
f1.grid_rowconfigure(11, minsize=15)
#----------- Labels/Buttons Destination -----------#
f1.grid_columnconfigure(6, minsize=60)
FNH = Label(f1, text='Destination Hex file', bg='#5e5', fg='#000')
FNH.grid(row=0, column=7, sticky=W)

SB_PD = Scrollbar(f1, orient=HORIZONTAL)            # Scroll bar for path destination
SB_PD.grid(row=2, column=7, columnspan=5, sticky=W+N+E)

pathNewHx = Entry(f1, width=55, xscrollcommand=SB_PD.set)
pathNewHx.grid(row=1, column=7, columnspan=5, sticky=W)
pathNewHx.insert(0,ConfigData[1])                         # path where the generated hex file will be saved

SB_PD.config(command=pathNewHx.xview)

ButtonST = Button(f1, width=30, height=20, image=folderpic, command=dirDialog)   #Genarate new button
ButtonST.grid(row=1, column=12, sticky=E)

DS = Label(f1, text='Destination serial')
DS.grid(row=3, column=7, sticky=W)

f1.grid_columnconfigure(8, minsize=3)

SoS = Label(f1, text='Hex of serial Destination')
SoS.grid(row=3, column=9, sticky=W)

serialDestination = Entry(f1)
serialDestination.grid(row=4, column=7, sticky=W)
serialDestination.insert(0, ConfigData[3])                # Serial destination
label_var_HOD = tk.StringVar() # var to update label text holder
label_var_HOD.set("")
HOD = Label(f1, text='HexDestinationHolder', relief=SUNKEN, width=30, textvariable = label_var_HOD)
HOD.grid(row=4, column=9, sticky=W)

DMA = Label(f1, text='Destination MAC address')
DMA.grid(row=5, column=7, sticky=W)
MACDestination = Entry(f1)#, width=55)
MACDestination.grid(row=6, column=7, sticky=W)
MACDestination.insert(0, ConfigData[5])                 # Mac addr destination

ButtonGN = Button(f1, text="Generate New", fg='red', width=15, height=2, command=generatHex)   # Genarate new button
ButtonPRV = Button(f1, text="<", fg='red', width=3, height=2, command=lambda:NextPrevSerial("P"))   # Previous serial
ButtonNXT = Button(f1, text=">", fg='red', width=3, height=2, command=lambda:NextPrevSerial("N"))   # Next serial
ButtonSV = Button(f1, text="Save", fg='#62674b', command=SaveToHex, width=15, height=2)   # Save genarated file

ButtonGN.grid(row=10, column=7, sticky=W)
ButtonPRV.grid(row=8, column=7, sticky=W)
ButtonNXT.grid(row=8, column=9, sticky=W)
ButtonSV.grid(row=10, column=9)

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
#-------------------- Info right bar --------------------#

InfoLines = Label(f1, relief=SUNKEN, width=30, textvariable = label_var_InfoLines, anchor=W, justify=LEFT)
InfoLines.grid(row=12, column=13, sticky=W+N+E)

#-------------------- Status bar --------------------#
statusFrame = Frame(root)
statusFrame.pack(side=BOTTOM, fill=X)
status = Label(statusFrame, relief=SUNKEN, anchor=W, textvariable = label_status)
status.pack(fill=X)

root.mainloop()
