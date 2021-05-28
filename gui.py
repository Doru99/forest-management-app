import tkinter as tk
from detect import load_image, load_template, detect_template


def upload_image():
    if len(img_path.get()) == 0:
        img_path.set('images/forest2.png')
    img = load_image(img_path.get())


def upload_template():
    if len(temp_path.get()) == 0:
        temp_path.set('templates/tree3.png')
    template = load_template(temp_path.get())


def start_count():
    if len(img_path.get()) == 0:
        upload_image()
    if len(temp_path.get()) == 0:
        upload_template()
    detect_template(load_image(img_path.get()), load_template(temp_path.get()), float(threshold.get()))


def only_lt1(string):
    try:
        if 0 <= float(string) < 1:
            return True
        return False
    except ValueError:
        if string == '.':
            return True
        return False


window = tk.Tk()

img_path = tk.StringVar(window)
temp_path = tk.StringVar(window)
threshold = tk.StringVar(window)

window.geometry('800x200')
window.title('Forest management')

# Incarcare imagine
path_img_entry = tk.Entry(window, textvariable=img_path, width=20)
path_img_entry.place(x=200, y=25)
img_lbl = tk.Label(window, text='Calea relativa a imaginii:')
img_lbl.place(x=50, y=25)
btn1 = tk.Button(window, text='Incarca', command=upload_image)
btn1.place(x=350, y=25)

# Incarcare template
path_temp_entry = tk.Entry(window, textvariable=temp_path, width=20)
path_temp_entry.place(x=225, y=75)
temp_lbl = tk.Label(window, text='Calea relativa a template-ului:')
temp_lbl.place(x=50, y=75)
btn1 = tk.Button(window, text='Incarca', command=upload_template)
btn1.place(x=350, y=75)

# Threshold
threshold_lbl = tk.Label(window, text='Threshold:')
threshold_lbl.place(x=125, y=125)
validation = window.register(only_lt1)
threshold_entry = tk.Entry(window, textvariable=threshold, validate='key', validatecommand=(validation, '%P'), width=5)
threshold_entry.place(x=195, y=125)

# Start
btn2 = tk.Button(window, text='Start', bg='blue', fg='white', width=10, command=start_count)
btn2.place(x=375, y=165)

window.mainloop()
