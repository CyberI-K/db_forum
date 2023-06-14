#pip innstal flask-mysqldb
#pip install flask , render_template , request

from flask import  Flask , render_template , request
from flask_mysqldb import MySQL

app = Flask(__name__)




app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= ''
app.config['MYSQL_DB']= 'db_forum'

mysql = MySQL(app)

#--------------------------Index Seite---------------------------------------#
@app.route('/')
def index():
    return render_template('index.html')

#-------------------------------------Newsforum-------------------------------#
@app.route('/newsforum')
def newsforum():
    #Verbindung zur Datenbank herstellen
    cursor = mysql.connection.cursor()

    #SQL Anweisung
    query = '''
            SELECT tbl_eintraege. *,
            tbl_user.Vorname,
            tbl_user.Nachname
            FROM tbl_eintraege
            LEFT JOIN tbl_user ON tbl_user.IDUser = tbl_eintraege.FIDUser
            ORDER by Eintragezeitpunkt ASC   
                    
        '''

    cursor.execute(query)
    ausgaben = cursor.fetchall()



    return render_template('newsforum.html',ausgaben=ausgaben)


#----------------------------User-eintraege-----------------------------#
@app.route('/usereintraege', methods=['GET', 'POST'])
def usereintreage():
    #Verbindung zur Datenbank herstellen
    cursor = mysql.connection.cursor()
    #Abfrage ob Post Daten Vorhanden sind
    if request.method == 'POST':
        # übergibt die eingabe von der HTML suche in die Variable search_query
        search_query = request.form['search']
        #SQL anweisung
        query = f'''
        SELECT  tbl_eintraege. *,
        tbl_user.Vorname,
        tbl_user.Nachname,
        tbl_user.Emailadresse
        FROM tbl_eintraege
        LEFT JOIN tbl_user on tbl_user.IDUser = tbl_eintraege.FIDUser
        WHERE tbl_user.Emailadresse LIKE '{search_query}'
            order by Eintragezeitpunkt ASC
        '''

        #lasse mir die eingabe aus der suche auf der konsole ausgeben
        print(search_query)
    else:
        query = '''
            SELECT  tbl_eintraege. *,
            tbl_user.Vorname,
            tbl_user.Nachname,
            tbl_user.Emailadresse
            FROM tbl_eintraege
            LEFT JOIN tbl_user on tbl_user.IDUser = tbl_eintraege.FIDUser
            
            order by Eintragezeitpunkt ASC

        '''

    cursor.execute(query)
    #Die Datenbank einträge werden in die Variable ausgabe geschrieben
    ausgaben = cursor.fetchall()

    return render_template('usereintraege.html',ausgaben=ausgaben)





#-------------------------------------Suche-----------------------------------#

@app.route('/suche',methods=['GET','POST'])
def suche():
    #Verbindung zur Datenbank herstellen
    cursor = mysql.connection.cursor()
    #Abfrage ob Post Daten vorhanden sind
    if request.method == 'POST':
        # übergibt die eingabe von der HTML suche in die Variable search_query
        search_query = request.form['suche']
        #SQL Anweisung
        query = f'''
                SELECT  tbl_eintraege. *,
            tbl_user.Vorname,
            tbl_user.Nachname,
            tbl_user.Emailadresse
            FROM tbl_eintraege
            LEFT JOIN tbl_user on tbl_user.IDUser = tbl_eintraege.FIDUser
            WHERE tbl_eintraege.Eintrag LIKE '%{search_query}%'
                order by Eintragezeitpunkt ASC
            '''
    else:
        query = '''
                SELECT  tbl_eintraege. *,
            tbl_user.Vorname,
            tbl_user.Nachname,
            tbl_user.Emailadresse
            FROM tbl_eintraege
            LEFT JOIN tbl_user on tbl_user.IDUser = tbl_eintraege.FIDUser
    
                order by Eintragezeitpunkt ASC
        
        '''

    cursor.execute(query)
    # Die Datenbank einträge werden in die Variable ausgabe geschrieben
    ausgaben = cursor.fetchall()



    return render_template('suche.html',ausgaben=ausgaben)


if __name__ == '__main__':
    app.run(debug=True)



