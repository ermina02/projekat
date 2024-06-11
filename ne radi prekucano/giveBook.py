from tkinter import *
from tkinter import ttk
import sqlite3
#import addbook, addmember, giveBook
from tkinter import messagebox

con = sqlite3.connect('libary.db')
cur = con.cursor()

class Main(object):
    def __init__(self,master):
        self.master = master
        
        def displayStatisstics(evt):
            count_books=cur.execute("SELECT count(book_id) FROM books").fetchall()
            count_members = cur.execute("SELECT count(member_id) FROM members").fetchall()
            taken_books = cur.execute("SELECT count(book_status) FROM books WHERE book_status='taken'").fetchall()
            
            print(count_books)
            
            self.lbl_book_count.config(text="Total books: " + str(count_books[0][0]) + "books in libary")
            self.lbl_member_count.config(text="Total members: " + str(count_members[0][0]))
            self.lbl_taken_count.config(text="Taken books: " + str(taken_books[0][0]))
            displayBooks(self)
        
        def displayBooks(self):
            books = cur.execute("SELECT * FROM books").fetchall()
            count = 0
            
            self.list_books.delete(0, END)  
            for book in books:
                print(book)
                self.list_books.insert(count, str(book[0]) + "-" + book[1]) 
                count += 1
        
        def bookInfo(evt):
            value = str(self.list_books.get(self.list_books.curselection()))
            id = value.split("-")[0]
            book = cur.execute("SELECT * FROM books WHERE book_id=?", (id,))
            book_info = book.fetchall()
            print(book_info)
            
            self.list_details.delete(0, 'end') 
            self.list_details.insert(0, "Book Name : " + book_info[0][1])
            self.list_details.insert(1, "Author : " + book_info[0][2])
            self.list_details.insert(2, "Page : " + str(book_info[0][3]))
            self.list_details.insert(3, "Language : " + book_info[0][4])
            
            if book_info[0][5] == 0:
                self.list_details.insert(4, "Status : Available")
            else:
                self.list_details.insert(4, "Status : Not Available")
        
        def doubleClick(evt):
            global given_id
            value = str(self.list_books.get(self.list_books.curselection())) 
            given_id = value.split('-')[0]
            give_book = GiveBook()
        
        
        
        self.list_books.bind('<<ListboxSelect>>', bookInfo)
        self.tabs.bind('<NotebookTabChanged>', displayStatistics)
        #self.tabs.bind("<ButtonRealise-1", displayBooks)
        self.lst_books.bind('<Double-Button-1>', doubleClick)


    def giveBook(self):
        pass
class GiveBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.title("Lend Book")
        self.resizable(False,False)
        global given_id
        self.book_id=int(given_id)
        print(type(given_id))
        self.book_id=int(given_id)
        
        query = "SELECT * FROM books"
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
        heading = Label(self.topFrame, text='Lend a book', font='arial 22 bold', fg='#003f8a', bg='white')
        heading.place(x=290, y=60)
        
        self.book_name = StringVar()
        self.lbl_name = Label(self.bottomFrame, text="Book: ", font=("Arial", 15, "bold"))
        self.lbl_name.place(x=40, y=40)
        self.combo_name = ttk.Combobox(self.bottomFrame ,textvariable=self.book_name)
        self.combo_name["values"] = book_list
        
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
        self.book_id= book_name.split("-")[0]
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




def main():
    root = Tk()