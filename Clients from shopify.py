import requests
import mysql.connector
from mysql.connector import Error

# Funksioni për të marrë klientët nga API e Shopify
def get_shopify_customers(shop_url, access_token):
    url = f'https://{shop_url}/admin/api/2023-10/customers.json'  # Adresa për të marrë klientët nga Shopify
    headers = {
        'X-Shopify-Access-Token': access_token  # Tokeni i qasjes për Shopify
    }

    response = requests.get(url, headers=headers)  # Kërkesa për të marrë të dhënat e klientëve
    
    if response.status_code == 200:  # Kontroll nëse kërkesa ka qenë e suksesshme
        customers = response.json().get('customers', [])  # Merr të dhënat e klientëve
        return customers  # Kthe klientët nëse ka të dhëna
    else:
        print(f"Gabim gjatë marrjes së klientëve: {response.status_code}, {response.text}")  # Shfaq mesazh gabimi
        return None  # Kthe null nëse ka ndodhur gabim

# Funksioni për të futur të dhënat e klientëve në bazën e të dhënave MySQL
def insert_customers_to_db(customers, db_config):
    try:
        connection = mysql.connector.connect(**db_config)  # Konektimi me bazën e të dhënave MySQL
        if connection.is_connected():  # Kontroll nëse lidhja është e suksesshme
            cursor = connection.cursor()

            # Krijo pyetjen për të futur të dhënat
            insert_query = """
            INSERT INTO customers (id, first_name, last_name, email, phone, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            # Për çdo klient të marrë nga Shopify, vendos të dhënat në bazën e të dhënave
            for customer in customers:
                customer_data = (
                    customer['id'],
                    customer['first_name'],
                    customer['last_name'],
                    customer['email'],
                    customer.get('phone'),  # Telefoni mund të jetë null
                    customer['created_at']
                )
                cursor.execute(insert_query, customer_data)  # Ekzekuto pyetjen për të futur të dhënat
            
            connection.commit()  # Ruaj ndryshimet në bazën e të dhënave
            print(f"Klientët e regjistruar u vendosën në tabelën 'customers' në bazën e të dhënave")
    
    except Error as e:  # Kap gabimet nëse ka ndonjë problem me lidhjen ose query
        print(f"Gabim gjatë lidhjes me MySQL: {e}")
    finally:
        if connection.is_connected():  # Mbyll lidhjen nëse është ende aktive
            cursor.close()
            connection.close()

if __name__ == "__main__":
    # Kredencialet e API të Shopify
    SHOP_URL = 'URL of shopify'  # URL i dyqanit Shopify
    ACCESS_TOKEN = 'acces token'  # Tokeni i qasjes

    # Konfigurimi i bazës së të dhënave MySQL
    db_config = {
        'host': 'localhost',  # Serveri i bazës së të dhënave
        'database': '',  # Emri i bazës së të dhënave
        'user': '',  # Përdoruesi i MySQL
        'password': '?'  # Fjalëkalimi i MySQL (mund të jetë bosh nëse nuk ka fjalëkalim)
    }

    # Merr klientët nga Shopify
    customers = get_shopify_customers(SHOP_URL, ACCESS_TOKEN)
    
    # Fut klientët në bazën e të dhënave nëse janë marrë me sukses
    if customers:
        insert_customers_to_db(customers, db_config)
