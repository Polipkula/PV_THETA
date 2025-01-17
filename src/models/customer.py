import datetime
from src.db import get_connection

class Customer:
    def __init__(self, id=None, full_name=None, email=None, created_at=None):
        self.id = id
        self.full_name = full_name
        self.email = email
        self.created_at = created_at

    def save(self):
        """
        Vloží nebo aktualizuje zákazníka (Active Record).
        """
        conn = get_connection()
        cursor = conn.cursor()

        if self.id is None:
            # INSERT
            self.created_at = datetime.datetime.now()
            sql = """
                INSERT INTO customers (full_name, email, created_at)
                VALUES (%s, %s, %s)
            """
            values = (self.full_name, self.email, self.created_at)
            cursor.execute(sql, values)
            self.id = cursor.lastrowid
        else:
            # UPDATE
            sql = """
                UPDATE customers 
                SET full_name = %s, email = %s
                WHERE id = %s
            """
            values = (self.full_name, self.email, self.id)
            cursor.execute(sql, values)

        conn.commit()
        cursor.close()
        conn.close()

    def delete(self):
        """
        Smaže zákazníka z DB.
        """
        if self.id is None:
            return

        conn = get_connection()
        cursor = conn.cursor()
        sql = "DELETE FROM customers WHERE id = %s"
        cursor.execute(sql, (self.id,))
        conn.commit()

        cursor.close()
        conn.close()
        self.id = None

    @staticmethod
    def find_by_id(customer_id):
        """
        Najde zákazníka podle ID, vrátí instanci Customer nebo None.
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            return Customer(
                id=row['id'],
                full_name=row['full_name'],
                email=row['email'],
                created_at=row['created_at']
            )
        return None

    @staticmethod
    def all():
        """
        Vrátí list všech zákazníků.
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM customers")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        result = []
        for row in rows:
            result.append(Customer(
                id=row['id'],
                full_name=row['full_name'],
                email=row['email'],
                created_at=row['created_at']
            ))
        return result
