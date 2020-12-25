from tkinter import *
from tkinter import filedialog as fd


def open_file():
    fd.askopenfilename()


def save_file():
    fd.asksaveasfilename()


root = Tk()
root.title('Biomed Tibb Merkezi')

main_menu = Menu(root)
root.configure(menu=main_menu)
root.configure(width=99999, height=99999)

first_item = Menu(main_menu, tearoff=0)
main_menu.add_cascade(label="Меню", menu=first_item)
first_item.add_command(label="open file", command=open_file)
first_item.add_command(label="save file", command=save_file)

second_item = Menu(main_menu, tearoff=0)
main_menu.add_cascade(label="Настойки", menu=second_item)
second_item.add_command(label="New")

btn = Button(root)
btn.configure(bg='grey', fg='white', text='????')
btn.place(x=0, y=1, width=300, height=100)

btn1 = Button(root)
btn1.configure(bg='grey', fg='white', text='????')
btn1.place(x=0, y=100, width=300, height=100)

btn2 = Button(root)
btn2.configure(bg='grey', fg='white', text='????')
btn2.place(x=0, y=200, width=300, height=100)

btn3 = Button(root)
btn3.configure(bg='grey', fg='white', text='????')
btn3.place(x=0, y=300, width=300, height=100)

btn4 = Button(root)
btn4.configure(bg='grey', fg='white', text='????')
btn4.place(x=0, y=400, width=300, height=100)

btn5 = Button(root)
btn5.configure(bg='grey', fg='white', text='????')
btn5.place(x=0, y=500, width=300, height=100)

btn6 = Button(root)
btn6.configure(bg='grey', fg='white', text='????')
btn6.place(x=0, y=600, width=300, height=100)

btn7 = Button(root)
btn7.configure(bg='grey', fg='white', text='????')
btn7.place(x=0, y=700, width=300, height=100)

root.mainloop()
