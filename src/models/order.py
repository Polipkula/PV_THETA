import datetime
from src.db import get_connection

class Order:
    def __init__(self, id=None, customer_id=None, order_date=None, status='new', paid=False):
        self.id = id
        self.customer_id = customer_id
        self.order_date = order_date
        self.status = status  # enum: new, shipped, closed (v DB řešeno CHECK nebo VARCHAR)
        self.paid = paid

    def save(self):
        """
        Vloží nebo aktualizuje objednávku (Active Record).
        """
        conn = get_connection()
        cursor = conn.cursor()

        if self.id is None:
            # INSERT
            self.order_date = datetime.datetime.now()
            sql = """
                INSERT INTO orders (customer_id, order_date, status, paid)
                VALUES (%s, %s, %s, %s)
            """
            values = (self.customer_id, self.order_date, self.status, self.paid)
            cursor.execute(sql, values)
            self.id = cursor.lastrowid
        else:
            # UPDATE
            sql = """
                UPDATE orders 
                SET customer_id = %s, status = %s, paid = %s
                WHERE id = %s
            """
            values = (self.customer_id, self.status, self.paid, self.id)
            cursor.execute(sql, values)

        conn.commit()
        cursor.close()
        conn.close()

    def delete(self):
        """
        Smaže objednávku z DB.
        """
        if self.id is None:
            return

        conn = get_connection()
        cursor = conn.cursor()
        sql = "DELETE FROM orders WHERE id = %s"
        cursor.execute(sql, (self.id,))
        conn.commit()

        cursor.close()
        conn.close()
        self.id = None

    @staticmethod
    def find_by_id(order_id):
        """
        Najde objednávku podle ID, vrátí instanci Order nebo None.
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            return Order(
                id=row['id'],
                customer_id=row['customer_id'],
                order_date=row['order_date'],
                status=row['status'],
                paid=bool(row['paid'])
            )
        return None

    @staticmethod
    def all():
        """
        Vrátí list všech objednávek.
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM orders")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        result = []
        for row in rows:
            result.append(Order(
                id=row['id'],
                customer_id=row['customer_id'],
                order_date=row['order_date'],
                status=row['status'],
                paid=bool(row['paid'])
            ))
        return result
