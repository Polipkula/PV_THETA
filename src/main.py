from src.models.customer import Customer
from src.models.product import Product
from src.app import (
    create_order, 
    transfer_credits, 
    generate_report,
    import_customers_from_csv,
    import_products_from_json
)

def main_menu():
    while True:
        print("\n--- HLAVNÍ MENU ---")
        print("1) Vytvořit novou objednávku")
        print("2) Převod kreditů")
        print("3) Vygenerovat report")
        print("4) Import zákazníků z CSV")
        print("5) Import produktů z JSON")
        print("6) Konec")

        choice = input("Zvolte akci: ")

        if choice == "1":
            # Vytvoření objednávky
            cust_id = int(input("Zadejte ID zákazníka: "))
            # Pro zjednodušení ručně:
            prod_id = int(input("Zadejte ID produktu: "))
            qty = int(input("Zadejte množství: "))

            create_order(cust_id, [(prod_id, qty)])

        elif choice == "2":
            # Převod kreditů
            from_id = int(input("Zadejte ID zdrojového zákazníka: "))
            to_id = int(input("Zadejte ID cílového zákazníka: "))
            amount = float(input("Zadejte částku: "))

            transfer_credits(from_id, to_id, amount)

        elif choice == "3":
            # Report
            r = generate_report()
            print("\n--- REPORT ---")
            print(f"Počet objednávek: {r['total_orders']}")
            print(f"Celková hodnota: {r['total_revenue']}")
            print(f"Průměrná cena objednávky: {r['avg_order_price']}")

        elif choice == "4":
            # Import CSV
            path = input("Zadejte cestu k CSV souboru: ")
            import_customers_from_csv(path)

        elif choice == "5":
            # Import JSON
            path = input("Zadejte cestu k JSON souboru: ")
            import_products_from_json(path)

        elif choice == "6":
            print("Ukončuji program.")
            break

        else:
            print("Neplatná volba, zkuste znovu.")

if __name__ == "__main__":
    main_menu()
