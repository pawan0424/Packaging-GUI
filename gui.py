# Importing necessary packages
from asyncio.log import logger
from asyncio.windows_events import NULL
import shutil
import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog
import logging
from tkinter import ttk
import pandas as pd
import os

 

def CreateWidgets():
    link_Label = Label(root, text ="Input Path: ",
                    bg = "#91d14f")
    link_Label.grid(row = 1, column = 0,
                    pady = 5, padx = 5)
     
    root.sourceText = Entry(root, width = 50,
                            textvariable = sourceLocation)
    root.sourceText.grid(row = 1, column = 1,
                        pady = 5, padx = 5,
                        columnspan = 2)
     
    source_browseButton = Button(root, text ="Browse",
                                command = SourceBrowse, width = 15)
    source_browseButton.grid(row = 1, column = 3,
                            pady = 5, padx = 5)
     
    destinationLabel = Label(root, text ="Destination Path: ",
                            bg ="#91d14f")
    destinationLabel.grid(row = 2, column = 0,
                        pady = 5, padx = 5)
     
    root.destinationText = Entry(root, width = 50,
                                textvariable = destinationLocation)
    root.destinationText.grid(row = 2, column = 1,
                            pady = 5, padx = 5,
                            columnspan = 2)

    dest_browseButton = Button(root, text ="Browse",
                            command = DestinationBrowse, width = 15)
    dest_browseButton.grid(row = 2, column = 3,
                        pady = 5, padx = 5)
     
    copyButton = Button(root, text ="Submit",bg="#a9d08f",
                     command = CopyFile, width = 15)
    copyButton.grid(row = 5, column = 1,pady = 5, padx = 5)
    quitButton = Button(root, text ="Quit",bg="#a9d08f",
                        command = closeApp, width = 15)
    quitButton.grid(row = 5, column = 2,
                    pady = 5, padx = 5)

    ttk.Checkbutton(root, text ='Copy Source images',
                state='normal',takefocus=0,variable=check1,onvalue=1).grid(row = 3, column = 0,pady = 5, padx = 5)

    ttk.Checkbutton(root, text ='Copy renders',
                state='normal',takefocus=0,variable=check2,onvalue=1).grid(row = 4, column = 0,pady = 5, padx = 5)             
  
 
def SourceBrowse():
     
    root.files_list = list(filedialog.askopenfilenames())
    root.sourceText.insert('1', root.files_list)
     
def DestinationBrowse():
    destinationdirectory = filedialog.askdirectory(initialdir ="C:/Users/pawan/Desktop")
    root.destinationText.insert('1', destinationdirectory)
     
def CopyFile(rendercopy=0,imagecopy=0):
    
    files_list = ''.join([str(elem) for elem in root.files_list])
 
    destination_location = destinationLocation.get()
    df=pd.read_excel(files_list)
    df = df.apply(lambda x: pd.Series(x.dropna().values))
    df = df.fillna('')
    df=df.iloc[1:]
    res=[]
    for column in df.columns:
        li = df[column].tolist()
        
        res.append(li)
 
    finalfile=res[0]
    
    if check2.get()==1:
        print("here0")
        for x in res[1]:
            if x!='':
                print(type(x))
                print(os.listdir(x+"\\"))
                finalfile=finalfile+[ x + "\\" + y for y in os.listdir(x)]
    print("here")   
    if check1.get()==1:
        
        for x in res[2]:
            if x!='':
                print(os.listdir(x+"\\"))
                finalfile=finalfile+[ x + "\\" + y for y in os.listdir(x)]
    print(finalfile)
    for f in finalfile:
       
        try:
            
            shutil.copy(f, destination_location)
            py_logger.info("File copied successfully.")
  
        except shutil.SameFileError:
            py_logger.exception("Source and destination represent the same file.")
       
        except PermissionError:
            py_logger.exception("Permission denied.")
       
        except:
            py_logger.exception("Error occurred while copying file.")
 
    messagebox.showinfo("SUCCESSFUL")
       
def MoveFile():
     
    files_list = root.files_list
 
    destination_location = destinationLocation.get()
 
    for f in files_list:
        
        shutil.move(f, destination_location)
 
    messagebox.showinfo("SUCCESSFUL")
def closeApp():
    root.destroy()

root = tk.Tk()
     
root.geometry("900x170")
root.title("Saffron Packaging Tool")
root.config(background = "#F5F5F5")
     

sourceLocation = StringVar()
destinationLocation = StringVar()
py_logger = logging.getLogger(__name__)
py_logger.setLevel(logging.INFO)

py_handler = logging.FileHandler(f"{__name__}.log", mode='w')
py_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

py_handler.setFormatter(py_formatter)

py_logger.addHandler(py_handler)

check1=IntVar()
check2=IntVar()
CreateWidgets()

root.mainloop()