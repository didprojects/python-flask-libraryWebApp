# Name: Didi Liu    Student Number: 1151952
from flask import Flask, render_template, request
from flask import redirect
from flask import url_for
import re
import datetime
import mysql.connector
from mysql.connector import FieldType
import connect

app = Flask(__name__)

dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

# home page
@app.route("/")
def home():
    return render_template("base.html")

@app.route("/listborrowers")
def listborrowers():
    connection = getCursor()
    connection.execute("SELECT * FROM borrowers;")
    borrowerList = connection.fetchall()
    return render_template("borrower_list.html", borrowerlist = borrowerList)

# list current loan detail
@app.route("/currentloans")
def currentloans():
    connection = getCursor()
    sql=""" select br.borrowerid, br.firstname, br.familyname,  
                l.borrowerid, l.bookcopyid, l.loandate, l.returned, b.booktitle, b.author, 
                b.category, b.yearofpublication, bc.format 
            from books b
                inner join bookcopies bc on b.bookid = bc.bookid
                    inner join loans l on bc.bookcopyid = l.bookcopyid
                        inner join borrowers br on l.borrowerid = br.borrowerid
            order by br.familyname, br.firstname, l.loandate;"""
    connection.execute(sql)
    loanList = connection.fetchall()
    return render_template("current_loans.html", loanlist = loanList)

# public search book
@app.route("/searchbooks")
def searchbooks():
    return render_template("search_book.html")

# public search book
@app.route("/searchtype", methods=['POST'])
def searchType():
    searchtype = request.form.get('searchtype')
    if searchtype == "booktitle":
        return render_template("search_book_by_title.html")
    elif searchtype == "bookauthor":
        return render_template("search_book_by_author.html")
    elif searchtype == "both":
        return render_template("search_book_by_both.html")
    

# staff search book
@app.route("/staff/searchbooks")
def staffSearchBooks():
    return render_template("staff_search_book.html")


# public book search result, get the search data by POST method
@app.route("/search-book-results", methods=['GET','POST'])
def searchBookResults():
    searchtype = request.form.get("searchtype")
    if searchtype == "booktitle":
        searchbytitle = request.form.get("titleorauthor")    
        params = ("%"+searchbytitle + "%",)
        connection = getCursor()
        sql = "select books.booktitle,books.author,books.category,books.yearofpublication,\
            books.description,bookcopies.format,loans.returned,date_sub(loans.loandate, interval -28 day)\
            from books \
            inner join bookcopies on books.bookid = bookcopies.bookid \
            left join loans on bookcopies.bookcopyid = loans.bookcopyid\
            where booktitle like %s"
    elif searchtype == "bookauthor":
        searchbyauthor = request.form.get("titleorauthor")
        params = ("%"+searchbyauthor + "%",)
        connection = getCursor()
        sql = "select books.booktitle,books.author,books.category,books.yearofpublication,\
            books.description,bookcopies.format,loans.returned,date_sub(loans.loandate, interval -28 day)\
            from books \
            inner join bookcopies on books.bookid = bookcopies.bookid \
            left join loans on bookcopies.bookcopyid = loans.bookcopyid\
            where author like %s"
    elif searchtype == "both":
        searchbyboth = request.form.get("titleorauthor")
        params = ("%"+searchbyboth + "%","%"+searchbyboth + "%")
        connection = getCursor()
        sql = "select books.booktitle,books.author,books.category,books.yearofpublication,\
            books.description,bookcopies.format,loans.returned,date_sub(loans.loandate, interval -28 day)\
            from books \
            inner join bookcopies on books.bookid = bookcopies.bookid \
            left join loans on bookcopies.bookcopyid = loans.bookcopyid\
            where booktitle like %s or author like %s"
    connection.execute(sql,params)
    result = connection.fetchall()
    listLength = len(result)
    return render_template("search_book_result.html", result = result, len=listLength)

# staff book search result, get the search data by POST method
@app.route("/staff/search-book-results", methods=['GET','POST'])
def staffSearchBookResults():
    searchtype = request.form.get("searchtype")
    if searchtype == "booktitle":
        searchbytitle = request.form.get("titleorauthor")    
        params = ("%"+searchbytitle + "%",)
        connection = getCursor()
        sql = "select books.booktitle,books.author,books.category,books.yearofpublication,\
            books.description,bookcopies.format,loans.returned,date_sub(loans.loandate, interval -28 day)\
            from books \
            inner join bookcopies on books.bookid = bookcopies.bookid \
            left join loans on bookcopies.bookcopyid = loans.bookcopyid\
            where booktitle like %s"
    elif searchtype == "bookauthor":
        searchbyauthor = request.form.get("titleorauthor")
        params = ("%"+searchbyauthor + "%",)
        connection = getCursor()
        sql = "select books.booktitle,books.author,books.category,books.yearofpublication,\
            books.description,bookcopies.format,loans.returned,date_sub(loans.loandate, interval -28 day)\
            from books \
            inner join bookcopies on books.bookid = bookcopies.bookid \
            left join loans on bookcopies.bookcopyid = loans.bookcopyid\
            where author like %s"
    elif searchtype == "both":
        searchbyboth = request.form.get("titleorauthor")
        params = ("%"+searchbyboth + "%","%"+searchbyboth + "%")
        connection = getCursor()
        sql = "select books.booktitle,books.author,books.category,books.yearofpublication,\
            books.description,bookcopies.format,loans.returned,date_sub(loans.loandate, interval -28 day)\
            from books \
            inner join bookcopies on books.bookid = bookcopies.bookid \
            left join loans on bookcopies.bookcopyid = loans.bookcopyid\
            where booktitle like %s or author like %s"

    connection.execute(sql,params)
    result = connection.fetchall()
    listLength = len(result)
    return render_template("staff_search_book_result.html", result = result, len=listLength)

