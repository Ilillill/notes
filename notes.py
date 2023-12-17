from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import font
from tkinter import colorchooser
import datetime
import mysql.connector
import pickle
import os
import os.path
import io
from tkinter import filedialog
from tkinter import messagebox
import sqlite3
import smtplib
from email.message import EmailMessage
import re
# pip install python-docx
import docx
import random



try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

list_emoji = ['😀','😄','😉','😍','😐','😴','🦊','🦝','🐹','🐾','🐕','🦥','🦨','🐘','🦔','🐿','🦎','🐊','🦖','🦈','🐬','🦅',
              '🦢','🦉','🦇','🕷','🎄','🎁','🎞','🖼','🎨','🛒','🏆','🎮','🕹','♟','🔈','🔔','🎵','🎤','🎧','🎹','🔒','🔑','🛠',
              '🔧','⚙','🧱','💊','🔭','🧰','🛡','🏹','🗡','⚔','💣','☎','📞','📱','💻','🖥','🖨','⌨','🖱','💾','📀','🎬','📷',
              '📸','📹','🔍','💡','🔦','📕','📖','📗','📚','💰','💷','📦','✏','🖊','🖌','📝','💼','📁','📅','📆','📈','📉','📊',
              '📋','📏','⌛','⏳','⌚','⏰','⏱','🍕','🍟','🥪','🌮','🍦','🍩','🎂','🍰','🍫','🍬','🍭','🍽','🥝','🍓','🍏','🍄',
              '🌸','🌻','🌼','🌲','🌳','🌴','🌵','🍀','🍁','🚗','🚀','⛵','🌍','🌎','🗺','🧭','⛰','🏕','🏞','🏜','🏝','🏡','⛺',
              '🌄','🛏','🧻','🧽','⛅','🌤','🌦','🌩','🌠','🌈','⚡','🔥','🌊','💕','💤','💥','❌','⭕','❗','❓',
              '➕','➖','💭','🗯','🕒','✔','✖','⬜','✅','❎','⬛','🔲','🔳']


########################################################################################################################
########################################################################################################################
#####################################                                               ####################################
#####################################    L O A D    E M A I L    S E T T I N G S    ####################################
#####################################                                               ####################################
########################################################################################################################
########################################################################################################################

try:
    with open("./assets/email_data.dat", "rb") as email_file:
        stored_email_address = pickle.load(email_file)
        stored_email_password = pickle.load(email_file)
except:
    stored_email_address = ''
    stored_email_password = ''

########################################################################################################################
########################################################################################################################
#############################################                              #############################################
#############################################    D A T A B A S E    I D    #############################################
#############################################                              #############################################
########################################################################################################################
########################################################################################################################

database_id = 'notes_database'

########################################################################################################################
########################################################################################################################
##################################                                                     #################################
##################################    L O A D    D A T A B A S E    S E T T I N G S    #################################
##################################                                                     #################################
########################################################################################################################
########################################################################################################################

try:
    with open("./database_data.dat", "rb") as file:
        database_type = pickle.load(file)
        database_name = pickle.load(file)
        database_data = pickle.load(file)
except:
    database_type = ''
    database_name = ''
    database_data = ["", "", ""]


########################################################################################################################
########################################################################################################################
########################################                                        ########################################
########################################    D A T A B A S E    M A N A G E R    ########################################
########################################                                        ########################################
########################################################################################################################
########################################################################################################################

