from sys import argv
import mysql.connector

cnx = mysql.connector.connect(user='yulia2', password='eda2',
                                host='127.0.0.1',
                                database='books')
cursor = cnx.cursor()

sql_update = "UPDATE author.author" \
            " INNER JOIN main ON author.id = main.author_id" \
            " SET author = %s" \
            " WHERE main.id = %s"
sql_data = (value, number,)
cursor.execute(sql_update, sql_data)
cnx.commit()


"UPDATE author.author INNER JOIN main ON author.id = main.author_id" \
                         " SET author = %s" \
                         " WHERE main.id = %s"
"""if not argv[1:]:
    print("Whatever")
else:
    for x in range(0, len(argv[1:])):
        sql_genre = "SELECT id FROM genre WHERE genre = %s"
        sql_data = (argv[1:][x],)
        cursor.execute(sql_genre, sql_data)
        genre_id = cursor.fetchone()
        print(genre_id)
        genre_id_list.append(genre_id)
    print(genre_id_list)
"""
"""sql_author = "SELECT id FROM author WHERE author = %s"
sql_data = (argv[1],)
cursor.execute(sql_author, sql_data)
author_id = cursor.fetchone()
cursor.execute(("SELECT SUM(number) FROM main WHERE author_id = %s"),
                   (author_id))
for x in cursor:
    book_sum = x[0]
print(book_sum)"""
#books_sum = cursor.fetchone
#print(books_sum)

"""if genre_id is None:
    print("It is not here!")
    cursor.execute(("INSERT INTO genre(genre) VALUES(%s,)"),
                   (argv[5], ))
    select_genre()
    author_id = select_author()
author_id = author_id[0]
cursor.execute(("INSERT INTO main(name,author_id,number) VALUES(%s,%s,%s)"),
               (argv[2], author_id, argv[4]))
print("Книга", argv[2], "создана")
"""
"""
sql_author = "SELECT id FROM author WHERE author = %s"
sql_data = (argv[1],)
cursor.execute(sql_author, sql_data)
author_id = cursor.fetchone()
author_id = author_id[0]
print(author_id)

"""
#cnx.commit()
cursor.close()
cnx.close()