import pickle
import requests
import base64
import os
from subprocess import call
from tkinter import TOP, W, Button, Checkbutton, Entry, Frame, Label, StringVar, Tk, IntVar


window = Tk()
user_base = ''


def submitData():
    userid = userid_var.get()
    apikey = apikey_var.get()
    if not userid or not apikey:
        errorlabel.config(
            text='please enter the required information', fg='red')

    else:
        sample_string = str(userid)+':'+str(apikey)
        sample_string_bytes = sample_string.encode("ascii")
        base64_bytes = base64.b64encode(sample_string_bytes)
        base64_string = base64_bytes.decode("ascii")

        headers = {
            'Authorization': 'Basic '+base64_string,
            'Host': 'picoworkers.com',
        }

        response = requests.get(
            'https://picoworkers.com/api/users/get-balances.php', headers=headers)

        errorlabel.config(text='loading', fg='green')

        try:
            if response.json()['message'] == 'Unauthorized':
                errorlabel.config(
                    text='Wrong information entered. Please try again.', fg='red')
                userid_var.set('')
                apikey_var.set('')
        except:
            setinfo()


def setinfo():
    # get request + set variables
    userid = userid_var.get()
    apikey = apikey_var.get()
    sample_string = str(userid)+':'+str(apikey)
    sample_string_bytes = sample_string.encode("ascii")
    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")
    global user_base
    user_base = base64_string
    headers = {
        'Authorization': 'Basic ' + user_base,
        'Host': 'picoworkers.com',
    }
    response = requests.get(
        'https://picoworkers.com/api/users/get-balances.php', headers=headers)
    errorlabel.config(text='loading', fg='green')
    earned = response.json()['earned']
    spendable = response.json()['spendable']

    # check login checkbox
    login_value = Checkbox_keep_logedin.get()
    if login_value == 1:

        with open('login_data.pkl', 'wb') as file:

            pickle.dump(login_value, file)

        with open('user_base.pkl', 'wb') as file:
            pickle.dump(user_base, file)
    else:
        pass

    # destroy previous window
    userid_entry.destroy()
    apikey_entry.destroy()
    userid_label.destroy()
    apikey_label.destroy()
    login_checkbox.destroy()
    submit_frame.destroy()
    submit_btn.destroy()
    errorlabel.destroy()
    exit_frame.destroy()

    # buid new window
    header.config(width=200, height=20, bg="#FFF3CF")
    Earned.config(text=f'Earned: {earned}', bg='#FFF3CF')
    Spendable.config(text=f'Spendable: {spendable}', bg='#FFF3CF')
    border.config(bg='#09FF01')
    exit_f = Frame(window, bg='#1A7CD1')
    exit_f.place(x=350, y=235)
    exit_btn = Button(master=exit_f, text='Exit', relief="groove",
                      bg="white", bd='0', command=window.destroy)
    exit_btn.pack(padx=2, pady=2)
    logout_btn.config(text='logout')
    # copy to clipboard btn
    copyToClipboard = Button(text='copyToClipboard ', command=(window.clipboard_clear(),
                                                               window.clipboard_append('i can has clipboardz?')))
    copyToClipboard.place(x=200, y=100)

    #
    refreshdata()


def refreshdata():
    headers = {
        'Authorization': 'Basic ' + user_base,
        'Host': 'picoworkers.com',
    }
    response = requests.get(
        'https://picoworkers.com/api/users/get-balances.php', headers=headers)
    earned = response.json()['earned']
    spendable = response.json()['spendable']
    Earned.config(text=f'Earned: {earned}', bg='#FFF3CF')
    Spendable.config(text=f'Spendable: {spendable}', bg='#FFF3CF')
    Spendable.after(1000, refreshdata)


