#Launch the web server with a minimal Flask application

#Flask ist ein Web-Framework für Python, das es Entwicklern ermöglicht, 
#Webanwendungen schnell und einfach zu erstellen.

import os
from flask import Flask, render_template, redirect, url_for, request
import db # importierte Die benutzerdefinierten Datenbankfunktionen und datenbank

#Dieser Befehl importiert die Flask-Klasse aus dem Flask-Paket,
#das du zuvor installiert hast. Dann kannst du eine Instanz der Flask-Klasse erstellen, um deine Webanwendung zu erstellen:

app = Flask(__name__) # Nun hast du eine Flask-App erstellt

app.config.from_mapping( #Die Konfiguration der Anwendung wird über die Methode app.config.from_mapping() festgelegt
    SECRET_KEY='secret_key_just_for_dev_environment', #SECRET_KEY: Eine geheime Schlüsselzeichenfolge, die für die Sitzungsverwaltung und andere Sicherheitsmechanismen verwendet wird.
    DATABASE=os.path.join(app.instance_path, 'todos.sqlite') 
    # ist ein Pfad zu dem Ordner, der für die Instanzspeicherung der Flask-Anwendung verwendet wird.
    #'todos.sqlite': Dies ist der Name der SQLite-Datenbankdatei. In diesem Fall wird die Datenbank als todos.sqlite bezeichnet.
    #Die os.path.join()-Funktion verbindet die Pfade, die als Argumente übergeben werden. In diesem Fall werden zwei Pfade verbunden:
        #app.instance_path: Dies ist der Pfad zum Ordner, der für die Instanzspeicherung der Flask-Anwendung verwendet wird. Dieser Pfad ist relativ zum Hauptordner der Anwendung.
            #'todos.sqlite': Dies ist der Name der SQLite-Datenbankdatei, die in diesem Fall todos.sqlite heißt.
    #DATABASE=: Dieser Ausdruck weist der Konfigurationsvariablen DATABASE den Wert des zusammengesetzten Pfades zu.
         #Diese Konfigurationsvariable wird später von der Flask-Anwendung verwendet, um auf die Datenbank zuzugreifen.
)

#Hier wird der Befehl db.init_db zur Befehlszeilen-Schnittstelle (CLI) der Flask-Anwendung hinzugefügt.
#db.init_db ist ein Befehl, der definiert, wie die Datenbank initialisiert werden soll. Dieser Befehl wird in einem separaten Modul namens db definiert, das Funktionen zur Datenbankverwaltung enthält.
#Durch Hinzufügen dieses Befehls zur CLI kann er von der Befehlszeile aus aufgerufen werden, um die Datenbank zu initialisieren. 
#Zum Beispiel: flask init-db.
app.cli.add_command(db.init_db)

#app.teardown_appcontext(db.close_db_con)`**: 
#Registriert eine Funktion (`db.close_db_con`), die automatisch am Ende jeder Anfrage ausgeführt wird.
#Diese Funktion schließt die Verbindung zur Datenbank, um sicherzustellen, dass Ressourcen ordnungsgemäß 
#freigegeben werden und keine Lecks auftreten.
app.teardown_appcontext(db.close_db_con)


#Die @app.route()-Dekoratorfunktion in Flask wird verwendet, um URL-Routen mit bestimmten Python-Funktionen oder Ansichten (Views) zu verknüpfen. 
#Wenn ein Client eine URL aufruft, die mit einer bestimmten Route übereinstimmt, führt Flask die damit verknüpfte 
#Python-Funktion aus und gibt das Ergebnis an den Client zurück.
@app.route('/')
def index():
    return redirect(url_for('lists'))

#index(), lists()... sind die Namen der Funktionen
@app.route('/lists/')
def lists():
    db_con = db.get_db_con()
    sql_query = 'SELECT * from list ORDER BY name'
    lists_temp = db_con.execute(sql_query).fetchall()
    lists = []
    for list_temp in lists_temp:
        list = dict(list_temp)
        sql_query = (
            ##Die SQL-Abfrage SELECT COUNT(complete) = SUM(complete) gibt eine 
            ##einzelne Zeile zurück, die entweder 1 (wahr) oder 0 (falsch) enthält, 
            ##je nachdem, ob die Anzahl der abgeschlossenen To-dos 
            ##(dargestellt durch COUNT(complete)) gleich der Summe der abgeschlossenen To-dos (dargestellt durch SUM(complete)) ist.

            ##als complete (spalte) gespeichert

            ##f'JOIN todo_list ON list_id={list["id"]} ': Dies ist ein Teil der SQL-Abfrage, der eine JOIN-Klausel verwendet, 
           ##um die Tabelle todo_list mit der Tabelle todo zu verknüpfen. Das f am Anfang der Zeichenkette signalisiert 
            ##eine f-String-Zeichenfolge, und {list["id"]} wird durch den Wert der ID der aktuellen Liste ersetzt. Dies ermöglicht es, 
            ##die Abfrage dynamisch an die spezifische To-do-Liste anzupassen, die gerade verarbeitet wird.

            ##verknüpft die tabellen.
            'SELECT COUNT(complete) = SUM(complete) ' 
            'AS complete FROM todo ' 
            f'JOIN todo_list ON list_id={list["id"]} ' 
                'AND todo_id=todo.id; ' 
        )
        complete = db_con.execute(sql_query).fetchone()['complete'] ## bei fetch one braucht man das ansonsten nicht
        ##Das [...] ist die Indexnotation in Python, die verwendet wird, um auf Elemente in einer Datenstruktur zuzugreifen. 
        ##In diesem Fall wird die Indexnotation verwendet, 
        ##um auf ein spezifisches Element in einem Ergebnis zuzugreifen, das von der Datenbank zurückgegeben wurde.
        list['complete'] = complete ##Der Wert von complete wird dem Dictionary list als neuer Schlüssel 'complete' hinzugefügt. 
        ##Dies ermöglicht es, den abgeschlossenen Status der Liste im Dictionary zu speichern, um ihn später zu verwenden.
        lists.append(list) ##Das aktualisierte Dictionary list wird der Liste lists hinzugefügt. 
        ##Nachdem alle Listen verarbeitet wurden, enthält lists die aktualisierten Daten aller Listen.
    if request.args.get('json') is not None: ## Dieser Teil des Codes überprüft, ob der Benutzer eine JSON-Antwort angefordert hat. 
        ##request.args.get('json') sucht nach einem Argument mit dem Namen 'json' in der URL-Anfrage. Wenn ein solches Argument vorhanden ist, 
        ##wird die Bedingung is not None erfüllt und der Codeblock wird ausgeführt.
        return lists ##
    else: 
        return render_template('lists.html', lists=lists) ## Wenn der Benutzer keine JSON-Antwort angefordert hat, wird die Liste lists 
    ##an die Vorlage 'lists.html' übergeben und die gerenderte HTML-Seite zurückgegeben, um die Listen anzuzeigen.


  #  <int:id>: Dies ist der dynamische Teil der URL, der mit <int:id> markiert ist. 
  #  Es wird erwartet, dass ein Integer-Wert für diesen Teil der URL bereitgestellt wird. 
  #Der Wert dieses Teils wird an die zugehörige Ansichtsfunktion übergeben.

