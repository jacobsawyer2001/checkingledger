#***NOTE: This file creates a local file on the user's device and must be downloaded to work properly.***

from tkinter import *
from tkinter import messagebox
import csv
import pandas as pd
from pandas import Series
import pandastable as pt
import os

win = Tk()
win.title("Checking Ledger")
win.geometry("350x700")

date = StringVar()
desc = StringVar()
amt_in = StringVar()
amt_out = StringVar()
ind = StringVar()
#setting up Tkinter, modules, and user-input variables

with open('ledger.csv', 'a'):
    pass
    #creating a new ledger CSV if one does not exist
    #preserving old transactions when application is run again ('a')
    #***IF A PERMISSION ERROR ARISES, RUN THE PROGRAM AGAIN***

def new_file():
    with open('ledger.csv', 'w') as new_ledger:
        col = ['Date', 'Description', 'Deposit', 'Expense']
        writer = csv.DictWriter(new_ledger, fieldnames=col)
        writer.writeheader()
        #adding column headers to block EmptyDataErrors
        
if os.stat('ledger.csv').st_size == 0:
    new_file()

def save():
    try:
        date_s = int(date.get())
        date_str = str(date_s)
        y = date_str[0:4]
        m = date_str[4:6]
        d = date_str[6:8]
        if int(m) > 12 or int(d) > 31:
            messagebox.showerror('Error', 'Please enter a valid date.')
            date.set('')
            return
            #filtering out most invalid 8-number dates
        date_s = "{}-{}-{}".format(y, m, d)
        #checking for non-numerical characters within dates
        #separating years, months, and days with hyphens for legibility
    except ValueError:
        messagebox.showerror('Error', 'Please enter the date in the format YYYYMMDD with no delimiters.')
        date.set('')
        return
    desc_s = desc.get()
    #retrieving global variables to pass to Entry widgets
    try:
        if len(amt_in.get()) > 0 and len(amt_out.get()) > 0:
            messagebox.showerror('Error', 'Please enter deposits and withdrawals separately.')
            amt_in.set('')
            amt_out.set('')
            return
            #preventing both a deposit and withdrawal from being entered in the same transaction
            #runs first to prevent amt_out from being set to '' and allowing the program to continue 
        elif len(amt_in.get()) > 0:
            amt_in_s = float(amt_in.get())
            amt_in_f = f'{amt_in_s:.2f}'
            amt_out_f = ''
        elif len(amt_out.get()) > 0:
            amt_out_s = -1 * float(amt_out.get())
            amt_out_f = f'{amt_out_s:.2f}'
            amt_in_f = ''
            #rounding all transaction amounts to two decimal places
            #preventing decimal points from triggering non-numerical character errors
                #IMPORTANT: Expenses appear to be rounded to the nearest whole number,
                #but the decimals are still passed, as evidenced by the precise subtraction of the balance amount.'''
    except ValueError:
        messagebox.showerror('Error', 'Please enter only numerical and decimal characters within transaction fields.')
        amt_in.set('')
        amt_out.set('')
        return
        #checking for non-numerical characters within Deposit and Withdrawal fields
    if len(str(date_s)) != 10:
        messagebox.showerror('Error', 'Please enter the date in the format YYYYMMDD with no delimiters.')
        date.set('')
        #len of date_s set to 10 to account for hyphens
    elif len(amt_in_f) > 0:
        append(date_s, desc_s, amt_in_f, '')
    elif len(amt_out_f) > 0:
        append(date_s, desc_s, '', amt_out_f)
        #blocks that call append (and don't throw errors) are called after all error checks pass
    else:
        messagebox.showerror('Error', 'Please enter a deposit or withdrawal.')
        #ensuring a deposit OR withdrawal is entered (but NOT both)
        
