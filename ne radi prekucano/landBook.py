from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox

con = sqlite3.connect('libary.db')
cur = con.cursor()
class GiveBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.title("Lend Book")
        self.resizable(False,False)
       
        self.book_id=int(given_id)
        print(type(given_id))
        self.book_id=int(given_id)
        
        query = "SELECT * FROM books WHERE book_status = 0"
        books = cur.execute(query).fetchall()
        book_list = []
        for book in books:
            book_list.apent(str(book[0])+"-"+book[1])
            
        query2 = "SELECT * FROM members"
        members = cur.execute(query2).fetchall()
        member_list=[]
        for member in members:
            member_list.append(str(membber[0])+"-"+member[1])
            
        
        self.topFrame = Frame(self, height=150)
        self.topFrame.pack(fill=X)
        
        self.bottomFrame = Frame(self, height=600)
        self.bottomFrame.pack(fill=X)
                       
        self.top_image = PhotoImage(file='icons/addperson.png')
        top_image_lbl = Label(self.topFrame, image=self.top_image)
        top_image_lbl.place(x=120, y=10)
        heading = Label(self.topFrame, text='Add Person', font='arial 22 bold', fg='#003f8a', bg='white')
        heading.place(x=290, y=60)
        
        self.book_name = StringVar()
        self.lbl_name = Label(self.bottomFrame, text="Book: ", font=("Arial", 15, "bold"))
        self.lbl_name.place(x=40, y=40)
        self.combo_name = ttk.Combobox(self.bottomFrame ,textvariable=self.book_name)
        self.combo_name["values"] = book_list
        self.combo_name.current(self.book_id-1)
        self.combo_name.place(x = 150,y = 45)
        
        
        
        self.member_name = StringVar()
        self.lbl_phone = Label(self.bottomFrame, text="Member: ", font=("Arial", 15, "bold"))
        self.lbl_phone.place(x=40, y=80)
        
        self.combo_member = ttk.Combobox(self.bottomFrame, textvariable=self.member_name)
        self.combo_member["values"] = member_list
        self.combo_member.place(x=150, y=85)
        
       
        button = Button(self.bottomFrame,text= 'Lend book',command = self.lendBook)
        
        button.place(x=220,y = 120)

    def lendBook(self):
        book_name = self.book_name.get()
        member_name = self.member_name.get()
        
        if (book_name and member_name !=""):
            try:
                query="INSERT INTO 'borrows'(book_id, member_id), VALUES(?,?)"
                cur.execute(query,(book_name, member_name))
                con.commit()
                messagebox.showinfo("success","succeassfully added to database")
                cur.execute("UPDATE books SET books_status = ? WHERE book_id = ?",(1,self.book_id))
                con.commit()
            except:
                messagebox.showerror("Error", "Can't add to database")
                
        else:
            messagebox.showerror("Error", "Fields can't be empty")











