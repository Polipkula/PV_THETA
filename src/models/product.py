from src.db import get_connection

class Product:
    def __init__(self, id=None, name=None, price=0.0, stock=0):
        self.id = id
        self.name = name
        self.price = price
        self.stock = stock

    def save(self):
        """
        Vloží nebo aktualizuje produkt (Active Record).
        """
        conn = get_connection()
        cursor = conn.cursor()

        if self.id is None:
            # INSERT
            sql = """
                INSERT INTO products (name, price, stock)
                VALUES (%s, %s, %s)
            """
            values = (self.name, self.price, self.stock)
            cursor.execute(sql, values)
            self.id = cursor.lastrowid
        else:
            # UPDATE
            sql = """
                UPDATE products
                SET name = %s, price = %s, stock = %s
                WHERE id = %s
            """
            values = (self.name, self.price, self.stock, self.id)
            cursor.execute(sql, values)

        conn.commit()
        cursor.close()
        conn.close()

    def delete(self):
        """
        Smaže produkt z DB.
        """
        if self.id is None:
            return

        conn = get_connection()
        cursor = conn.cursor()
        sql = "DELETE FROM products WHERE id = %s"
        cursor.execute(sql, (self.id,))
        conn.commit()

        cursor.close()
        conn.close()
        self.id = None

    @staticmethod
    def find_by_id(product_id):
        """
        Najde produkt podle ID, vrátí instanci Product nebo None.
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            return Product(
                id=row['id'],
                name=row['name'],
                price=row['price'],
                stock=row['stock']
            )
        return None

    @staticmethod
    def all():
        """
        Vrátí list všech produktů.
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        result = []
        for row in rows:
            result.append(Product(
                id=row['id'],
                name=row['name'],
                price=row['price'],
                stock=row['stock']
            ))
        return result
