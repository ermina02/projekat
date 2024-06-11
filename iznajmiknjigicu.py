import customtkinter as ctk
from tkinter import messagebox, END, Listbox
import sqlite3


def setup_database():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS available_books (id INTEGER PRIMARY KEY, title TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS rented_books (id INTEGER PRIMARY KEY, title TEXT)''')
    conn.commit()
    conn.close()


class Library:
    def __init__(self):
        setup_database()

    def rent_book(self, book_title):
        if book_title:
            conn = sqlite3.connect('library.db')
            c = conn.cursor()
            c.execute("INSERT INTO rented_books (title) VALUES (?)", (book_title,))
            c.execute("DELETE FROM available_books WHERE title = ?", (book_title,))
            conn.commit()
            conn.close()
            return True
        return False

    def return_book(self, book_title):
        if book_title:
            conn = sqlite3.connect('library.db')
            c = conn.cursor()
            c.execute("INSERT INTO available_books (title) VALUES (?)", (book_title,))
            c.execute("DELETE FROM rented_books WHERE title = ?", (book_title,))
            conn.commit()
            conn.close()
            return True
        return False

    def list_available_books(self):
        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("SELECT title FROM available_books")
        books = [row[0] for row in c.fetchall()]
        conn.close()
        return books

    def list_rented_books(self):
        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("SELECT title FROM rented_books")
        books = [row[0] for row in c.fetchall()]
        conn.close()
        return books


class LibraryGUI:
    def __init__(self, root, library):
        self.root = root
        self.library = library
        self.root.title("Biblioteka")

        ctk.set_appearance_mode("dark")  
        ctk.set_default_color_theme("dark-blue")  

        self.frame = ctk.CTkFrame(root)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.label = ctk.CTkLabel(self.frame, text="Naziv knjige:")
        self.label.pack(pady=5)

        self.entry = ctk.CTkEntry(self.frame)
        self.entry.pack(pady=5)

        self.rent_button = ctk.CTkButton(self.frame, text="Iznajmi knjigu", command=self.rent_book)
        self.rent_button.pack(pady=5)

        self.return_button = ctk.CTkButton(self.frame, text="Vrati knjigu", command=self.return_book)
        self.return_button.pack(pady=5)

        self.list_available_button = ctk.CTkButton(self.frame, text="Prikaz dostupnih knjiga", command=self.list_available_books)
        self.list_available_button.pack(pady=5)

        self.list_rented_button = ctk.CTkButton(self.frame, text="Prikaz iznajmljenih knjiga", command=self.list_rented_books)
        self.list_rented_button.pack(pady=5)

        self.books_listbox = Listbox(self.frame, bg="black", fg="white")
        self.books_listbox.pack(pady=5, fill="both", expand=True)

    def rent_book(self):
        book_title = self.entry.get()
        if self.library.rent_book(book_title):
            messagebox.showinfo("Uspeh", f'Knjiga "{book_title}" je iznajmljena.')
            self.entry.delete(0, END)
            self.update_listbox(self.library.list_available_books())
        else:
            messagebox.showwarning("Greška", "Morate uneti naziv knjige ili knjiga nije dostupna.")

    def return_book(self):
        selected_book = self.books_listbox.get(self.books_listbox.curselection())
        if self.library.return_book(selected_book):
            messagebox.showinfo("Uspeh", f'Knjiga "{selected_book}" je vraćena.')
            self.update_listbox(self.library.list_rented_books())
        else:
            messagebox.showwarning("Greška", "Knjiga nije pronađena ili nije iznajmljena.")

    def list_available_books(self):
        self.update_listbox(self.library.list_available_books())

    def list_rented_books(self):
        self.update_listbox(self.library.list_rented_books())

    def update_listbox(self, books):
        self.books_listbox.delete(0, END)
        for book in books:
            self.books_listbox.insert(END, book)

if __name__ == "__main__":
    root = ctk.CTk()
    library = Library()
    gui = LibraryGUI(root, library)
    root.mainloop()
