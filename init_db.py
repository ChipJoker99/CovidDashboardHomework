# init_db.py
import sqlalchemy
from sqlalchemy import create_engine, text

# Percorso del tuo file database SQLite
# Assicurati che il percorso sia corretto rispetto a dove esegui lo script.
# Se 'covid-dashboard.sqlite' è nella stessa cartella di init_db.py:
DATABASE_URL = "sqlite:///./covid-dashboard.sqlite"
# Se è in una posizione specifica sulla tua chiavetta, usa il percorso assoluto o relativo corretto.
# Esempio se la chiavetta è E: e il file è in E:\progetti\covid-dashboard.sqlite
# DATABASE_URL = "sqlite:///E:/progetti/covid-dashboard.sqlite" # Windows
# DATABASE_URL = "sqlite:////media/tuoutente/NOME_CHIAVETTA/covid-dashboard.sqlite" # Linux

engine = create_engine(DATABASE_URL, echo=True) # echo=True mostra gli SQL eseguiti

# Definisci lo statement CREATE TABLE e gli indici
# (lo stesso che abbiamo definito nella FASE 0)
create_table_statement = """
CREATE TABLE IF NOT EXISTS province_daily_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_rilevamento DATE NOT NULL,
    codice_regione INTEGER NOT NULL,
    denominazione_regione TEXT NOT NULL,
    codice_provincia INTEGER NOT NULL,
    denominazione_provincia TEXT NOT NULL,
    sigla_provincia TEXT,
    totale_casi_provincia INTEGER NOT NULL,
    data_inserimento_db DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (data_rilevamento, codice_provincia)
);
"""

create_index_data_statement = """
CREATE INDEX IF NOT EXISTS idx_data_rilevamento ON province_daily_data (data_rilevamento);
"""

create_index_regione_statement = """
CREATE INDEX IF NOT EXISTS idx_codice_regione ON province_daily_data (codice_regione);
"""

def initialize_database():
    try:
        with engine.connect() as connection:
            print(f"Connesso al database: {DATABASE_URL}")

            # Esegui lo statement per creare la tabella
            connection.execute(text(create_table_statement))
            print("Tabella 'province_daily_data' verificata/creata.")

            # Esegui gli statement per creare gli indici
            connection.execute(text(create_index_data_statement))
            print("Indice 'idx_data_rilevamento' verificato/creato.")

            connection.execute(text(create_index_regione_statement))
            print("Indice 'idx_codice_regione' verificato/creato.")

            # Importante: SQLAlchemy di default esegue le operazioni DDL
            # (come CREATE TABLE) in una transazione che viene automaticamente
            # committata. Se stessi facendo DML (INSERT, UPDATE, DELETE),
            # avresti bisogno di connection.commit() qui.
            # Per DDL come CREATE TABLE/INDEX, il commit è implicito o non necessario
            # a seconda della configurazione del driver DBAPI, ma è buona pratica
            # assicurarsi che le modifiche siano persistite.
            # In SQLite, con autocommit a livello di connection per DDL, non serve esplicitamente.

            print("Database inizializzato con successo!")

    except Exception as e:
        print(f"Errore durante l'inizializzazione del database: {e}")

if __name__ == "__main__":
    initialize_database()