@app.route("/listbooks")
def listAllBooks():
    connection = getCursor()
    sql = "select books.booktitle,books.author,books.category,books.yearofpublication,\
        books.description,bookcopies.format,loans.returned,date_sub(loans.loandate, interval -28 day)\
        from books \
        inner join bookcopies on books.bookid = bookcopies.bookid \
        left join loans on bookcopies.bookcopyid = loans.bookcopyid"
    connection.execute(sql)
    result = connection.fetchall()
    listLength = len(result)
    return render_template("search_book_result.html", result = result, len=listLength)

@app.route("/staff/listbooks")
def staffListAllBooks():
    connection = getCursor()
    sql = "select books.booktitle,books.author,books.category,books.yearofpublication,\
        books.description,bookcopies.format,loans.returned,date_sub(loans.loandate, interval -28 day)\
        from books \
        inner join bookcopies on books.bookid = bookcopies.bookid \
        left join loans on bookcopies.bookcopyid = loans.bookcopyid"
    connection.execute(sql)
    result = connection.fetchall()
    listLength = len(result)
    return render_template("staff_search_book_result.html", result = result, len=listLength)

# staff page, the staff manage functions appear
@app.route("/staff")
def staffPage():
    return render_template("staff_page.html")

# staff search borrower
@app.route("/staff-search-borrower")
def staffSearchBorrower():
    return render_template("staff_search_borrower.html")

# staff borrower search result, get the search data by POST method
@app.route("/search-borrower-results", methods=['GET','POST'])
def searchBorrowerResults():
    searchcontent = request.form.get("borrower")
    strcontent = "%"+searchcontent + "%"
    params = (strcontent,strcontent,strcontent)
    connection = getCursor()
    sql = "select * from borrowers \
            where borrowerid like %s or firstname like %s or familyname like %s"
    connection.execute(sql,params)
    result = connection.fetchall()
    listLength = len(result)
    return render_template("staff_search_borrower_result.html", result = result, len=listLength)

# staff add new borrower, the template will provide an enmpty form
@app.route("/new-borrower-info")
def newBorrowerInfo():
    return render_template("staff_add_new_borrower.html")

# after user add a new borrower, get the data and update borrower table by inserting a row
@app.route("/borrower/add", methods=["POST"])
def addNewborrower():
    firstname = request.form.get("firstname")
    familyname = request.form.get("familyname")
    dateofbirth = request.form.get("dateofbirth")
    housenumbername = request.form.get("housenumbername")
    street = request.form.get("street")
    town = request.form.get("town")
    city = request.form.get("city")
    postalcode = request.form.get("postalcode")
    cur = getCursor()
    cur.execute("INSERT INTO borrowers (firstname, familyname, dateofbirth, housenumbername,\
        street, town, city,postalcode) VALUES(%s,%s,%s,%s,%s,%s,%s,%s);",(firstname, familyname, dateofbirth, 
        housenumbername,street, town, city,postalcode))
    return render_template("/staff_add_new_borrower_success.html")

# staff update borrower, the template will provide a form with original borrower detail
@app.route("/update_borrower/<borrowerid>")
def updateBorrower(borrowerid):
    connection = getCursor()
    params = (borrowerid,)
    sql = "SELECT * FROM borrowers where borrowerid= %s"
    connection.execute(sql,params)
    borrower = connection.fetchall()    
    return render_template("staff_update_borrower.html", borrower = borrower)

#always search the borrower before updating its detail, or list all the borrowers and then choose one
@app.route("/update_borrower_search")
def searchBeforeUpdate():
    return render_template("staff_search_before_update_borrower.html")
    
# update database after user editing borrower detail successfully
@app.route("/borrower/update", methods=["POST"])
def currentBorrower():
    borrowerid = request.form.get("borrowerid") 
    firstname = request.form.get("firstname")
    familyname = request.form.get("familyname")
    dateofbirth = request.form.get("dateofbirth")
    housenumbername = request.form.get("housenumbername")
    street = request.form.get("street")
    town = request.form.get("town")
    city = request.form.get("city")
    postalcode = request.form.get("postalcode")

    cur = getCursor()
    cur.execute("update borrowers set firstname=%s, familyname=%s, dateofbirth=%s, housenumbername=%s,\
            street=%s, town=%s, city=%s,postalcode=%s where borrowerid=%s",(firstname, familyname, dateofbirth, 
            housenumbername,street, town, city,postalcode,borrowerid))
    updateflag = True
    return render_template("/staff_add_new_borrower_success.html",updateflag=updateflag)

