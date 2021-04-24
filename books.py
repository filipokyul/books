from sys import argv
import mysql.connector

def select_author(author: str) -> tuple:
    sql_author = "SELECT id FROM author WHERE author = %s"
    sql_data = (author,)
    cursor.execute(sql_author, sql_data)
    return cursor.fetchone()

def select_genre(genre: list) -> list:
    format_strings = ','.join(['%s'] * len(genre))
    cursor.execute("SELECT id, genre FROM genre WHERE genre in (%s)" % format_strings, tuple(genre))
    return cursor.fetchall()

def create(author: str, genre: list, name: str, book_number: int):
    author_id = select_author(author)
    if author_id is None:
        print("author is not here!")
        cursor.execute(("INSERT INTO author(author) VALUES(%s)"),
                       (author,))
        cnx.commit()
        author_id = select_author(author)
    author_id = author_id[0]

    cursor.execute(("INSERT INTO main(name,author_id,number) VALUES(%s,%s,%s)"),
                   (name, author_id, book_number))
    cnx.commit()
    sql_book = "SELECT id FROM main WHERE name = %s"
    sql_data = (name,)
    cursor.execute(sql_book, sql_data)
    book_id = cursor.fetchone()[0]

    if not genre:
        genre_message = 'не указан'
    else:
        genre_message = genre
        genre_data = select_genre(genre)

        len_genre_data = len(genre_data)
        len_genre = len(genre)
        old_genres = []
        for i in range(0, len_genre):
            for j in range(0, len_genre_data):
                if genre[i] == genre_data[j][1]:
                    old_genres.append(genre[i])
        set1 = set(genre)
        set2 = set(old_genres)
        new_genres = list(set1.difference(set2))

        if new_genres:
            print("genre is not here!")
            sql = """INSERT INTO genre(genre) VALUES ( %s )"""
            val = []
            for i in range(0, len(new_genres)):
                x = [new_genres[i]]
                val.append(tuple(x))
            cursor.executemany(sql, val)
            cnx.commit()
            format_strings = ','.join(['%s'] * len(new_genres))
            cursor.execute("SELECT id FROM genre WHERE genre in (%s)" % format_strings, tuple(new_genres))
            new_genres_ids = cursor.fetchall()
            new_genres_ids2 = []
            for i in range(0, len(new_genres_ids)):
                new_genres_ids2.append(new_genres_ids[i][0])
        old_genres_ids = []
        for i in range(0, len(genre_data)):
            old_genres_ids.append(genre_data[i][0])
        if new_genres:
            genres_ids = old_genres_ids + new_genres_ids2
        else:
            genres_ids = old_genres_ids

        sql_genre_book = """INSERT INTO genre_book(genre_id,book_id) VALUES ( %s, %s )"""
        val_genre_book = []
        for i in range(0, len(genres_ids)):
            val_genre_book1 = (genres_ids[i], int(book_id))
            val_genre_book.append(val_genre_book1)
        cursor.executemany(sql_genre_book, val_genre_book)
        cnx.commit()

    print("Книга номер", book_id, ":\nназвание -", name,
          "\nавтор -", author, "\nколичество книг -", book_number, "\nжанр -", genre_message )

def delete(name:str):
    sql_delete = "DELETE FROM main WHERE id = %s"
    sql_data = (name,)
    cursor.execute(sql_delete, sql_data)
    cnx.commit()
    print("Книга номер", name, "удалена")

