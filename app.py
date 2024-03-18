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
app.config['MYSQL_USER'] = 'cs340_ONID'
app.config['MYSQL_PASSWORD'] = 'XXXX' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_ONID'
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
            # first query, query to get the original book with original isbn, then check two variables og isbn and new isbn if og == new, can pass in either
            # if og != new then where bookisbn needs to be equal to origianl, set bookisbn == new 
            
            newISBN = request.form["newISBN"]
            oldISBN = id
            title= request.form["title"]
            genre = request.form["genre"]
            copyTotal = request.form["copyTotal"]
            copyAvailable = request.form["copyAvailable"]
            cost = request.form["cost"]
            print("oldISBN", oldISBN, "newISBN", newISBN)

            if genre == "NULL":
                query = "UPDATE Books SET bookISBN = %s, bookTitle = %s, bookGenre = NULL, copyTotal = %s, copyAvailable = %s, bookCost = %s WHERE bookISBN = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (newISBN, title, copyTotal, copyAvailable, cost, oldISBN))
                mysql.connection.commit()

            # no null 
            else:
                query = "UPDATE Books SET bookISBN = %s, bookTitle = %s, bookGenre = %s, copyTotal = %s, copyAvailable = %s, bookCost = %s WHERE bookISBN = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (newISBN, title, genre, copyTotal, copyAvailable, cost, oldISBN))
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
    
# route for delete functionality, deleting an author
# we want to pass the 'id' value of that author on button click (see HTML) via the route
@app.route("/delete_author/<int:id>")
def delete_author(id):
    
    # mySQL query to delete the book with our passed id
    query = "DELETE FROM Authors WHERE authorID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    # redirect back to books page
    return redirect("/authors")

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
    
@app.route("/delete_member/<int:id>")
def delete_member(id):
    
    # mySQL query to delete the member with our passed id
    query = "DELETE FROM Members WHERE memberID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    # redirect back to members page
    return redirect("/members")

# route handles Browse and Insert functions for the reservations entity
@app.route("/reservations", methods=["POST", "GET"])
def reservations():
    # Separate out the request methods, in this case this is for a POST
    # insert an author into the Reservations entity
    if request.method == "POST":
        # fire off if user presses the Add Reservation button
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

        #dropdown for statusCode
        query = "SELECT statusCode FROM Statuses;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        status = cur.fetchall()

        # render reservations page passing our query data and 
        return render_template("reservations.j2", data=data, memberId=memberId, isbn=isbn, status=status)
    
@app.route("/edit_reservations/<int:id>", methods=["POST", "GET"])
def edit_reservations(id):
    if request.method == "GET":

        query = "SELECT * FROM Reservations WHERE reservationID = %s" % (id)
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

        #dropdown for statusCode
        query = "SELECT statusCode FROM Statuses;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        status = cur.fetchall()

        return render_template("edit_reservations.j2", data=data, isbn=isbn, memberId=memberId, status=status)

    if request.method == "POST":
        # fire off if user clicks the 'Edit' button
        if request.form.get("editReservation"):
            id = request.form["reservationID"] 
            memberId = request.form["memberId"]
            isbn = request.form["isbn"]
            status = request.form["status"]
            date = request.form["date"]
            print(id, memberId, isbn, status, date)

            if isbn == "":
                query = "UPDATE Reservations SET memberID = %s, bookISBN = Null, statusCode = %s, reservationDate = %s WHERE reservationID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (memberId, status, date, id))
                mysql.connection.commit()
            else:

                query = "UPDATE Reservations SET memberID = %s, bookISBN = %s, statusCode = %s, reservationDate = %s WHERE reservationID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (memberId, isbn, status, date, id))
                mysql.connection.commit()

        return redirect("/reservations")


# route handles Browse and Insert functions for the books_authors entity
@app.route("/books_authors", methods=['GET', 'POST'])
def books_authors():
# Separate out the request methods, in this case this is for a POST
    # insert a books_authors into the books_authors entity
    if request.method == "POST":
        if request.form.get("addBookAuthor"):
            authorId = request.form["authorId"]
            isbn = request.form["isbn"]
            print(authorId, isbn)

            query = "INSERT INTO books_authors (authorID, bookISBN) VALUES(%s, %s);"
            cur = mysql.connection.cursor()
            cur.execute(query, (authorId, isbn))
            mysql.connection.commit()

            # redirect back to reservations page
        return redirect("/books_authors")

      # Grab books_authors data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the books_authors
        query = "SELECT authorID, bookISBN FROM books_authors ORDER BY bookISBN, authorID;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # dropdownn for authorid 
        query = "SELECT authorID FROM Authors ORDER BY authorID;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        authorId = cur.fetchall()

        #dropdown for bookISBN 
        query = "SELECT bookISBN FROM Books ORDER By bookISBN;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        isbn = cur.fetchall()

        # render books_authors page passing our query data and 
        return render_template("books_authors.j2", authorId=authorId, isbn=isbn, data=data)

# route for delete functionality, deleting a book_author
# we want to pass the 'id' value of that book on button click (see HTML) via the route
@app.route("/delete_books_authors/<int:id>/<int:isbn>")
def delete_books_authors(id, isbn):
    
    # mySQL query to delete the book with our passed id
    print(id, isbn)
    query = "DELETE FROM books_authors WHERE authorID = '%s' and bookISBN = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id, isbn))
    mysql.connection.commit()

    # redirect back to books_authors page
    return redirect("/books_authors")

@app.route("/edit_books_authors/<int:id>/<int:isbn>", methods=["POST", "GET"])
def edit_books_authors(id, isbn):
    if request.method == "GET":
        # mySQL query to grab the info of the author with our passed id
        query = "SELECT * FROM books_authors WHERE authorID = %s and bookISBN = %s" % (id, isbn)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        #dropdown for bookISBN 
        query = "SELECT bookISBN FROM Books;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        isbn = cur.fetchall()

        #dropdown for memberId
        query = "SELECT authorID FROM Authors;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        authorId = cur.fetchall()

        # render edit_books_authors page passing our query data
        return render_template("edit_books_authors.j2", data=data, isbn=isbn, authorId=authorId)

    if request.method == "POST":
        # fire off if user clicks the 'Edit' button
        if request.form.get("editBookAuthor"):
            authorId = request.form["authorId"]
            isbn = request.form["isbn"]
            print(authorId, isbn)

            query = "UPDATE books_authors SET authorID = %s, bookISBN = %s WHERE authorID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (authorId, isbn, authorId))
            mysql.connection.commit()

            # redirect back to books page after we execute the update query
        return redirect("/books_authors")


@app.route("/statuses")
def statuses():
    return render_template("statuses.j2")
    

# Listener
if __name__ == "__main__":

    app.run(port=4546, debug=True)
