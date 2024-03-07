# Citation for routes using render_template, redirect and showform() templates:
# Date: 2/27/2022
# Copied and Adapted from the course material provided for CS340 Developing in Flask module
# URL: https://github.com/osu-cs340-ecampus/flask-starter-app/tree/master/bsg_people_app

from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_ejazr'
app.config['MYSQL_PASSWORD'] = '4524' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_ejazr'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"


mysql = MySQL(app)


# Routes

# routes to index template if going to root
@app.route('/')
def root():

    return render_template("index.j2")

# routes to index template
@app.route('/index')
def index():

    return render_template("index.j2")

# route handles Browse and Insert functions for the books entity
@app.route("/books", methods=["POST", "GET"])
def books():
    # Separate out the request methods, in this case this is for a POST
    # insert a book into the Books entity
    if request.method == "POST":
        # fire off if user presses the Add Book button
        if request.form.get("addBook"):
            # grab user form inputs
            isbn = request.form["isbn"]
            title = request.form["title"]
            genre = request.form["genre"]
            copies = request.form["copies"]
            available = request.form["available"]
            price = request.form["price"]
            print(isbn, title, genre, copies, available, price)
            # account for null genre
            if genre == "":
                # mySQL query to insert a new book into Books with our form inputs
                query = "INSERT INTO Books (bookISBN, bookTitle, copyTotal, copyAvailable, bookCost) VALUES (%s, %s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (isbn, title, copies, available, price))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "INSERT INTO Books (bookISBN, bookTitle, bookGenre, copyTotal, copyAvailable, bookCost) VALUES (%s, %s, %s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (isbn, title, genre, copies, available, price))
                mysql.connection.commit()

            # redirect back to books page
            return redirect("/books")

    # Grab Books data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the books in Books
        query = "SELECT bookISBN, bookTitle, bookGenre, copyTotal, copyAvailable, bookCost FROM Books ORDER BY bookGenre, bookTitle;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render books page passing our query data and 
        return render_template("books.j2", data=data)


# route for delete functionality, deleting a book
# we want to pass the 'id' value of that book on button click (see HTML) via the route
@app.route("/delete_book/<int:id>")
def delete_book(id):
    
    # mySQL query to delete the book with our passed id
    query = "DELETE FROM Books WHERE bookISBN = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    # redirect back to books page
    return redirect("/books")

# route for edit functionality, updating the attributes of a book in Books
# similar to our delete route, we want to the pass the 'id' value of that book on button click (see HTML) via the route
@app.route("/edit_books/<int:id>", methods=["POST", "GET"])
def edit_books(id):
    if request.method == "GET":
        # mySQL query to grab the info of the book with our passed id
        query = "SELECT * FROM Books WHERE bookISBN = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render edit_books page passing our query data
        return render_template("edit_books.j2", data=data)

    if request.method == "POST":
        # fire off if user clicks the 'Edit Book' button
        
        if request.form.get("editBook"):
            # grab book form inputs
            
            id = request.form["bookISBN"]
            title= request.form["title"]
            genre = request.form["genre"]
            copyTotal = request.form["copyTotal"]
            copyAvailable = request.form["copyAvailable"]
            cost = request.form["cost"]
            print(id, title, genre)
            # account for null genre
            if genre == "NULL":
                query = "UPDATE Books SET bookISBN = %s, bookTitle = %s, bookGenre = NULL, copyTotal = %s, copyAvailable = %s, bookCost = %s WHERE bookISBN = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (id, title, copyTotal, copyAvailable, cost, id))
                mysql.connection.commit()

            # no null 
            else:
                
                query = "UPDATE Books SET bookISBN = %s, bookTitle = %s, bookGenre = %s, copyTotal = %s, copyAvailable = %s, bookCost = %s WHERE bookISBN = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (id, title, genre, copyTotal, copyAvailable, cost, id))
                mysql.connection.commit()

            # redirect back to books page after we execute the update query
            return redirect("/books")

# route handles Browse and Insert functions for the authors entity
@app.route("/authors", methods=["POST", "GET"])
def authors():
    # Separate out the request methods, in this case this is for a POST
    # insert an author into the Authors entity
    if request.method == "POST":
        # fire off if user presses the Add Book button
        if request.form.get("addAuthor"):
            authorFirst = request.form["authorFirst"]
            authorLast = request.form["authorLast"]
            print(authorFirst, authorLast)
            # account for null first name 
            if authorFirst == "":
                # mySQL query to insert a new author into Authors with our form inputs
                query = "INSERT INTO Authors (authorFirst, authorLast) VALUES (%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (authorFirst, authorLast))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "INSERT INTO Authors (authorFirst, authorLast) VALUES (%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (authorFirst, authorLast))
                mysql.connection.commit()

            # redirect back to authors page
            return redirect("/authors")

    # Grab Authors data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the authors in Authors
        query = "SELECT authorID, authorFirst, authorLast FROM Authors ORDER BY authorID;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render books page passing our query data and 
        return render_template("authors.j2", data=data)