def append(date_s, desc_s, amt_in_n, amt_out_n):
    df = pd.read_csv('ledger.csv', index_col=[0])
    #index_col[0] blocking the addition of new columns with each new entry
    new = pd.DataFrame(data={'Date': [date_s], 'Description': [desc_s], 'Deposit': [amt_in_n], 'Expense': [amt_out_n]})
    '''date column not shown when printing df'''
    new_df = pd.concat([df, new], ignore_index=True)
    #ignore_index=True allowing each entry to have a unique index number
    '''date column appended to the end but is otherwise fine'''
    #converting CSV into dataframe to append new transaction
    new_df.to_csv('ledger.csv')
    #overriding existing CSV with updated dataframe
    date.set('')
    desc.set('')
    amt_in.set('')
    amt_out.set('')

def remove():
    try:
        num_i = int(ind.get()) - 1
        #accounting for differences between the Tkinter table's indexing
        #(which begins at one) and Pandas' (which begins at zero)
    except ValueError:
        messagebox.showerror('Error', 'Please enter the numerical identifier of the record to remove.')
        ind.set('')
        return
        #checking for non-numerical index values
    df = pd.read_csv('ledger.csv', index_col=[0])
    try:
        df.drop([num_i], inplace=True)
    except KeyError:
        messagebox.showerror('Error', 'This record seems to have already withdrawn itself from the ledger!')
        ind.set('')
        return
        #checking for non-existent transactions
    df.to_csv('ledger.csv')
    #converting CSV floato dataframe to delete unwanted transaction
    #overriding existing CSV with updated dataframe
    ind.set('')

def load_csv():
    try:
        df = pd.read_csv('ledger.csv', index_col=[0])
        df = df.fillna(0)
        df['All Transactions'] = df['Deposit'] + df['Expense'].astype('float64')
        df['Balance'] = df['All Transactions'].cumsum()
        df = df[['Date', 'Description', 'Deposit', 'Expense', 'Balance']]
        #arranging columns in desired order
        #hiding 'All Transactions'
        show_df = Toplevel()
        show_df.title('Ledger')
        show_df.geometry('800x200')
        df_table = pt.Table(show_df, dataframe=df)
        df_table.show()
        #loading the ledger in a separate Tkinter window
    except:
        messagebox.showerror('Error', '''The ledger must exist before you can load it!''')
        ind.set('')

add_header = Label(win, text="Add Transaction", font=('Courier', 14)).place(x=20, y=20)
date_l = Label(win, text="Date (YYYYMMDD)", font=('Times New Roman', 12)).place(x=20, y=80)
date_e = Entry(win, textvariable=date, width=10).place(x=200, y=80)

desc_l = Label(win, text="Description", font=('Times New Roman', 12)).place(x=20, y=120)
desc_e = Entry(win, textvariable=desc, width=10).place(x=200, y=120)

amt_in_l = Label(win, text="Money In", font=('Times New Roman', 12)).place(x=20, y=160)
amt_in_e = Entry(win, textvariable=amt_in, width=10).place(x=200, y=160)

amt_out_l = Label(win, text="Money Out", font=('Times New Roman', 12)).place(x=20, y=200)
amt_out_e = Entry(win, textvariable=amt_out, width=10).place(x=200, y=200)

save_btn = Button(win, text="Add Transaction", font=('Times New Roman', 12), command=save).place(relx=.5, y=260, anchor=CENTER)

del_header = Label(win, text="Delete Transaction", font=('Courier', 14)).place(x=20, y=300)
del_l = Label(win, text="Index (Left-Most Column)", font=('Times New Roman', 12)).place(x=20, y=360)
del_entry = Entry(win, textvariable=ind, width=10).place(x=200, y=360)
del_btn = Button(win, text="Remove Transaction", font=('Times New Roman', 12), command=remove).place(relx=.5, y=420, anchor=CENTER)

load_l = Label(win, text="Display Ledger Entries", font=('Courier', 14)).place(x=20, y=460)
load_btn = Button(win, text="Load Ledger", font=('Times New Roman', 12), command=load_csv).place(relx=.5, y=520, anchor=CENTER)

del_all_l = Label(win, text="Clear Ledger", font=('Courier', 14)).place(x=20, y=560)
del_all_b = Button(win, text="Clear", font=('Times New Roman', 12), command=new_file).place(relx=.5, y=620, anchor=CENTER)
#configuring widgets

win.mainloop()
