import tkinter as tk
import datetime
import mysql.connector

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

def save():
    global note_text
    timestamp = datetime.datetime.now().strftime('%Y.%m.%d %H:%M')
    note_date = datetime.datetime.now().strftime('%Y-%m-%d')
    note = note_text.get("1.0", "end-1c")
    note_text.delete("1.0", "end")
    if len(note) > 0:
        mydb = mysql.connector.connect(host='localhost', user="root", passwd="*****", database="*****")
        cursor = mydb.cursor()
        add_new_note_command = f"INSERT INTO notes (db_note_name, db_note_text, db_note_date, db_note_id_subcategory, db_note_font_name, db_note_font_size, db_note_font_colour, db_note_font_bold, db_note_font_italic, db_note_position) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        add_new_note_value = (timestamp, note, note_date, 30, "Calibri Light", 12, "#000000", 0, 0, 'left')
        cursor.execute(add_new_note_command, add_new_note_value)
        mydb.commit()
        cursor.close()
        mydb.close()

        note_text.config(font=("Calibri Light", 35, 'bold'), fg="#00b0f0")
        note_text.insert("1.0", '\n       NOTE ADDED')
        note_text.config(state='disabled')
        root.after(2000, lambda: [note_text.config(state='normal'), note_text.delete("1.0", "end"), note_text.config(font=("Calibri Light", 12), fg="black")])


root = tk.Tk()
root.geometry("500x250+3340+1815")
root.resizable(False, False)
root.title('Quick Note')
root.config(bg="#99cc00")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

root.bind("<Control-s>", lambda event: save())
root.bind("<Control-S>", lambda event: save())

note_text = tk.Text(root, font=("Calibri Light", 12), padx=5, pady=5, bg="#99cc00", bd=0)
note_text.grid(row=0, column=0, sticky="NEWS")
note_text.focus()

tk.Button(root, text="💾", command=lambda: save(), font=("Calibri", 10), bg='#00b0f0', activebackground='#00b0f0', relief='flat', bd=0).grid(row=1, column=0, sticky="EW")

root.mainloop()
