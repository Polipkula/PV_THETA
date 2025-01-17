import mysql.connector
import configparser
import os

def get_connection():
    """
    Načte konfigurační údaje z config.ini a vytvoří spojení s databází.
    Vrací objekt 'connection' pro práci s MySQL/MariaDB.
    """
    # Sestavení cesty k souboru config.ini
    config_path = os.path.join(os.path.dirname(__file__), 'config.ini')

    # Kontrola existence config.ini
    if not os.path.exists(config_path):
        raise FileNotFoundError("Konfigurační soubor 'config.ini' nebyl nalezen v adresáři 'src'.")

    # Načtení z config.ini
    config = configparser.ConfigParser()
    config.read(config_path)

    try:
        db_config = {
            'host': config['DATABASE']['HOST'],
            'user': config['DATABASE']['USER'],
            'password': config['DATABASE']['PASSWORD'],
            'database': config['DATABASE']['NAME']
        }
        conn = mysql.connector.connect(**db_config)
        return conn
    except KeyError as e:
        raise KeyError(f"Chybí klíč v konfiguračním souboru: {str(e)}")
    except mysql.connector.Error as err:
        raise ConnectionError(f"Chyba při připojování k databázi: {str(err)}")
