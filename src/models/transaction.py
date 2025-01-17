import datetime
from src.db import get_connection

class Transaction:
    def __init__(self, id=None, from_customer_id=None, to_customer_id=None, amount=0.0, trans_date=None):
        self.id = id
        self.from_customer_id = from_customer_id
        self.to_customer_id = to_customer_id
        self.amount = amount
        self.trans_date = trans_date

    def save(self):
        """
        Vloží nebo aktualizuje transakci.
        """
        conn = get_connection()
        cursor = conn.cursor()

        if self.id is None:
            # INSERT
            self.trans_date = datetime.datetime.now()
            sql = """
                INSERT INTO transactions (from_customer_id, to_customer_id, amount, trans_date)
                VALUES (%s, %s, %s, %s)
            """
            values = (self.from_customer_id, self.to_customer_id, self.amount, self.trans_date)
            cursor.execute(sql, values)
            self.id = cursor.lastrowid
        else:
            # UPDATE
            sql = """
                UPDATE transactions
                SET from_customer_id = %s, to_customer_id = %s, amount = %s
                WHERE id = %s
            """
            values = (self.from_customer_id, self.to_customer_id, self.amount, self.id)
            cursor.execute(sql, values)

        conn.commit()
        cursor.close()
        conn.close()

    def delete(self):
        """
        Smaže transakci z DB.
        """
        if self.id is None:
            return

        conn = get_connection()
        cursor = conn.cursor()
        sql = "DELETE FROM transactions WHERE id = %s"
        cursor.execute(sql, (self.id,))
        conn.commit()

        cursor.close()
        conn.close()
        self.id = None

    @staticmethod
    def find_by_id(transaction_id):
        """
        Najde transakci dle ID.
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM transactions WHERE id = %s", (transaction_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            return Transaction(
                id=row['id'],
                from_customer_id=row['from_customer_id'],
                to_customer_id=row['to_customer_id'],
                amount=row['amount'],
                trans_date=row['trans_date']
            )
        return None

    @staticmethod
    def all():
        """
        Vrátí list všech transakcí.
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM transactions")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        result = []
        for row in rows:
            result.append(Transaction(
                id=row['id'],
                from_customer_id=row['from_customer_id'],
                to_customer_id=row['to_customer_id'],
                amount=row['amount'],
                trans_date=row['trans_date']
            ))
        return result
