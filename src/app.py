from src.models.order import Order
from src.models.order_item import OrderItem
from src.models.customer import Customer
from src.models.transaction import Transaction
from src.db import get_connection

def create_order(customer_id, products_with_qty):
    """
    Vytvoří novou objednávku pro daného zákazníka
    a vloží položky (products_with_qty = [(product_id, qty), ...]).
    """
    # Vytvoření objektu Order a uložení
    order = Order(customer_id=customer_id)
    order.save()
    
    # Vložení položek do order_items
    for (product_id, qty) in products_with_qty:
        oi = OrderItem(order_id=order.id, product_id=product_id, quantity=qty)
        oi.save()

    print(f"Objednávka (ID {order.id}) úspěšně vytvořena.")

def transfer_credits(from_customer_id, to_customer_id, amount):
    """
    Ukázková funkce pro transakci: Převod bodů/kreditů z jednoho zákazníka na druhého.
    Využívá explicitní transakce (BEGIN, COMMIT, ROLLBACK).
    """
    conn = get_connection()
    try:
        conn.start_transaction()
        cursor = conn.cursor()

        # (1) Zkontrolovat zůstatek (zde jen ukázka, jak by mohla vypadat logika).
        # Můžete mít tabulku 'customer_balance', apod. Tady je to jen ilustrace:
        cursor.execute("SELECT SUM(amount) FROM transactions WHERE to_customer_id = %s", (from_customer_id,))
        result = cursor.fetchone()
        current_balance = result[0] if result[0] else 0.0
        if current_balance < amount:
            raise ValueError("Nedostatečný kredit.")

        # (2) Odečíst z from_customer_id (záporná transakce)
        cursor.execute("""
            INSERT INTO transactions (from_customer_id, to_customer_id, amount, trans_date)
            VALUES (%s, %s, %s, NOW())
        """, (from_customer_id, to_customer_id, -amount))

        # (3) Přičíst to_customer_id (kladná transakce)
        cursor.execute("""
            INSERT INTO transactions (from_customer_id, to_customer_id, amount, trans_date)
            VALUES (%s, %s, %s, NOW())
        """, (from_customer_id, to_customer_id, amount))

        conn.commit()
        print("Převod úspěšný.")
    except Exception as e:
        conn.rollback()
        print("Chyba při převodu:", str(e))
    finally:
        cursor.close()
        conn.close()

def generate_report():
    """
    Vytvoří jednoduchý report s agregovanými údaji (př. počet objednávek, tržby...).
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    sql = """
        SELECT 
            COUNT(DISTINCT o.id) AS total_orders,
            SUM(p.price * oi.quantity) AS total_revenue,
            AVG(p.price * oi.quantity) AS avg_order_price
        FROM orders o
        JOIN order_items oi ON o.id = oi.order_id
        JOIN products p ON p.id = oi.product_id
    """
    cursor.execute(sql)
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    report = {
        'total_orders': row['total_orders'],
        'total_revenue': row['total_revenue'],
        'avg_order_price': row['avg_order_price']
    }
    return report

def import_customers_from_csv(csv_file_path):
    """
    Import zákazníků z CSV souboru.
    Očekává sloupce: full_name, email
    """
    import csv
    conn = get_connection()
    cursor = conn.cursor()

    with open(csv_file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sql = """
                INSERT INTO customers (full_name, email, created_at)
                VALUES (%s, %s, NOW())
            """
            cursor.execute(sql, (row['full_name'], row['email']))

    conn.commit()
    cursor.close()
    conn.close()
    print("Import zákazníků z CSV proběhl úspěšně.")

def import_products_from_json(json_file_path):
    """
    Import produktů z JSON souboru.
    Očekává list objektů se strukturou: { 'name': ..., 'price': ..., 'stock': ... }
    """
    import json
    conn = get_connection()
    cursor = conn.cursor()

    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data:
            sql = """
                INSERT INTO products (name, price, stock)
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (item['name'], item['price'], item['stock']))

    conn.commit()
    cursor.close()
    conn.close()
    print("Import produktů z JSON proběhl úspěšně.")
