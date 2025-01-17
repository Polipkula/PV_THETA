from src.db import get_connection

class OrderItem:
    def __init__(self, id=None, order_id=None, product_id=None, quantity=1):
        self.id = id
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity

    def save(self):
        """
        Vloží nebo aktualizuje položku objednávky (Active Record).
        """
        conn = get_connection()
        cursor = conn.cursor()

        if self.id is None:
            # INSERT
            sql = """
                INSERT INTO order_items (order_id, product_id, quantity)
                VALUES (%s, %s, %s)
            """
            values = (self.order_id, self.product_id, self.quantity)
            cursor.execute(sql, values)
            self.id = cursor.lastrowid
        else:
            # UPDATE
            sql = """
                UPDATE order_items
                SET order_id = %s, product_id = %s, quantity = %s
                WHERE id = %s
            """
            values = (self.order_id, self.product_id, self.quantity, self.id)
            cursor.execute(sql, values)

        conn.commit()
        cursor.close()
        conn.close()

    def delete(self):
        """
        Smaže položku z DB.
        """
        if self.id is None:
            return

        conn = get_connection()
        cursor = conn.cursor()
        sql = "DELETE FROM order_items WHERE id = %s"
        cursor.execute(sql, (self.id,))
        conn.commit()

        cursor.close()
        conn.close()
        self.id = None

    @staticmethod
    def find_by_id(item_id):
        """
        Najde položku dle ID.
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM order_items WHERE id = %s", (item_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            return OrderItem(
                id=row['id'],
                order_id=row['order_id'],
                product_id=row['product_id'],
                quantity=row['quantity']
            )
        return None

    @staticmethod
    def all():
        """
        Vrátí list všech položek objednávek.
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM order_items")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        result = []
        for row in rows:
            result.append(OrderItem(
                id=row['id'],
                order_id=row['order_id'],
                product_id=row['product_id'],
                quantity=row['quantity']
            ))
        return result