# return book
@app.route("/staff-return-book")
def staffReturnBook():
    connection = getCursor()
    sql = "select *from books \
    inner join bookcopies on books.bookid = bookcopies.bookid \
    left join loans on bookcopies.bookcopyid = loans.bookcopyid \
    left join borrowers on borrowers.borrowerid=loans.borrowerid"
    connection.execute(sql)
    bookResult = connection.fetchall()
    onloanList = []
    # provide on loan books and their borrowers for user to choose which one needs to be returned
    for row in bookResult:
        if row[13] == 0:
            onloanList.append(row)
    return render_template("staff_return_book.html", onloanbook = onloanList)

# if a book has returned , update loans table by changing the Returned column
@app.route("/staff-return-book-success", methods=["POST"])
def staffReturnBookSuccess():
    loanid = request.form.get('onloan')
    cur=getCursor()
    param = (loanid,)
    sql = "update loans set returned=1 where loanid=%s" 
    cur.execute(sql,param)
    return render_template("staff_return_book_success.html")

# issue book, only provide availible books on web page
@app.route("/staff-issue-book")
def staffIssueBook():
    dateoftoday = datetime.date.today()

    connection = getCursor()
    sql = "select *from books \
    inner join bookcopies on books.bookid = bookcopies.bookid \
    left join loans on bookcopies.bookcopyid = loans.bookcopyid "
    connection.execute(sql)
    bookResult = connection.fetchall()
    availableList = []
    for row in bookResult:
        if row[13] == 1 or row[13] == None:
            availableList.append(row)
    connection = getCursor()
    connection.execute("select borrowerid, firstname, familyname from borrowers")
    borrowers = connection.fetchall()
    return render_template("staff_issue_book_to_borrower.html", availableBook = availableList, 
                            borrowers=borrowers, loandate=dateoftoday)

# if a book has issued , update loans table by inserting one new row
@app.route("/issue-book-success", methods=["POST"])
def issueBookSuccess():
    bookcopyid = request.form.get("bookcopy")    
    loandate = request.form.get("loandate")
    borrowerid = request.form.get("borrower")
    param = (bookcopyid,)
    connection = getCursor()
    sql = "select format from bookcopies where bookcopyid = %s"
    connection.execute(sql,param)
    format = connection.fetchall()
    # Physical Books can only be loaned once at a time, eBooks and Audio Books can be loaned multiple times
    params = (bookcopyid,borrowerid,loandate)
    if format[0][0] != "eBook" and format[0][0] != "Audio Book":        
        sql = "insert into loans (bookcopyid, borrowerid, loandate, returned) values(%s,%s,%s,0)"
    else:
        sql = "insert into loans (bookcopyid, borrowerid, loandate, returned) values(%s,%s,%s,1)"
    con = getCursor()
    con.execute(sql,params)
    return render_template("staff_issue_book_success.html")

# list overdue books and their borrowers, overdue days
@app.route("/list-overdue-books")
def listOverdueBooks():
    connection=getCursor()
    connection.execute("select bookcopies.bookcopyid, books.booktitle,borrowers.borrowerid,\
                        borrowers.firstname, borrowers.familyname, borrowers.dateofbirth,\
                        borrowers.housenumbername,borrowers.street,borrowers.town,borrowers.city,borrowers.postalcode,\
                        datediff(curdate(),loans.loandate)\
                        from loans left join bookcopies on loans.bookcopyid=bookcopies.bookcopyid\
                        inner join books on bookcopies.bookid=books.bookid\
                        left join borrowers on loans.borrowerid=borrowers.borrowerid\
                        where datediff(curdate(),loans.loandate)>35\
                        order by borrowerid")
    overdueBooks = connection.fetchall()
    return render_template("staff_list_overdue_books.html", overdueBooks=overdueBooks)

# list loan summary and how many times a book has been loaned
@app.route("/list-loan-summary")
def listLoanSummary():
    connection=getCursor()
    connection.execute("select books.booktitle,books.author,bookcopies.format,\
                        count(loans.bookcopyid) as loantime from loans\
                        join bookcopies on loans.bookcopyid = bookcopies.bookcopyid\
                        join books on books.bookid = bookcopies.bookid\
                        group by loans.bookcopyid")
    summarylist = connection.fetchall()
    return render_template("staff_list_loan_summary.html", summarylist=summarylist)

# list borrower summary and how many loans they have been had
@app.route("/list-borrower-summary")
def listBorrowerSummary():
    connection=getCursor()
    connection.execute("select borrowers.firstname, borrowers.familyname,\
                        borrowers.dateofbirth,borrowers.city,\
                        count(borrowers.borrowerid) from loans\
                        join bookcopies on loans.bookcopyid = bookcopies.bookcopyid\
                        join books on books.bookid = bookcopies.bookid\
                        join borrowers on borrowers.borrowerid=loans.borrowerid\
                        group by borrowers.borrowerid")
    summarylist = connection.fetchall()
    return render_template("staff_list_borrower_summary.html", summarylist=summarylist)