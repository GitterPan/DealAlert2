from tkinter import *
from tkinter import ttk

import json

import time

def GatherData(name,ksp,ivory,superpharm,mh):
    
    data = [ksp,ivory,superpharm,mh]

    data = {
        'Name' : name,
        'ksp' : ksp,
        'ivory' : ivory,
        'super-pharm' : superpharm,
        'MH' : mh
    }
    

    
        
    
    with open('products.json','r+') as f :
        # load json file
        file_data = json.load(f)
        # append to corresponding list in json
        file_data['products'].append(data)

        f.seek(0)
        json.dump(file_data, f , indent = 4)

root = Tk()
# root.geometry('500x500')

root.title('DealAlert')


label = Label(root , text = 'hello' , font = ('Arial', 18))
# label.pack(padx = 20, pady=20)


namelabel = Label(root, text = 'Name',font = ('Arial',12))
namebox = Entry(root ,font =('Arial', 12))
# namebox.pack(pady=20)

ksplabel = Label(root, text = 'KSP',font = ('Arial',12))
kspbox = Entry(root ,font =('Arial', 12))
# kspbox.pack(pady=20)

ivorylabel = Label(root, text = 'Ivory',font = ('Arial',12))
ivorybox = Entry(root ,font =('Arial', 12))
# ivorybox.pack(pady=20)

superpharmlabel = Label(root, text = 'super-pharm',font = ('Arial',12))
superpharmbox = Entry(root ,font =('Arial', 12))
# superpharmbox.pack(pady=20)

mhlabel = Label(root, text = 'mahsanei-hashmal',font = ('Arial',12))
mhbox = Entry(root ,font =('Arial', 12))
# mhbox.pack(pady=20)


namelabel.grid(row = 1 , column = 0,padx=10)
namebox.grid(row = 1 , column = 1,pady=10)

ksplabel.grid(row = 2 , column = 0,padx=10)
kspbox.grid(row = 2 , column = 1,pady=10)

ivorylabel.grid(row = 3 , column = 0,padx=10)
ivorybox.grid(row = 3 , column = 1,pady=10)

superpharmlabel.grid(row = 4 , column = 0,padx=10)
superpharmbox.grid(row = 4 , column = 1 ,pady=10)

mhlabel.grid(row = 5 , column = 0,padx=10)
mhbox.grid(row = 5 , column = 1, pady=10)



submit = Button(root, text = 'Submit',command = lambda : GatherData(namebox.get(),kspbox.get(),ivorybox.get(),superpharmbox.get(),mhbox.get()) , font = ('Arial', 12) )
submit.grid(row = 7, column = 1 , pady = 20)




root.mainloop()

