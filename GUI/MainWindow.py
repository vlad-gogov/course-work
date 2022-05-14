from cgitb import text
from email.policy import default
from tkinter import *


def clicked():
    print(float(entry_t1.get()) + float(entry_t3.get()) + float(entry_c.get()))


main_window = Tk()
main_window.title(
    "Определение квазипотимальных параметров управления перекрестка")
main_window.geometry('600x400')

entry_frame = Frame(main_window, width=300, height=200)
entry_frame.pack(side=TOP)

label_l1 = Label(entry_frame, text="λ1", font=(
    "Arial Bold", 15)).grid(row=0, column=0)
entry_l1 = Entry(entry_frame, width=5).grid(
    row=0, column=1)

label_l2 = Label(entry_frame, text="λ2", font=(
    "Arial Bold", 15)).grid(row=0, column=2)
entry_l2 = Entry(entry_frame, width=5).grid(
    row=0, column=3)

label_r1 = Label(entry_frame, text="r1", font=(
    "Arial Bold", 15)).grid(row=1, column=0)
entry_r1 = Entry(entry_frame, width=5).grid(
    row=1, column=1)

label_r2 = Label(entry_frame, text="r2", font=(
    "Arial Bold", 15)).grid(row=1, column=2)
entry_r2 = Entry(entry_frame, width=5).grid(
    row=1, column=3)

label_g1 = Label(entry_frame, text="g1", font=(
    "Arial Bold", 15)).grid(row=2, column=0)
entry_g1 = Entry(entry_frame, width=5).grid(
    row=2, column=1)

label_g2 = Label(entry_frame, text="g2", font=(
    "Arial Bold", 15)).grid(row=2, column=2)
entry_g1 = Entry(entry_frame, width=5).grid(
    row=2, column=3)

label_t1 = Label(entry_frame, text="T1", font=(
    "Arial Bold", 15)).grid(row=3, column=0)
entry_t1 = Entry(entry_frame, width=5).grid(
    row=3, column=1)

label_t3 = Label(entry_frame, text="T3", font=(
    "Arial Bold", 15)).grid(row=3, column=2)
entry_t3 = Entry(entry_frame, width=5).grid(row=3, column=3)

label_c = Label(entry_frame, text="c", font=(
    "Arial Bold", 15)).grid(row=4, column=0)
entry_c = Entry(entry_frame, width=5).grid(row=4, column=1)

bottom_frame = Frame(main_window, width=600, height=150)
bottom_frame.pack(side=BOTTOM)

btn = Button(bottom_frame, text="Посчитать", command=clicked)
btn.grid(row=0, column=0)
#
# label_log = Label(main_window, font=("Arial Bold", 10))
# label_log.grid(column=1, row=1)

main_window.mainloop()
