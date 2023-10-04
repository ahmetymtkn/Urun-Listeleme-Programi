from tkinter.ttk import Progressbar, Style
from tkinter import Tk, Frame, Button, Label
from PyQt5.QtWidgets import QApplication
from main import AnapencerePage
w = Tk()
width_of_window = 427
height_of_window = 250
screen_width = w.winfo_screenwidth()
screen_height = w.winfo_screenheight()
x_coordinate = (screen_width / 2) - (width_of_window / 2)
y_coordinate = (screen_height / 2) - (height_of_window / 2)
w.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))
w.overrideredirect(1)
s = Style()
s.theme_use('clam')
s.configure("red.Horizontal.TProgressbar", foreground='red', background='#4f4f4f')
progress = Progressbar(w, style="red.Horizontal.TProgressbar", orient="horizontal", length=500, mode='determinate')
def hide():
    w.withdraw()
def new_win():
    hide()
    app = QApplication([])
    pencere = AnapencerePage()
    pencere.show()
    app.exec_()
    w.destroy()  
def bar():
    l4 = Label(w, text='Yükleniyor...', fg='white', bg=a)
    l4.config(font=('Calibri (Body)', 10))
    l4.place(x=18, y=210)   
    import time
    r = 0
    for i in range(100):
        progress['value'] = r
        w.update_idletasks()
        time.sleep(0.03)
        r += 1
    new_win()  
progress.place(x=-10, y=235)
a = '#249794'
Frame(w, width=427, height=241, bg=a).place(x=0, y=0)
b1 = Button(w, width=10, height=1, text='Başla', command=bar, border=0, fg=a, bg='white')
b1.place(x=170, y=200)
l1 = Label(w, text='FABELTEK', fg='white', bg=a)
l1.config(font=('Calibri (Body)', 18, 'bold'))
l1.place(x=50, y=80)
l2 = Label(w, text='OTOMASYON', fg='white', bg=a)
l2.config(font=('Calibri (Body)', 18))
l2.place(x=200, y=82)
l3 = Label(w, text='ÜRÜN LİSTELEME PROGRAMI', fg='white', bg=a)
l3.config(font=('Calibri (Body)', 13))
l3.place(x=50, y=110)
w.mainloop()
