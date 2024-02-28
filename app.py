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

@app.route('/index')
def index():

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
            print(isbn, title, genre, copies, available, price)
            # account for null genre
            if genre == "":
                # mySQL query to insert a new person into bsg_people with our form inputs
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


# Listener
if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    app.run(port=4546, debug=True)
