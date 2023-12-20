from tkinter import *
import text_razor
import komprehend



def home_window(source):
    if(source!="null"):
        source.destroy()

    global root
    root = Tk()
    root.title("NLP API Client")

    #creating a label widget
    homescreen_message= Label(root, text="Select API service to use")
    homescreen_message.grid(row=0,column=1)

    textrazor_launcher=Button(root, text="textrazor",command=lambda: text_razor.openwindow(root))
    textrazor_launcher.grid(row=1,column=0)

    textrazor_launcher=Button(root, text="komprehend",command=lambda: komprehend.openwindow(root))
    textrazor_launcher.grid(row=1,column=3)

    root.mainloop()
if __name__ == '__main__':
    home_window("null")