def update(number: int, field: str, value: str):

    if field == 'id':
        print("Изменнения id запрещены!!!")
    else:
        if field == 'genre':
            sql_show_book_id = "SELECT id FROM main WHERE main.id = %s"
            sql_data = (number,)
            cursor.execute(sql_show_book_id, sql_data)
            row = cursor.fetchall()
            if row == []:
                print("Такой книги в наличии нет!")
                exit()
            else:
                book_id = row[0][0]
                sql_show_genre_id = "SELECT id FROM genre WHERE genre = %s"
                sql_data = (value,)
                cursor.execute(sql_show_genre_id, sql_data)
                row1 = cursor.fetchall()
                if row1 == []:
                    sql_insert_genre = "INSERT INTO genre(genre) VALUES ( %s )"
                    sql_data = (value,)
                    cursor.execute(sql_insert_genre, sql_data)
                    cnx.commit()
                    sql_show_genre_id = "SELECT id FROM genre WHERE genre = %s"
                    sql_data = (value,)
                    cursor.execute(sql_show_genre_id, sql_data)
                    row1 = cursor.fetchall()
                genre_id = row1[0][0]
                sql_delete = "DELETE FROM genre_book WHERE book_id = %s"
                sql_data = (book_id,)
                cursor.execute(sql_delete, sql_data)
                cnx.commit()
                sql_insert_genre_book = "INSERT INTO genre_book(genre_id,book_id) VALUES ( %s, %s )"
                sql_data = (genre_id,book_id)
                cursor.execute(sql_insert_genre_book, sql_data)
                cnx.commit()
        else:
            if field == 'author':
                sql_update = "UPDATE author" \
                         " INNER JOIN main ON author.id = main.author_id" \
                         " SET author = %s" \
                         " WHERE main.id = %s"
            elif field == 'name' or field == 'number':
                sql_update = "UPDATE main SET " + field + " = %s WHERE id = %s"
            else:
                print('Something is completely wrong')
                exit()
            sql_data = (value, number,)
            cursor.execute(sql_update, sql_data)
            cnx.commit()
        print("Информация о книге номер ", number, "изменена.")
        show_book(number)

def show_book(book_id: int):
    sql_show_book = "SELECT * FROM main " \
                    "INNER JOIN author ON main.author_id = author.id " \
                    "LEFT JOIN genre_book ON main.id = genre_book.book_id " \
                    "LEFT JOIN genre ON genre_book.genre_id = genre.id " \
                    "WHERE main.id = %s"
    sql_data = (book_id,)
    cursor.execute(sql_show_book, sql_data)
    row = cursor.fetchall()
    book_id = row[0][0]
    name = row[0][1]
    author = row[0][5]
    books_number = row[0][3]
    genre = []
    for x in range(0,len(row)):
        genre.append(row[x][11])
    if genre == [None]:
        genre = 'не указан'

    print("Информация о книге номер", book_id, ":\nназвание -", name,
          "\nавтор -", author,"\nколичество книг -", books_number, "\nжанр -", genre )

def books_number():
    sql_books_number = "SELECT name, number FROM main"
    cursor.execute(sql_books_number)
    rows = cursor.fetchall()
    print(rows)
    print(sorted(rows, key=lambda x: x[1]))
    a = sorted(rows, key=lambda x: x[1])
    a.reverse()
    print("Книги,сортированные по количеству(в порядке убывания): \n", a)

def num_books_author(author: str):
    cursor.execute(("SELECT SUM(main.number) FROM main"
                    " INNER JOIN author ON main.author_id = author.id"
                    " WHERE author = %s"),(author,))
    sum_prev = cursor.fetchone()
    book_sum = sum_prev[0]
    print(book_sum)

def num_books_genre(genre):
    cursor.execute(("SELECT SUM(main.number) FROM main"
                    " INNER JOIN genre_book ON main.id = genre_book.book_id"
                    " INNER JOIN genre ON genre_book.genre_id = genre.id"
                    " WHERE genre = %s"), (genre,))
    sum_prev = cursor.fetchone()
    genre_book_sum = sum_prev[0]
    print(genre_book_sum)

cnx = mysql.connector.connect(user='yulia2', password='eda2',
                                host='127.0.0.1',
                                database='books')
cursor = cnx.cursor(buffered=True)
if str(argv[1]) == 'create':
    create(argv[3], argv[5:], argv[2], int(argv[4]))
elif str(argv[1]) == 'delete':
    delete(argv[2])
elif str(argv[1]) == 'update':
    update(int(argv[2]), argv[3], argv[4])
elif str(argv[1]) == 'show_book':
    show_book(int(argv[2]))
elif str(argv[1]) == 'books_number':
    books_number()
elif str(argv[1]) == 'num_books_author':
    num_books_author(argv[2])
elif str(argv[1]) == 'num_books_genre':
    num_books_genre(argv[2])
else:
    print('Something went wrong')
cursor.close()
cnx.close()