def setting_page_from_loggedin():
    global user_base
    headers = {
        'Authorization': 'Basic ' + user_base,
        'Host': 'picoworkers.com',
    }
    response = requests.get(
        'https://picoworkers.com/api/users/get-balances.php', headers=headers)
    errorlabel.config(text='loading', fg='green')
    earned = response.json()['earned']
    spendable = response.json()['spendable']

    # destroy previous window
    userid_entry.destroy()
    apikey_entry.destroy()
    userid_label.destroy()
    apikey_label.destroy()
    login_checkbox.destroy()
    errorlabel.destroy()
    submit_frame.destroy()
    submit_btn.destroy()
    exit_frame.destroy()

    # buid new window
    header.config(width=200, height=20, bg="#FFF3CF")
    Earned.config(text=f'Earned: {earned}', bg='#FFF3CF')
    Spendable.config(text=f'Spendable: {spendable}', bg='#FFF3CF')
    border.config(bg='#09FF01')
    exit_f = Frame(window, bg='#1A7CD1')
    exit_f.place(x=350, y=235)
    exit_btn = Button(master=exit_f, text='Exit', relief="groove",
                      bg="white", bd='0', command=window.destroy)
    exit_btn.pack(padx=2, pady=2)
    logout_btn.config(text='logout')
# copy to clipboard btn
    copyToClipboard = Button(text='copyToClipboard ', command=(window.clipboard_clear(),
                                                               window.clipboard_append('i can has clipboardz?')))
    copyToClipboard.place(x=200, y=100)
    #
    refreshdata()


def check_login():

    try:
        with open('user_base.pkl', 'rb')as file:
            global user_base
            user_base = pickle.load(file)
            setting_page_from_loggedin()

    except IOError:
        pass


def check_user_login_data():
    try:
        with open('login_data.pkl', 'rb')as file:
            x = pickle.load(file)
            if x == 1:
                check_login()
            else:
                pass
    except IOError:
        pass


def logout():
    try:
        os.remove('login_data.pkl')
        os.remove('user_base.pkl')
    except:
        pass
    window.destroy()
    call(["python", "app.py"])


# window settings
window.title('Shaaban\'s Industries')
window.geometry('400x300')
window.minsize(width=400, height=300)
window.resizable(False, False)

# global variables
userid_var = StringVar()
apikey_var = StringVar()
Checkbox_keep_logedin = IntVar()

# header
header = Frame(window, relief='sunken')
header.pack(side=TOP,  expand=False, fill="x")
# header border-bottom
border = Frame(window, width=50000, height=3, bg=None)
border.place(x=0, y=35)

# earned - spendable
Earned = Label(master=header, text='', font=('Roboto', 12))
Earned.grid(row=0, column=0, padx=55, pady=5)
Spendable = Label(master=header, text='', bd='0', font=('Roboto', 12))
Spendable.grid(sticky=W, column=2, row=0)


# logout
logout_btn = Button(text='', command=logout)
logout_btn.place(x=250, y=235)

# UI login
userid_label = Label(window, text='user id:')
userid_entry = Entry(window, textvariable=userid_var,
                     font=('calibre', 10, 'normal'))

apikey_label = Label(window, text='user api key:')
apikey_entry = Entry(window, textvariable=apikey_var,
                     font=('calibre', 10, 'normal'))

login_checkbox = Checkbutton(window, text="keep me loggedin", variable=Checkbox_keep_logedin,
                             onvalue=1, offvalue=0, height=2, width=20)

userid_label.pack()
userid_entry.pack()
apikey_label.pack()
apikey_entry.pack()
login_checkbox.pack()


# error label
errorlabel = Label(window, text='', fg='red', bg=None, font=('Roboto', 12))
errorlabel.pack(pady=5)

# exit btn
exit_frame = Frame(window, bg='#1A7CD1')
exit_frame.place(x=250, y=235)
exit = Button(master=exit_frame, text='Exit', relief="groove",
              bg="white", bd='0', command=window.destroy)
exit.pack(padx=2, pady=2)

# submit info btn
submit_frame = Frame(window, bg='#1A7CD1')
submit_frame.place(x=310, y=235)
submit_btn = Button(master=submit_frame, text='Submit',
                    relief="groove", bg="white", bd='0', command=submitData)
submit_btn.pack(padx=2, pady=2)

check_user_login_data()

window.mainloop()
