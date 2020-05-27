import tkinter as tk
import tkinter.filedialog
import ar
from tkinter import messagebox
from tkinter import simpledialog
rules=StrongRules=df=0
def getFile():  
        file = tkinter.filedialog.askopenfile(parent=root, mode='r', title='Choose a file')
        if file != None:
            data = file.read()
            file.close()
            #print(f"I got {data} bytes from this file.")
            #inputFile.delete(0,END)
            #inputFile.insert(0,file.name)
            inputFilePath.set(file.name)            

def runAssociation():
    try:
        f= open(inputFilePath.get(),'r')
        f.close()
    except:
        print("error")
        messagebox.showerror("Invalid File Path", "Given path is invalid")
        inputFilePath.set("")
        return
    global rules,StrongRules,df
    df,rules,StrongRules = ar.AssociationMain(inputFilePath.get())
    resultText.set("Result\t\t\t\t\t\n")
    resultText.set(str(resultText.get())+str(StrongRules))
    #print('ddd')
def Plot_Rules_Conf():
    if resultText.get() == "Result\t\t\t\t\t\n":
        messagebox.showinfo("No result", "Result is not yet generated")
    else:
        ar.Plot_Rules_Conf(rules)
def Plot_Rules_Conf_Sup():
    if resultText.get() == "Result\t\t\t\t\t\n":
        messagebox.showinfo("No result", "Result is not yet generated")
    else:
        ar.Plot_Rules_Conf_Sup(df)


def SaveResult():
    if resultText.get()=="Result\t\t\t\t\t\n":                
        messagebox.showinfo("No result", "Result is not yet generated")
    else:
        filename = simpledialog.askstring(title="Name",prompt="File Name?:")
        if filename=="":
            messagebox.showinfo("No filename", "No filename is Entered")
            SaveResult()
        else:
            try:
                f = open(filename,"w")
                f.writelines(resultText.get())
                f.close()
                messagebox.showinfo("Saved", "result saved")
            except:
                pass
root = tk.Tk()
root.geometry("1000x800")
root.title("Association Rule Mining")

Title =tk.Label(root,text="Welcome to Association Rule Mining",relief='solid',fg='blue',bg='red',font=("arial",16,"bold"))
Title.pack(fill=tk.BOTH,padx=2,pady=2)
image = tk.PhotoImage(file = "img3.png")

photo = tk.Label(image=image)
photo.place(x=750,y=40)

tk.Label(root,text="Browse the Dataset file ",font=("arial",14,"bold")).place(x=20,y=160)
inputFilePath = tk.StringVar()
inputFile = tk.Entry(root,font=("arial",16,"bold"),width=40,textvariable=inputFilePath).place(x=20,y=202)
browse = tk.Button(root,text="Browse",relief=tk.GROOVE,fg='red',bg='orange',font=("arial",16,"bold"),command=getFile)
browse.place(x=530,y=200)

generate = tk.Button(root,text="Generate",relief=tk.GROOVE,fg='red',bg='orange',font=("arial",16,"bold"),command=runAssociation)
generate.place(x=260,y=240)

resultText = tk.StringVar()
resultText.set('Result\t\t\t\t\t\n')
result = tk.Label(root,textvariable=resultText,relief='solid',fg='white',bg='green',font=("arial",16,"bold"))
result.place(x=100,y=300)

graph1 = tk.Button(root,text="Graph1",relief=tk.GROOVE,fg='red',bg='orange',font=("arial",16,"bold"),command=Plot_Rules_Conf)
graph1.place(x=200,y=700)

graph2 = tk.Button(root,text="Graph2",relief=tk.GROOVE,fg='red',bg='orange',font=("arial",16,"bold"),command=Plot_Rules_Conf_Sup)
graph2.place(x=360,y=700)


save_result = tk.Button(root,text="Save Result",relief=tk.GROOVE,fg='red',bg='orange',font=("arial",16,"bold"),command=SaveResult)
save_result.place(x=560,y=700)

root.mainloop()