class DatabaseManager(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.columnconfigure((0, 2), weight=1)
        self.rowconfigure((0, 2), weight=1)
        self.config(bg='white')

        self.grid(row=0, column=0, sticky='NEWS', columnspan=20, rowspan=20)

        self.mysql_logo = tk.PhotoImage(file="./assets/logo_mysql.png")
        self.sqlite_logo = tk.PhotoImage(file="./assets/logo_sqlite.png")
        self.error_icon = tk.PhotoImage(file="./assets/error.png")

        self.frame_middle = tk.Frame(self, bg="white")
        self.frame_middle.grid(row=1, column=1, sticky="NEWS")
        self.frame_middle.columnconfigure((0, 1), weight=1)
        self.frame_middle.rowconfigure((0, 1), weight=1)

        ################################################################################################################
        ##############################################    FRAME STATUS    ##############################################
        ################################################################################################################

        self.frame_status = tk.Frame(self.frame_middle, bg="white", highlightcolor='white', highlightbackground='white', highlightthickness=5)
        self.frame_status.grid(row=0, column=0, columnspan=2, sticky="EW", padx=1, pady=1)
        self.frame_status.columnconfigure(0, weight=1)
        self.frame_status.rowconfigure(0, minsize=135, weight=1)

        tk.Label(self.frame_status, text="CURRENT CONNECTION:", bg='white', font=("Calibri", 20)).grid(row=0, column=0, padx=(5, 20), pady=5)
        tk.Label(self.frame_status, text="Database type:", bg='white').grid(row=0, column=1, padx=20, sticky="w")

        self.status_label_database_type = tk.Label(self.frame_status, text='', bg='white', fg="red")
        self.status_label_database_type.grid(row=0, column=2, padx=20, sticky="WE")
        tk.Label(self.frame_status, text="Database name:", bg='white').grid(row=0, column=3, padx=20, sticky="w")
        self.status_label_database_name = tk.Label(self.frame_status, text='', bg='white', fg="black")
        self.status_label_database_name.grid(row=0, column=4, padx=20, sticky="WE")

        self.edit_current_connection_frame()

        ################################################################################################################
        ###############################################    FRAME MYSQL    ##############################################
        ################################################################################################################

        self.frame_mysql = tk.Frame(self.frame_middle, bg="white", highlightcolor='#e48e00', highlightbackground='#e48e00', highlightthickness=5)
        self.frame_mysql.grid(row=1, column=0, sticky="NEWS", padx=1, pady=1)
        self.frame_mysql.columnconfigure(0, minsize=500, weight=1)

        self.label_logo_mysql = tk.Label(self.frame_mysql, image=self.mysql_logo, bg='white', height=100)
        self.label_logo_mysql.grid(row=0, column=0, pady=5)

        self.button_use_mysql = ButtonIconDBManager(self.frame_mysql, text='', command=lambda: self.change_database_type("mysql"), pic="./assets/apply.png", pic_px=40)
        self.button_use_mysql.config(bg='white', relief="flat")
        self.button_use_mysql.grid(row=0, column=1, sticky="NE", padx=1, pady=1)

        ############################################    SERVER SETTINGS    #############################################

        frame_database = tk.LabelFrame(self.frame_mysql, text=' SERVER SETTINGS ', labelanchor='n', bg='white', padx=10, pady=10, width=340, height=205)
        frame_database.grid(row=1, column=0, padx=5, pady=5, sticky="EW", columnspan=2)
        frame_database.columnconfigure((0, 1), weight=1)

        self.label_database_status = tk.Label(frame_database, text="", bg='white', font="Calibri, 12")
        self.label_database_status.grid(row=0, column=0, sticky="EW", columnspan=2, padx=5, pady=(0, 15))

        tk.Label(frame_database, text='Host', bg='white').grid(row=1, column=0, sticky="EW")
        self.entry_host = tk.Entry(frame_database)
        self.entry_host.grid(row=1, column=1, sticky="EW")
        self.entry_host.bind("<Return>", lambda event: self.test_database([self.entry_host.get(), self.entry_login.get(), self.entry_password.get()]))

        tk.Label(frame_database, text='Login', bg='white').grid(row=2, column=0, sticky="EW")
        self.entry_login = tk.Entry(frame_database)
        self.entry_login.grid(row=2, column=1, sticky="EW")
        self.entry_login.bind("<Return>", lambda event: self.test_database([self.entry_host.get(), self.entry_login.get(), self.entry_password.get()]))

        tk.Label(frame_database, text='Password', bg='white').grid(row=3, column=0, sticky="EW")
        self.entry_password = tk.Entry(frame_database, show="*")
        self.entry_password.grid(row=3, column=1, sticky="EW")
        self.entry_password.bind("<Return>", lambda event: self.test_database([self.entry_host.get(), self.entry_login.get(), self.entry_password.get()]))

        self.button_mysql_test = ButtonIconDBManager(frame_database, text='    Test', bg='white', pic="./assets/server.png", pic_px=30, command=lambda: self.test_database([self.entry_host.get(), self.entry_login.get(), self.entry_password.get()]))
        self.button_mysql_test.grid(row=4, column=0, sticky="EW", columnspan=2, pady=(5, 0))

        #######################################    AVAILABLE DATABASES LISTBOX   #######################################

        self.frame_available_databases = tk.LabelFrame(self.frame_mysql, text=' AVAILABLE DATABASES ', labelanchor='n', bg='white', padx=10, pady=10, width=340, height=205)
        self.frame_available_databases.grid(row=2, column=0, padx=5, pady=5, sticky="EW", columnspan=2)
        self.frame_available_databases.columnconfigure(0, weight=1)
        self.frame_available_databases.rowconfigure(0, weight=1)

        self.available_data = tk.StringVar()
        self.scrollbar = tk.Scrollbar(self.frame_available_databases, orient='vertical')
        self.listbox_available_databases = tk.Listbox(self.frame_available_databases,
                                                      listvariable=self.available_data,
                                                      width=30,
                                                      height=7,
                                                      relief="flat",
                                                      selectmode="single",
                                                      foreground='black',
                                                      background='white',
                                                      selectborderwidth=0,
                                                      yscrollcommand=self.scrollbar.set,
                                                      borderwidth=5)

        self.listbox_available_databases.grid(row=0, column=0, sticky="NEWS", pady=(0, 10))

        self.scrollbar.config(command=self.listbox_available_databases.yview)
        self.scrollbar.grid(row=0, column=1, sticky="NS")

        self.button_mysql_connect = ButtonIconDBManager(self.frame_available_databases, text='    Connect', bg='white', pic="./assets/connect.png", pic_px=30, command=lambda: self.mysql_database_connect())
        self.button_mysql_connect.grid(row=1, column=0, sticky="EW", columnspan=2)


        ###########################################    CREATE NEW DATABASE    ##########################################

        self.create_new_database = tk.LabelFrame(self.frame_mysql, text=' CREATE NEW ', labelanchor='n', bg='white', padx=10, pady=10, width=340, height=205)
        self.create_new_database.grid(row=3, column=0, padx=5, pady=5, sticky="EW", columnspan=2)
        self.create_new_database.columnconfigure(0, weight=1)
        self.create_new_database.rowconfigure(0, weight=1)

        self.entry_create_new = ttk.Entry(self.create_new_database)
        self.entry_create_new.grid(row=0, column=0, padx=5, pady=5, sticky="EW")
        self.button_mysql_create = ButtonIconDBManager(self.create_new_database, text='    Create', bg='white', pic="./assets/database_add.png", pic_px=30, command=lambda: self.mysql_database_create())
        self.button_mysql_create.grid(row=1, column=0, padx=5, pady=5, sticky="NEWS")


        ################################################################################################################
        ###############################################    FRAME SQLITE    #############################################
        ################################################################################################################

        self.frame_sqlite = tk.Frame(self.frame_middle, bg="white", highlightcolor='#0f80cc', highlightbackground='#0f80cc', highlightthickness=5)
        self.frame_sqlite.grid(row=1, column=1, sticky="NEWS", padx=1, pady=1)
        self.frame_sqlite.columnconfigure(0, minsize=500, weight=1)
        self.frame_sqlite.rowconfigure((1, 2), weight=1)

        self.label_logo_sqlite = tk.Label(self.frame_sqlite, image=self.sqlite_logo, bg='white', height=100)
        self.label_logo_sqlite.grid(row=0, column=0, pady=5)

        self.button_use_sqlite = ButtonIconDBManager(self.frame_sqlite, text='', command=lambda: self.change_database_type("sqlite"), pic="./assets/apply.png", pic_px=40)
        self.button_use_sqlite.config(bg='white', relief='flat')
        self.button_use_sqlite.grid(row=0, column=1, sticky="NE", padx=1, pady=1)

        self.button_sqlite_create = ButtonIconDBManager(self.frame_sqlite, pic="./assets/database_open.png", pic_px=70, text="     OPEN", command=lambda: self.sqlite_database_open())
        self.button_sqlite_create.grid(row=1, column=0, sticky="NEWS", padx=5, pady=(10, 0), columnspan=2)

        self.button_sqlite_open = ButtonIconDBManager(self.frame_sqlite, pic="./assets/database_add.png", pic_px=70, text="     CREATE", command=lambda: self.sqlite_database_create())
        self.button_sqlite_open.grid(row=2, column=0, sticky="NEWS", padx=5, pady=(5, 10), columnspan=2)

        ################################################################################################################
        ###################################    READ PICKLE AND AUTO-FORMAT FRAMES    ###################################
        ################################################################################################################
        self.edit_frames()


    ####################################################################################################################
    #############################    D A T A B A S E    M A N A G E R    M E T H O D S    ##############################
    ####################################################################################################################

    def edit_current_connection_frame(self):
        try:
            with open("./database_data.dat", "rb") as edit_file:
                current_database_type = pickle.load(edit_file)
                current_database_name = pickle.load(edit_file)
        except:
            current_database_type = ''
            current_database_name = ''

        if current_database_type == '':
            self.status_label_database_type.config(image=self.error_icon, fg='black')
            self.frame_status.config(highlightcolor='red', highlightbackground='red')
            self.status_label_database_name.config(text='Not selected', fg='red')

        elif current_database_type == "mysql":
            self.status_label_database_type.config(image=self.mysql_logo, fg='black')
            self.frame_status.config(highlightcolor='#e48e00', highlightbackground='#e48e00')
            self.status_label_database_name.config(text=current_database_name, fg='#e48e00')

        elif current_database_type == "sqlite":
            self.status_label_database_type.config(image=self.sqlite_logo, fg='black')
            self.frame_status.config(highlightcolor='#0f80cc', highlightbackground='#0f80cc')
            self.status_label_database_name.config(text=os.path.basename(current_database_name), fg='#0f80cc')

    def edit_frames(self):
        if database_type == "":
            self.frame_mysql.config(highlightcolor='grey95', highlightbackground='grey95')
            self.frame_sqlite.config(highlightcolor='grey95', highlightbackground='grey95')
            self.label_logo_mysql.config(state='disabled')
            self.label_logo_sqlite.config(state='disabled')
            self.button_use_mysql.config(state='normal')
            self.label_database_status.config(state='disabled')
            self.entry_host.config(state='disabled')
            self.entry_login.config(state='disabled')
            self.entry_password.config(state='disabled')
            self.button_mysql_test.config(state='disabled')
            self.listbox_available_databases.config(state='disabled')
            self.button_mysql_connect.config(state='disabled')
            self.entry_create_new.config(state='disabled')
            self.button_mysql_create.config(state='disabled')
            self.label_database_status.config(state='disabled')
            self.button_use_sqlite.config(state='normal')
            self.button_sqlite_create.config(state='disabled')
            self.button_sqlite_open.config(state='disabled')
        elif database_type == "mysql":
            self.entry_host.insert(0, database_data[0])
            self.entry_login.insert(0, database_data[1])
            self.entry_password.insert(0, database_data[2])
            self.frame_mysql.config(highlightcolor='#e48e00', highlightbackground='#e48e00')
            self.frame_sqlite.config(highlightcolor='grey95', highlightbackground='grey95')
            self.label_logo_mysql.config(state='normal')
            self.label_logo_sqlite.config(state='disabled')
            self.button_use_mysql.config(state='disabled')
            self.label_database_status.config(state='normal')
            self.entry_host.config(state='normal')
            self.entry_login.config(state='normal')
            self.entry_password.config(state='normal')
            self.button_mysql_test.config(state='normal')
            self.listbox_available_databases.config(state='disabled')
            self.button_mysql_connect.config(state='disabled')
            self.entry_create_new.config(state='disabled')
            self.button_mysql_create.config(state='disabled')
            self.label_database_status.config(state='normal')
            self.button_use_sqlite.config(state='normal')
            self.button_sqlite_create.config(state='disabled')
            self.button_sqlite_open.config(state='disabled')
        elif database_type == "sqlite":
            self.frame_mysql.config(highlightcolor='grey95', highlightbackground='grey95')
            self.frame_sqlite.config(highlightcolor='#0f80cc', highlightbackground='#0f80cc')
            self.label_logo_mysql.config(state='disabled')
            self.label_logo_sqlite.config(state='normal')
            self.button_use_mysql.config(state='normal')
            self.entry_host.config(state='disabled')
            self.entry_login.config(state='disabled')
            self.entry_password.config(state='disabled')
            self.button_mysql_test.config(state='disabled')
            self.listbox_available_databases.config(state='disabled')
            self.button_mysql_connect.config(state='disabled')
            self.entry_create_new.config(state='disabled')
            self.button_mysql_create.config(state='disabled')
            self.label_database_status.config(state='disabled')
            self.button_use_sqlite.config(state='disabled')
            self.button_sqlite_create.config(state='normal')
            self.button_sqlite_open.config(state='normal')

    def change_database_type(self, option):
        global database_type
        if option == "mysql":
            database_type = "mysql"
        elif option == "sqlite":
            database_type = "sqlite"
        self.edit_frames()

    ####################################################################################################################
    ##########################################    M Y S Q L    C R E A T E    ##########################################
    ####################################################################################################################

    def mysql_database_create(self):
        global database_type
        global database_name
        global database_data

        new_mysql_database_name = self.entry_create_new.get()
        if len(new_mysql_database_name) != 0:
            try:
                mydb = mysql.connector.connect(host=self.entry_host.get(), user=self.entry_login.get(), passwd=self.entry_password.get())
                cursor = mydb.cursor()
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {new_mysql_database_name}")
                mydb.commit()
                cursor.close()
                mydb.close()
                mydb = mysql.connector.connect(host=self.entry_host.get(), user=self.entry_login.get(), passwd=self.entry_password.get(), database=new_mysql_database_name)
                cursor = mydb.cursor()
                cursor.execute("CREATE TABLE IF NOT EXISTS database_id(d_id text)")
                cursor.execute("INSERT INTO database_id VALUES (%s)", (database_id,))
                mydb.commit()
                cursor.close()
                mydb.close()
                database_type = 'mysql'
                database_name = new_mysql_database_name
                database_data = [self.entry_host.get(), self.entry_login.get(), self.entry_password.get()]
                with open("./database_data.dat", "wb") as dumpfile:
                    pickle.dump(database_type, dumpfile)
                    pickle.dump(database_name, dumpfile)
                    pickle.dump(database_data, dumpfile)
                self.edit_current_connection_frame()

                create_table_command = f"CREATE TABLE IF NOT EXISTS settings(settings_colour_mode TEXT, settings_pictures_path TEXT, settings_selected_listbox_font_name TEXT, settings_selected_listbox_font_size INT, settings_main_menu_icon_size INT, settings_main_menu_padding INT, settings_note_menu_icon_size INT, settings_note_menu_padding INT, settings_window_width INT, settings_window_height INT, settings_window_position_x INT, settings_window_position_y INT, settings_notes_panel_visibility TEXT)"
                mydb = mysql.connector.connect(host=database_data[0], user=database_data[1], passwd=database_data[2], database=database_name)
                cursor = mydb.cursor()
                cursor.execute(create_table_command)
                mydb.commit()
                add_item_command = f"INSERT INTO settings (settings_colour_mode, settings_pictures_path, settings_selected_listbox_font_name, settings_selected_listbox_font_size, settings_main_menu_icon_size, settings_main_menu_padding, settings_note_menu_icon_size, settings_note_menu_padding, settings_window_width, settings_window_height, settings_window_position_x, settings_window_position_y, settings_notes_panel_visibility) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                add_item_value = ('white', "./icons/colourful/", "Calibri Light", 9, 40, 10, 20, 10, 1920, 1080, 700, 500, "show")
                cursor.execute(add_item_command, add_item_value)

                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS categories (db_category_name VARCHAR(255), db_category_description TEXT, db_category_colour VARCHAR(255), db_category_id INT AUTO_INCREMENT PRIMARY KEY)")
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS subcategories (db_subcategory_name VARCHAR(255), db_subcategory_description TEXT, db_subcategory_id_category INT, db_subcategory_id INT AUTO_INCREMENT PRIMARY KEY)")
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS notes (db_note_name VARCHAR(255), db_note_text LONGTEXT, db_note_date VARCHAR(255), db_note_id_subcategory INT, db_note_font_name VARCHAR(255), db_note_font_size INT, db_note_font_colour VARCHAR(255), db_note_font_bold INT, db_note_font_italic INT, db_note_position VARCHAR(255), db_note_id INT AUTO_INCREMENT PRIMARY KEY)")

                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS archived (db_archived_name VARCHAR(255), db_archived_text LONGTEXT, db_archived_id INT AUTO_INCREMENT PRIMARY KEY)")

                mydb.commit()

                '''Insert blank Category, Subcategory and Note'''

                add_category_command = f"INSERT INTO categories (db_category_name, db_category_description, db_category_colour) VALUES (%s, %s, %s)"
                add_category_value = ("- N O T E S -", '', "#00b0f0")
                cursor.execute(add_category_command, add_category_value)
                mydb.commit()


                add_blank_subcategory_command = f"INSERT INTO subcategories (db_subcategory_name, db_subcategory_description, db_subcategory_id_category) VALUES (%s, %s, %s)"
                add_blank_subcategory_value = ("NOTES", '', 1)
                cursor.execute(add_blank_subcategory_command, add_blank_subcategory_value)
                mydb.commit()


                add_blank_note_command = f"INSERT INTO notes (db_note_name, db_note_text, db_note_date, db_note_id_subcategory, db_note_font_name, db_note_font_size, db_note_font_colour, db_note_font_bold, db_note_font_italic, db_note_position) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                add_blank_note_value = ("New note", '', datetime.date.today(), 1, "Calibri Light", 9, "#000000", 0, 0, 'left')
                cursor.execute(add_blank_note_command, add_blank_note_value)

                mydb.commit()
                cursor.close()
                mydb.close()

                ##############################################
                ##########    S T A R T    A P P    ##########
                ##############################################
                apply_settings_and_start_app(database.table_get_all('settings')[0][0])

            except:
                messagebox.showinfo(title='Error', message=f"Error creating database")

    def mysql_database_connect(self):
        global database_type
        global database_name
        global database_data
        currently_selected_database = self.listbox_available_databases.get('active')[0]
        try:
            mydb = mysql.connector.connect(host=self.entry_host.get(), user=self.entry_login.get(), passwd=self.entry_password.get(), database=currently_selected_database)
            cursor = mydb.cursor()
            cursor.execute("SELECT * FROM database_id")
            search_result = cursor.fetchone()
            cursor.close()
            mydb.close()

            if search_result[0] == database_id:
                database_type = 'mysql'
                database_name = currently_selected_database
                database_data = [self.entry_host.get(), self.entry_login.get(), self.entry_password.get()]
                with open("./database_data.dat", "wb") as dumpfile:
                    pickle.dump(database_type, dumpfile)
                    pickle.dump(database_name, dumpfile)
                    pickle.dump(database_data, dumpfile)
                self.edit_current_connection_frame()

                ##############################################
                ##########    S T A R T    A P P    ##########
                ##############################################
                apply_settings_and_start_app(database.table_get_all('settings')[0][0])

            else:
                messagebox.showinfo(title='Database Error', message=f"{currently_selected_database.capitalize()} doesn't belong to this app.")
        except:
            messagebox.showinfo(title='Database Error', message=f"{currently_selected_database.capitalize()} doesn't belong to this app.")

    def test_database(self, data):
        try:
            mydb = mysql.connector.connect(host=data[0], user=data[1], passwd=data[2])
            cursor = mydb.cursor()
            cursor.execute("SHOW DATABASES")
            self.available_databases_list = []
            for db in cursor:
                self.available_databases_list.append(db)
            cursor.close()
            mydb.close()
            self.listbox_available_databases.config(state='normal')
            self.button_mysql_connect.config(state='normal')
            self.entry_create_new.config(state='normal')
            self.button_mysql_create.config(state='normal')
            self.label_database_status.config(text='Server connection: OK', fg="green")
            self.available_data.set(value=self.available_databases_list)
        except:
            self.label_database_status.config(text='Server connection: ERROR', fg="red")
            self.available_data.set(value=[])
            self.listbox_available_databases.config(state='disabled')
            self.button_mysql_connect.config(state='disabled')
            self.entry_create_new.config(state='disabled')
            self.button_mysql_create.config(state='disabled')

    def sqlite_database_open(self):
        global database_type
        global database_name
        global database_data
        try:
            database_to_import = filedialog.askopenfilename(title="Select database file to open", filetypes=(("Database files", "*.db"), ("All files", "*.*")))
        except:
            messagebox.showinfo(title='Error', message="Error opening database, please try again.")
            return
        if len(database_to_import) != 0:
            if database_to_import != '':
                try:
                    connection = sqlite3.connect(database_to_import)
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM database_id")
                    check_id = cursor.fetchone()
                    cursor.close()
                    connection.close()

                    if check_id[0] == database_id:
                        database_type = 'sqlite'
                        database_name = database_to_import
                        database_data = ["", "", ""]
                        with open("./database_data.dat", "wb") as dumpfile:
                            pickle.dump(database_type, dumpfile)
                            pickle.dump(database_name, dumpfile)
                            pickle.dump(database_data, dumpfile)
                        self.edit_current_connection_frame()

                        ##############################################
                        ##########    S T A R T    A P P    ##########
                        ##############################################

                        apply_settings_and_start_app(database.table_get_all('settings')[0][0])

                    else:
                        messagebox.showinfo(title='Database Error', message=f"{os.path.basename(database_to_import).capitalize()} doesn't belong to this app.")
                except:
                    messagebox.showinfo(title='Database Error', message=f"{os.path.basename(database_to_import).capitalize()} doesn't belong to this app.")


    ####################################################################################################################
    #########################################    S Q L I T E    C R E A T E    #########################################
    ####################################################################################################################

    def sqlite_database_create(self):
        global database_type
        global database_name
        global database_data
        try:
            database_path = filedialog.asksaveasfilename(title="Create Database", initialdir="./assets/", defaultextension="db", filetypes=(("Database files *.db", "*.db"), ("All files", "*.*")))
        except (AttributeError, FileNotFoundError):
            return
        if len(database_path) != 0:
            try:
                database_type = 'sqlite'
                database_name = database_path
                database_data = ["", "", ""]
                connection = sqlite3.connect(database_path)
                cursor = connection.cursor()
                cursor.execute("CREATE TABLE IF NOT EXISTS database_id(d_id text)")
                cursor.execute("INSERT INTO database_id VALUES(?)", (database_id, ))

                connection.commit()
                connection.close()
                with open("./database_data.dat", "wb") as dumpfile:
                    pickle.dump(database_type, dumpfile)
                    pickle.dump(database_name, dumpfile)
                    pickle.dump(database_data, dumpfile)
                self.edit_current_connection_frame()

                mydb = sqlite3.connect(database_name)
                cursor = mydb.cursor()
                cursor.execute(f"CREATE TABLE IF NOT EXISTS settings (settings_colour_mode TEXT, settings_pictures_path TEXT, settings_selected_listbox_font_name TEXT, settings_selected_listbox_font_size INT, settings_main_menu_icon_size INT, settings_main_menu_padding INT, settings_note_menu_icon_size INT, settings_note_menu_padding INT, settings_window_width INT, settings_window_height INT, settings_window_position_x INT, settings_window_position_y INT, settings_notes_panel_visibility TEXT)")
                add_item_command = f"INSERT INTO settings (settings_colour_mode, settings_pictures_path, settings_selected_listbox_font_name, settings_selected_listbox_font_size, settings_main_menu_icon_size, settings_main_menu_padding, settings_note_menu_icon_size, settings_note_menu_padding, settings_window_width, settings_window_height, settings_window_position_x, settings_window_position_y, settings_notes_panel_visibility) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                mydb.commit()
                add_item_value = ('white', "./icons/colourful/", "Calibri Light", 9, 40, 10, 20, 10, 1920, 1080, 700, 500, "show")
                cursor.execute(add_item_command, add_item_value)

                cursor.execute("CREATE TABLE IF NOT EXISTS categories (db_category_name VARCHAR(255), db_category_description TEXT, db_category_colour VARCHAR(255), db_category_id INT AUTO_INCREMENT PRIMARY KEY)")
                cursor.execute("CREATE TABLE IF NOT EXISTS subcategories (db_subcategory_name VARCHAR(255), db_subcategory_description TEXT, db_subcategory_id_category INT, db_subcategory_id INT AUTO_INCREMENT PRIMARY KEY)")
                cursor.execute("CREATE TABLE IF NOT EXISTS notes (db_note_name VARCHAR(255), db_note_text TEXT, db_note_date VARCHAR(255), db_note_id_subcategory INT, db_note_font_name TEXT, db_note_font_size INT, db_note_font_colour TEXT, db_note_font_bold INT, db_note_font_italic INT, db_note_position TEXT, db_note_id INT AUTO_INCREMENT PRIMARY KEY)")

                mydb.commit()

                cursor.execute("CREATE TABLE IF NOT EXISTS archived (db_archived_name VARCHAR(255), db_archived_text TEXT, db_archived_id INT AUTO_INCREMENT PRIMARY KEY)")

                add_category_command = f"INSERT INTO categories (db_category_name, db_category_description, db_category_colour) VALUES (?, ?, ?)"
                add_category_value = ("- N O T E S -", '', '#00b0f0')
                cursor.execute(add_category_command, add_category_value)
                mydb.commit()

                add_blank_subcategory_command = f"INSERT INTO subcategories (db_subcategory_name, db_subcategory_description, db_subcategory_id_category) VALUES (?, ?, ?)"
                add_blank_subcategory_value = ("NOTES", '', 1)
                cursor.execute(add_blank_subcategory_command, add_blank_subcategory_value)
                mydb.commit()

                add_blank_note_command = f"INSERT INTO notes (db_note_name, db_note_text, db_note_date, db_note_id_subcategory, db_note_font_name, db_note_font_size, db_note_font_colour, db_note_font_bold, db_note_font_italic, db_note_position) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                add_blank_note_value = ("New note", '', datetime.date.today(), 1, "Calibri Light", 9, "#000000", 0, 0, 'left')
                cursor.execute(add_blank_note_command, add_blank_note_value)

                mydb.commit()
                cursor.close()
                mydb.close()

                ##############################################
                ##########    S T A R T    A P P    ##########
                ##############################################

                apply_settings_and_start_app(database.table_get_all('settings')[0][0])

            except:
                messagebox.showinfo(title='Database Error', message=f"DATABASE ERROR")

    ####################################################################################################################
    ######################################    D A T A B A S E    M E T H O D S    ######################################
    ####################################################################################################################

    def get_db(self):
        if database_type == 'mysql':
            try:
                mydb = mysql.connector.connect(host=database_data[0], user=database_data[1], passwd=database_data[2], database=database_name)
                return mydb
            except:
                DatabaseManager(root)
                return

        elif database_type == 'sqlite':
            mydb = sqlite3.connect(database_name)
            return mydb

    def table_settings_update_colour_modes(self, c_mode):
        if database_type == 'mysql':
            try:
                mydb = mysql.connector.connect(host=database_data[0], user=database_data[1], passwd=database_data[2], database=database_name)
            except:
                DatabaseManager(root)
                return
            update_item_command = f"UPDATE settings SET settings_colour_mode=%s"
        elif database_type == 'sqlite':
            mydb = sqlite3.connect(database_name)
            update_item_command = f"UPDATE settings SET settings_colour_mode=?"
        update_item_value = (c_mode, )
        cursor = mydb.cursor()
        cursor.execute(update_item_command, update_item_value)
        mydb.commit()
        cursor.close()
        mydb.close()
        apply_settings_and_start_app(c_mode)

    '''VARCHAR - specified length text / TEXT - any length text / INT - 32bit integer / BIGINT - 64bit integer'''
    def table_create(self, table_name):

        create_table_command = f"CREATE TABLE IF NOT EXISTS {table_name} (item_name VARCHAR(255), item_description TEXT, item_rating INT, item_picture BLOB, item_id INT AUTO_INCREMENT PRIMARY KEY)"
        if database_type == 'mysql':
            try:
                mydb = mysql.connector.connect(host=database_data[0], user=database_data[1], passwd=database_data[2], database=database_name)
            except:
                DatabaseManager(root)
                return
        elif database_type == 'sqlite':
            mydb = sqlite3.connect(database_name)
        cursor = mydb.cursor()
        cursor.execute(create_table_command)
        mydb.commit()
        cursor.close()
        mydb.close()

    def table_destroy(self, table_name):
        if database_type == 'mysql':
            try:
                mydb = mysql.connector.connect(host=database_data[0], user=database_data[1], passwd=database_data[2], database=database_name)
            except:
                DatabaseManager(root)
                return
        elif database_type == 'sqlite':
            mydb = sqlite3.connect(database_name)
        cursor = mydb.cursor()
        cursor.execute(f"DROP TABLE {table_name}")
        mydb.commit()
        cursor.close()
        mydb.close()

    def table_add_item(self, table_name, i_name, i_description, i_rating, i_picture):
        if database_type == 'mysql':
            try:
                mydb = mysql.connector.connect(host=database_data[0], user=database_data[1], passwd=database_data[2], database=database_name)
            except:
                DatabaseManager(root)
                return
            add_item_command = f"INSERT INTO {table_name} (item_name, item_description, item_rating, item_picture) VALUES (%s, %s, %s, %s)"
        elif database_type == 'sqlite':
            mydb = sqlite3.connect(database_name)
            add_item_command = f"INSERT INTO {table_name} (item_name, item_description, item_rating, item_picture) VALUES (?, ?, ?, ?)"
        add_item_value = (i_name, i_description, i_rating, i_picture)
        cursor = mydb.cursor()
        cursor.execute(add_item_command, add_item_value)
        mydb.commit()
        cursor.close()
        mydb.close()

    def table_update_item_by_id(self, table_name, i_name, i_description, i_rating, i_picture, item_id):
        if database_type == 'mysql':
            try:
                mydb = mysql.connector.connect(host=database_data[0], user=database_data[1], passwd=database_data[2], database=database_name)
            except:
                DatabaseManager(root)
                return
            update_item_command = f"UPDATE {table_name} SET item_name=%s, item_description=%s, item_rating=%s, item_picture=%s WHERE item_id=%s"
        elif database_type == 'sqlite':
            mydb = sqlite3.connect(database_name)
            update_item_command = f"UPDATE {table_name} SET item_name=?, item_description=?, item_rating=?, item_picture=? WHERE rowid=?"
        update_item_value = (i_name, i_description, i_rating, i_picture, item_id)
        cursor = mydb.cursor()
        cursor.execute(update_item_command, update_item_value)
        mydb.commit()
        cursor.close()
        mydb.close()

    '''The auto key is called oid, I can refer to it: connection.execute("DELETE FROM table WHERE oid=1")'''
    def table_delete_item(self, table_name, item_id):
        if database_type == 'mysql':
            try:
                mydb = mysql.connector.connect(host=database_data[0], user=database_data[1], passwd=database_data[2], database=database_name)
            except:
                DatabaseManager(root)
                return
            delete_item_command = f"DELETE FROM {table_name} WHERE item_id=%s"
        elif database_type == 'sqlite':
            mydb = sqlite3.connect(database_name)
            delete_item_command = f"DELETE FROM {table_name} WHERE rowid=?"
        delete_item_id = (item_id, )
        cursor = mydb.cursor()
        cursor.execute(delete_item_command, delete_item_id)
        mydb.commit()
        cursor.close()
        mydb.close()

    def table_get_all(self, table_name):
        if database_type == 'mysql':
            try:
                mydb = mysql.connector.connect(host=database_data[0], user=database_data[1], passwd=database_data[2], database=database_name)
            except:
                DatabaseManager(root)
                return
        elif database_type == 'sqlite':
            mydb = sqlite3.connect(database_name)
        cursor = mydb.cursor()
        if database_type == 'mysql':
            cursor.execute(f"SELECT * FROM {table_name}")
        elif database_type == 'sqlite':
            cursor.execute(f"SELECT *, rowid FROM {table_name}")
        search_result = []
        for row in cursor.fetchall():
            search_result.append(row)

        if not search_result:
            search_result = [[]]
        cursor.close()
        mydb.close()
        return search_result

    def table_get_by_id(self, table_name, item_id):
        if database_type == 'mysql':
            try:
                mydb = mysql.connector.connect(host=database_data[0], user=database_data[1], passwd=database_data[2], database=database_name)
            except:
                DatabaseManager(root)
                return
            get_by_id_command = f"SELECT * FROM {table_name} WHERE item_id=%s"
        elif database_type == 'sqlite':
            mydb = sqlite3.connect(database_name)
            get_by_id_command = f"SELECT *, rowid FROM {table_name} WHERE rowid=?"
        get_by_id_value = (item_id, )
        cursor = mydb.cursor()
        cursor.execute(get_by_id_command, get_by_id_value)
        search_result = []
        for row in cursor.fetchall():
            search_result.append(row)
        if not search_result:
            search_result = None
        cursor.close()
        mydb.close()

        return search_result[0]

    def table_search(self, table_name, search_phrase):
        if database_type == 'mysql':
            try:
                mydb = mysql.connector.connect(host=database_data[0], user=database_data[1], passwd=database_data[2], database=database_name)
            except:
                DatabaseManager(root)
                return
            search_command = f"SELECT * FROM {table_name} WHERE item_name LIKE '%{search_phrase}%' OR item_description LIKE '%{search_phrase}%' "
            cursor = mydb.cursor(buffered=True)
        elif database_type == 'sqlite':
            mydb = sqlite3.connect(database_name)
            search_command = f"SELECT * FROM {table_name} WHERE item_name LIKE '%{search_phrase}%' OR item_description LIKE '%{search_phrase}%' "
            cursor = mydb.cursor()
        cursor.execute(search_command)
        search_result = [
            [row[0], row[1], row[2], row[3], row[4]] for
            row in cursor.fetchall()]
        if not search_result:
            search_result = [[]]
        cursor.close()
        mydb.close()
        return search_result

########################################################################################################################
########################################################################################################################
##################################################                   ###################################################
##################################################    S Y S T E M    ###################################################
##################################################                   ###################################################
########################################################################################################################
########################################################################################################################

def copy_to_clipboard(input):
    root.clipboard_clear()
    root.clipboard_append(input)
    statusbar.set(f"{input} copied to clipboard")

def note_print(print_data):
    with open("./assets/temp.txt", "w", encoding="utf-8") as file:
        file.write(print_data[1])
    os.startfile(".\\assets\\temp.txt", 'print')

def timestamp():
    return f"{datetime.datetime.now().strftime('%Y.%m.%d %H:%M')}"

def note_email(email_data):
    def check_email(email_address):
        email_str = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        return re.search(email_str, email_address)

    def send_now():
        if check_email(email_entry.get()):
            email = EmailMessage()
            email['from'] = 'Notes App'
            email['to'] = email_entry.get()
            email['subject'] = email_data[0]
            email.set_content(email_data[1])
            with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                try:
                    smtp.login(stored_email_address, stored_email_password)
                    smtp.send_message(email)
                    statusbar.set('Email sent')
                    email_frame.destroy()
                except TypeError:
                    email_frame.destroy()
                    messagebox.showerror(title='Send-from email error', message="Go to settings and set up send-from email first.")
                except smtplib.SMTPAuthenticationError:
                    email_frame.destroy()
                    messagebox.showerror(title='Send-from email error', message="The send-from email details seem to be incorrect.")
                email_frame.destroy()
        else:
            statusbar.set('Invalid email address')


    email_frame = tk.Toplevel()
    email_frame.title("Send Email")
    email_frame.columnconfigure(0, weight=1)
    email_frame.rowconfigure(2, weight=1)
    ttk.Label(email_frame, text='Your email', anchor='center').grid(row=1, column=0, columnspan=3, sticky="EW", pady=5)
    email_entry = ttk.Entry(email_frame)
    email_entry.grid(row=2, column=0, columnspan=3, sticky="EW", padx=10, pady=(0, 10))
    email_entry.focus()
    email_entry.bind("<Return>", lambda event: send_now())
    ttk.Button(email_frame, text='Send', command=lambda: send_now()).grid(row=3, column=1, sticky="W")
    ttk.Button(email_frame, text='Cancel', command=lambda: email_frame.destroy()).grid(row=3, column=2, sticky="W")

def note_drive(drive_data):
    '''IMPORTANT: Each Google API Pickle and Credentials file should have it's own Folder Check paths'''
    SCOPES = ['https://www.googleapis.com/auth/drive']
    from googleapiclient import discovery
    creds = None
    if os.path.exists('./assets/google_api_drive/token.pickle'):
        with open('./assets/google_api_drive/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './assets/google_api_drive/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('./assets/google_api_drive/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    try:
        # CREATE DOCUMENT
        service = build('docs', 'v1', credentials=creds)
        doc_title = drive_data[0]
        body = {
            'title': doc_title,
        }
        doc = service.documents().create(body=body).execute()
        doc_id = doc.get('documentId')
        requests = [
            {
                'insertText': {
                    'location': {
                        'index': 1,
                    },
                    'text': drive_data[1]
                }
            }
        ]
        result = service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
        statusbar.set("Google Drive Document created")
    except:
        statusbar.set("Error")

def note_word(word_data):
    try:
        file_path = filedialog.askdirectory(title="Where would you like to save your Word Document?")
        '''Remove special characters from filename'''
        filename = ''.join(char for char in word_data[0] if char.isalnum())
        document = docx.Document()
        content = word_data[1]
        document.add_paragraph(content)
        document.save(f"{file_path}/{filename}.docx")
    except (AttributeError, FileNotFoundError):
        statusbar.set("Save operation cancelled")
        return


########################################################################################################################
########################################################################################################################
#################################################                     ##################################################
#################################################    B U T T O N S    ##################################################
#################################################                     ##################################################
########################################################################################################################
########################################################################################################################

class ButtonCategories(tk.Button):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.config(bg=button_category_background, fg=button_category_text, bd=0, font=("Calilbri", 9, 'bold'), relief='flat', height=1, activebackground=button_category_background_selected, activeforeground=button_category_text_selected)


class ButtonSubCategories(tk.Button):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.config(bg=button_subcategory_background, fg=button_subcategory_text, bd=0, font=("Calibri", 8), relief='flat', height=1, activebackground=button_subcategory_background_selected, activeforeground=button_subcategory_text_selected)

################################    A P P    B U T T O N S    W I T H    I M A G E S    ################################

class ButtonIcon(tk.Button):
    def __init__(self, container, pic='', pic_px=0, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.pic = pic
        self.px = pic_px

        self.im = Image.open(pictures_path + self.pic)
        self.im.thumbnail((pic_px, pic_px))
        self.pic = ImageTk.PhotoImage(self.im)

        self.config(background=button_default_background,
                    foreground=button_default_text,
                    image=self.pic,
                    compound="left",
                    bd=0,
                    relief="flat",
                    borderwidth=0,
                    activebackground=button_default_background,
                    width=int(pic_px),
                    font=("Calibri", 9))

#########################    D B    M A N A G E R    B U T T O N S    W I T H    I M A G E S    ########################

class ButtonIconDBManager(tk.Button):
    def __init__(self, container, pic='', pic_px=0, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.pic = pic
        self.px = pic_px

        self.im = Image.open(self.pic)
        self.im.thumbnail((pic_px, pic_px))
        self.pic = ImageTk.PhotoImage(self.im)

        self.config(background='grey97', foreground='black', image=self.pic, compound="left", bd=1,
                    borderwidth=1, activebackground='grey90', width=int(pic_px), font=("Calibri", 9))


##########    L A B E L    C L A S S    C O N V E R T I N G    B I N A R Y    D A T A    T O    I M A G E    ###########

class LabelImage(tk.Label): # import io, from PIL import ImageTk, Image
    def __init__(self, container, binary_data, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.binary_data = binary_data

        self.read_binary = io.BytesIO(self.binary_data)
        self.img = ImageTk.PhotoImage(Image.open(self.read_binary))

        self.config(image=self.img, compound="left", bg='white')

########################################################################################################################
########################################################################################################################
###############################################                          ###############################################
###############################################    S T A R T    A P P    ###############################################
###############################################                          ###############################################
########################################################################################################################
########################################################################################################################

def apply_settings_and_start_app(theme_option):

    list_of_settings = database.table_get_all('settings')[0]

    global pictures_path

    global selected_notes_font_name
    global selected_notes_font_size

    global window_width
    global window_height
    global window_position_x
    global window_position_y
    global notes_panel_visible

    global main_menu_icon_size
    global main_menu_padding
    global note_menu_icon_size
    global note_menu_padding

    global selected_theme
    global root_colour
    global text_colour
    global frame_menu_colour
    global frame_categories_colour
    global frame_subcategories_colour
    global frame_listbox_and_text_colour
    global frame_text_colour
    global button_menu_background
    global button_menu_text
    global button_default_background
    global button_default_text
    global button_category_background
    global button_category_background_selected
    global button_category_text
    global button_category_text_selected
    global button_subcategory_background
    global button_subcategory_background_selected
    global button_subcategory_text
    global button_subcategory_text_selected
    global button_subcategory_background_separator
    global button_subcategory_text_separator
    global listbox_text_colour
    global listbox_background_colour
    global listbox_text_selected_colour
    global listbox_background_selected_colour
    global notes_panel_visible
    global font_list_notes

    try:
        pictures_path = list_of_settings[1]
        selected_notes_font_name = list_of_settings[2]
        selected_notes_font_size = list_of_settings[3]
        main_menu_icon_size = list_of_settings[4]
        main_menu_padding = list_of_settings[5]
        note_menu_icon_size = list_of_settings[6]
        note_menu_padding = list_of_settings[7]
        window_width = list_of_settings[8]
        window_height = list_of_settings[9]
        window_position_x = list_of_settings[10]
        window_position_y = list_of_settings[11]
        notes_panel_visible = list_of_settings[12]
    except:
        pictures_path = "./icons/colourful/"
        selected_notes_font_name = "Calibri Light"
        selected_notes_font_size = 9
        main_menu_icon_size = 40
        main_menu_padding = 10
        note_menu_icon_size = 20
        note_menu_padding = 10
        window_width = 1920
        window_height = 1080
        window_position_x = 700
        window_position_y = 500
        notes_panel_visible = 'show'

    if theme_option == 'dark':
        statusbar.set("Dark Mode selected")
        selected_theme = 'dark'
        root_colour = "black"
        text_colour = "#000000"
        frame_menu_colour = "#B3B3B3"
        frame_categories_colour = "#3c3c3c"
        frame_subcategories_colour = "#747a80"
        frame_listbox_and_text_colour = "#747a80"
        frame_text_colour = 'white'  # 3c3c3c
        button_menu_background = "#B3B3B3"
        button_menu_text = "white"
        button_default_background = "#B3B3B3"
        button_default_text = "white"
        button_category_background = "#3c3c3c"
        button_category_background_selected = '#747a80'
        button_category_text = "white"
        button_category_text_selected = "white"
        button_subcategory_background = "#3c3c3c"
        button_subcategory_background_selected = "#747a80"
        button_subcategory_text = "white"
        button_subcategory_text_selected = "white"
        button_subcategory_background_separator = "#B3B3B3"
        button_subcategory_text_separator = "black"
        listbox_text_colour = "white"
        listbox_background_colour = "#747a80"
        listbox_text_selected_colour = "black"
        listbox_background_selected_colour = 'white'

    elif theme_option == 'light':
        selected_theme = 'light'
        root_colour = "white"
        text_colour = "black"
        frame_menu_colour = "grey95"
        frame_categories_colour = "#00b0f0"
        frame_subcategories_colour = "#99cc00"
        frame_listbox_and_text_colour = "#99cc00"
        frame_text_colour = 'white'
        button_menu_background = "grey95"
        button_menu_text = "black"
        button_default_background = "#F2F2F2"
        button_default_text = "black"
        button_category_background = '#00b0f0'
        button_category_background_selected = "#99cc00"
        button_category_text = "white"#"#00b0f0"
        button_category_text_selected = "white"
        button_subcategory_background = '#00b0f0'
        button_subcategory_background_selected = "#99cc00"
        button_subcategory_text = "white" #"#99cc00"
        button_subcategory_text_selected = "white"
        button_subcategory_background_separator = "white"#"grey95"
        button_subcategory_text_separator = "black"
        listbox_text_colour = "black"
        listbox_background_colour = "#99cc00"
        listbox_text_selected_colour = "black"
        listbox_background_selected_colour = "white"
        statusbar.set("Colourful Mode selected")

    elif theme_option == 'white':
        selected_theme = 'white'
        root_colour = "white"
        text_colour = "black"
        frame_menu_colour = "grey90"
        frame_categories_colour = "grey90"
        frame_subcategories_colour = "grey90"
        frame_listbox_and_text_colour = "grey90"
        frame_text_colour = 'white'
        button_menu_background = "white"
        button_menu_text = "black"
        button_default_background = "#E5E5E5"
        button_default_text = "black"
        button_category_background = "white"
        button_category_background_selected = 'grey90'
        button_category_text = "black"
        button_category_text_selected = "black"
        button_subcategory_background = "white"
        button_subcategory_background_selected = "grey90"
        button_subcategory_text = "black"
        button_subcategory_text_selected = "black"
        button_subcategory_background_separator = "grey90"
        button_subcategory_text_separator = "black"
        listbox_text_colour = "black"
        listbox_background_colour = "white"
        listbox_text_selected_colour = "black"
        listbox_background_selected_colour = "grey90"
        statusbar.set("Light Mode selected")

    elif theme_option == 'user':
        selected_theme = 'user'
        root_colour = "white"
        text_colour = "black"
        frame_menu_colour = "grey90"
        frame_categories_colour = "grey90"
        frame_subcategories_colour = "grey90"
        frame_listbox_and_text_colour = "grey90"
        frame_text_colour = 'white'
        button_menu_background = "white"
        button_menu_text = "black"
        button_default_background = "#E5E5E5"
        button_default_text = "black"
        button_subcategory_background_separator = "grey90"
        button_subcategory_text_separator = "black"
        listbox_text_colour = "black"
        listbox_background_colour = "white"
        listbox_text_selected_colour = "black"
        listbox_background_selected_colour = "grey90"
        statusbar.set("User Mode selected")

    else:
        if theme_option is not None:
            selected_theme = 'select'
            root_colour = "white"
            text_colour = "black"
            frame_menu_colour = "white"
            frame_categories_colour = "white"
            frame_subcategories_colour = "white"
            frame_listbox_and_text_colour = "white"
            frame_text_colour = 'white'
            button_menu_background = "white"
            button_menu_text = theme_option
            button_default_background = "#ffffff"
            button_default_text = theme_option
            button_category_background = theme_option
            button_category_background_selected = 'white'
            button_category_text = "white"
            button_category_text_selected = theme_option
            button_subcategory_background = theme_option
            button_subcategory_background_selected = "white"
            button_subcategory_text = "white"
            button_subcategory_text_selected = theme_option
            button_subcategory_background_separator = "white"
            button_subcategory_text_separator = theme_option
            listbox_text_colour = theme_option
            listbox_background_colour = "white"
            listbox_text_selected_colour = "white"
            listbox_background_selected_colour = theme_option
            statusbar.set("Single Choice Colour Mode selected")

    for each_widget in root.winfo_children():
        each_widget.destroy()

    root.config(bg=root_colour)
    font_list_notes = font.Font(family=selected_notes_font_name, size=selected_notes_font_size)
    root.geometry(f"{window_width}x{window_height}+{window_position_x}+{window_position_y}")

    start()

def start():
    MenuMain(root)
    FrameCategories(root)
    BottomFrame(root)

########################################################################################################################
########################################################################################################################
####################################################               #####################################################
####################################################    M E N U    #####################################################
####################################################               #####################################################
########################################################################################################################
########################################################################################################################

class MenuMain(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.config(background="white")
        self.grid(row=0, column=0, sticky='EW')

        button_categories = ButtonIcon(self, command=lambda: start(), pic="category.png", text="  C A T E G O R I E S", pic_px=main_menu_icon_size)
        button_categories.grid(row=0, column=0, sticky="NEWS", pady=5, padx=main_menu_padding)
        button_categories.bind("<Enter>", lambda event: statusbar.set("CATEGORIES"))
        button_categories.bind("<Leave>", lambda event: statusbar.set(""))

        button_settings = ButtonIcon(self, command=lambda: FrameSettings(root), text="  S E T T I N G S", pic="settings.png", pic_px=main_menu_icon_size)
        button_settings.grid(row=0, column=1, sticky="EW", pady=5, padx=main_menu_padding)
        button_settings.bind("<Enter>", lambda event: statusbar.set("SETTINGS"))
        button_settings.bind("<Leave>", lambda event: statusbar.set(""))

        ttk.Separator(self, orient='vertical').grid(row=0, column=10, sticky="NS", pady=5, padx=main_menu_padding)

        ButtonIcon(self, command=lambda: database.table_settings_update_colour_modes('white'), pic="light.png", pic_px=main_menu_icon_size).grid(row=0, column=20, sticky="EW", pady=5, padx=main_menu_padding)
        ButtonIcon(self, command=lambda: database.table_settings_update_colour_modes('dark'), pic="dark.png", pic_px=main_menu_icon_size).grid(row=0, column=21, sticky="EW", pady=5, padx=main_menu_padding)
        ButtonIcon(self, command=lambda: database.table_settings_update_colour_modes('light'), pic="nature.png", pic_px=main_menu_icon_size).grid(row=0, column=22, sticky="EW", pady=5, padx=main_menu_padding)
        ButtonIcon(self, command=lambda: database.table_settings_update_colour_modes(colorchooser.askcolor()[1]), pic="colour.png", pic_px=main_menu_icon_size).grid(row=0, column=23, sticky="EW", pady=5, padx=main_menu_padding)
        ButtonIcon(self, command=lambda: database.table_settings_update_colour_modes('user'), pic="user.png", pic_px=main_menu_icon_size).grid(row=0, column=24, sticky="EW", pady=5, padx=main_menu_padding)

        for i, each_button in enumerate(self.winfo_children()):
            if str(type(each_button)) == "<class '__main__.ButtonIcon'>" or str(type(each_button)) == "<class 'tkinter.Button'>":
                each_button.config(bg="white", fg="white", text='', activebackground="white")

########################################################################################################################
########################################################################################################################
##############################################                           ###############################################
##############################################    C A T E G O R I E S    ###############################################
##############################################                           ###############################################
########################################################################################################################
########################################################################################################################

class FrameCategories(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.config(bg=frame_categories_colour)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.grid(row=1, column=0, sticky="NEWS")

        ################################################################################################################
        #######################    F R A M E    W I T H    C A T E G O R Y    B U T T O N S    #########################
        ################################################################################################################

        self.button_frame = tk.Frame(self, bg=frame_categories_colour)
        self.button_frame.grid(row=0, column=0, sticky="NEWS")
        self.button_frame.rowconfigure(1, minsize=0, weight=1)

        self.list_of_buttons = []
        mydb = database.get_db()
        cursor = mydb.cursor()
        if database_type == 'mysql':
            cursor.execute(f"SELECT * FROM categories ORDER BY db_category_name")
        elif database_type == 'sqlite':
            cursor.execute(f"SELECT *, rowid FROM categories ORDER BY db_category_name COLLATE NOCASE")
        for row in cursor.fetchall():
            self.list_of_buttons.append(row)
        if not self.list_of_buttons:
            self.list_of_buttons = [[]]
        cursor.close()
        mydb.close()

        '''Get list of buttons with all data from the database
        print(f"CATEGORIES\nList of categories: {self.list_of_buttons[0]} ... and so on ...")
        print(f"Automaticely selected category button: {self.list_of_buttons[0]}")'''

        '''Format frame and create buttons for each category entry'''
        for i, each_entry in enumerate(self.list_of_buttons, 0):
            self.button_frame.columnconfigure(i, weight=1)
            self.create_buttons(i, each_entry)

        ################################################################################################################
        #############################################    MAIN APP FRAME    #############################################
        ################################################################################################################

        self.frame_display = tk.Frame(self, bg=frame_categories_colour)
        self.frame_display.grid(row=1, column=0, sticky="NEWS")
        self.frame_display.columnconfigure(0, weight=1)
        self.frame_display.rowconfigure(0, weight=1)

        ################################################################################################################
        ############    A U T O    S H O W    F I R S T    C A T E G O R Y    O N    A P P    S T A R T    #############
        ################################################################################################################

        self.update_category(self.button_frame.winfo_children()[0], self.list_of_buttons[0])

    ####################################################################################################################
    ########################    C R E A T E    C A T E G O R Y    P A N E L    B U T T O N S    ########################
    ####################################################################################################################

    def create_buttons(self, i, each_entry):
        b = tk.Button(self.button_frame, text=str(each_entry[0]).upper(), command=lambda: self.update_category(b, each_entry))

        b.grid(row=0, column=i, sticky="NEW", padx=1, pady=(2, 2))
        if selected_theme != 'user':
            b.config(bg=button_category_background,
                     fg=button_category_text,
                     bd=1,
                     font=("Calilbri", 9, 'bold'),
                     relief='sunken',
                     height=1,
                     activebackground=button_category_background_selected,
                     activeforeground=button_category_text_selected)
        else:
            b.config(bd=1,
                     font=("Calilbri", 9, 'bold'),
                     relief='sunken',
                     height=1,
                     bg=each_entry[2],
                     fg='white',
                     activebackground=each_entry[2],
                     activeforeground='white')

    ####################################################################################################################
    ####################    CHANGE BUTTON AND FRAME STYLE DEPENDING ON THEME AND BUTTON PRESSED    #####################
    ####################################################################################################################

    def update_category(self, widget, each_entry):
        if selected_theme != 'user':
            for each_button in self.button_frame.winfo_children():
                each_button.config(bg=button_category_background, fg=button_category_text)
            self.button_frame.config(bg=frame_categories_colour)
            widget.config(bg=button_category_background_selected, fg=button_category_text_selected)
            FrameSubCategories(self.frame_display, each_entry)
        else:
            self.button_frame.config(bg='white')
            FrameSubCategories(self.frame_display, each_entry)

########################################################################################################################
########################################################################################################################
###########################################                                 ############################################
###########################################    S U B C A T E G O R I E S    ############################################
###########################################                                 ############################################
########################################################################################################################
########################################################################################################################

class FrameSubCategories(tk.Frame):
    def __init__(self, container, category_data, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        root.bind("<Control-n>", lambda event: self.add_note())

        self.category_data = category_data

        self.image_show_original = Image.open(f"{pictures_path}buttons_show.png")
        self.image_show_original.thumbnail((15, 15)) # note_menu_icon_size
        self.image_show = ImageTk.PhotoImage(self.image_show_original)

        self.image_hide_original = Image.open(f"{pictures_path}buttons_hide.png")
        self.image_hide_original.thumbnail((15, 15))
        self.image_hide = ImageTk.PhotoImage(self.image_hide_original)

        '''category_data - selected category data passed down to subcategory
        print(f"\nSUBCATEGORY\nCategory data given to subcategory ---------- {category_data}")'''

        self.config(bg=frame_subcategories_colour)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self.grid(row=0, column=0, sticky="NEWS")

        #####################################    FRAME WITH SUBCATEGORY BUTTONS    #####################################
        self.button_frame = tk.Frame(self, bg=frame_subcategories_colour)
        self.button_frame.grid(row=0, column=0, sticky="NEWS")
        self.button_frame.rowconfigure(0, minsize=0, weight=1)

        '''Fetch list of subcategories belonging to selected category from subcategories table,
        category_data[-1] is the category ID subcategories refer to'''

        mydb = database.get_db()
        if database_type == 'mysql':
            get_by_id_command = f"SELECT * FROM subcategories WHERE db_subcategory_id_category=%s ORDER BY db_subcategory_name"
        elif database_type == 'sqlite':
            get_by_id_command = f"SELECT *, rowid FROM subcategories WHERE db_subcategory_id_category=? ORDER BY db_subcategory_name COLLATE NOCASE"
        get_by_id_value = (category_data[-1], )
        cursor = mydb.cursor()
        cursor.execute(get_by_id_command, get_by_id_value)

        self.list_of_subbuttons = []
        for row in cursor.fetchall():
            self.list_of_subbuttons.append(row)
        cursor.close()
        mydb.close()

        ''' self.list_of_subbutons contains all subcategories belonging to the selected category
                self.list_of_subbuttons[0] is used to auto select and display the first subcategory
        print(f"This is the first subcategory to populate first list of notes {self.list_of_subbuttons[0]}")'''

        ################################################################################################################
        ####################    MAIN FRAME TO DISPLAY LISTBOX ON THE LEFT AND TEXT ON THE RIGHT    #####################
        ################################################################################################################
        self.frame_list_and_note = tk.Frame(self, bg=listbox_background_colour) # frame_listbox_and_text_colour
        self.frame_list_and_note.grid(row=2, column=0, sticky="NEWS")
        self.frame_list_and_note.columnconfigure(1, weight=1)
        self.frame_list_and_note.rowconfigure(0, weight=1)
        ################################################################################################################

        ################################################################################################################
        #####################    L E F T    P A N E L    -    S C R O L L A B L E    F R A M E    ######################
        ################################################################################################################

        #####################    SCROLLABLE FRAME TO DISPLAY LIST OF NOTES AS CLICKABLE LABELS    ######################
        self.scrollable_canvas = ScrollableFrame(self.frame_list_and_note)
        self.scrollable_canvas.grid(row=0, column=0, sticky="NEWS")
        self.scrollable_canvas.columnconfigure(0, weight=1)
        self.scrollable_canvas.rowconfigure(0, weight=1)
        self.scroll = self.scrollable_canvas.frame_to_scroll
        self.scrollable_canvas.canvas.config(bg=listbox_background_colour, highlightthickness=0)
        self.scroll.config(bg=listbox_background_colour)

        '''As the scrollable frame doesn't allow for sticky='news' to work, this frame (self.frame_in_px) has a set
        width which forces all notes buttons inside it to cover full width of the SCROLL frame'''
        self.frame_in_px = tk.Frame(self.scroll, bg=listbox_background_colour)
        self.frame_in_px.grid(row=0, column=0, sticky="news")
        self.frame_in_px.columnconfigure(0, minsize=300, weight=1)
        self.frame_in_px.rowconfigure(0, weight=1)
        ################################################################################################################

        ################################################################################################################
        #############    L E F T    P A N E L    -    H I D E    N O T E S    A N D    A D D    N E W    ###############
        ################################################################################################################

        self.manage_notes_frame = tk.Frame(self.frame_list_and_note, bg=frame_menu_colour)
        self.manage_notes_frame.grid(row=1, column=0, sticky="NEWS")
        self.manage_notes_frame.columnconfigure((2, 3, 4, 5), weight=1)
        self.manage_notes_frame.rowconfigure(0, weight=1)

        self.button_hide_show = ButtonIcon(self.manage_notes_frame, pic="arrow.png", pic_px=note_menu_icon_size, command=lambda: self.hide_show('hide'))
        self.button_hide_show.grid(row=0, column=0, sticky="W", padx=(5, 0), pady=1)
        self.button_hide_show.bind("<Enter>", lambda event: statusbar.set("HIDE / SHOW PANEL"))
        self.button_hide_show.bind("<Leave>", lambda event: statusbar.set(""))

        ttk.Separator(self.manage_notes_frame, orient="vertical").grid(row=0, column=1, sticky="NSW", padx=note_menu_padding, pady=0)

        self.button_add_new = ButtonIcon(self.manage_notes_frame, pic="add.png", pic_px=note_menu_icon_size, command=lambda: self.add_note())
        self.button_add_new.grid(row=0, column=2, sticky="NEWS", padx=10, pady=1)
        self.button_add_new.bind("<Enter>", lambda event: statusbar.set("ADD NEW NOTE"))
        self.button_add_new.bind("<Leave>", lambda event: statusbar.set(""))

        self.button_save = ButtonIcon(self.manage_notes_frame, pic="backup.png", pic_px=note_menu_icon_size)
        self.button_save.grid(row=0, column=3, sticky="NEWS", padx=note_menu_padding, pady=1)
        self.button_save.bind("<Enter>", lambda event: statusbar.set("Save changes to database"))
        self.button_save.bind("<Leave>", lambda event: statusbar.set(""))
        self.button_save.config(width=50, bd=1)

        self.button_delete = ButtonIcon(self.manage_notes_frame, pic="delete.png", pic_px=note_menu_icon_size)
        self.button_delete.grid(row=0, column=4, sticky="NEWS", padx=note_menu_padding, pady=1)
        self.button_delete.bind("<Enter>", lambda event: statusbar.set("Delete this note"))
        self.button_delete.bind("<Leave>", lambda event: statusbar.set(""))

        self.button_archive = ButtonIcon(self.manage_notes_frame, pic="archived.png", pic_px=note_menu_icon_size)
        self.button_archive.grid(row=0, column=5, sticky="NEWS", padx=note_menu_padding, pady=1)
        self.button_archive.bind("<Enter>", lambda event: statusbar.set("Show statistics"))
        self.button_archive.bind("<Leave>", lambda event: statusbar.set(""))

        ttk.Separator(self.manage_notes_frame, orient="vertical").grid(row=0, column=6, sticky="NSE", padx=(10, 0))

        self.button_hide_show_buttons = tk.Button(self.manage_notes_frame,
                                                  image=self.image_hide,
                                                  command=lambda: self.show_hide_buttons('hide'),
                                                  bg=button_default_background,
                                                  foreground=button_default_text,
                                                  compound="left",
                                                  bd=0,
                                                  relief="flat",
                                                  borderwidth=0,
                                                  activebackground=button_default_background,
                                                  width=20,
                                                  font=("Calibri", 9))
        self.button_hide_show_buttons.grid(row=0, column=7, sticky="NSE", padx=0, pady=1)
        self.button_hide_show_buttons.bind("<Enter>", lambda event: statusbar.set("Show/Hide buttons bar"))
        self.button_hide_show_buttons.bind("<Leave>", lambda event: statusbar.set(""))

        ################################################################################################################
        ###########################    R I G H T    P A N E L    -    MENU BUTTONS AND TEXT    #########################
        ################################################################################################################
        self.frame_details = tk.Frame(self.frame_list_and_note, bg=frame_listbox_and_text_colour)
        self.frame_details.grid(row=0, column=1, sticky="NEWS")
        self.frame_details.columnconfigure(0, weight=1)
        self.frame_details.rowconfigure(2, weight=1)

        self.frame_details.grid_forget()

        ################################################################################################################
        ############################################    Frame - Note Title   ###########################################
        ################################################################################################################

        '''Use the Notes Clickable Labels Font and make it twice the size'''
        self.title_font = font.Font(family=font_list_notes['family'], size=int(font_list_notes['size'])*2)

        self.entry_title = tk.Entry(self.frame_details, bg=frame_text_colour, fg=text_colour, font=self.title_font, bd=5, relief='flat')
        self.entry_title.grid(row=0, column=0, sticky="EW", columnspan=2)
        self.entry_title.bind("<KeyRelease>", lambda event: self.check_note_for_changes())

        ttk.Separator(self.frame_details).grid(row=1, column=0, sticky="EW")

        ######################################    NOTE TEXT WITH SCROLLBAR    ##########################################

        self.notes_text = tk.Text(self.frame_details, bd=5, bg=frame_text_colour, fg=text_colour, relief='flat', undo=True)
        self.notes_text.grid(row=2, column=0, sticky="NEWS")
        self.notes_text.bind("<KeyRelease>", lambda event: self.check_note_for_changes())

        self.text_scrollbar = ttk.Scrollbar(self.frame_details, orient="vertical")
        self.text_scrollbar.grid(row=2, column=1, sticky="NS")

        self.text_scrollbar.config(command=self.notes_text.yview)
        self.notes_text["yscrollcommand"] = self.text_scrollbar.set

        '''NoteText class is located inside self.frame_details and the grid is .grid(row=0, column=0, sticky="NEWS")
        It is called from self.note_selected() method.'''

        ################################################################################################################
        ###################################    Frame - Buttons Bar at the bottom    ####################################
        ################################################################################################################

        self.frame_buttons_cover = tk.Frame(self.frame_list_and_note, bg=frame_text_colour)
        self.frame_buttons_cover.grid(row=1, column=1, sticky="NEWS")
        self.frame_buttons_cover.columnconfigure(29, weight=1)

        self.frame_buttons = tk.Frame(self.frame_list_and_note, bg=frame_menu_colour)
        self.frame_buttons.grid(row=1, column=1, sticky="NEWS")
        self.frame_buttons.columnconfigure(29, weight=1)

        self.button_undo = ButtonIcon(self.frame_buttons, pic="undo.png", pic_px=note_menu_icon_size)
        self.button_undo.grid(row=0, column=1, sticky="NSW", padx=note_menu_padding, pady=1)
        self.button_undo.bind("<Enter>", lambda event: statusbar.set("Undo"))
        self.button_undo.bind("<Leave>", lambda event: statusbar.set(""))

        self.button_redo = ButtonIcon(self.frame_buttons, pic="redo.png", pic_px=note_menu_icon_size)
        self.button_redo.grid(row=0, column=2, sticky="NSW", padx=note_menu_padding, pady=1)
        self.button_redo.bind("<Enter>", lambda event: statusbar.set("Redo"))
        self.button_redo.bind("<Leave>", lambda event: statusbar.set(""))

        option_fonts = []
        for each_font in font.families():
            option_fonts.append(each_font)
        option_fonts.sort()

        # option_fonts = font.families()
        self.selected_font = tk.StringVar()
        self.font_combobox = ttk.Combobox(self.frame_buttons, textvariable=self.selected_font, values=option_fonts, state="readonly")
        self.font_combobox.grid(row=0, column=3, sticky="NSW", padx=note_menu_padding, pady=1)

        self.button_font_more = ButtonIcon(self.frame_buttons, pic="font+.png", pic_px=note_menu_icon_size)
        self.button_font_more.grid(row=0, column=4, sticky="NSW", padx=note_menu_padding, pady=1)
        self.button_font_more.bind("<Enter>", lambda event: statusbar.set("Font larger"))
        self.button_font_more.bind("<Leave>", lambda event: statusbar.set(""))

        self.button_font_less = ButtonIcon(self.frame_buttons, pic="font-.png", pic_px=note_menu_icon_size)
        self.button_font_less.grid(row=0, column=5, sticky="NSW", padx=note_menu_padding, pady=1)
        self.button_font_less.bind("<Enter>", lambda event: statusbar.set("Font smaller"))
        self.button_font_less.bind("<Leave>", lambda event: statusbar.set(""))

        self.button_bold = ButtonIcon(self.frame_buttons, pic="tbold.png", pic_px=note_menu_icon_size)
        self.button_bold.grid(row=0, column=6, sticky="NSW", padx=note_menu_padding, pady=1)
        self.button_bold.bind("<Enter>", lambda event: statusbar.set("Bold"))
        self.button_bold.bind("<Leave>", lambda event: statusbar.set(""))

        self.button_italic = ButtonIcon(self.frame_buttons, pic="titalic.png", pic_px=note_menu_icon_size)
        self.button_italic.grid(row=0, column=7, sticky="NSW", padx=note_menu_padding, pady=1)
        self.button_italic.bind("<Enter>", lambda event: statusbar.set("Italic"))
        self.button_italic.bind("<Leave>", lambda event: statusbar.set(""))

        self.button_colour = ButtonIcon(self.frame_buttons, pic="colour.png", pic_px=note_menu_icon_size)
        self.button_colour.grid(row=0, column=8, sticky="NSW", padx=note_menu_padding, pady=1)
        self.button_colour.bind("<Enter>", lambda event: statusbar.set("Font colour"))
        self.button_colour.bind("<Leave>", lambda event: statusbar.set(""))

        ttk.Separator(self.frame_buttons, orient="vertical").grid(row=0, column=9, sticky="NSW", padx=note_menu_padding, pady=1)

        self.button_aleft = ButtonIcon(self.frame_buttons, pic="aleft.png", pic_px=note_menu_icon_size)
        self.button_aleft.grid(row=0, column=10, sticky="NSW", padx=note_menu_padding, pady=1)
        self.button_aleft.bind("<Enter>", lambda event: statusbar.set("Justify left"))
        self.button_aleft.bind("<Leave>", lambda event: statusbar.set(""))

        self.button_acenter = ButtonIcon(self.frame_buttons, pic="acenter.png", pic_px=note_menu_icon_size)
        self.button_acenter.grid(row=0, column=11, sticky="NSW", padx=note_menu_padding, pady=1)
        self.button_acenter.bind("<Enter>", lambda event: statusbar.set("Justify center"))
        self.button_acenter.bind("<Leave>", lambda event: statusbar.set(""))

        self.button_aright = ButtonIcon(self.frame_buttons, pic="aright.png", pic_px=note_menu_icon_size)
        self.button_aright.grid(row=0, column=12, sticky="NSW", padx=note_menu_padding, pady=1)
        self.button_aright.bind("<Enter>", lambda event: statusbar.set("Justify right"))
        self.button_aright.bind("<Leave>", lambda event: statusbar.set(""))

        ttk.Separator(self.frame_buttons, orient="vertical").grid(row=0, column=13, sticky="NSW", padx=note_menu_padding, pady=1)

        self.button_print = ButtonIcon(self.frame_buttons, pic="print.png", pic_px=note_menu_icon_size)
        self.button_print.grid(row=0, column=14, sticky="NSW", padx=note_menu_padding, pady=1)
        self.button_print.bind("<Enter>", lambda event: statusbar.set("Print note"))
        self.button_print.bind("<Leave>", lambda event: statusbar.set(""))

        self.button_export_drive = ButtonIcon(self.frame_buttons, pic="drive.png", pic_px=note_menu_icon_size)
        self.button_export_drive.grid(row=0, column=15, sticky="NSW", padx=note_menu_padding, pady=1)
        self.button_export_drive.bind("<Enter>", lambda event: statusbar.set("Export note to Google Drive"))
        self.button_export_drive.bind("<Leave>", lambda event: statusbar.set(""))

        self.button_export_word = ButtonIcon(self.frame_buttons, pic="word.png", pic_px=note_menu_icon_size)
        self.button_export_word.grid(row=0, column=16, sticky="NSW", padx=note_menu_padding, pady=1)
        self.button_export_word.bind("<Enter>", lambda event: statusbar.set("Export as Word file"))
        self.button_export_word.bind("<Leave>", lambda event: statusbar.set(""))

        self.button_send_email = ButtonIcon(self.frame_buttons, pic="email.png", pic_px=note_menu_icon_size)
        self.button_send_email.grid(row=0, column=17, sticky="NSW", padx=note_menu_padding, pady=1)
        self.button_send_email.bind("<Enter>", lambda event: statusbar.set("Email note"))
        self.button_send_email.bind("<Leave>", lambda event: statusbar.set(""))

        ttk.Separator(self.frame_buttons, orient="vertical").grid(row=0, column=18, sticky="NSW", padx=note_menu_padding, pady=1)

        self.button_timestamp = ButtonIcon(self.frame_buttons, pic="time.png", pic_px=note_menu_icon_size)
        self.button_timestamp.grid(row=0, column=19, sticky="NSW", padx=note_menu_padding, pady=1)
        self.button_timestamp.bind("<Enter>", lambda event: statusbar.set("Timestamp"))
        self.button_timestamp.bind("<Leave>", lambda event: statusbar.set(""))

        self.button_emoji = ButtonIcon(self.frame_buttons, pic="emoji.png", pic_px=note_menu_icon_size)
        self.button_emoji.grid(row=0, column=20, sticky="NSW", padx=note_menu_padding, pady=1)
        self.button_emoji.bind("<Enter>", lambda event: statusbar.set("Emoji"))
        self.button_emoji.bind("<Leave>", lambda event: statusbar.set(""))

        self.button_time_difference = ButtonIcon(self.frame_buttons, pic="hourglass.png", pic_px=note_menu_icon_size)
        self.button_time_difference.grid(row=0, column=21, sticky="NSW", padx=note_menu_padding, pady=1)
        self.button_time_difference.bind("<Enter>", lambda event: statusbar.set("Time Difference"))
        self.button_time_difference.bind("<Leave>", lambda event: statusbar.set(""))

        self.button_divider = ButtonIcon(self.frame_buttons, pic="line.png", pic_px=note_menu_icon_size)
        self.button_divider.grid(row=0, column=22, sticky="NSW", padx=note_menu_padding, pady=1)
        self.button_divider.bind("<Enter>", lambda event: statusbar.set("Divider"))
        self.button_divider.bind("<Leave>", lambda event: statusbar.set(""))

        self.search_entry = tk.Entry(self.frame_buttons)
        self.search_entry.grid(row=0, column=31, sticky="NSE", pady=(1, 2))

        self.button_search_text = ButtonIcon(self.frame_buttons, pic="searchtext.png", pic_px=note_menu_icon_size, text="  Search")
        self.button_search_text.grid(row=0, column=32, sticky="NSW", padx=note_menu_padding, pady=1)
        self.button_search_text.config(width=100)

        for i, each_entry in enumerate(self.list_of_subbuttons, 0): # 1
            self.button_frame.columnconfigure(i, weight=1)
            self.create_buttons(i, each_entry)

        ################################################################################################################
        ################################################################################################################
        ###############################    R U N    M E T H O D S    O N    S T A R T    ###############################
        ################################################################################################################
        ################################################################################################################

        ################################################################################################################
        #####    A U T O    S H O W    F I R S T    S U B C A T E G O R Y    O N    C A T E G O R Y    O P E N    ######
        ################################################################################################################
        self.update_subcategory(self.button_frame.winfo_children()[0], self.list_of_subbuttons[0])

        ################################################################################################################
        #####    A U T O    S E T    P A N E L    V I S I B I L I T Y    D E P E N D I N G    O N    G L O B A L    ####
        ################################################################################################################

        self.update_buttons(self.frame_in_px.winfo_children()[0])
        self.hide_show(notes_panel_visible)


    ####################################################################################################################
    #####################    C R E A T E    S U B C A T E G O R Y    P A N E L    B U T T O N S    #####################
    ####################################################################################################################
    def create_buttons(self, i, each_entry):
        button = tk.Button(self.button_frame, text=str(each_entry[0]).upper(), command=lambda: self.update_subcategory(button, each_entry))
        button.grid(row=0, column=i, sticky="NEW", padx=1, pady=(0, 2))

        if selected_theme != 'user':
            button.config(bg=button_subcategory_background,
                          fg=button_subcategory_text,
                          bd=1,
                          font=("Calibri", 8),
                          relief='sunken',
                          height=1,
                          activebackground=button_subcategory_background_selected,
                          activeforeground=button_subcategory_text_selected)
        else:
            button.config(bg=self.category_data[2],
                          fg='white',
                          bd=1,
                          font=("Calibri", 8),
                          relief='sunken',
                          highlightcolor=self.category_data[2],
                          height=1,
                          activebackground='white',
                          activeforeground=self.category_data[2])

    ####################################################################################################################
    ####################    CHANGE BUTTON AND FRAME STYLE DEPENDING ON THEME AND BUTTON PRESSED    #####################
    ####################################################################################################################

    def update_subcategory(self, button, subcategory_data):
        self.subcategory_data_currently_selected = subcategory_data
        if selected_theme != 'user':
            for each_button in self.button_frame.winfo_children():
                each_button.config(bg=button_subcategory_background, fg=button_subcategory_text)
            self.button_frame.config(bg=frame_subcategories_colour)
            button.config(bg=button_subcategory_background_selected, fg=button_subcategory_text_selected)
        else:
            for each_button in self.button_frame.winfo_children():
                each_button.config(bg=self.category_data[2], fg='white')
            self.button_frame.config(bg='white')
            button.config(bg='white', fg=self.category_data[2])

        ################################    RUN NOTES_BUTTONS METHOD ON BUTTON PRESS    ################################
        self.notes_buttons(subcategory_data)

    ####################################################################################################################
    #########################    SHOW / HIDE / AUTO-HIDE PANEL DEPENDING ON GLOBAL SETTINGS    #########################
    ####################################################################################################################
    '''This method is run automaticaly with FrameSubCategories class'''

    def hide_show(self, option):
        if option == 'hide':
            self.frame_details.grid(row=0, column=0, columnspan=2, sticky="NEWS")
            self.frame_details.tkraise()
            self.button_hide_show.config(command=lambda: self.hide_show('show'))
        elif option == 'show':
            self.frame_details.grid(row=0, column=1, columnspan=1, sticky="NEWS")
            # self.frame_notes.tkraise()
            self.button_hide_show.config(command=lambda: self.hide_show('hide'))
        elif option == 'auto_hide':
            self.after(2000, self.auto_hide)

    def auto_hide(self):
        self.frame_details.grid(row=0, column=0, columnspan=2, sticky="NEWS")
        self.frame_details.tkraise()
        self.button_hide_show.config(command=lambda: self.hide_show('show'))

    def show_hide_buttons(self, option):
        if option == 'show':
            self.button_hide_show_buttons.config(image=self.image_hide, command=lambda: self.show_hide_buttons('hide'))
            self.frame_buttons.tkraise()
        elif option == 'hide':
            self.button_hide_show_buttons.config(image=self.image_show, command=lambda: self.show_hide_buttons('show'))
            self.frame_buttons_cover.tkraise()

    ####################################################################################################################
    ###########################    FETCH LIST OF NOTES AND START CREATING CLICKABLE LABELS    ##########################
    ####################################################################################################################

    def notes_buttons(self, selected_subcategory):
        '''Destroy parent frame content to allow for first clickable label to be auto selected and re-selected'''
        for each_label in self.frame_in_px.winfo_children():
            each_label.destroy()

        selected_subcategory_id = selected_subcategory[-1]

        '''selected_subcategory is a selected subcategory list:
        print(f"\nNOTES BUTTONS\nNotes_buttons function is getting 'selected_subcategory' data ---------- {selected_subcategory}")
        print(f"This selected_subcategory ID is 'selected_subcategory[-1]' ---------- {selected_subcategory_id}")'''

        mydb = database.get_db()
        if database_type == 'mysql':
            get_by_id_command = f"SELECT db_note_name, db_note_id FROM notes WHERE db_note_id_subcategory=%s ORDER BY db_note_name"
        elif database_type == 'sqlite':
            get_by_id_command = f"SELECT db_note_name, rowid FROM notes WHERE db_note_id_subcategory=? ORDER BY db_note_name COLLATE NOCASE"
        get_by_id_value = (selected_subcategory_id, )
        cursor = mydb.cursor()
        cursor.execute(get_by_id_command, get_by_id_value)
        self.list_of_notes_with_id = []
        for row in cursor.fetchall():
            self.list_of_notes_with_id.append(row)
        cursor.close()
        mydb.close()

        '''Get only each note name and id instead of the entire note data. This data is used only to display notes names
        in clicklable labels and the ID is used to reference each label in database if/when clicked
        print(f"Use ID {selected_subcategory_id} to get list of note_name + note_id as reference:
         {self.list_of_notes_with_id}")'''

        '''Run create_note_buttons method and start creating clickable labels for each note belonging to this subcat'''
        for e, each_button in enumerate(self.list_of_notes_with_id):
            self.create_note_buttons(e, each_button)

        '''Automaticaly run note_selected method with the first note in all notes list. This way the first note will
        be auto selected and display it's content in the NotesText class'''
        self.note_selected(self.list_of_notes_with_id[0], self.frame_in_px.winfo_children()[0])

        '''Automaticaly update first note button selected on clicking on Subcategory Button'''
        self.update_buttons(self.frame_in_px.winfo_children()[0])

    ####################################################################################################################
    ##################    C R E A T E    N O T E S    P A N E L    C L I C K A B L E    L A B E L S    #################
    ####################################################################################################################

    def create_note_buttons(self, e, note_data):
        note_button = tk.Label(self.frame_in_px,
                               text=note_data[0],
                               font=font_list_notes,
                               bd=5,
                               foreground=listbox_text_colour,
                               bg=listbox_background_colour, anchor='w')
        note_button.grid(row=e, column=0, sticky="EW")
        note_button.bind("<Button-1>", lambda event: [self.note_selected(note_data, note_button), self.update_buttons(note_button)])

    ####################################################################################################################
    ##############################    UPDATE BUTTONS STYLE DEPENDING ON BUTTON PRESSED    ##############################
    ####################################################################################################################

    def update_buttons(self, button_widget):
        if selected_theme != 'user':
            for each_button in self.frame_in_px.winfo_children():
                each_button.config(bg=listbox_background_colour, foreground=listbox_text_colour)
            button_widget.config(bg=listbox_background_selected_colour, foreground=listbox_text_selected_colour)
        else:
            for each_button in self.frame_in_px.winfo_children():
                each_button.config(bg=listbox_background_colour, foreground=self.category_data[2])
            button_widget.config(bg=self.category_data[2], foreground='white')

    ####################################################################################################################
    ############################    FETCH ENTIRE NOTE DATA AND INSERT IN NotesText CLASS    ############################
    ####################################################################################################################

    def note_selected(self, note_data, widget_button):
        self.search_entry.delete(0, 'end')

        current_button = note_data
        selected_id = current_button[-1]

        mydb = database.get_db()
        if database_type == 'mysql':
            get_by_id_command = f"SELECT * FROM notes WHERE db_note_id=%s"
        elif database_type == 'sqlite':
            get_by_id_command = f"SELECT *, rowid FROM notes WHERE rowid=?"
        get_by_id_value = (selected_id, )
        cursor = mydb.cursor()
        cursor.execute(get_by_id_command, get_by_id_value)
        full_note_info = cursor.fetchall()[0]
        cursor.close()
        mydb.close()

        '''Create Note Title'''
        self.entry_title.delete(0, 'end')
        self.entry_title.insert(0, note_data[0])
        self.original_title = note_data[0]

        '''Display note data in NoteText (parent frame: self.frame_details, grid: row=0, column=0, sticky="NEWS"'''

        self.notes_text.delete("1.0", "end")
        self.notes_text.insert("end", full_note_info[1])

        '''Needed for checking if note has been changed'''
        self.original_note = self.notes_text.get("1.0", "end-1c")

        self.button_delete.config(command=lambda: self.delete_note(selected_id))
        self.button_archive.config(command=lambda: self.archive_note(selected_id, full_note_info))
        self.button_undo.config(command=lambda: self.undo_redo('undo'))
        self.button_redo.config(command=lambda: self.undo_redo('redo'))

        '''Read current font from database and set it in combobox'''

        option_fonts = []
        for each_font in font.families():
            option_fonts.append(each_font)
        option_fonts.sort()

        font_index = 0
        for i, font_name in enumerate(option_fonts):
            if font_name == full_note_info[4]:
                font_index = i

        # font_index = 0
        # for i, font_name in enumerate(font.families()):
        #     if font_name == full_note_info[4]:
        #         font_index = i
        self.font_combobox.current(font_index)
        note_font_family = tk.StringVar()
        note_font_size = tk.StringVar()
        note_font_family.set(full_note_info[4])
        note_font_size.set(full_note_info[5])

        '''font.Font of the entire text widget'''
        note_font = font.Font(family=note_font_family.get(), size=note_font_size.get())
        self.font_combobox.bind("<<ComboboxSelected>>", lambda event: self.change_font('name', note_font_size, note_font_family, self.selected_font, note_font))
        self.notes_text.config(font=note_font)

        self.button_font_more.config(command=lambda: self.change_font('large', note_font_size, note_font_family, '', note_font))
        self.button_font_less.config(command=lambda: self.change_font('small', note_font_size, note_font_family, '', note_font))

        ''' Text Bold '''
        note_font_bold = tk.StringVar()
        note_font_bold.set(full_note_info[7])

        if int(note_font_bold.get()) == 1:
            self.button_bold.config(bg="grey50", command=lambda: self.bold_normal("normal", note_font_bold, note_font))
            note_font.config(weight="bold")
            self.notes_text.bind("<Control-b>", lambda event: self.bold_normal("normal", note_font_bold, note_font))
            self.notes_text.bind("<Control-B>", lambda event: self.bold_normal("normal", note_font_bold, note_font))
        else:
            self.button_bold.config(bg=button_default_background, command=lambda: self.bold_normal("bold", note_font_bold, note_font))
            note_font.config(weight="normal")
            self.notes_text.bind("<Control-b>", lambda event: self.bold_normal("bold", note_font_bold, note_font))
            self.notes_text.bind("<Control-B>", lambda event: self.bold_normal("normal", note_font_bold, note_font))

        ''' Text Italic '''
        note_font_italic = tk.StringVar()
        note_font_italic.set(full_note_info[8])

        if int(note_font_italic.get()) == 1:
            self.button_italic.config(bg="grey50", command=lambda: self.italic_roman("roman", note_font_italic, note_font))
            note_font.config(slant="italic")
            self.notes_text.bind("<Control-i>", lambda event: self.italic_roman("roman", note_font_italic, note_font))
            self.notes_text.bind("<Control-I>", lambda event: self.italic_roman("roman", note_font_italic, note_font))
        else:
            self.button_italic.config(bg=button_default_background, command=lambda: self.italic_roman("italic", note_font_italic, note_font))
            note_font.config(slant="roman")
            self.notes_text.bind("<Control-i>", lambda event: self.italic_roman("italic", note_font_italic, note_font))
            self.notes_text.bind("<Control-I>", lambda event: self.italic_roman("roman", note_font_italic, note_font))

        ''' Text Colour '''
        note_font_colour = tk.StringVar()
        note_font_colour.set(full_note_info[6])

        # Set up automaticaly
        self.notes_text.config(foreground=note_font_colour.get())

        # Set up on lick
        self.button_colour.config(command=lambda: [note_font_colour.set(colorchooser.askcolor()[1]), self.notes_text.config(foreground=note_font_colour.get())])

        ''' Text Align '''
        note_font_justify = tk.StringVar()
        note_font_justify.set(full_note_info[9])

        self.notes_text.tag_configure("left", justify="left")
        self.button_aleft.config(command=lambda: self.text_align('left', note_font_justify))
        self.notes_text.bind("<Control-l>", lambda event: self.text_align('left', note_font_justify))
        self.notes_text.bind("<Control-L>", lambda event: self.text_align('left', note_font_justify))

        self.notes_text.tag_configure("center", justify="center")
        self.button_acenter.config(command=lambda: self.text_align('center', note_font_justify))
        self.notes_text.bind("<Control-e>", lambda event: self.text_align('center', note_font_justify))
        self.notes_text.bind("<Control-E>", lambda event: self.text_align('center', note_font_justify))

        self.notes_text.tag_configure("right", justify="right")
        self.button_aright.config(command=lambda: self.text_align('right', note_font_justify))
        self.notes_text.bind("<Control-r>", lambda event: self.text_align('right', note_font_justify))
        self.notes_text.bind("<Control-R>", lambda event: self.text_align('right', note_font_justify))

        if note_font_justify.get() == 'left':
            self.button_aleft.config(bg='grey50')
            self.button_acenter.config(bg=button_default_background)
            self.button_aright.config(bg=button_default_background)
            self.notes_text.tag_add("left", "1.0", "end")
        elif note_font_justify.get() == 'center':
            self.button_aleft.config(bg=button_default_background)
            self.button_acenter.config(bg='grey50')
            self.button_aright.config(bg=button_default_background)
            self.notes_text.tag_add("center", "1.0", "end")
        elif note_font_justify.get() == 'right':
            self.button_aleft.config(bg=button_default_background)
            self.button_acenter.config(bg=button_default_background)
            self.button_aright.config(bg='grey50')
            self.notes_text.tag_add("right", "1.0", "end")

        self.button_print.config(command=lambda: note_print(full_note_info))
        self.button_export_drive.config(command=lambda: note_drive(full_note_info))
        self.button_export_word.config(command=lambda: note_word(full_note_info))
        self.button_send_email.config(command=lambda: note_email(full_note_info))
        self.button_timestamp.config(command=lambda: self.insert_timestamp())
        self.button_divider.config(command=lambda: self.insert_divider())
        self.button_time_difference.config(command=lambda: self.calculate_time_difference())
        self.button_emoji.config(command=lambda: self.insert_emoji())
        self.button_search_text.config(command=lambda: self.search_text(self.search_entry.get()))


        self.search_entry.bind("<Control-f>", lambda event: self.search_text(self.search_entry.get()))
        self.search_entry.bind("<Control-F>", lambda event: self.search_text(self.search_entry.get()))
        self.search_entry.bind("<Return>", lambda event: self.search_text(self.search_entry.get()))

        self.button_save.config(bg=button_default_background, relief='flat', bd=1)
        self.button_save.config(command=lambda: self.save_note(selected_id,
                                                               self.entry_title.get(),
                                                               self.notes_text.get("0.1", "end-1c"),
                                                               widget_button,
                                                               note_font_family.get(),
                                                               note_font_size.get(),
                                                               note_font_colour.get(),
                                                               note_font_bold.get(),
                                                               note_font_italic.get(),
                                                               note_font_justify.get()))

        self.entry_title.bind("<Control-s>", lambda event: self.save_note(selected_id,
                                                               self.entry_title.get(),
                                                               self.notes_text.get("0.1", "end-1c"),
                                                               widget_button,
                                                               note_font_family.get(),
                                                               note_font_size.get(),
                                                               note_font_colour.get(),
                                                               note_font_bold.get(),
                                                               note_font_italic.get(),
                                                               note_font_justify.get()))
        self.notes_text.bind("<Control-s>", lambda event: self.save_note(selected_id,
                                                               self.entry_title.get(),
                                                               self.notes_text.get("0.1", "end-1c"),
                                                               widget_button,
                                                               note_font_family.get(),
                                                               note_font_size.get(),
                                                               note_font_colour.get(),
                                                               note_font_bold.get(),
                                                               note_font_italic.get(),
                                                               note_font_justify.get()))



        '''Get note full data and display it inside NotesText class:
        print(f"\n\nCurrently selected button: {current_button}")
        print(f"Which gives us the Note's ID: {selected_id}")
        print(f"DATABASE RETURNS FULL NOTE DATA: {full_note_info[0]} - NOTE TEXT... {full_note_info[2]} ...\n\n")'''

    def text_align(self, option, align_variable):
        align_variable.set(option)
        for each_tag in self.notes_text.tag_names():
            self.notes_text.tag_remove(each_tag, "1.0", "end")

        if option == 'left':
            self.button_aleft.config(bg='grey50')
            self.button_acenter.config(bg=button_default_background)
            self.button_aright.config(bg=button_default_background)
            self.notes_text.tag_add("left", "1.0", "end")
        elif option == 'center':
            self.button_aleft.config(bg=button_default_background)
            self.button_acenter.config(bg='grey50')
            self.button_aright.config(bg=button_default_background)
            self.notes_text.tag_add("center", "1.0", "end")
        elif option == 'right':
            self.button_aleft.config(bg=button_default_background)
            self.button_acenter.config(bg=button_default_background)
            self.button_aright.config(bg='grey50')
            self.notes_text.tag_add("right", "1.0", "end")


    def bold_normal(self, option, font_bold_variable, font_variable):
        if option == "bold":
            font_bold_variable.set(1)
            font_variable.config(weight="bold")
            self.button_bold.config(bg="grey50", command=lambda: self.bold_normal("normal", font_bold_variable, font_variable))
            self.notes_text.bind("<Control-b>", lambda event: self.bold_normal("normal", font_bold_variable, font_variable))
            self.notes_text.bind("<Control-B>", lambda event: self.bold_normal("normal", font_bold_variable, font_variable))
        elif option == 'normal':
            font_bold_variable.set(0)
            font_variable.config(weight="normal")
            self.button_bold.config(bg=button_default_background, command=lambda: self.bold_normal("bold", font_bold_variable, font_variable))
            self.notes_text.bind("<Control-b>", lambda event: self.bold_normal("bold", font_bold_variable, font_variable))
            self.notes_text.bind("<Control-B>", lambda event: self.bold_normal("normal", font_bold_variable, font_variable))


    def italic_roman(self, option, font_italic_variable, font_variable):
        if option == "italic":
            font_italic_variable.set(1)
            self.button_italic.config(bg="grey50", command=lambda: self.italic_roman("roman", font_italic_variable, font_variable))
            font_variable.config(slant="italic")
            self.notes_text.bind("<Control-i>", lambda event: self.italic_roman("roman", font_italic_variable, font_variable))
            self.notes_text.bind("<Control-I>", lambda event: self.italic_roman("roman", font_italic_variable, font_variable))
        elif option == "roman":
            font_italic_variable.set(0)
            self.button_italic.config(bg=button_default_background, command=lambda: self.italic_roman("italic", font_italic_variable, font_variable))
            font_variable.config(slant="roman")
            self.notes_text.bind("<Control-i>", lambda event: self.italic_roman("italic", font_italic_variable, font_variable))
            self.notes_text.bind("<Control-I>", lambda event: self.italic_roman("roman", font_italic_variable, font_variable))


    def undo_redo(self, option):
        if option == 'undo':
            try:
                self.notes_text.edit_undo()
            except:
                statusbar.set("Nothing to undo")
        elif option == 'redo':
            try:
                self.notes_text.edit_redo()
            except:
                statusbar.set("Nothing to redo")

    def insert_timestamp(self):
        self.notes_text.insert("insert", timestamp())

    def insert_divider(self):
        self.notes_text.insert("insert", f"{'_'*100}\n")

    def insert_emoji(self):
        self.emoji_window = tk.Toplevel(bg='white')
        self.emoji_window.title("Emoji")
        self.emoji_window.geometry(f"{700}x{1000}+{int((root.winfo_screenwidth() / 2) - 350)}+{int((root.winfo_screenheight() / 2) - 500)}")

        counter = 0
        for x in range(17):
            for y in range(10):

                self.create_emoticons(counter, x, y)
                self.emoji_window.rowconfigure(x, weight=1)
                self.emoji_window.columnconfigure(y, weight=1)
                counter += 1

    def create_emoticons(self, emoticon_number, x_position, y_position):
        current_emoji = list_emoji[emoticon_number]
        emoji_button = tk.Label(self.emoji_window, text=current_emoji, font=("Arial", 20), bg='white', fg=f"#{''.join([random.choice('0123456789ABCDEF') for i in range(6)])}", padx=5, pady=5)
        emoji_button.grid(row=x_position, column=y_position, sticky="NEWS")
        emoji_button.bind("<Button-1>", lambda event: [self.notes_text.insert("insert", current_emoji), self.emoji_window.destroy(), root.clipboard_clear(), root.clipboard_append(current_emoji)])

    def calculate_time_difference(self):
        def time_difference():
            try:
                total_time = datetime.datetime.strptime(time_end_entry.get(), '%H:%M') - datetime.datetime.strptime(time_start_entry.get(), '%H:%M')

                # If starting time is later than finishing time, calculate only hours
                if total_time < datetime.timedelta(hours=0):
                    total_time += datetime.timedelta(days=1)

                statusbar.set(f"{time_start_entry.get()} - {time_end_entry.get()}\t⏳\t{total_time}"[:-3])
                root.clipboard_clear()
                root.clipboard_append(f"{total_time}"[:-3])
                self.time_window.destroy()
            except ValueError:
                statusbar.set("Improper format, try again")

        self.time_window = tk.Toplevel(bg='white')
        self.time_window.title("Time")
        self.time_window.columnconfigure((0, 2), weight=1)
        self.time_window.rowconfigure((0, 1), weight=1)

        self.time_window.geometry(f"{300}x{110}+{int((root.winfo_screenwidth() / 2) - 150)}+{int((root.winfo_screenheight() / 2) - 55)}")

        tk.Label(self.time_window, text="Start", bg='white').grid(row=0, column=0, sticky="EW", padx=5, pady=5)
        tk.Label(self.time_window, text="End", bg='white').grid(row=0, column=2, sticky="EW", padx=5, pady=5)

        time_start_entry = ttk.Entry(self.time_window, width=5)
        time_start_entry.grid(row=1, column=0, sticky="EW", padx=5, pady=5)
        time_start_entry.focus()

        tk.Label(self.time_window, text=" - ", bg='white').grid(row=1, column=1, sticky="EW", padx=5, pady=5)

        time_end_entry = ttk.Entry(self.time_window, width=5)
        time_end_entry.grid(row=1, column=2, sticky="EW", padx=5, pady=5)
        time_end_entry.bind("<Return>", lambda event: time_difference())

        tk.Button(self.time_window, text='Calculate', command=lambda: time_difference(), bg='white').grid(row=2, column=0, columnspan=3, sticky="EW", padx=5, pady=5)

    def change_font(self, option, size_variable, family_variable, combobox_variable, font_variable):
        if option == 'large':
            if int(size_variable.get()) < 44:
                size_variable.set(int(size_variable.get()) + 1)
                font_variable.config(size=int(size_variable.get()))
                # print(size_variable.get())
        elif option == 'small':
            if int(size_variable.get()) > 4:
                size_variable.set(int(size_variable.get()) - 1)
                font_variable.config(size=int(size_variable.get()))
                # print(size_variable.get())
        elif option == 'name':
            family_variable.set('%s' % self.selected_font.get())
            font_variable.config(family=combobox_variable.get())


    def dummy(self, text_to_display, widget_button, option):
        colour_to_display = button_default_background[0] + "5" + button_default_background[2:]
        if option == 'on':
            widget_button.config(bg=colour_to_display, command=lambda: self.dummy(text_to_display, widget_button, 'off'))
            statusbar.set(f"{text_to_display}")
        elif option == 'off':
            widget_button.config(bg=button_default_background, command=lambda: self.dummy(text_to_display, widget_button, 'on'))


    def save_note(self, save_id, save_title, save_text, widget_button, f_family, f_size, f_colour, f_b, f_i, f_a):
        button_index = self.frame_in_px.winfo_children().index(widget_button)
        currently_selected_subcategory = self.subcategory_data_currently_selected
        '''print(f"Currently selected subcategory: {currently_selected_subcategory}")'''

        if len(save_title) != 0:
            mydb = database.get_db()
            if database_type == 'mysql':
                update_note_command = f"UPDATE notes SET db_note_name=%s, db_note_text=%s, db_note_font_name=%s, db_note_font_size=%s, db_note_font_colour=%s, db_note_font_bold=%s, db_note_font_italic=%s, db_note_position=%s WHERE db_note_id=%s"
            elif database_type == 'sqlite':
                update_note_command = f"UPDATE notes SET db_note_name=?, db_note_text=?, db_note_font_name=?, db_note_font_size=?, db_note_font_colour=?, db_note_font_bold=?, db_note_font_italic=?, db_note_position=? WHERE rowid=?"
            update_note_value = (save_title, save_text, f_family, f_size, f_colour, f_b, f_i, f_a, save_id)
            cursor = mydb.cursor()
            cursor.execute(update_note_command, update_note_value)
            mydb.commit()
            cursor.close()
            mydb.close()

            '''Recreate list of notes'''
            self.notes_buttons(currently_selected_subcategory)
            '''Get index of the newly created button'''

            for each_widget in self.frame_in_px.winfo_children():
                if each_widget['text'] == save_title:
                    '''Configure buttons styling selecting the newly created note'''
                    new_button_index = self.frame_in_px.winfo_children().index(each_widget)

                    self.note_selected(self.list_of_notes_with_id[new_button_index],
                                       self.frame_in_px.winfo_children()[new_button_index])
                    '''Update styling of all buttons in the lsit'''
                    self.update_buttons(self.frame_in_px.winfo_children()[new_button_index])

            statusbar.set(f"{save_title.capitalize()} has been updated.")
            self.button_save.config(bg=button_default_background, relief='flat', bd=1)
        else:
            statusbar.set("Add title")


    def check_note_for_changes(self):
        if hash(self.notes_text.get("1.0", "end-1c")) != hash(self.original_note) or hash(self.entry_title.get()) != hash(self.original_title):
            self.button_save.config(bg='red', relief='raised', bd=1)

        else:
            self.button_save.config(bg=button_default_background, relief='flat', bd=1)


    def delete_note(self, delete_id):
        if messagebox.askyesno(title=f"Delete note", message="Are you sure you want to delete this note?"):
            if len(self.frame_in_px.winfo_children()) > 1:
                mydb = database.get_db()
                if database_type == 'mysql':

                    delete_item_command = f"DELETE FROM notes WHERE db_note_id=%s"
                elif database_type == 'sqlite':

                    delete_item_command = f"DELETE FROM notes WHERE rowid=?"
                delete_item_id = (delete_id,)
                cursor = mydb.cursor()
                cursor.execute(delete_item_command, delete_item_id)
                mydb.commit()
                cursor.close()
                mydb.close()

                '''Recreate list of notes except the deleted one'''
                currently_selected_subcategory = self.subcategory_data_currently_selected
                self.notes_buttons(currently_selected_subcategory)

                statusbar.set(f"Note deleted")
                self.button_save.config(bg=button_default_background, relief='flat', bd=1)
            else:
                statusbar.set("At least one note has to remain")
        else:
            statusbar.set("Operation cancelled")


    def add_note(self):
        self.popup_add_note = tk.Toplevel(root, bg='white')
        self.popup_add_note.columnconfigure(0, weight=1)
        self.popup_add_note.rowconfigure(0, weight=1)
        self.popup_add_note.geometry("600x50+1200+700")
        self.popup_add_note.title(f"Enter new note title...")
        self.popup_add_note.focus_set()

        entry_note_add = ttk.Entry(self.popup_add_note)
        entry_note_add.grid(row=0, column=0, sticky="EW", padx=5)

        entry_note_add.bind("<Return>", lambda event: self.add_note_save(entry_note_add.get()))
        entry_note_add.focus()

        self.button_category_add = ButtonIcon(self.popup_add_note, text='    Add', command=lambda: self.add_note_save(entry_note_add.get()), pic="add.png", pic_px=20)
        self.button_category_add.grid(row=0, column=2, sticky="W", padx=5)
        self.button_category_add.config(width=150, relief='ridge', bd=1)

    def add_note_save(self, save_note_title):
        currently_selected_subcategory = self.subcategory_data_currently_selected
        subcategory_id = currently_selected_subcategory[-1]
        new_note_title = save_note_title
        new_note_date = datetime.date.today()

        if len(save_note_title) != 0 and save_note_title != "Enter note title...":
            mydb = database.get_db()
            if database_type == 'mysql':
                add_new_note_command = f"INSERT INTO notes (db_note_name, db_note_text, db_note_date, db_note_id_subcategory, db_note_font_name, db_note_font_size, db_note_font_colour, db_note_font_bold, db_note_font_italic, db_note_position) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            elif database_type == 'sqlite':
                add_new_note_command = f"INSERT INTO notes (db_note_name, db_note_text, db_note_date, db_note_id_subcategory, db_note_font_name, db_note_font_size, db_note_font_colour, db_note_font_bold, db_note_font_italic, db_note_position) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

            add_new_note_value = (new_note_title, '', new_note_date, subcategory_id, "Calibri Light", 9, "#000000", 0, 0, 'left')
            cursor = mydb.cursor()
            cursor.execute(add_new_note_command, add_new_note_value)
            mydb.commit()
            cursor.close()
            mydb.close()

            self.popup_add_note.destroy()

            '''Recreate list of notes'''
            self.notes_buttons(currently_selected_subcategory)

            '''Get index of the newly created button'''
            for each_widget in self.frame_in_px.winfo_children():
                if each_widget['text'] == new_note_title:
                    '''Configure buttons styling selecting the newly created note'''
                    new_button_index = self.frame_in_px.winfo_children().index(each_widget)

                    self.note_selected(self.list_of_notes_with_id[new_button_index], self.frame_in_px.winfo_children()[new_button_index])
                    '''Update styling of all buttons in the lsit'''
                    self.update_buttons(self.frame_in_px.winfo_children()[new_button_index])

            self.button_save.config(bg=button_default_background, relief='flat', bd=1)
            statusbar.set(f"{save_note_title} note added")
        else:
            statusbar.set('Add title')

    def archive_note(self, archive_id, note_data):
        if messagebox.askyesno(title=f"Archive note", message="Are you sure you want to archive this note?"):

            if len(self.frame_in_px.winfo_children()) > 1:
                archived_note_title = f"{self.subcategory_data_currently_selected[0]} - {note_data[0]}"
                archived_note_text = note_data[1]

                mydb = database.get_db()
                if database_type == 'mysql':
                    add_archived_command = f"INSERT INTO archived (db_archived_name, db_archived_text) VALUES (%s, %s)"
                    delete_item_command = f"DELETE FROM notes WHERE db_note_id=%s"
                elif database_type == 'sqlite':
                    add_archived_command = f"INSERT INTO archived (db_archived_name, db_archived_text) VALUES (?, ?)"
                    delete_item_command = f"DELETE FROM notes WHERE rowid=?"

                add_archived_value = (archived_note_title, archived_note_text)
                delete_item_id = (archive_id,)

                cursor = mydb.cursor()
                cursor.execute(add_archived_command, add_archived_value)
                mydb.commit()
                cursor.execute(delete_item_command, delete_item_id)
                mydb.commit()
                cursor.close()
                mydb.close()

                '''Restart the subcategory screen'''
                self.notes_buttons(self.list_of_subbuttons[0])

                statusbar.set(f"Note deleted")
                self.button_save.config(bg=button_default_background, relief='flat', bd=1)
            else:
                statusbar.set("At least one note has to remain")
        else:
            statusbar.set("Operation cancelled")

    def search_text(self, text_to_search):
        if len(text_to_search) != 0:
            self.notes_text.tag_configure("selected", background="yellow")
            self.notes_text.tag_remove("selected", "1.0", "end")
            start = 1.0
            found = 0
            while True:
                position = self.notes_text.search(text_to_search, start, stopindex="end")
                if not position:
                    break
                found += 1
                self.notes_text.tag_add("selected", position, position + f"+{str(len(text_to_search))}c")
                start = position + "+1c"
            statusbar.set(f"{found} found")

    def search_in_subcategory(self):
        pass

########################################################################################################################
########################################################################################################################
#######################################                                          #######################################
#######################################    S C R O L L A B L E    C A N V A S    #######################################
#######################################                                          #######################################
########################################################################################################################
########################################################################################################################

class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.config(bg=listbox_background_colour)
        self.canvas = tk.Canvas(self, width=250) # width=250 - to change the width of widget
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.frame_to_scroll = tk.Frame(self.canvas)
        self.frame_to_scroll.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.frame_to_scroll.bind("<Enter>", self.mouse_on)
        self.frame_to_scroll.bind("<Leave>", self.mouse_off)
        self.canvas.create_window((0, 0), window=self.frame_to_scroll, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    def mouse_on(self, event):
        self.canvas.bind_all("<MouseWheel>", self.mouse_use)
    def mouse_off(self, event):
        self.canvas.unbind_all("<MouseWheel>")
    def mouse_use(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

########################################################################################################################
########################################################################################################################
###############################################                         ################################################
###############################################    S T A T U S B A R    ################################################
###############################################                         ################################################
########################################################################################################################
########################################################################################################################

class BottomFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.config(background=root_colour)
        self.grid(row=10, column=0, sticky="EW")
        self.columnconfigure(0, weight=1)

        ttk.Separator(self, orient="horizontal").grid(row=0, column=0, sticky="EW", columnspan=3)
        tk.Label(self, textvariable=statusbar, bg=root_colour, fg=text_colour, font=statusbar_font).grid(row=1, column=0, sticky="EW")
        ttk.Separator(self, orient="vertical").grid(row=1, column=1, sticky="NSE", padx=10)
        self.date_label = tk.Label(self, text=datetime.date.today(), bg=root_colour, fg=text_colour, font=statusbar_font)
        self.date_label.grid(row=1, column=2, sticky="E", padx=(0, 20))
        self.date_label.bind("<Enter>", lambda event: statusbar.set("CLICK ON DATE TO COPY TO CLIPBOARD"))
        self.date_label.bind("<Leave>", lambda event: statusbar.set(""))
        self.date_label.bind("<Button-1>", lambda event: [root.clipboard_clear(), root.clipboard_append(datetime.date.today()), statusbar.set(f"{datetime.date.today()} copied to clipboard")])

########################################################################################################################
########################################################################################################################
################################################                       #################################################
################################################    S E T T I N G S    #################################################
################################################                       #################################################
########################################################################################################################
########################################################################################################################

class FrameSettings(ttk.Notebook):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, **kwargs)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(row=1, column=0, sticky="NEWS")

        ################################################################################################################
        ###################################                 P A N E L                 ##################################
        ###################################    MANAGE CATEGORIES AND SUBCATEGORIES    ##################################
        ################################################################################################################

        self.frame_categories = FrameManageCategories(self)
        self.add(self.frame_categories, text="     Categories & Subcategories     ", sticky="NEWS")

        ################################################################################################################
        ###########################################        P A N E L        ############################################
        ###########################################    I N T E R F A C E    ############################################
        ################################################################################################################

        self.frame_gui = FrameInterfaceOptions(self)
        self.add(self.frame_gui, text="     Interface settings     ", sticky="NEWS")

        ################################################################################################################
        ############################################       P A N E L       #############################################
        ############################################    D A T A B A S E    #############################################
        ################################################################################################################

        self.frame_database_settings = tk.Frame(self, bg="white")
        self.add(self.frame_database_settings, text="     Database settings     ", sticky="NEWS")
        self.frame_database_settings.columnconfigure(0, weight=1)
        self.frame_database_settings.rowconfigure(0, weight=1)

        DatabaseManager(self.frame_database_settings)

        ################################################################################################################
        ############################################       P A N E L       #############################################
        ############################################    A R C H I V E D    #############################################
        ################################################################################################################

        self.frame_archived = tk.Frame(self, bg="white")
        self.add(self.frame_archived, text="     Archived Notes     ", sticky="NEWS")
        self.frame_archived.columnconfigure(0, weight=1)
        self.frame_archived.rowconfigure(0, weight=1)

        mydb = database.get_db()
        cursor = mydb.cursor()
        if database_type == 'mysql':
            cursor.execute(f"SELECT * FROM archived ORDER BY db_archived_name ASC")
        elif database_type == 'sqlite':
            cursor.execute(f"SELECT *, rowid FROM archived ORDER BY db_archived_name ASC")
        self.archived_messages = []
        for row in cursor.fetchall():
            self.archived_messages.append(row)
        if len(self.archived_messages) != 0:

            listbox = tk.Listbox(self.frame_archived,
                                 background="white",
                                 bd=10,
                                 highlightthickness=0,
                                 highlightbackground="white",
                                 relief="flat",
                                 activestyle='none',
                                 selectmode='single')
            listbox.grid(row=0, column=0, sticky="NEWS")

            listbox_scrollbar = tk.Scrollbar(self.frame_archived, orient="vertical", command=listbox.yview)
            listbox_scrollbar.grid(row=0, column=1, sticky="NS")
            listbox["yscrollcommand"] = listbox_scrollbar.set

            '''Reverse order for inserting into Listbox'''
            right_order = self.archived_messages.copy()
            right_order.reverse()

            for each_archived_message in right_order:
                listbox.insert(0, each_archived_message[0])

            listbox.bind("<<ListboxSelect>>", lambda event: self.select_archived_note(listbox))


    def select_archived_note(self, listbox):
        try:
            selected_item = listbox.curselection()

            archived_note_data = self.archived_messages[selected_item[0]]
            self.popup_archived_message = tk.Toplevel(root, bg='#ffffff')
            self.popup_archived_message.title(archived_note_data[0])

            self.popup_archived_message.columnconfigure(0, weight=1)
            self.popup_archived_message.rowconfigure(0, weight=1)

            archived_text = tk.Text(self.popup_archived_message, bd=5, relief='flat', font=("Calibri Light", 14))
            archived_text.grid(row=0, column=0, sticky="NEWS")
            archived_scrollbar = tk.Scrollbar(self.popup_archived_message, orient="vertical", command=archived_text.yview)
            archived_scrollbar.grid(row=0, column=1, sticky="NS")
            archived_text["yscrollcommand"] = archived_scrollbar.set

            archived_text.insert("1.0", archived_note_data[1])
            archived_text.focus()

            archived_buttons_frame = tk.Frame(self.popup_archived_message, bg="#ffffff")
            archived_buttons_frame.grid(row=1, column=0, sticky="EW")

            save_button = ButtonIcon(archived_buttons_frame, pic="backup.png", pic_px=30, command=lambda: self.update_archived_note(archived_note_data[-1], archived_text.get("0.1", "end-1c")))
            save_button.grid(row=0, column=0, padx=10, pady=2)
            save_button.config(bg='white')

            delete_button = ButtonIcon(archived_buttons_frame, pic="delete.png", pic_px=30, command=lambda: self.delete_archived_note(archived_note_data[-1]))
            delete_button.grid(row=0, column=1, padx=10, pady=2)
            delete_button.config(bg='white')
        except IndexError:
            pass


    def update_archived_note(self, archived_id, note_text):
        mydb = database.get_db()
        if database_type == 'mysql':
            update_archived_command = f"UPDATE archived SET db_archived_text=%s WHERE db_archived_id=%s"
        elif database_type == 'sqlite':
            update_archived_command = f"UPDATE archived SET db_archived_text=? WHERE rowid=?"
        update_archived_value = (note_text, archived_id)
        cursor = mydb.cursor()
        cursor.execute(update_archived_command, update_archived_value)
        mydb.commit()
        cursor.close()
        mydb.close()

        statusbar.set(f"Archived note updated")
        self.popup_archived_message.destroy()

        '''Get the current Notebook Tab ID'''
        current_tab = self.index("current")
        '''Select the current Notebook Tab ID'''
        FrameSettings(root).select(current_tab)


    def delete_archived_note(self, delete_id):
        if messagebox.askyesno(title="Delete archived note", message='Are you sure you want to delete this archived message?'):
            mydb = database.get_db()
            if database_type == 'mysql':
                delete_archived_command = f"DELETE FROM archived WHERE db_archived_id=%s"
            elif database_type == 'sqlite':
                delete_archived_command = f"DELETE FROM archived WHERE rowid=?"
            delete_archived_id = (delete_id,)
            cursor = mydb.cursor()
            cursor.execute(delete_archived_command, delete_archived_id)
            mydb.commit()
            cursor.close()
            mydb.close()

            statusbar.set(f"Archived note deleted")
            self.popup_archived_message.destroy()

            '''Get the current Notebook Tab ID'''
            current_tab = self.index("current")

            for each_widget in self.winfo_children():
                each_widget.destroy()

            '''Select the current Notebook Tab ID'''
            FrameSettings(root).select(current_tab)

########################################################################################################################
########################################################################################################################
##############################                                                             #############################
##############################    S E T T I N G S    M A N A G E    C A T E G O R I E S    #############################
##############################                                                             #############################
########################################################################################################################
########################################################################################################################

class FrameManageCategories(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.config(bg='white')
        self.columnconfigure(0, weight=1)

        self.button_add_new_category = ButtonIcon(self, pic="add.png", text="    ADD NEW CATEGORY", pic_px=15, command=lambda: PopupCategoryAdd(root))
        self.button_add_new_category.grid(row=0, column=0, columnspan=4, sticky="NEWS", padx=5, pady=5)

        self.list_of_categories = []
        mydb = database.get_db()
        cursor = mydb.cursor()
        if database_type == 'mysql':
            cursor.execute(f"SELECT * FROM categories ORDER BY db_category_name ")
        elif database_type == 'sqlite':
            cursor.execute(f"SELECT *, rowid FROM categories ORDER BY db_category_name COLLATE NOCASE")
        for row in cursor.fetchall():
            self.list_of_categories.append(row)
        if not self.list_of_categories:
            self.list_of_categories = [[]]
        cursor.close()
        mydb.close()

        '''Limit number of categories to 10'''
        if len(self.list_of_categories) >= 10:
            self.button_add_new_category.config(state='disabled', text='    Maximum of 10 reached')
        else:
            self.button_add_new_category.config(state='normal', text="    ADD NEW CATEGORY")

        for i, each_category in enumerate(self.list_of_categories, 1):
            self.create_categories_settings(i, each_category)


    ##############################    Create elements for the Categories Settings Page    ##############################
    def create_categories_settings(self, i, each_category):
        mydb = database.get_db()
        if database_type == 'mysql':
            get_by_id_command = f"SELECT * FROM subcategories WHERE db_subcategory_id_category=%s ORDER BY db_subcategory_name"
        elif database_type == 'sqlite':
            get_by_id_command = f"SELECT *, rowid FROM subcategories WHERE db_subcategory_id_category=? ORDER BY db_subcategory_name COLLATE NOCASE"
        get_by_id_value = (each_category[-1],)
        cursor = mydb.cursor()
        cursor.execute(get_by_id_command, get_by_id_value)

        list_of_subcategories = []
        list_of_subcategories_names = []

        for row in cursor.fetchall():
            list_of_subcategories.append(row)
            list_of_subcategories_names.append(row[0])

        cursor.close()
        mydb.close()

        '''List of Subcategories in this Category
        print(f"Subcategories of {each_category[0]}:    {list_of_subcategories}")
        print(f"Subcategory names of {each_category[0]}:    {list_of_subcategories_names}")'''

        self.frame_category_settings = tk.Frame(self, bg='white')
        self.frame_category_settings.grid(row=i, column=0, sticky="EW", pady=10)
        self.frame_category_settings.columnconfigure(0, weight=1)

        category_entry = tk.Entry(self.frame_category_settings, bg=each_category[2], fg="black", width=40, relief="flat", bd=0)
        category_entry.grid(row=0, column=0, sticky="NEWS", padx=5, pady=5)
        category_entry.insert(0, each_category[0])

        self.category_selected_colour = tk.StringVar()
        button_colour = ButtonIcon(self.frame_category_settings, command=lambda: self.category_selected_colour.set(colorchooser.askcolor()[1]), pic="colour.png", pic_px=20, text="    COLOUR")
        button_colour.grid(row=0, column=1, padx=5, pady=5)
        button_colour.config(width=100)

        button_update_category = ButtonIcon(self.frame_category_settings, text="    UPDATE", pic="update.png", command=lambda: self.category_update(category_entry, each_category),
                                            pic_px=20)
        button_update_category.grid(row=0, column=2, padx=5, pady=5)
        button_update_category.config(width=100)

        button_delete_category = ButtonIcon(self.frame_category_settings, text="    DELETE", pic="delete.png", pic_px=20, command=lambda: self.category_delete(each_category, list_of_subcategories))
        button_delete_category.grid(row=0, column=3, padx=5, pady=5)
        button_delete_category.config(width=100)

        if len(database.table_get_all('categories')) == 1:
            button_delete_category.config(state='disabled')
            button_delete_category.bind("<Enter>", lambda event: statusbar.set("Cannot delete last category"))
            button_delete_category.bind("<Leave>", lambda event: statusbar.set(""))
        else:
            button_delete_category.config(state='normal')
            button_delete_category.unbind_all("<Enter>")

        ttk.Separator(self.frame_category_settings, orient="vertical").grid(row=0, column=4, padx=30, pady=5, sticky="NS")

        button_add_new_subcategory = ButtonIcon(self.frame_category_settings, pic="add.png", text="    ADD NEW SUBCATEGORY", pic_px=15, command=lambda: PopupSubcategoryAdd(root, each_category, len(list_of_subcategories)))
        button_add_new_subcategory.grid(row=0, column=5, padx=(5, 10), pady=5, sticky="NS")
        button_add_new_subcategory.config(width=200)
        if len(list_of_subcategories) >= 20:
            button_add_new_subcategory.config(state='disabled', text='    Maximum of 20 reached')
        else:
            button_add_new_subcategory.config(state='normal', text="    ADD NEW SUBCATEGORY")

        tk.Label(self.frame_category_settings, text=f"{len(list_of_subcategories)}/20", bg='white', width=5).grid(row=0, column=6, pady=5)

        combobox_subcategories = ttk.Combobox(self.frame_category_settings, values=list_of_subcategories_names, state='readonly')
        combobox_subcategories.grid(row=0, column=7, padx=10, pady=5)
        combobox_subcategories.current(0)

        entry_selected_subcategory = ttk.Entry(self.frame_category_settings)
        entry_selected_subcategory.grid(row=0, column=8, padx=10, pady=5)
        entry_selected_subcategory.insert(0, combobox_subcategories.get())

        frame_subcategory_settings = tk.Frame(self.frame_category_settings, bg='white')
        frame_subcategory_settings.grid(row=0, column=9, sticky="EW")

        combobox_subcategories.bind("<<ComboboxSelected>>", lambda event: [entry_selected_subcategory.delete(0, "end"),
                                                                           entry_selected_subcategory.insert(0, combobox_subcategories.get()),
                                                                           self.create_subcategories_settings(list_of_subcategories[combobox_subcategories.current()], frame_subcategory_settings, len(list_of_subcategories), entry_selected_subcategory)])

        '''Automaticaly display the remaining subcategory settings buttons for the first subcategory'''
        self.create_subcategories_settings(list_of_subcategories[combobox_subcategories.current()], frame_subcategory_settings, len(list_of_subcategories), entry_selected_subcategory)


    def create_subcategories_settings(self, selected_subcategory, frame_widget, number_of_categories, widget_entry):
        button_update_subcategory = ButtonIcon(frame_widget, text="    UPDATE", pic="update.png", pic_px=20, command=lambda: self.subcategory_update(selected_subcategory, widget_entry))
        button_update_subcategory.grid(row=0, column=0, padx=5, pady=5)
        button_update_subcategory.config(width=100)

        self.button_delete_subcategory = ButtonIcon(frame_widget, text="    DELETE", pic="delete.png", pic_px=20, command=lambda: self.subcategory_delete(selected_subcategory))
        self.button_delete_subcategory.grid(row=0, column=1, padx=5, pady=5)
        self.button_delete_subcategory.config(width=100)

        if number_of_categories == 1:
            self.button_delete_subcategory.config(state='disabled')
            self.button_delete_subcategory.bind("<Enter>", lambda event: statusbar.set("Cannot delete last subcategory"))
            self.button_delete_subcategory.bind("<Leave>", lambda event: statusbar.set(""))
        else:
            self.button_delete_subcategory.config(state='normal')
            self.button_delete_subcategory.unbind_all("<Enter>")


    def subcategory_update(self, subcategory_data, widget_entry):
        try:
            if len(widget_entry.get()) != 0:
                s_title = widget_entry.get()
            else:
                s_title = subcategory_data[0]

            if widget_entry.get() != subcategory_data[0]:
                mydb = database.get_db()
                if database_type == 'mysql':
                    update_subcategory_command = f"UPDATE subcategories SET db_subcategory_name=%s, db_subcategory_description=%s WHERE db_subcategory_id=%s"
                elif database_type == 'sqlite':
                    update_subcategory_command = f"UPDATE subcategories SET db_subcategory_name=?, db_subcategory_description=? WHERE rowid=?"
                update_subcategory_value = (s_title, '', subcategory_data[-1])
                cursor = mydb.cursor()
                cursor.execute(update_subcategory_command, update_subcategory_value)
                mydb.commit()
                cursor.close()
                mydb.close()

                FrameSettings(root)
                statusbar.set(f"Subcategory {subcategory_data[0]} changed to {s_title}")
            else:
                statusbar.set(f"Subcategory {subcategory_data[0]} has not been updated, text was the same.")
        except:
            statusbar.set(f"Subcategory {subcategory_data[0]} has not been updated.")


    def category_delete(self, target_data, subcategories_to_delete):
        if messagebox.askyesno(title=f"DELETE:    {target_data[0]}", message=f"Are you sure you want to delete this category?\nAll subcategories and notes will be removed as well.\nThis operation is irrevocable."):
            try:
                for each_subcategory in subcategories_to_delete:
                    mydb = database.get_db()
                    if database_type == 'mysql':
                        delete_notes_command = f"DELETE FROM notes WHERE db_note_id_subcategory=%s"
                        delete_self_command = f"DELETE FROM subcategories WHERE db_subcategory_id=%s"
                    elif database_type == 'sqlite':
                        delete_notes_command = f"DELETE FROM notes WHERE db_note_id_subcategory=?"
                        delete_self_command = f"DELETE FROM subcategories WHERE rowid=?"

                    delete_item_id = (each_subcategory[-1],)
                    cursor = mydb.cursor()
                    cursor.execute(delete_notes_command, delete_item_id)
                    mydb.commit()
                    cursor.execute(delete_self_command, delete_item_id)
                    mydb.commit()
                    cursor.close()
                    mydb.close()

                mydb = database.get_db()
                if database_type == 'mysql':
                    delete_category_command = f"DELETE FROM categories WHERE db_category_id=%s"
                elif database_type == 'sqlite':
                    delete_category_command = f"DELETE FROM categories WHERE rowid=?"
                delete_category_id = (target_data[-1],)
                cursor = mydb.cursor()
                cursor.execute(delete_category_command, delete_category_id)
                mydb.commit()
                cursor.close()
                mydb.close()

                FrameSettings(root)
                statusbar.set(f"Category {target_data[0]}, all subcategories and notes deleted.")
            except:
                statusbar.set(f"Deleting category {target_data[0]} not completed.")
        else:
            statusbar.set(f"Operation cancelled, category {target_data[0]} not deleted.")


    def subcategory_delete(self, target_data):
        if messagebox.askyesno(title=f"DELETE:    {target_data[0]}", message=f"Are you sure you want to delete this subcategory?\nAll notes will be removed as well.\nThis operation is irrevocable."):
            try:
                mydb = database.get_db()
                if database_type == 'mysql':
                    delete_notes_command = f"DELETE FROM notes WHERE db_note_id_subcategory=%s"
                    delete_self_command = f"DELETE FROM subcategories WHERE db_subcategory_id=%s"
                elif database_type == 'sqlite':
                    delete_notes_command = f"DELETE FROM notes WHERE db_note_id_subcategory=?"
                    delete_self_command = f"DELETE FROM subcategories WHERE rowid=?"
                delete_item_id = (target_data[-1],)
                cursor = mydb.cursor()
                cursor.execute(delete_notes_command, delete_item_id)
                mydb.commit()
                cursor.execute(delete_self_command, delete_item_id)
                mydb.commit()
                cursor.close()
                mydb.close()

                FrameSettings(root)
                statusbar.set(f"Category {target_data[0]}, and all notes deleted.")
            except:
                statusbar.set(f"Deleting subcategory {target_data[0]} not completed.")
        else:
            statusbar.set(f"Operation cancelled, subcategory {target_data[0]} not deleted.")


    def category_update(self, entry_widget, category_data):
        if len(entry_widget.get()) != 0:
            c_title = entry_widget.get()
        else:
            c_title = category_data[0]

        if self.category_selected_colour.get() != "None" and self.category_selected_colour.get() != '':
            c_colour = self.category_selected_colour.get()
        else:
            c_colour = category_data[2]

        mydb = database.get_db()
        if database_type == 'mysql':
            update_category_command = f"UPDATE categories SET db_category_name=%s, db_category_description=%s, db_category_colour=%s WHERE db_category_id=%s"
        elif database_type == 'sqlite':
            update_category_command = f"UPDATE categories SET db_category_name=?, db_category_description=?, db_category_colour=? WHERE rowid=?"
        update_category_value = (c_title, '', c_colour, category_data[-1])
        cursor = mydb.cursor()
        cursor.execute(update_category_command, update_category_value)
        mydb.commit()
        cursor.close()
        mydb.close()

        FrameSettings(root)


########################################################################################################################
########################################################################################################################
##############################                                                             #############################
##############################    S E T T I N G S    M A N A G E    C A T E G O R I E S    #############################
##############################          P O P U P    A D D    C A T E G O R I E S          #############################
##############################                                                             #############################
########################################################################################################################
########################################################################################################################

class PopupCategoryAdd(tk.Toplevel):
    def __init__(self, container,  *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.config(bg='white')

        self.selected_colour = tk.StringVar()

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.geometry("600x50")
        self.title("Enter new category name... ")
        self.focus_set()

        self.entry_category_add = ttk.Entry(self)
        self.entry_category_add.grid(row=0, column=0, sticky="EW", padx=5)
        self.entry_category_add.focus()

        self.button_category_add_colour = ButtonIcon(self, text='    Select colour', command=lambda: [self.selected_colour.set(colorchooser.askcolor()[1]), self.get_category_colour()], pic="colour.png", pic_px=20)
        self.button_category_add_colour.grid(row=0, column=1, sticky="W")
        self.button_category_add_colour.config(width=150, relief='ridge', bd=1)

        self.button_category_add = ButtonIcon(self, text='    Add', command=lambda: self.category_add(), pic="add.png", pic_px=20, state='disabled')
        self.button_category_add.grid(row=0, column=2, sticky="W", padx=5)
        self.button_category_add.config(width=150, relief='ridge', bd=1)

    def get_category_colour(self):

        if self.selected_colour.get() != "None" and self.selected_colour.get() != '':
            self.button_category_add.config(state='normal')

        self.focus_set()

    def category_add(self):
        """Limit number of categories to 10"""
        if len(database.table_get_all('categories')) < 10:
            c_title, c_colour = False, False
            if len(self.entry_category_add.get()) != 0:
                c_title = self.entry_category_add.get()

            if self.selected_colour.get() != "None" and self.selected_colour.get() != '':
                c_colour = self.selected_colour.get()

            if c_title and c_colour:
                mydb = database.get_db()
                cursor = mydb.cursor()

                if database_type == 'mysql':
                    add_category_command = f"INSERT INTO categories (db_category_name, db_category_description, db_category_colour) VALUES (%s, %s, %s)"
                    get_category_id = "SELECT last_insert_id()"
                elif database_type == 'sqlite':
                    add_category_command = f"INSERT INTO categories (db_category_name, db_category_description, db_category_colour) VALUES (?, ?, ?)"
                    get_category_id = "SELECT last_insert_rowid()"

                add_category_value = (c_title, '', c_colour)
                cursor.execute(add_category_command, add_category_value)
                cursor.execute(get_category_id)
                last_category_id = cursor.fetchone()[0]
                mydb.commit()

                if database_type == 'mysql':
                    add_blank_subcategory_command = f"INSERT INTO subcategories (db_subcategory_name, db_subcategory_description, db_subcategory_id_category) VALUES (%s, %s, %s)"
                    get_subcategory_id = "SELECT last_insert_id()"
                elif database_type == 'sqlite':
                    add_blank_subcategory_command = f"INSERT INTO subcategories (db_subcategory_name, db_subcategory_description, db_subcategory_id_category) VALUES (?, ?, ?)"
                    get_subcategory_id = "SELECT last_insert_rowid()"

                add_blank_subcategory_value = ("NOTES", '', last_category_id)
                cursor.execute(add_blank_subcategory_command, add_blank_subcategory_value)
                cursor.execute(get_subcategory_id)
                last_subcategory_id = cursor.fetchone()[0]
                mydb.commit()

                if database_type == 'mysql':
                    add_blank_note_command = f"INSERT INTO notes (db_note_name, db_note_text, db_note_date, db_note_id_subcategory, db_note_font_name, db_note_font_size, db_note_font_colour, db_note_font_bold, db_note_font_italic, db_note_position) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                elif database_type == 'sqlite':
                    add_blank_note_command = f"INSERT INTO notes (db_note_name, db_note_text, db_note_date, db_note_id_subcategory, db_note_font_name, db_note_font_size, db_note_font_colour, db_note_font_bold, db_note_font_italic, db_note_position) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

                add_blank_note_value = ("New note", '', datetime.date.today(), last_subcategory_id, "Calibri Light", 9, "#000000", 0, 0, 'left')
                cursor.execute(add_blank_note_command, add_blank_note_value)

                mydb.commit()
                cursor.close()
                mydb.close()

                self.destroy()
                FrameSettings(root)
        else:
            self.destroy()
            '''This is redundant, you shouldn't be able to click the button to add more categories'''
            messagebox.showinfo(title='Too many categories', message='Maximum of 10 categories reached.')

########################################################################################################################
########################################################################################################################
##############################                                                             #############################
##############################    S E T T I N G S    M A N A G E    C A T E G O R I E S    #############################
##############################       P O P U P    A D D    S U B C A T E G O R I E S       #############################
##############################                                                             #############################
########################################################################################################################
########################################################################################################################

class PopupSubcategoryAdd(tk.Toplevel):
    def __init__(self, container, category_data, number_of_subcategories, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.category_data = category_data
        self.number_of_subcategories = number_of_subcategories

        self.config(bg='white')
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.geometry("600x50")
        self.title("Enter new subcategory name... ")
        self.focus_set()

        tk.Label(self, text=f'Add to: {self.category_data[0]}', bg=self.category_data[2]).grid(row=0, column=0, sticky="W", padx=5)

        self.entry_subcategory_add = ttk.Entry(self)
        self.entry_subcategory_add.grid(row=0, column=1, sticky="EW")

        self.entry_subcategory_add.focus()
        self.entry_subcategory_add.bind("<Return>", lambda event: self.subcategory_add())

        self.button_category_add = ButtonIcon(self, text='    Add', command=lambda: self.subcategory_add(), pic="add.png", pic_px=20)
        self.button_category_add.grid(row=0, column=2, sticky="W", padx=5)
        self.button_category_add.config(width=150, relief='ridge', bd=1)

    def subcategory_add(self):
        """Get selected Category ID"""
        category_id = self.category_data[-1]

        """Limit number of subcategories to 20"""
        if self.number_of_subcategories < 20:
            # global display_option
            # Check if entry isn't empty or isn't Enter subcategory name...
            sc_title = False
            entry_subcategory = self.entry_subcategory_add.get()
            if len(entry_subcategory) != 0 and entry_subcategory != "Enter subcategory name...":
                sc_title = entry_subcategory
            if sc_title:
                mydb = database.get_db()
                cursor = mydb.cursor()
                if database_type == 'mysql':
                    add_blank_subcategory_command = f"INSERT INTO subcategories (db_subcategory_name, db_subcategory_description, db_subcategory_id_category) VALUES (%s, %s, %s)"
                    get_subcategory_id = "SELECT last_insert_id()"
                elif database_type == 'sqlite':
                    add_blank_subcategory_command = f"INSERT INTO subcategories (db_subcategory_name, db_subcategory_description, db_subcategory_id_category) VALUES (?, ?, ?)"
                    get_subcategory_id = "SELECT last_insert_rowid()"

                add_blank_subcategory_value = (entry_subcategory, '', category_id)
                cursor.execute(add_blank_subcategory_command, add_blank_subcategory_value)
                cursor.execute(get_subcategory_id)
                last_subcategory_id = cursor.fetchone()[0]
                mydb.commit()

                if database_type == 'mysql':
                    add_blank_note_command = f"INSERT INTO notes (db_note_name, db_note_text, db_note_date, db_note_id_subcategory, db_note_font_name, db_note_font_size, db_note_font_colour, db_note_font_bold, db_note_font_italic, db_note_position) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                elif database_type == 'sqlite':
                    add_blank_note_command = f"INSERT INTO notes (db_note_name, db_note_text, db_note_date, db_note_id_subcategory, db_note_font_name, db_note_font_size, db_note_font_colour, db_note_font_bold, db_note_font_italic, db_note_position) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                add_blank_note_value = ("New note", '', datetime.date.today(), last_subcategory_id, "Calibri Light", 9, "#000000", 0, 0, 'left')
                cursor.execute(add_blank_note_command, add_blank_note_value)
                mydb.commit()
                cursor.close()
                mydb.close()

                FrameSettings(root)
                self.destroy()
        else:
            self.destroy()
            '''This is redundant, you shouldn't be able to click the button to add more subcategories'''
            messagebox.showinfo(title='Too many subcategories', message='Maximum of 20 subcategories reached.')

########################################################################################################################
########################################################################################################################
##############################                                                             #############################
##############################    S E T T I N G S    I N T E R F A C E    O P T I O N S    #############################
##############################                                                             #############################
########################################################################################################################
########################################################################################################################

class FrameInterfaceOptions(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.config(bg='white')
        self.columnconfigure((0, 1, 2, 3), weight=1)
        self.rowconfigure(10, weight=1)

        ################################################################################################################
        ########################################    C O L O U R    M O D E S    ########################################
        ################################################################################################################

        self.frame_modes = tk.LabelFrame(self, text=' Colour Modes ', labelanchor='n', bg="white", padx=10, pady=10, width=340, height=205)
        self.frame_modes.grid(row=0, column=0, padx=5, pady=5, sticky="NEWS")
        self.frame_modes.columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.frame_modes.rowconfigure(0, weight=1)
        self.frame_modes.grid_propagate(0)

        b_light = ButtonIcon(self.frame_modes, command=lambda: database.table_settings_update_colour_modes('white'), pic="light.png", pic_px=50)
        b_light.grid(row=0, column=0, sticky="EW")
        b_light.config(bg="white", fg="black", text="\nLIGHT", compound="top")

        b_dark = ButtonIcon(self.frame_modes, command=lambda: database.table_settings_update_colour_modes('dark'), pic="dark.png", pic_px=50)
        b_dark.grid(row=0, column=1, sticky="EW")
        b_dark.config(bg="white", fg="black", text="\nDARK", compound="top")

        b_colourful = ButtonIcon(self.frame_modes, command=lambda: database.table_settings_update_colour_modes('light'), pic="nature.png", pic_px=50)
        b_colourful.grid(row=0, column=2, sticky="EW")
        b_colourful.config(bg="white", fg="black", text="\nNATURE", compound="top")

        b_single = ButtonIcon(self.frame_modes, command=lambda: database.table_settings_update_colour_modes(colorchooser.askcolor()[1]), pic="colour.png", pic_px=50)
        b_single.grid(row=0, column=3, sticky="EW")
        b_single.config(bg="white", fg="black", text="\nCHOICE", compound="top")

        b_user = ButtonIcon(self.frame_modes, command=lambda: database.table_settings_update_colour_modes('user'), pic="user.png", pic_px=50)
        b_user.grid(row=0, column=4, sticky="EW")
        b_user.config(bg="white", fg="black", text="\nUSER", compound="top")

        ################################################################################################################
        ################################################    I C O N S    ###############################################
        ################################################################################################################

        self.frame_icons = tk.LabelFrame(self, text=' Icon Sets ', labelanchor='n', bg="white", padx=10, pady=10, width=340, height=205)
        self.frame_icons.grid(row=0, column=1, padx=5, pady=5, sticky="NEWS")
        self.frame_icons.columnconfigure((0, 1), weight=1)
        self.frame_icons.rowconfigure(0, weight=1)
        self.frame_icons.grid_propagate(0)
        bright_icon = tk.PhotoImage(file="./icons/colourful.png")
        b_colourful_icons = tk.Button(self.frame_icons, image=bright_icon, text="Colourful", bg="white", fg="black", compound="top", command=lambda: self.change_icons('colourful'), bd=0)
        b_colourful_icons.grid(row=0, column=0, sticky="NEWS")
        b_colourful_icons.image = bright_icon
        material_icon = tk.PhotoImage(file="./icons/material.png")
        b_w_icons = tk.Button(self.frame_icons, image=material_icon, text="B & W", bg="white", fg="black", compound="top", command=lambda: self.change_icons('material'), bd=0)
        b_w_icons.grid(row=0, column=1, sticky="NEWS")
        b_w_icons.image = material_icon

        ################################################################################################################
        ###########################    C H A N G E    I N T E R F A C E    E L E M E N T S    ##########################
        ################################################################################################################

        self.frame_interface_elements = tk.LabelFrame(self, text=' Change Interface Elements ', labelanchor='n', bg="white", padx=10, pady=10, width=340, height=205)
        self.frame_interface_elements.grid(row=0, column=2, padx=5, pady=5, sticky="NEWS")
        self.frame_interface_elements.columnconfigure((0, 1), weight=1)
        self.frame_interface_elements.rowconfigure(6, weight=1)
        self.frame_interface_elements.grid_propagate(0)
        tk.Label(self.frame_interface_elements, text="Main Menu Icon Size", bg="white").grid(row=2, column=0, sticky="W")
        self.icon_menu_size_combobox = ttk.Combobox(self.frame_interface_elements, values=[20, 30, 40, 50, 60], state="readonly", width=3)
        self.icon_menu_size_combobox.grid(row=2, column=1, sticky="EW", padx=5)
        self.icon_menu_size_combobox.set(main_menu_icon_size)
        tk.Label(self.frame_interface_elements, text="Main Menu Icon Spacing", bg="white").grid(row=3, column=0, sticky="W")
        self.icon_menu_padding_combobox = ttk.Combobox(self.frame_interface_elements, values=[10, 20, 30, 40], state="readonly", width=3)
        self.icon_menu_padding_combobox.grid(row=3, column=1, sticky="EW", padx=5)
        self.icon_menu_padding_combobox.set(main_menu_padding)
        tk.Label(self.frame_interface_elements, text="Text Edit Icon Size", bg="white").grid(row=4, column=0, sticky="W")
        self.icon_text_size_combobox = ttk.Combobox(self.frame_interface_elements, values=[15, 20, 25, 30], state="readonly", width=3)
        self.icon_text_size_combobox.grid(row=4, column=1, sticky="EW", padx=5)
        self.icon_text_size_combobox.set(note_menu_icon_size)
        self.button_apply_settings = ButtonIcon(self.frame_interface_elements, text="    APPLY SETTINGS", command=lambda: self.update_interface_elements(), pic="backup.png", pic_px=20)
        self.button_apply_settings.grid(row=7, column=0, columnspan=2, sticky="EWS")

        ################################################################################################################
        ###########    C H A N G E    I N I T I A L    W I N D O W    S I Z E    A N D    P O S I T I O N    ###########
        ################################################################################################################

        self.frame_size_and_position = tk.LabelFrame(self, text=' Change Initial Window Size and Position ', labelanchor='n', bg="white", padx=10, pady=10, width=340, height=205)
        self.frame_size_and_position.grid(row=0, column=3, padx=5, pady=5, sticky="NEWS")
        self.frame_size_and_position.columnconfigure((0, 1), weight=1)
        self.frame_size_and_position.rowconfigure(4, weight=1)
        self.frame_size_and_position.grid_propagate(0)

        tk.Label(self.frame_size_and_position, text="Window width", bg="white").grid(row=0, column=0, sticky="W")
        self.spinbox_width = ttk.Spinbox(self.frame_size_and_position, from_=1400, to=3840, increment=20, wrap=True, state='readonly')
        self.spinbox_width.grid(row=0, column=1)
        self.spinbox_width.set(window_width)

        tk.Label(self.frame_size_and_position, text="Window height", bg="white").grid(row=1, column=0, sticky="W")
        self.spinbox_height = ttk.Spinbox(self.frame_size_and_position, from_=500, to=2160, increment=20, wrap=True, state='readonly')
        self.spinbox_height.grid(row=1, column=1)
        self.spinbox_height.set(window_height)

        tk.Label(self.frame_size_and_position, text="Position X", bg="white").grid(row=2, column=0, sticky="W")
        self.spinbox_x = ttk.Spinbox(self.frame_size_and_position, from_=0, to=1000, increment=20, wrap=True, state='readonly')
        self.spinbox_x.grid(row=2, column=1)
        self.spinbox_x.set(window_position_x)

        tk.Label(self.frame_size_and_position, text="Position Y", bg="white").grid(row=3, column=0, sticky="W")
        self.spinbox_y = ttk.Spinbox(self.frame_size_and_position, from_=0, to=500, increment=20, wrap=True, state='readonly')
        self.spinbox_y.grid(row=3, column=1)
        self.spinbox_y.set(window_position_y)

        self.button_apply_size = ButtonIcon(self.frame_size_and_position, text="    APPLY", command=lambda: self.update_initial_window_size_and_position(), pic="backup.png", pic_px=20)
        self.button_apply_size.grid(row=5, column=0, columnspan=2, sticky="EWS")

        ################################################################################################################
        ##############################    N O T E S    P A N E L    V I S I B I L I T Y    #############################
        ################################################################################################################

        self.frame_notes_panel = tk.LabelFrame(self, text=' Notes Panel ', labelanchor='n', bg="white",
                                               padx=10, pady=10, width=340, height=205)
        self.frame_notes_panel.grid(row=1, column=0, padx=5, pady=5, sticky="NEWS")
        self.frame_notes_panel.columnconfigure((0, 1, 2), weight=1)
        self.frame_notes_panel.rowconfigure(0, weight=1)
        self.frame_notes_panel.grid_propagate(0)

        self.notes_panel_radiobutton = tk.StringVar()
        self.button_panel_show = ButtonIcon(self.frame_notes_panel, text="Start visible",
                                            command=lambda: self.notes_panel_visibility('show'), pic="panel_show.png",
                                            pic_px=50)
        self.button_panel_show.grid(row=0, column=0, padx=10, pady=10, sticky="NEWS")
        self.button_panel_show.config(bg='white', fg='black', compound='top', activebackground='white')

        self.button_panel_hide = ButtonIcon(self.frame_notes_panel, text="Start hidden",
                                            command=lambda: self.notes_panel_visibility('hide'), pic="panel_hide.png",
                                            pic_px=50)
        self.button_panel_hide.grid(row=0, column=1, padx=10, pady=10, sticky="NEWS")
        self.button_panel_hide.config(bg='white', fg='black', compound='top', activebackground='white')

        self.button_panel_auto = ButtonIcon(self.frame_notes_panel, text="Auto hide",
                                            command=lambda: self.notes_panel_visibility('auto_hide'), pic="panel_auto.png",
                                            pic_px=50)
        self.button_panel_auto.grid(row=0, column=2, padx=10, pady=10, sticky="NEWS")
        self.button_panel_auto.config(bg='white', fg='black', compound='top', activebackground='white')

        if notes_panel_visible == 'show':
            self.button_panel_show.config(state='disabled')
            self.button_panel_hide.config(state='normal')
            self.button_panel_auto.config(state='normal')
        elif notes_panel_visible == 'hide':
            self.button_panel_show.config(state='normal')
            self.button_panel_hide.config(state='disabled')
            self.button_panel_auto.config(state='normal')
        elif notes_panel_visible == 'auto_hide':
            self.button_panel_show.config(state='normal')
            self.button_panel_hide.config(state='normal')
            self.button_panel_auto.config(state='disabled')


        ################################################################################################################
        ###########################    C H A N G E    F O N T    -    N O T E S    L I S T    ##########################
        ################################################################################################################

        self.frame_font_lis_notes = tk.LabelFrame(self, text=' Notes Panel font ', labelanchor='n', bg="white", padx=10, pady=10, width=340, height=205)
        self.frame_font_lis_notes.grid(row=1, column=1, padx=5, pady=5, sticky="NEWS")
        self.frame_font_lis_notes.columnconfigure((0, 1), weight=1)
        self.frame_font_lis_notes.rowconfigure(3, weight=1)
        self.frame_font_lis_notes.grid_propagate(0)
        tk.Label(self.frame_font_lis_notes, text='Select font', bg="white").grid(row=0, column=0, sticky="W", padx=5, pady=5)
        option_fonts = font.families()
        self.selected_font = tk.StringVar()
        self.font_combobox = ttk.Combobox(self.frame_font_lis_notes, textvariable=self.selected_font, values=option_fonts, state="readonly")
        self.font_combobox.grid(row=0, column=1, sticky="EW", padx=5, pady=5)
        font_index = 0
        for i, font_name in enumerate(font.families()):
            if font_name == selected_notes_font_name:
                font_index = i
        self.font_combobox.current(font_index)
        tk.Label(self.frame_font_lis_notes, text='Select font size', bg="white").grid(row=1, column=0, sticky="W", padx=5, pady=5)
        self.font_size = tk.StringVar()
        self.font_values = [6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 24]
        self.font_combobox_size = ttk.Combobox(self.frame_font_lis_notes, textvariable=self.font_size, values=self.font_values, state="readonly")
        self.font_combobox_size.grid(row=1, column=1, sticky="EW", padx=5, pady=5)
        size_index = 0
        for i, each_font_size in enumerate(self.font_values):
            if int(each_font_size) == int(selected_notes_font_size):
                size_index = i
        self.font_combobox_size.current(size_index)
        self.preview = tk.Label(self.frame_font_lis_notes, text='Font preview 01234...', bg="white", font='"%s"' % font.families()[font_index])
        self.preview.grid(row=2, column=0,  sticky="EW", padx=5, pady=5, columnspan=2)
        self.font_combobox.bind("<<ComboboxSelected>>", lambda event: self.preview.config(font='"%s"' % self.selected_font.get()))

        self.button_update_font = ButtonIcon(self.frame_font_lis_notes, text="    UPDATE FONT", command=lambda: self.notes_list_font(), pic="update.png", pic_px=20)
        self.button_update_font.grid(row=4, column=0, columnspan=2, padx=5, sticky="EWS")

        ################################################################################################################
        ############################    S E N D - F R O M    E M A I L    S E T T I N G S    ###########################
        ################################################################################################################

        self.frame_email = tk.LabelFrame(self, text=' Send-from email settings ', labelanchor='n', bg="white", padx=10,
                                                  pady=10, width=340, height=205)
        self.frame_email.grid(row=1, column=2, padx=5, pady=5, sticky="NEWS")
        self.frame_email.columnconfigure((0, 1), weight=1)
        self.frame_email.rowconfigure((0, 3), weight=1)
        self.frame_email.grid_propagate(0)

        tk.Label(self.frame_email, text="Email address", bg="white").grid(row=1, column=0, padx=5)

        self.entry_email_address = tk.Entry(self.frame_email)
        self.entry_email_address.grid(row=2, column=0, sticky="EW", padx=5)
        self.entry_email_address.insert(0, stored_email_address)

        tk.Label(self.frame_email, text="Email password", bg="white").grid(row=1, column=1, padx=5)

        self.entry_email_password = tk.Entry(self.frame_email, show="*")
        self.entry_email_password.grid(row=2, column=1, sticky="EW", padx=5)
        self.entry_email_password.insert(0, stored_email_password)

        self.button_update_font = ButtonIcon(self.frame_email, text="    UPDATE EMAIL DETAILS", pic="email.png", pic_px=20, command=lambda: self.update_email_details())
        self.button_update_font.grid(row=4, column=0, columnspan=2, padx=5, sticky="EWS")

    ####################################################################################################################
    ###############################################    M E T H O D S    ################################################
    ####################################################################################################################

    def update_email_details(self):
        global stored_email_address
        global stored_email_password

        stored_email_address = self.entry_email_address.get()
        stored_email_password = self.entry_email_password.get()

        with open("./assets/email_data.dat", "wb") as email_dumpfile:
            pickle.dump(stored_email_address, email_dumpfile)
            pickle.dump(stored_email_password, email_dumpfile)


    def notes_list_font(self):
        global font_list_notes
        global selected_notes_font_name
        global selected_notes_font_size
        font_list_notes = font.Font(family=self.selected_font.get(), size=self.font_size.get())
        selected_notes_font_name = self.selected_font.get()
        selected_notes_font_size = self.font_size.get()
        statusbar.set(f"Font updated: {self.selected_font.get()}, size: {self.font_size.get()}")
        mydb = database.get_db()
        if database_type == 'mysql':
            update_item_command = f"UPDATE settings SET settings_selected_listbox_font_name=%s, settings_selected_listbox_font_size=%s"
        elif database_type == 'sqlite':
            update_item_command = f"UPDATE settings SET settings_selected_listbox_font_name=?, settings_selected_listbox_font_size=?"
        update_item_value = (selected_notes_font_name, selected_notes_font_size)
        cursor = mydb.cursor()
        cursor.execute(update_item_command, update_item_value)
        mydb.commit()
        cursor.close()
        mydb.close()

    def update_interface_elements(self):
        global main_menu_icon_size
        global main_menu_padding
        global note_menu_icon_size
        main_menu_icon_size = int(self.icon_menu_size_combobox.get())
        main_menu_padding = int(self.icon_menu_padding_combobox.get())
        note_menu_icon_size = int(self.icon_text_size_combobox.get())
        for each_widget in root.winfo_children():
            each_widget.destroy()
        mydb = database.get_db()
        if database_type == 'mysql':
            update_item_command = f"UPDATE settings SET settings_main_menu_icon_size=%s, settings_main_menu_padding=%s, settings_note_menu_icon_size=%s"
        elif database_type == 'sqlite':
            update_item_command = f"UPDATE settings SET settings_main_menu_icon_size=?, settings_main_menu_padding=?, settings_note_menu_icon_size=?"
        update_item_value = (main_menu_icon_size, main_menu_padding, note_menu_icon_size)
        cursor = mydb.cursor()
        cursor.execute(update_item_command, update_item_value)
        mydb.commit()
        cursor.close()
        mydb.close()
        start()

    def change_icons(self, option):
        global pictures_path
        if option == 'colourful':
            pictures_path = "./icons/colourful/"
        elif option == 'material':
            pictures_path = "./icons/material/"

        mydb = database.get_db()
        if database_type == 'mysql':
            update_item_command = f"UPDATE settings SET settings_pictures_path=%s"
        elif database_type == 'sqlite':
            update_item_command = f"UPDATE settings SET settings_pictures_path=?"
        update_item_value = (pictures_path, )
        cursor = mydb.cursor()
        cursor.execute(update_item_command, update_item_value)
        mydb.commit()
        cursor.close()
        mydb.close()

        start()


    def update_initial_window_size_and_position(self):
        global window_width
        global window_height
        global window_position_x
        global window_position_y
        window_width = self.spinbox_width.get()
        window_height = self.spinbox_height.get()
        window_position_x = self.spinbox_x.get()
        window_position_y = self.spinbox_y.get()
        root.geometry(f"{window_width}x{window_height}+{window_position_x}+{window_position_y}")
        statusbar.set(f"New size and position applied: {window_height}x{window_width}px, position X:{window_position_x}, position Y:{window_position_y}")
        if database_type == 'mysql':
            try:
                mydb = mysql.connector.connect(host=database_data[0], user=database_data[1], passwd=database_data[2], database=database_name)
            except:
                DatabaseManager(root)
                return
            update_item_command = f"UPDATE settings SET settings_window_width=%s, settings_window_height=%s, settings_window_position_x=%s, settings_window_position_y=%s"
        elif database_type == 'sqlite':
            mydb = sqlite3.connect(database_name)
            update_item_command = f"UPDATE settings SET settings_window_width=?, settings_window_height=?, settings_window_position_x=?, settings_window_position_y=?"
        update_item_value = (window_width, window_height, window_position_x, window_position_y)
        cursor = mydb.cursor()
        cursor.execute(update_item_command, update_item_value)
        mydb.commit()
        cursor.close()
        mydb.close()


    def notes_panel_visibility(self, option):
        global notes_panel_visible
        notes_panel_visible = option
        if option == 'show':
            self.button_panel_show.config(state='disabled')
            self.button_panel_hide.config(state='normal')
            self.button_panel_auto.config(state='normal')
        elif option == 'hide':
            self.button_panel_show.config(state='normal')
            self.button_panel_hide.config(state='disabled')
            self.button_panel_auto.config(state='normal')
        elif option == 'auto_hide':
            self.button_panel_show.config(state='normal')
            self.button_panel_hide.config(state='normal')
            self.button_panel_auto.config(state='disabled')
        if database_type == 'mysql':
            try:
                mydb = mysql.connector.connect(host=database_data[0], user=database_data[1], passwd=database_data[2], database=database_name)
            except:
                DatabaseManager(root)
                return
            update_item_command = f"UPDATE settings SET settings_notes_panel_visibility=%s"
        elif database_type == 'sqlite':
            mydb = sqlite3.connect(database_name)
            update_item_command = f"UPDATE settings SET settings_notes_panel_visibility=?"
        update_item_value = (option, )
        cursor = mydb.cursor()
        cursor.execute(update_item_command, update_item_value)
        mydb.commit()
        cursor.close()
        mydb.close()

########################################################################################################################
########################################################################################################################
##################################################                   ###################################################
##################################################    S Y S T E M    ###################################################
##################################################                   ###################################################
########################################################################################################################
########################################################################################################################

if __name__ == "__main__":
    root = tk.Tk()


    root.title("Notes")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    statusbar = tk.StringVar()
    text_font = font.Font(family="Calibri Light", size=10)
    statusbar_font = font.Font(family="Calibri Light", size=9)

    database = DatabaseManager(root)

    try:
        c_mode = database.table_get_all('settings')[0][0]
    except:
        c_mode = 'white'

    try:
        apply_settings_and_start_app(c_mode)
    except:
        DatabaseManager(root)

    root.mainloop()
