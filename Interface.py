import tkinter as tk
from tkinter import *
from tkinter import filedialog
from Comparaison import launcher
#import Extraction

# Declarations:
url = ''

def ouvrir_image ():
    global url
    url = filedialog.askopenfilename(title= "choisir image", 
                                     filetypes = (('Image Files', '*.png'),))
    print(url)
    inputimg.insert(0,url)
    
def lancer():
    upld['stat'] = 'disabled'
    global url

    if url == None or url == '':
        print("Bad url")
        upld['stat'] = 'Normal'
    else:
        decision, id_person, score = launcher(url= url)
        upld['stat'] = 'normal'
        if decision:
            resultat(id_person, score)
        else:
            sorry()

def sorry():
    for widget in lower_frame.winfo_children():
            widget.destroy()
    error = tk.Label(
            lower_frame, 
            text="Personne introuvable dans la base de données", 
            font=("Courrier",15),
            fg   = "#000000").grid(row = 0 ,column = 0)

def resultat(id_person, score):
    for widget in lower_frame.winfo_children():
        widget.destroy()

    title1= tk.Label(
            lower_frame, 
            text="Before", 
            font=("Courrier",15),
            bg="#009999").grid(row = 0 ,column = 0) 

    title2 = tk.Label(
            lower_frame, 
            text="After", 
            font=("Courrier",15),
            bg="#009999").grid(row = 0 ,column = 1)

    title3 = tk.Label(
        lower_frame, 
        text="Matching", 
        font=("Courrier",15),
        bg="#009999").grid(row = 0 ,column = 2)

    global img1
    global img2
    global img3

    img1 = tk.PhotoImage(file="./results/bdd.png")
    my_label = tk.Label(lower_frame, image = img1).grid(row = 1,column = 0)   

    img2 = tk.PhotoImage(file="./results/real.png")
    my_label2 = tk.Label(lower_frame, image = img2).grid(row = 1,column = 1) 

    img3 = tk.PhotoImage(file="./results/matching.png")
    my_label3 = tk.Label(lower_frame, image = img3).grid(row = 1,column = 2) 

    person_id  =tk.Label(
        lower_frame, 
        text= "ID :"+str(id_person)+"\nScore :"+str(score)+"%", 
        font=("Courrier",15),
        bg="#009999").grid(row = 1,column = 3) 

root = tk.Tk()
root.iconbitmap("logo.ico")
root.config()
MainFrame = tk.Frame(root, width=1280, height=700, relief='raised')
upper_frame = tk.Frame(MainFrame, width=375, height=100,bg = "#deeaee", relief='raised', borderwidth=5)
lower_frame = tk.Frame(MainFrame, width=375, height=330,bg = "#deeaee", relief='raised', borderwidth=5)

inputframe=LabelFrame(root, borderwidth=4, height = 85, width=650)
inputframe.place(x=50, y=80)
inputframe.grid_propagate(0)
inputframe.config(bg = "#deeaee")

title = tk.Label(
    upper_frame, 
    text="Système Biométrique D’Identification Par L'Iris", 
    font=("Courrier",25),
    bg="#009999")
title.pack()

inputimg = Entry(root,width=70)  
inputimg.pack(expand=True,side = tk.LEFT)
inputimg.place(x = 70 , y=85)

btn = tk.Button(
    root, 
    text ='Choisir une image iris',
    font=("Courrier",15), 
    bg="#009999", 
    relief='groove',
    command = ouvrir_image
    )
btn.pack(expand=True,side = tk.LEFT)
btn.place(x = 70 , y=115)

upld = tk.Button(
    upper_frame, 
    text="Lancer l'analyse", 
    font=("Courrier",15), 
    bg="#009999" , 
    relief='groove',
    command=lancer
    )
upld.pack(side = tk.LEFT, expand = True, pady = 30)
upld.place(x = 800 , y=115)

for frame in [MainFrame, upper_frame, lower_frame]:
    frame.pack(expand=True, fill='both')
    frame.pack_propagate(0)

root.mainloop()