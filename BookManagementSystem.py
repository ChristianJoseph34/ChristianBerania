import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog

# Database Initialization
conn = sqlite3.connect("bookmanagementsystem")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year INTEGER NOT NULL,
        is_borrowed INTEGER NOT NULL DEFAULT 0
    )
    """)
conn.commit()
conn.close()


class LoginScreen:
    def __init__(self, root, users):
        self.root = root
        self.users = users
        self.root.title("Login")
        self.root.geometry("400x450")
        self.root.config(bg="#f8f9fa")
        self.root.resizable(False, False)

        self.create_login_widgets()

    def create_login_widgets(self):
        self.login_frame = tk.Frame(self.root, bg="#f8f9fa")
        self.login_frame.pack(pady=20)

        tk.Label(self.login_frame, text="Login", font=("Arial", 20, "bold"), bg="#f8f9fa").pack(pady=10)

        tk.Label(self.login_frame, text="Username:", font=("Arial", 12), bg="#f8f9fa").pack(pady=5)
        self.username_entry = tk.Entry(self.login_frame, font=("Arial", 12), bd=2, relief="solid", highlightthickness=2, highlightcolor="#4CAF50")
        self.username_entry.pack(pady=5, ipadx=2, ipady=4)

        tk.Label(self.login_frame, text="Password:", font=("Arial", 12), bg="#f8f9fa").pack(pady=10)
        self.password_entry = tk.Entry(self.login_frame, show="*", font=("Arial", 12), bd=2, relief="solid", highlightthickness=2, highlightcolor="#4CAF50")
        self.password_entry.pack(pady=5, ipadx=2, ipady=4)

        self.login_button = tk.Button(self.login_frame, text="Login", font=("Arial", 12), width=20, bg="#4CAF50", fg="white", relief="flat", command=self.login)
        self.login_button.pack(pady=15)
        self.login_button.config(borderwidth=2, relief="solid", activebackground="#388E3C", activeforeground="white", padx=10)

        self.create_account_button = tk.Button(self.login_frame, text="Create Account", font=("Arial", 12), width=20, bg="#2196F3", fg="white", relief="flat", command=self.create_account)
        self.create_account_button.pack(pady=10)
        self.create_account_button.config(borderwidth=2, relief="solid", activebackground="#1976D2", activeforeground="white", padx=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        conn = sqlite3.connect("bookmanagementsystem")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            self.open_book_management_system()
        else:
            messagebox.showerror("Login Error", "Invalid username or password")

    def create_account(self):
        self.login_frame.destroy()
        self.create_account_screen = CreateAccountScreen(self.root, self.users)

    def open_book_management_system(self):
        self.root.destroy()
        root = tk.Tk()
        app = BookManagementSystem(root)
        root.mainloop()


class CreateAccountScreen:
    def __init__(self, root, users):
        self.root = root
        self.root.title("Create Account")
        self.root.geometry("450x500")
        self.root.config(bg="#ffffff")
        self.root.resizable(False, False)

        self.users = users


        self.create_account_widgets()

    def create_account_widgets(self):
        self.frame = tk.Frame(self.root, bg="#ffffff")
        self.frame.pack(pady=50)

        # Title label
        tk.Label(self.frame, text="Create Account", font=("Arial", 20, "bold"), bg="#ffffff").pack(pady=10)

        # Username entry
        tk.Label(self.frame, text="Username:", font=("Arial", 14), bg="#ffffff").pack(pady=5)
        self.username_entry = tk.Entry(self.frame, font=("Arial", 12), bd=2, relief="solid")
        self.username_entry.pack(pady=5, ipadx=5, ipady=5)

        # Password entry
        tk.Label(self.frame, text="Password:", font=("Arial", 14), bg="#ffffff").pack(pady=5)
        self.password_entry = tk.Entry(self.frame, show="*", font=("Arial", 12), bd=2, relief="solid")
        self.password_entry.pack(pady=5, ipadx=5, ipady=5)

        # Confirm Password entry
        tk.Label(self.frame, text="Confirm Password:", font=("Arial", 14), bg="#ffffff").pack(pady=5)
        self.confirm_password_entry = tk.Entry(self.frame, show="*", font=("Arial", 12), bd=2, relief="solid")
        self.confirm_password_entry.pack(pady=5, ipadx=5, ipady=5)

        # Create Account Button
        tk.Button(
            self.frame,
            text="Create Account",
            font=("Arial", 14),
            bg="#2196F3",
            fg="white",
            command=self.create_account
        ).pack(pady=20)

    def create_account(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required.")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        conn = sqlite3.connect("bookmanagementsystem")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Success", "Account created successfully!")
            self.root.destroy()  # Close the account creation window
            self.open_login_screen() 
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")
        finally:
            conn.close()

    def open_login_screen(self):
        login_root = tk.Tk()
        login_screen = LoginScreen(login_root, self.users)
        login_root.mainloop()

class BookManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Management System")
        self.root.geometry("800x600")
        self.root.config(bg="#e3f2fd")
        self.root.resizable(False, False)
        self.books = []

        self.create_widgets()

    def create_widgets(self):
        # Title Label
        self.title_label = tk.Label(
        self.root, text="Book Management System", font=("Helvetica", 24, "bold"), bg="#e3f2fd"
        )
        self.title_label.pack(pady=20)

        # Buttons Frame
        self.buttons_frame = tk.Frame(self.root, bg="#e3f2fd")
        self.buttons_frame.pack(pady=10)

        # Buttons
        button_style = {"font": ("Arial", 14), "width": 15, "bg": "#1976D2", "fg": "white", "relief": "solid"}

        self.add_button = tk.Button(self.buttons_frame, text="Add Book", command=self.add_book, **button_style)
        self.add_button.grid(row=0, column=0, padx=10, pady=10)

        self.view_button = tk.Button(self.buttons_frame, text="View Books", command=self.view_books, **button_style)
        self.view_button.grid(row=0, column=1, padx=10, pady=10)

        self.update_button = tk.Button(self.buttons_frame, text="Update Book", command=self.update_book, **button_style)
        self.update_button.grid(row=1, column=0, padx=10, pady=10)

        self.delete_button = tk.Button(self.buttons_frame, text="Delete Book", command=self.delete_book, **button_style)
        self.delete_button.grid(row=1, column=1, padx=10, pady=10)

        self.search_button = tk.Button(self.buttons_frame, text="Search Book", command=self.search_book, **button_style)
        self.search_button.grid(row=0, column=2, padx=10, pady=10)

        self.borrow_button = tk.Button(self.buttons_frame, text="Borrow Book", command=self.borrow_book, **button_style)
        self.borrow_button.grid(row=1, column=2, padx=10, pady=10)

        # Return Book Button
        self.return_button = tk.Button(self.buttons_frame, text="Return Book", command=self.return_book, **button_style)
        self.return_button.grid(row=2, column=1, padx=10, pady=10)

    def refresh_book_list(self):
        self.books_listbox.delete(0, tk.END)
        conn = sqlite3.connect("bookmanagementsystem")
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT title, author, year FROM books")
            books = cursor.fetchall()
            for book in books:
                self.books_listbox.insert(tk.END, f"{book[0]} by {book[1]} ({book[2]})")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            conn.close()


    def search_book(self):
        def perform_search():
            search_term = search_entry.get().strip().lower()
            if not search_term:
                error_label.config(text="Please enter a search term.")
                return

            conn = sqlite3.connect("bookmanagementsystem")
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    SELECT title, author, year FROM books
                    WHERE title LIKE ? OR author LIKE ? OR year LIKE ?
                """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
                books = cursor.fetchall()

                search_results.delete(0, tk.END)
                if books:
                    for book in books:
                        search_results.insert(tk.END, f"{book[0]} by {book[1]} ({book[2]})")
                    error_label.config(text="")
                else:
                    error_label.config(text="No matching books found.")
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")
            finally:
                conn.close()

        # Search Window
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Book")
        search_window.geometry("400x400")
        search_window.config(bg="#f8f9fa")
        search_window.resizable(False, False)

        # Search Input
        tk.Label(search_window, text="Search by Title, Author, or Year:", font=("Arial", 12), bg="#f8f9fa").pack(pady=10)
        search_entry = tk.Entry(search_window, font=("Arial", 12), width=30)
        search_entry.pack(pady=5)

        # Search Button
        tk.Button(
            search_window,
            text="Search",
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            command=perform_search,  # Correct the function call to `perform_search`
            relief="solid",
        ).pack(pady=10)

        # Error Label
        error_label = tk.Label(search_window, text="", font=("Arial", 10), fg="red", bg="#f8f9fa")
        error_label.pack(pady=5)

        # Search Results
        search_results = tk.Listbox(search_window, font=("Arial", 12), width=50, height=15, bg="#f8f9fa")
        search_results.pack(pady=10)


    def add_book(self):
        def submit():
            title = title_entry.get().strip()
            author = author_entry.get().strip()
            year = year_entry.get().strip()

            if not title or not author or not year.isdigit():
                error_label.config(text="All fields are required, and Year must be a number.")
                return

            # Insert the book directly into the database
            conn = sqlite3.connect("bookmanagementsystem")
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)", (title, author, int(year)))
                conn.commit()
                messagebox.showinfo("Success", "Book added successfully!")
                add_window.destroy()
                self.refresh_book_list()  # Refresh the list of books displayed
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")
            finally:
                conn.close()

        # Create a new window for adding a book
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Book")
        add_window.geometry("400x300")
        add_window.config(bg="#f8f9fa")
        add_window.resizable(False, False)

        # Title Input
        tk.Label(add_window, text="Title:", font=("Arial", 12), bg="#f8f9fa").pack(pady=5)
        title_entry = tk.Entry(add_window, font=("Arial", 12), width=30)
        title_entry.pack(pady=5)

        # Author Input
        tk.Label(add_window, text="Author:", font=("Arial", 12), bg="#f8f9fa").pack(pady=5)
        author_entry = tk.Entry(add_window, font=("Arial", 12), width=30)
        author_entry.pack(pady=5)

        # Year Input
        tk.Label(add_window, text="Year:", font=("Arial", 12), bg="#f8f9fa").pack(pady=5)
        year_entry = tk.Entry(add_window, font=("Arial", 12), width=30)
        year_entry.pack(pady=5)

        # Error Label
        error_label = tk.Label(add_window, text="", font=("Arial", 10), fg="red", bg="#f8f9fa")
        error_label.pack(pady=5)

        # Submit Button
        tk.Button(
            add_window,
            text="Submit",
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            command=submit,
            relief="solid",
        ).pack(pady=15)


    def view_books(self):
        # Create a new window for viewing books
        view_window = tk.Toplevel(self.root)
        view_window.title("View Books")
        view_window.geometry("800x400")  # Set a size for the window
        view_window.config(bg="#f8f9fa")
        view_window.resizable(False, False)

        # Create a Listbox for displaying books
        books_listbox = tk.Listbox(view_window, font=("Arial", 12), width=60, height=15, bg="#f8f9fa")
        books_listbox.pack(pady=10, padx=10, fill="both", expand=True)

        # Fetch and display books from the database
        conn = sqlite3.connect("bookmanagementsystem")
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT title, author, year, is_borrowed FROM books")
            books = cursor.fetchall()

            if books:
                for book in books:
                    availability = "Available" if book[3] == 0 else "Borrowed"
                    books_listbox.insert(tk.END, f"{book[0]} by {book[1]} ({book[2]}) - {availability}")
            else:
                messagebox.showinfo("No Books", "No books available.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            conn.close()

    def borrow_book(self):
        title_to_borrow = simpledialog.askstring("Input", "Enter the title of the book to borrow:")
        if not title_to_borrow:
            return

        conn = sqlite3.connect("bookmanagementsystem")
        cursor = conn.cursor()
        try:
            # Check if the book exists
            cursor.execute("SELECT * FROM books WHERE title = ?", (title_to_borrow,))
            book = cursor.fetchone()
            if not book:
                messagebox.showwarning("Book Not Found", "No book found with that title.")
                return

            # Check if the book is already borrowed
            if len(book) > 4 and book[4] == 1:
                messagebox.showwarning("Book Already Borrowed", "This book is already borrowed.")
                return

            # Borrow the book
            cursor.execute("UPDATE books SET is_borrowed = 1 WHERE id = ?", (book[0],))
            conn.commit()
            messagebox.showinfo("Success", "Book borrowed successfully!")
            self.refresh_book_list()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            conn.close()

    def return_book(self):
        title_to_return = simpledialog.askstring("Input", "Enter the title of the book to return:")
        if not title_to_return:
            return

        conn = sqlite3.connect("bookmanagementsystem")
        cursor = conn.cursor()
        try:
            # Check if the book exists
            cursor.execute("SELECT * FROM books WHERE title = ?", (title_to_return,))
            book = cursor.fetchone()
            if not book:
                messagebox.showwarning("Book Not Found", "No book found with that title.")
                return

            # Check if the book is already returned
            if len(book) > 4 and book[4] == 0:
                messagebox.showwarning("Book Already Returned", "This book is already returned.")
                return

            # Return the book
            cursor.execute("UPDATE books SET is_borrowed = 0 WHERE id = ?", (book[0],))
            conn.commit()
            messagebox.showinfo("Success", "Book returned successfully!")
            self.refresh_book_list()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            conn.close()


        # Borrow Book Button
        tk.Button(
            self.buttons_frame,
            text="Borrow Book",
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            command=self.borrow_book,
            relief="solid",
        ).grid(row=2, column=0, padx=10, pady=10)

        # Return Book Button
        tk.Button(
            self.buttons_frame,
            text="Return Book",
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            command=self.return_book,
            relief="solid",
        ).grid(row=2, column=1, padx=10, pady=10)

    def update_book(self):
        title_to_update = simpledialog.askstring("Input", "Enter the title of the book to update:")
        if not title_to_update:
            return

        conn = sqlite3.connect("book_management.db")
        cursor = conn.cursor()
        try:
            # Check if the book exists
            cursor.execute("SELECT * FROM books WHERE title = ?", (title_to_update,))
            book = cursor.fetchone()
            if not book:
                messagebox.showwarning("Book Not Found", "No book found with that title.")
                return

            # Get new details
            new_title = simpledialog.askstring("Input", f"Enter new title (current: {book[1]}):")
            new_author = simpledialog.askstring("Input", f"Enter new author (current: {book[2]}):")
            new_year = simpledialog.askinteger("Input", f"Enter new publication year (current: {book[3]}):")

            if new_title and new_author and new_year:
                cursor.execute("""
                    UPDATE books SET title = ?, author = ?, year = ? WHERE id = ?
                """, (new_title, new_author, new_year, book[0]))
                conn.commit()
                messagebox.showinfo("Success", "Book updated successfully!")
                self.refresh_book_list()
            else:
                messagebox.showerror("Error", "All fields are required.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            conn.close()

    def delete_book(self):
        title_to_delete = simpledialog.askstring("Input", "Enter the title of the book to delete:")
        if not title_to_delete:
            return

        conn = sqlite3.connect("bookmanagementsystem")
        cursor = conn.cursor()
        try:
            # Check if the book exists
            cursor.execute("SELECT * FROM books WHERE title = ?", (title_to_delete,))
            book = cursor.fetchone()
            if not book:
                messagebox.showwarning("Book Not Found", "No book found with that title.")
                return

            # Confirm deletion
            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{title_to_delete}'?")
            if confirm:
                cursor.execute("DELETE FROM books WHERE id = ?", (book[0],))
                conn.commit()
                messagebox.showinfo("Success", "Book deleted successfully!")
                self.refresh_book_list()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            conn.close()


if __name__ == "__main__":
    root = tk.Tk()
    users = {}
    app = LoginScreen(root,users)
    root.mainloop()
