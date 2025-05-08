# Base class
class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def get_info(self):
        return f"{self.title} by {self.author}, {self.year}"

# Derived class
class EBook(Book):
    def __init__(self, title, author, year, file_size_mb):
        super().__init__(title, author, year)
        self.file_size_mb = file_size_mb

    def get_info(self):
        return f"{super().get_info()} [E-Book, {self.file_size_mb}MB]"

# Library class
class Library:
    book_count = 0

    def __init__(self):
        self.books = []

    def add_books(self, book):
        self.books.append(book)
        Library.book_count += 1
        print(f"Book added: {book.get_info()}")

    def display_books(self):
        print("\nBooks available in the library:")
        for book in self.books:
            print(f"- {book.get_info()}")
        print(f"\nTotal books: {Library.book_count}")

# Example usage
if __name__ == "__main__":
    # Create some books
    b1 = Book("1984", "George Orwell", 1949)
    b2 = EBook("Digital Fortress", "Dan Brown", 1998, 2.5)

    # Create library and add books
    my_library = Library()
    my_library.add_books(b1)
    my_library.add_books(b2)

    # Display all books
    my_library.display_books()