# route handles Browse and Insert functions for the members entity
@app.route("/members", methods=["POST", "GET"])
def members():
    # Separate out the request methods, in this case this is for a POST
    # insert an author into the Members entity
    if request.method == "POST":
        # fire off if user presses the Add Book button
        if request.form.get("addMember"):
            email = request.form["email"]
            phone = request.form["phone"]
            address = request.form["address"]
            year = request.form["year"]
            print(email, phone, address, year)
            # account for null email
            if email == "":
                # mySQL query to insert a new author into Authors with our form inputs
                query = "INSERT INTO Members (email, phoneNumber, address, classYear) VALUES (%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (email, phone, address, year))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "INSERT INTO Members (email, phoneNumber, address, classYear) VALUES (%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (email, phone, address, year))
                mysql.connection.commit()

            # redirect back to members page
            return redirect("/members")

    # Grab Members data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the members in Members
        query = "SELECT memberID, email, phoneNumber, address, classYear FROM Members ORDER BY memberID;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render members page passing our query data and 
        return render_template("members.j2", data=data)

# route handles Browse and Insert functions for the reservations entity
@app.route("/reservations", methods=["POST", "GET"])
def reservations():
    # Separate out the request methods, in this case this is for a POST
    # insert an author into the Reservations entity
    if request.method == "POST":
        # fire off if user presses the Add Reservationbutton
        if request.form.get("addReservation"):
            memberId = request.form["memberId"]
            isbn = request.form["isbn"]
            code = request.form["code"]
            date = request.form["date"]
            print(memberId, isbn, code, date)
            # account for duplicate reservationId
            if memberId == "":
                # mySQL query to insert a new reservation into Reservations with our form inputs
                query = "INSERT INTO Reservations (memberID, bookISBN, statusCode, reservationDate) VALUES(%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (memberId, isbn, code, date))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "INSERT INTO Reservations (memberID, bookISBN, statusCode, reservationDate) VALUES(%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (memberId, isbn, code, date))
                mysql.connection.commit()

            # redirect back to reservations page
            return redirect("/reservations")

    # Grab Reservations data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the members in Members
        query = "SELECT reservationID, memberID, bookISBN, statusCode, reservationDate FROM Reservations ORDER BY reservationID;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        #dropdown for bookISBN 
        query = "SELECT bookISBN FROM Books;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        isbn = cur.fetchall()

        #dropdown for memberId
        query = "SELECT memberID FROM Members;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        memberId = cur.fetchall()

        # render reservations page passing our query data and 
        return render_template("reservations.j2", data=data, memberId=memberId, isbn=isbn)

# route handles Browse and Insert functions for the books_authors entity
@app.route("/books_authors", methods=['GET', 'POST'])
def books_authors():
# Separate out the request methods, in this case this is for a POST
    # insert a books_authors into the books_authors entity
    if request.method == "POST":
        if request.form.get("addBookAuthor"):
            authorID = request.form["authorID"]
            bookISBN = request.form["bookISBN"]
            print(authorID, bookISBN)

            if booksISBN == "":
                query = "INSERT INTO books_authors (authorID, bookISBN VALUES(%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (authorId, bookISBN))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "INSERT INTO books_authors (authorID, bookISBN) VALUES(%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (authorId, bookISBN))
                mysql.connection.commit()

            # redirect back to reservations page
            return redirect("/books_authors")

      # Grab books_authors data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the books_authors
        query = "SELECT authorID, bookISBN FROM books_authors;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # dropdwon for authorid 
        query = "SELECT authorID FROM Authors ORDER BY authorID;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        authorID = cur.fetchall()

        #dropdown for bookISBN 
        query = "SELECT bookISBN FROM Books;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        bookISBN = cur.fetchall()

        # render books_authors page passing our query data and 
        return render_template("books_authors.j2", authorID=authorID, bookISBN=bookISBN, data=data)

# route for delete functionality, deleting a book_author
# we want to pass the 'id' value of that book on button click (see HTML) via the route
@app.route("/delete_books_authors/<int:id>")
def delete_books_authors(id):
    
    # mySQL query to delete the book with our passed id
    query = "DELETE FROM books_authors WHERE authorID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id))
    mysql.connection.commit()

    # redirect back to books_authors page
    return redirect("/books_authors")

@app.route("/edit_books_authors/<int:id>", methods=["POST", "GET"])
def edit_books_authors(id):
    if request.method == "GET":
        # mySQL query to grab the info of the author with our passed id
        query = "SELECT * FROM books_authors WHERE authorID = %s" % (authorID)
        cur = mysql.connection.cursor()
        cur.execute(query)
        authorID = cur.fetchall()

        # render edit_books page passing our query data
        return render_template("edit_books_authors.j2", authorID=authorID)

    if request.method == "POST":
        # fire off if user clicks the 'Edit' button
        
        if request.form.get("editBookAuthor"):
            authorID = request.form["authorID"]
            bookISBN = request.form["bookISBN"]
            print(authorID, bookISBN)

            # account for null genre
            if bookISBN == "NULL":
                query = "UPDATE books_authors SET bookISBN = NULL WHERE authorID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (bookISBN, authorID))
                mysql.connection.commit()

            # no null 
            else:
                query = "UPDATE books_authors SET authorID = %s, bookISBN = %s WHERE authorID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (authorID, bookISBN))
                mysql.connection.commit()

            # redirect back to books page after we execute the update query
            return redirect("/books_authors")


@app.route("/statuses")
def statuses():
    return render_template("statuses.j2")
    

# Listener
if __name__ == "__main__":

    app.run(port=4546, debug=True)
