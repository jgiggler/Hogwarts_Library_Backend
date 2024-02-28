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
@app.route('/')
def root():

    return render_template("index.j2")

@app.route("/books", methods=["POST", "GET"])
def books():
    # Separate out the request methods, in this case this is for a POST
    # insert a person into the bsg_people entity
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

            # account for null genre
            if genre == "":
                # mySQL query to insert a new person into bsg_people with our form inputs
                query = "INSERT INTO Books (isbn, title, copies, available, price) VALUES (%s, %s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (isbn, title, copies, available, price))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "INSERT INTO Books (isbn, title, genre, copies, available, price) VALUES (%s, %s, %s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (isbn, title, genre, copies, available, price))
                mysql.connection.commit()

            # redirect back to people page
            return redirect("/books")

    # Grab bsg_people data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the people in bsg_people
        query = "SELECT bookISBN, bookTitle, bookGenre, copyTotal, copyAvailable, bookCost FROM Books GROUP BY bookGenre ORDER BY bookTitle;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render edit_people page passing our query data and 
        return render_template("books.j2", data=data)


# route for delete functionality, deleting a book
# we want to pass the 'id' value of that book on button click (see HTML) via the route
@app.route("/delete_book/<int:id>")
def delete_book(id):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM Books WHERE id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    # redirect back to people page
    return redirect("/books")

# route for edit functionality, updating the attributes of a book in Books
# similar to our delete route, we want to the pass the 'id' value of that book on button click (see HTML) via the route
@app.route("/edit_books/<int:id>", methods=["POST", "GET"])
def edit_books(id):
    if request.method == "GET":
        # mySQL query to grab the info of the book with our passed id
        query = "SELECT * FROM Books WHERE id = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab book id/name data for our dropdown
        query2 = "SELECT bookISBN FROM Books"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        book_data = cur.fetchall()

        # render edit_books page passing our query data
        return render_template("edit_books.j2", data=data, book=book_data)

    if request.method == "POST":
        # fire off if user clicks the 'Edit Book' button
        if request.form.get("Edit_Book"):
            # grab book form inputs
            id = request.form["bookISBN"]
            title= request.form["title"]
            genre = request.form["genre"]
            copyTotal = request.form["copyTotal"]
            copyAvailable = request.form["copyAvailable"]
            cost = request.form["cost"]

            # account for null genre
            if title == "" or title == "NULL":
                # mySQL query to update the attributes of book with our passed id value
                query = "UPDATE Books SET Books.title = NULL, Books.genre = %s, Books.copyTotal = %s, Books.copyAvailable = %s, Books.cost = %s WHERE bsg_people.id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (genre, copyTotal, copyAvailable, cost, id))
                mysql.connection.commit()

            # account for null genre
            elif genre == "NULL":
                query = "UPDATE Books SET Books.title = %s, Books.genre = NULL, Books.copyTotal = %s, Books.copyAvailable = %s, Books.cost = %s WHERE bsg_people.id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (title, copyTotal, copyAvailable, cost, id))
                mysql.connection.commit()

            # account for null copyTotal
            elif copyTotal == "0":
                query = "UPDATE Books SET Books.title = %s, Books.genre = %s, Books.copyTotal = NULL, Books.copyAvailable = %s, Books.cost = %s WHERE bsg_people.id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (title, genre, copyAvailable, cost, id))
                mysql.connection.commit()
            
            # account for null copyAvailable
            elif copyAvailable == "0":
                query = "UPDATE Books SET Books.title = %s, Books.genre = %s, Books.copyTotal = %s, Books.copyAvailable = NULL, Books.cost = %s WHERE bsg_people.id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (title, genre, copyTotal, cost, id))
                mysql.connection.commit()

            # account for null cost 
            elif cost == "0":
                query = "UPDATE Books SET Books.title = %s, Books.genre = %s, Books.copyTotal = %s, Books.copyAvailable = %s, Books.cost = NULL WHERE bsg_people.id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (title, genre, copyTotal, copyAvailable, id))
                mysql.connection.commit()

            # no null 
            else:
                query = "UPDATE Books SET Books.title = %s, Books.genre = %s, Books.copyTotal = %s, Books.copyAvailable = %s, Books.cost = %s WHERE bsg_people.id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (title, genre, copyTotal, copyAvailable, cost, id))
                mysql.connection.commit()

            # redirect back to books page after we execute the update query
            return redirect("/books")


# Listener
if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    app.run(port=4546, debug=True)
