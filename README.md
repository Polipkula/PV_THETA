# README – Školní projekt (E-shop Manager)

**Autor**: David Pulec
**Kontakt**: pulec@spsejecna.cz
**Škola**: Střední průmyslová škola elektrotechnická, Praha 2, Ječná 30
**Charakter projektu**: Školní projekt v rámci předmětu PV

---

## 1. Stručný popis projektu

Tento projekt slouží k ukázce databázové aplikace, která demonstruje:
- Vytváření a správu objednávek (modul e-shopu).
- Práci s transakcemi (např. převod kreditů mezi uživateli).
- Import a export dat (CSV, JSON).
- Využití návrhového vzoru (Active Record / Row Gateway).

Aplikace obsahuje uživatelské rozhraní (CLI menu), díky kterému lze:
1. **Vytvořit novou objednávku**  
2. **Provést převod kreditů**  
3. **Vygenerovat report**  
4. **Importovat zákazníky z CSV**  
5. **Importovat produkty z JSON**  
6. **Ukončit program**

---

## 2. Specifikace požadavků a Use Case diagramy

- **Funkční požadavky**:
  - Správa zákazníků, objednávek, produktů a transakcí.
  - Možnost importu dat z CSV (zákazníci) a JSON (produkty).
  - Evidence převodů (kreditů) s využitím transakcí.
  - Generování reportu nad objednávkami.

- **Use Case**:  
  - *Vytvoření objednávky* – uživatel vyplní ID zákazníka a produkty, program uloží objednávku do DB.  
  - *Převod kreditů* – uživatel zadá zdrojového a cílového uživatele, částku. Kontroluje se zůstatek, do DB se zapíší dvě transakce (záporná a kladná).  
  - *Report* – uživatel jedním příkazem získá souhrnnou statistiku.  

*(Pozn.: UML Use Case diagram lze vložit do dokumentace nebo sem přidat odkaz.)*

---

## 3. Popis architektury a návrhového vzoru

Aplikace využívá **Active Record** (případně Row Gateway) pro komunikaci s tabulkami:
- Každý model (Customer, Order, Product, OrderItem, Transaction) má metody `save()`, `delete()`, atd.
- Databázové operace se odehrávají přímo v instancích modelů.

*(Pro podrobnější UML Class diagram, Deployment diagram atd. viz dokumentace.)*

---

## 4. Chování aplikace (UML behavioral diagrams)

- **Activity diagram** (příklad):
  1. Aplikace se spustí, zobrazí se hlavní menu.
  2. Uživatel zvolí akci (např. vytvořit objednávku).
  3. Aplikace vyžádá detaily (zákazník, produkty…).
  4. Dojde k uložení objednávky, aplikace zobrazí výsledek.
  5. Uživatel se vrátí na hlavní menu.

*(Detailní diagramy mohou být v PDF dokumentaci.)*

---

## 5. E-R model databáze

Tabulky:
1. **customers**  
   - `id` (PK, INT, AI)  
   - `full_name` (VARCHAR)  
   - `email` (VARCHAR)  
   - `created_at` (DATETIME)

2. **orders**  
   - `id` (PK, INT, AI)  
   - `customer_id` (FK → customers.id)  
   - `order_date` (DATETIME)  
   - `status` (ENUM / VARCHAR s CHECK)  
   - `paid` (BOOL)

3. **products**  
   - `id` (PK, INT, AI)  
   - `name` (VARCHAR)  
   - `price` (FLOAT)  
   - `stock` (INT)

4. **order_items** (vazební tabulka M:N)
   - `id` (PK, INT, AI)
   - `order_id` (FK → orders.id)
   - `product_id` (FK → products.id)
   - `quantity` (INT)

5. **transactions**  
   - `id` (PK, INT, AI)  
   - `from_customer_id` (FK → customers.id)  
   - `to_customer_id` (FK → customers.id)  
   - `amount` (FLOAT)  
   - `trans_date` (DATETIME)

*(Pro ER diagram v grafické podobě viz dokumentaci.)*

---

## 6. Schéma importu a exportu

- **Import CSV (customers.csv)**  
  - Sloupce: `full_name`, `email`  
  - Atribut `created_at` se doplňuje automaticky v DB (NOW()).

- **Import JSON (products.json)**  
  - Pole objektů s klíči: `name`, `price`, `stock`.

*(Pokud by bylo potřeba exportovat, můžeme např. generovat CSV/JSON z dat v tabulkách.)*

---

## 7. Konfigurace a konfigurační volby

- **`config.ini`** obsahuje nastavení připojení k DB:
  - `[DATABASE]`  
    - `HOST`=…  
    - `USER`=…  
    - `PASSWORD`=…  
    - `NAME`=…

*(Další volby je možné doplnit, např. logování, port apod.)*

---

## 8. Instalace a spuštění aplikace

1. **Klonování či stažení projektu**:  
   - Rozbalte ZIP do složky `Theta/`.

2. **Nainstalujte závislosti**:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Nastavení DB**:
   - Upravte `src/config.ini` s vašimi přihlašovacími údaji do SQL serveru.
   - Importujte DB skript `.sql`, který vytvoří tabulky (a volitelně i testovací data).

4. **Spuštění**:
   ```bash
   cd Theta
   python -m src.main
   ```
   Poté se zobrazí CLI menu s volbami (1–6).

---

## 9. Popis chybových stavů

- **Nedostatečný kredit**: při převodu kreditů, pokud je `current_balance < amount`.  
- **Foreign Key selhání** (IntegrityError): pokud zadáte neexistující `customer_id` nebo `product_id`.  
- **Chyba při připojení k DB**: pokud jsou v `config.ini` špatné údaje.  
- **Neplatný vstup** (např. e-mail bez `@`): program buď vyvolá chybu, nebo vyzve uživatele k opakování zadání.

*(Detailnější chybové kódy a řešení mohou být vypsány v dokumentaci.)*

---

## 10. Knihovny třetích stran

- **mysql-connector-python** (verze 8.x) pro komunikaci s MySQL/MariaDB.
- **json**, **csv** (součást standardní knihovny Python) pro import dat.

---

## 11. Závěrečné resumé

Tento projekt předvádí základní možnosti databázové aplikace v jazyce Python, včetně práce s transakcemi, importem dat a návrhovým vzorem Active Record. Aplikace je vhodná jako ukázka pro školní projekt, ale lze ji rozšířit o další funkce (např. webové rozhraní, pokročilé reporty apod.).  

---

## 12. Formát dokumentace

- Tento **README** slouží jako přehledné shrnutí (ve formátu `.md`).  
- Podrobnější UML diagramy, testovací scénáře a případné rozšířené popisy lze nalézt v přiložené dokumentaci (např. `doc/dokumentace.pdf`).

---

### Export programu a zdrojových kódů
- **Zdrojové kódy** jsou v adresáři `src/`.  
- **Dokumentaci** najdete v `doc/`.  
- **Testy a testovací scénáře** v `test/`.  
- Archivaci do `.zip` provedete z kořenové složky projektu.  

### Export databáze
- Soubor `.sql` obsahuje DDL příkazy pro vytvoření tabulek a DML příkazy s testovacími daty.
- Vše je obvykle zabaleno v transakci a označeno komentářem s názvem projektu a autorem.