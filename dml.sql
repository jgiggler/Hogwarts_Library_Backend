-- INSERT entries into every table individually.
-- SELECT query for every table
-- one DELETE 
-- one UPDATE 
-- add and remove from one many-to-many 
-- add to all relationships 

-- All queries that use the character ":" represent that the variables
-- will have data from the backend

-- Books 
    -- get all book information for the Browse Books page
SELECT bookISBN, bookTitle, bookGenre, copyTotal, copyAvailable, bookCost FROM Books
ORDER BY bookGenre, bookTitle;
    -- add a new Book
INSERT INTO Books (bookISBN, bookTitle, bookGenre, copyTotal, copyAvailable, bookCost) VALUES
(:isbnInput, :titleInput, :genreInput, :totalInput, :availableInput, :costInput);
    -- update a Book
UPDATE Books SET bookISBN = :isbnInput, bookTitle= :titleInput, bookGenre= :genreInput,
 copyTotal = :totalInput, copyAvailable = :availableInput, bookCost = :costInput WHERE
id= :book_ISBN_from_table;
    -- Delete a Book
DELETE FROM Books where id = :book_ISBN_from_table;


-- Authors
    -- SELECT all Author information
SELECT authorID, authorFirst, authorLast FROM Authors
ORDER BY authorID;
    -- INSERT into Author
INSERT INTO Authors (authorFirst, authorLast) VALUES
(:fnameInput, :lnameInput);
    -- UPDATE a Book
UPDATE Authors SET authorFirst = :fnameInput, authorLast = :lnameInput WHERE
id= :author_ID_from_table;
    -- Delete an Author
DELETE FROM Authors where id = :author_ID_from_table;



-- Members
    -- SELECT all Member information
SELECT memberID, email, phoneNumber, address, classYear FROM Members
ORDER BY memberID;
    -- INSERT into Members
INSERT INTO Members (memberID, email, phoneNumber, address, classYear) VALUES
(:memberID, :memberEmail, :memberPhoneNumber, :memberAddress, :memberClassYear);
    -- DELETE member
DELETE FROM Members WHERE id = :member_ID_from_table;
    -- UPDATE member 
UPDATE Members SET memberID = :memberIDInput, email= :emailInput, phoneNumber= :phoneNumberInput,
 address = :addressInput, classYear = :classYearInput  WHERE id= :member_ID_from_table;


-- Reservations
    -- SELECT all Reservation information
SELECT reservationID, memberID, bookISBN, statusCode, reservationDate FROM Reservations
ORDER BY reservationID;
    -- INSERT into Reservations, bookISBN can be null becuase if reservation status is NA then no book has been checked out 
INSERT INTO Reservations (memberID, bookISBN, statusCode, reservationDate) VALUES
(:member_ID, :book_ISBN, :status_code, :reservation_date);
    -- DELETE reservation
DELETE FROM Reservations WHERE reservationID = :reservation_ID_from_table;
    -- UPDATE reservation
UPDATE Reservations SET bookISBN= :bookISBNInput, statusCode= :statusCodeInput,
 reservationDate = :reservationDateInput, WHERE reservationID= :reservation_ID_from_table;


-- get all member's data to populate a dropdown for associating with a reservation
SELECT member_id AS memberID, email, phoneNumber, address, classYear FROM Members;

-- get all reservations to populate a dropdown for associating with members
SELECT reservation_id AS reservationID, memberID, bookISBN, statusCode, reservationDate FROM Reservations;

-- associate a Author with a Book (M-to-M relationship addition)
INSERT INTO books_authors (authorID, bookISBN) VALUES
(:book_ISBN_from_table_Input, :author_ID_from_table_Input);

-- dis-associate a certificate from a person (M-to-M relationship deletion)
DELETE FROM books_authors WHERE authorID
= :author_ID_selected_from_table AND bookISBN
= :book_ISBN_from_table;



