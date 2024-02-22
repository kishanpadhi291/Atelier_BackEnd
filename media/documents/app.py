# Milestone-1 Miniproject
# ---------------------------------------------------------------------------------
# def add_movie(movie_list):
#     addmovie = input("Enter Movie name:")
#     genre = input("Enter genre of movie:")
#     movie_list.append({"Name": addmovie, "Genre": genre})
#     print("Movie added")


# def find_movie(movie_list):
#     find_movie = input("Enter Movie You want to find:")
#     for x in movie_list:
#         if x["Name"] == find_movie:
#             print("Got the movie")
#             print(x)


# def load_movie(movie_list):
#     for x in movie_list:
#         print(f'Name:{x["Name"]}')


# def menu(movie_list):
#     action = input(
#         "Enter a to add movies and l to load movies and f to find movies and q to quit:"
#     )
#     while action != "q":
#         if action == "a":
#             add_movie(movie_list)
#         elif action == "f":
#             find_movie(movie_list)
#         elif action == "l":
#             load_movie(movie_list)
#         else:
#             print("Select from the given action")
#         action = input(
#             "Enter a to add movies and l to load movies and f to find movies and q to quit:"
#         )


# Movie_list = [
#     {"Name": "Swades", "genre": "Rural"},
#     {"Name": "Sholay", "genre": "Rural"},
#     {"Name": "Jawan", "genre": "Star"},
# ]
# menu(Movie_list)

# Milestone-2 Miniproject with list
# ---------------------------------------------------------------------------------
# from utils import database
#
#
# def add_book():
#     addbook = input("Enter Book name:")
#     genre = input("Enter genre of book:")
#     database.add_books(addbook, genre)
#     print("Book added")
#
#
# def list_book():
#     book_list = database.list_books()
#     for x in book_list:
#         read = "No"
#         if x["Read"]:
#             read = "Yes"
#         print(f"Name:{x['Name']},  Genre:{x['Genre']},  Read:{read}")
#
#
# def read_book():
#     book_name = input("Enter Book name:")
#     database.read_books(book_name)
#     print("Book mark as read")
#
#
# def delete_book():
#     book_name = input("Enter Book name:")
#     database.delete_books(book_name)
#     print("Book deleted")
#
#
# def menu():
#     action = input(
#         "Enter a to add books and l to list books and r to mark book as read,d to delete book and q to quit:"
#     )
#     while action != "q":
#         if action == "a":
#             add_book()
#         elif action == "l":
#             list_book()
#         elif action == "r":
#             read_book()
#         elif action == "d":
#             delete_book()
#         else:
#             print("Select from the given action")
#         action = input(
#             "Enter a to add books and l to list books and r to mark book as read,d to delete book and q to quit:"
#         )
#
#
# menu()

# Milestone-2 csv file
# ---------------------------------------------------------------------------------
# from utils import database
#
#
# def add_book():
#     addbook = input("Enter Book name:")
#     genre = input("Enter genre of book:")
#     database.add_books(addbook, genre)
#     print("Book added")
#
#
# def list_book():
#     book_list = database.list_books()
#     for x in book_list:
#         read = "Yes" if x["Read"] == '1' else "No"
#         print(f"Name:{x['Name']},  Genre:{x['Genre']},  Read:{read}")
#
#
# def read_book():
#     book_name = input("Enter Book name:")
#     database.read_books(book_name)
#     print("Book mark as read")
#
#
# def delete_book():
#     book_name = input("Enter Book name:")
#     database.delete_books(book_name)
#     print("Book deleted")
#
# User_choice = '''
# Enter:
# -'a' to add a new book
# -'l' to list all books
# -'r' to mark a book as read
# -'d' to delete a book
# -'q' to quit
#
# Your Choice: '''
# def menu():
#     try:
#         database.create_book_table()
#     except FileExistsError:
#         pass
#
#     action = input(User_choice)
#     while action != "q":
#         if action == "a":
#             add_book()
#         elif action == "l":
#             list_book()
#         elif action == "r":
#             read_book()
#         elif action == "d":
#             delete_book()
#         else:
#             print("Select from the given action")
#         action = input(User_choice)
#
#
# menu()
# Milestone-2 csv file
# ---------------------------------------------------------------------------------
from utils import database, DatabaseConnection


def add_book():
    addbook = input("Enter Book name:")
    genre = input("Enter genre of book:")
    database.add_books(addbook, genre)
    print("Book added")


def list_book():
    book_list = database.list_books()
    for x in book_list:
        read = 'No' if x['Read'] == 0 else 'Yes'
        print(f"Name:{x['Name']},Genre:{x['Genre']},Read:{read}")


def read_book():
    book_name = input("Enter Book name:")
    database.read_books(book_name)
    print("Book mark as read")


def delete_book():
    book_name = input("Enter Book name:")
    database.delete_books(book_name)
    print("Book deleted")


User_choice = '''
Enter:
-'a' to add a new book
-'l' to list all books
-'r' to mark a book as read
-'d' to delete a book
-'q' to quit

Your Choice: '''
def menu():
    try:
        database.create_book_table()
    except FileExistsError:
        pass

    action = input(User_choice)
    while action != "q":
        if action == "a":
            add_book()
        elif action == "l":
            list_book()
        elif action == "r":
            read_book()
        elif action == "d":
            delete_book()
        else:
            print("Select from the given action")
        action = input(User_choice)


menu()