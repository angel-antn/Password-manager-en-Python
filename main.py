import tkinter as tk
from tkinter import messagebox
import json
from random import choice, shuffle, randint
import pyperclip

BACKGROUND = '#fce6e4'
BORDER = 'paleturquoise'
BUTTONS = '#ec6f62'
KEYS = ('website', 'user', 'password')

LETTERS = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')
NUMBERS = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
SYMBOLS = ('!', '#', '$', '%', '&', '(', ')', '*', '+')


def save_password():
    website = entry_website.get().strip().capitalize()
    user = entry_user.get().strip().lower()
    password = entry_password.get().strip()

    if website == '' or user == '' or password == '':

        messagebox.showerror(title='Error', message='Some fields are empty')

    else:

        if messagebox.askyesno(title=f"{website}'s password", message=f'Do you want to save this?'
                                                                      f'\nUser: {user}\nPassword: {password}'):

            try:
                with open('passwords_data.json', mode='r') as data:
                    loaded_data = json.load(data)

            except FileNotFoundError:
                with open('passwords_data.json', mode='w') as data:
                    json.dump({website: {user: {'password': password}}}, data, indent=4)

            else:

                try:
                    loaded_data[website].update({user: {'password': password}})
                except KeyError:
                    loaded_data.update({website: {user: {'password': password}}})
                    with open('passwords_data.json', mode='w') as data:
                        json.dump(loaded_data, data, indent=4)
                else:
                    with open('passwords_data.json', mode='w') as data:
                        json.dump(loaded_data, data, indent=4)

            finally:

                pyperclip.copy(password)

                entry_website.delete(0, tk.END)
                entry_user.delete(0, tk.END)
                entry_password.delete(0, tk.END)

                entry_website.focus()

                messagebox.showinfo(title='Password saved', message='Password saved successfully!'
                                                                    '\nPassword copy to clipboard')


def search_password():
    website = entry_website.get().strip().capitalize()
    user = entry_user.get().strip().lower()

    if website == '' or user == '':
        messagebox.showerror(title='Error', message='Some fields are empty')

    else:
        try:
            with open('passwords_data.json', mode='r') as data:
                data_loaded = json.load(data)
                messagebox.showinfo(title='Password Founded', message=f'{user}\nYour password is: '
                                                                      f'{data_loaded[website][user]["password"]}\n'
                                                                      'Password copy to clipboard')
        except (FileNotFoundError, KeyError):
            messagebox.showerror(title='Error', message=f'There is no password for {user} in {website}')
        else:
            pyperclip.copy(data_loaded[website][user]["password"])


def generate_password():
    generated_password = [choice(LETTERS) for _ in range(randint(8, 10))] + \
                         [choice(NUMBERS) for _ in range(randint(2, 4))] + \
                         [choice(SYMBOLS) for _ in range(randint(2, 4))]

    shuffle(generated_password)
    entry_password.delete(0, tk.END)
    entry_password.insert(0, "".join(generated_password))


windows = tk.Tk()
windows.title('Password Manager')
windows.config(pady=30, padx=50, bg=BACKGROUND)

canvas = tk.Canvas(width=200, height=200, bg=BACKGROUND, highlightthickness=0)
logo = tk.PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=logo)
canvas.grid(column=0, row=0, columnspan=3)

label_user = tk.Label(text='Email/Username', bg=BACKGROUND)
label_user.grid(column=0, row=1, pady=(10, 0))

entry_user = tk.Entry(width=50, relief=tk.FLAT, highlightthickness=1,
                      highlightcolor=BORDER, highlightbackground=BORDER)
entry_user.grid(column=1, row=1, columnspan=2, sticky='W', padx=(10, 0), pady=(10, 0))

label_website = tk.Label(text='Website', bg=BACKGROUND)
label_website.grid(column=0, row=2, pady=(10, 0))

entry_website = tk.Entry(width=30, relief=tk.FLAT, highlightthickness=1,
                         highlightcolor=BORDER, highlightbackground=BORDER)
entry_website.grid(column=1, row=2, sticky='W', padx=(10, 0), pady=(10, 0))
entry_website.focus()

button_search = tk.Button(text='Search Password', relief=tk.FLAT, command=search_password,
                          width=14, background=BUTTONS, activebackground=BUTTONS, fg='white', activeforeground='white')
button_search.grid(column=2, row=2, sticky='W', pady=(10, 0), padx=(5, 0), ipadx=1)

label_password = tk.Label(text='Password', bg=BACKGROUND)
label_password.grid(column=0, row=3, pady=(10, 0))

entry_password = tk.Entry(width=30, relief=tk.FLAT, highlightthickness=1,
                          highlightcolor=BORDER, highlightbackground=BORDER)
entry_password.grid(column=1, row=3, sticky='W', padx=(10, 0), pady=(10, 0))

button_password = tk.Button(text='Generate Password', relief=tk.FLAT, command=generate_password,
                            background=BUTTONS, activebackground=BUTTONS, fg='white', activeforeground='white')
button_password.grid(column=2, row=3, sticky='W', pady=(10, 0), padx=(5, 0))

button_add = tk.Button(text='Add', width=42, relief=tk.FLAT, command=save_password,
                       background=BUTTONS, activebackground=BUTTONS, fg='white', activeforeground='white')
button_add.grid(column=1, row=4, columnspan=2, sticky='W', padx=(10, 0), pady=(10, 0))

windows.mainloop()
