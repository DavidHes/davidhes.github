#man kann openai importieren

import click  # Für Befehlszeileninteraktionen
import os  # Für Betriebssystemoperationen
import sqlite3  # Für die SQLite-Datenbankverbindung
from flask import current_app, g  # Für Flask-spezifische Funktionen

#Die Verwendung von g und current_app ist spezifisch für Flask und bietet eine Möglichkeit, 
#Daten zwischen verschiedenen Teilen einer Anfrage zu übergeben, ohne globale Variablen verwenden zu müssen. 
#Die current_app-Variable gibt Zugriff auf das aktuelle Flask-Anwendungsobjekt, während g 
#eine temporäre Speicherstelle pro Anfrage ist, die verwendet werden kann, 
#um Daten zwischen verschiedenen Teilen der Anfrage zu übergeben.

#2 funktionen definieren
#1.Funktion datenbank session öffnen und 2.Funktion auch schließen.

## get_db_con wird verwendet, um eine Verbindung zur SQLite-Datenbank herzustellen
##Get Database Connection" 
def get_db_con(pragma_foreign_keys = True): ## in der voraussetzung dass die Fremdschlusselintegrität überprüft ist    
    if 'db_con' not in g: ##ob es schon eine Verbindung gibts
        g.db_con = sqlite3.connect( ##gibts keine- macht connection
            current_app.config['DATABASE'],##um den Pfad zur SQLite-Datenbankdatei abzurufen und später mit diesem Pfad die Verbindung zur Datenbank herzustellen
            detect_types=sqlite3.PARSE_DECLTYPES
            ##um sicherzustellen, dass SQLite benutzerdefinierte Datentypen erkennt und automatisch konvertiert, wenn eine Verbindung zur Datenbank hergestellt wird.
        )
        g.db_con.row_factory = sqlite3.Row  ##die ergebnisse werden als dieser Typ zurückgegeben um einen bequemeren Zugriff auf die Datenbankergebnisse, indem du Spaltennamen statt Indexe verwenden kannst.
        if pragma_foreign_keys: ##prüft, ob der Parameter pragma_foreign_keys als (True) ausgewertet wird. 
            g.db_con.execute('PRAGMA foreign_keys = ON;') ##, um die Fremdschlüssel-Integritätsprüfungen einzuschalten. 
    return g.db_con ## gibt einfach die SQLite-Datenbankverbindung zurück,
#Am Ende der Funktion wird diese Verbindung mit return g.db_con zurückgegeben. 
#Das bedeutet, dass die Verbindung zur Datenbank an den Aufrufer der Funktion zurückgegeben wird, 
#sodass dieser sie für Datenbankabfragen und -operationen verwenden kann.

def close_db_con(e=None): ##erstellung der methode close the connection
    db_con = g.pop('db_con', None )
    ##pop-Methode entfernt das Element mit dem Schlüssel 'db_con' aus dem g-Objekt. 
    ##"das element ist nicht vorhanden"
    if db_con is not None: ##  ist eine Datenbankverbindung vorhanden  ????
        db_con.close() #sowohl aus g loschen als auch die con schliessen

#Die Absicht hier ist, die Datenbankverbindung aus dem g-Objekt zu entfernen, 
#damit sie ordnungsgemäß geschlossen werden kann. Wenn die Verbindung nicht vorhanden ist 
#(weil sie bereits geschlossen wurde oder nie erstellt wurde), 
#wird None in db_con gespeichert, was darauf hinweist, 
#dass keine Aktion zum Schließen der Verbindung erforderlich ist.

def insert_sample():
    db_con = get_db_con()
    with current_app.open_resource('sql/insert_sample.sql') as f:
        db_con.executescript(f.read().decode('utf8'))

@click.command('init-db') #click befehl initialisiert und init-db genannt, im Terminal schreiben -> db starten
def init_db():
    try:
        os.makedirs(current_app.instance_path) #erstellt einen Ordner und nennt diesen instance
    except OSError:
        pass
    db_con = get_db_con() #verbindung zur datenbank herstellen
    with current_app.open_resource('sql/drop_tables.sql') as a: #führe drop_tables aus
        db_con.executescript(a.read().decode('utf8'))
    with current_app.open_resource('sql/create_tables.sql') as f: #führe create_tables aus
        db_con.executescript(f.read().decode('utf8'))
    click.echo('Database has been initialized.') #gibt Nachricht zurück