@app.route('/lists/<int:id>')
def list(id):
    db_con = db.get_db_con()
    sql_query_1 = f'SELECT name FROM list WHERE id={id}'
    sql_query_2 = (
        'SELECT id, complete, description FROM todo '
        f'JOIN todo_list ON todo_id=todo.id AND list_id={id} '
        'ORDER BY id;'
    )
    list = {}
    list['name'] = db_con.execute(sql_query_1).fetchone()['name']
    list['todos'] = db_con.execute(sql_query_2).fetchall()
    if request.args.get('json') is not None: ##wenn nicht vom benutzer nachgefragt, retutn die list sonst render die html template mit der liste list.
        list['todos'] = [dict(todo) for todo in list['todos']] ## Konvertiert die To-do-Daten in eine Liste von Dictionaries, 
        ##um sie leichter in JSON umzuwandeln. todo ist nur ein temporäre Bezeichnung die passend hier ist. 

 ## list['todos']: Ruft den Wert des Schlüssels 'todos' im Dictionary list ab. Dieser Wert wird angenommen, eine Liste von Dictionarys zu sein.
##[dict(todo) for todo in list['todos']]: Erstellt eine neue Liste, indem sie eine Liste von Dictionarys durchläuft, die als Wert des Schlüssels 'todos' im Dictionary list gespeichert ist. 
##Für jedes Dictionary (todo) in dieser Liste wird ein neues Dictionary erstellt (mit dict(todo)), das identische Schlüssel-Wert-Paare enthält. Dadurch wird eine Kopie jedes Dictionarys erstellt.

##Das Ergebnis ist eine neue Liste von Dictionarys, die eine Kopie der ursprünglichen Liste von Dictionarys ist.
##Diese neue Liste von Dictionarys wird dann als Wert für den Schlüssel 'todos' im Dictionary list gespeichert, wodurch die ursprüngliche Liste von Dictionarys durch die kopierte Liste ersetzt wird.
      
##Dadurch wird sichergestellt, dass Änderungen an der Liste von Dictionarys, die als Wert des Schlüssels 'todos' im Dictionary list gespeichert sind, unabhängig von der ursprünglichen Liste sind. 
##Dies ist nützlich, wenn du Änderungen an den Daten vornehmen möchtest, ohne die ursprünglichen Daten zu beeinflussen.

        return list ##wenn json im url aufgerufen wurde dann einfach liste ohne html(template) zurückgeben, also sehr einfach
    ##wenn nicht aufgerufen dann mit html rendern.
    else:
        return render_template('list.html', list=list) 
    ##By explicitly specifying the variable name (combined_list=combined_list), 
    ##you make it clear that the data being passed to the template is a list of combined items,

#Die Aussage besagt, dass die Funktionendefinition list() den Python-internen Datentyp list verdeckt oder "überschattet". 
#Das bedeutet, dass die Verwendung von list als Funktionsname die ursprüngliche Bedeutung von list als eingebauten Datentyp in Python überdeckt.
#In Python ist list ein eingebauter Datentyp, der dazu dient, eine Liste von Elementen zu speichern. Zum Beispiel:
#my_list = [1, 2, 3, 4, 5]

#Die Aussage bedeutet, dass es jetzt an der Zeit ist, die erstellte Flask-Anwendung auszuführen. 
#Um dies zu tun, verwenden wir den eingebauten Entwicklungsserver von Flask und geben ihm die Datei app.py,
#die wir gerade erstellt haben. 
##Dazu öffnen wir eine Terminal-Sitzung im Projektordner, in dem sich die Datei app.py befindet.

#DEF RUNT erst wenn man auf dem link /insert/sample ist
@app.route('/insert/sample')
def run_insert_sample():
    db.insert_sample()
    return 'Database flushed and populated with some sample data.'
