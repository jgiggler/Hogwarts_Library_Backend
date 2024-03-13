SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;

-- records the details of an author for a book
create or replace table Authors (
    authorID int AUTO_INCREMENT unique not NULL,
    authorFirst varchar(60) not NULL,
    authorLast varchar(60) not NUll,
    primary key (authorID)
);

-- records the details of books in the library
create or replace table Books (
    bookISBN varchar(50) unique not NULL,   
    bookTitle varchar(50) not NULL,
    bookGenre varchar(50),
    copyTotal int not NULL,
    copyAvailable int not NULL,
    bookCost decimal(19,2),
    primary key (bookISBN)
);

-- records the details of the library members 
create or replace table Members (
    memberID int(11) AUTO_INCREMENT unique not Null,
    email varchar(50) not NULL,
    phoneNumber varchar(50) not NULL, 
    address varchar(100) not NUll,
    classYear int(6) not NULL, 
    primary key (memberID)
);

-- create statuses category table 
create or replace table Statuses (
    statusCode varchar(50) not NULL,
    description varchar(255) not NULL,
    primary key (statusCode)
);

-- records the details of a specific book reservation by a member
create or replace table Reservations (
    reservationID int(11) AUTO_INCREMENT unique not NULL, 
    memberID int(11),
    bookISBN varchar(50),
    statusCode varchar(50) not NULL,
    reservationDate DATE,
    primary key (reservationID),
    foreign key (memberID) references Members (memberID) ON UPDATE CASCADE ON DELETE CASCADE,
    foreign key (bookISBN) references Books (bookISBN) ON UPDATE CASCADE ON DELETE CASCADE,
    foreign key (statusCode) references Statuses (statusCode)  
);

-- create intersection table between books and authors
create or replace table books_authors (
    authorID int(11),
    bookISBN varchar(50),  
    foreign key (bookISBN) references Books (bookISBN) ON UPDATE CASCADE ON DELETE CASCADE,
    foreign key (authorID) references Authors (authorID) ON DELETE CASCADE 
);

-- insert authors into the authors table
insert into Authors (authorFirst, authorLast)
values
    ("Harry", "Potter"),
    ("J.K.", "Rowling"),
    ("F. Scott", "Fitzgerald"),
    ("Orson Scott", "Card"),
    ("Albus", "Dumbledore")
;

-- insert data into books table 
insert into Books (bookISBN, bookTitle, bookGenre, copyTotal, copyAvailable, bookCost)
values 
('9781408855652', "Harry Potter: Philosopher's Stone", 'Fantasy', 30, 10, 24.99),
('439064872', "Harry Potter: Chamber of Secrets", "Fantasy", 28, 25, 25.00),
('9780333791035', "The Great Gatsby", "Historical Fiction", 20, 15, 12.00),
('9780812550702', "Ender's Game", "Science Fiction", 10, 3, 10.00)
;

-- insert category types into the status category table
insert into Statuses (statusCode, description)
values 
("RES", "Currently reserved."),
("RET", "Returned to library."),
("WAIT", "Waitlisted for reservation.")
;

-- insert data into reservations table
insert into Reservations (memberID, bookISBN, statusCode, reservationDate)
values
(1,"9781408855652", "RES", '2023-09-12'),
(1,"439064872", "RET", '2023-09-12'),
(1,"9780333791035", "RES", '2023-12-12'),
(2,"9780812550702", "RET", '2023-01-12')
;

-- insert members into the members table
insert into Members(email, phoneNumber, address, classYear)
values
    ("nevillelong@hogwarts.edu", "482-986-3846", "Surrey, England", 3),
    ("ronweasley@hogwarts.edu", "765-987-1010", "The Burrow, Devon, England", 5),
    ("lunalove@hogwarts.edu", "654-852-2222", "Lovegood Manor, Bath, England", 3),
    ("malfoylucius@hogwarts.edu", "121-987-0004", "Malfoy Manor, York, England", 6)
;

-- insert members into the members table
insert into books_authors(authorID, bookISBN)
values
    (2, '9781408855652'),
    (2, '439064872'),
    (3, '9780333791035'),
    (4, '9780812550702')
;

select * from Authors;
select * from Books;
select * from Members;
select * from Reservations;
select * from books_authors;
select * from Statuses;

SET FOREIGN_KEY_CHECKS=1;
COMMIT;