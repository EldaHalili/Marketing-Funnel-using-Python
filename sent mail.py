import smtplib  #për të dërguar emaile përmes një serveri SMTP (si Gmail
from email.mime.multipart import MIMEMultipart    # Importon MIMEMultipart, një klasë që lejon krijimin e mesazheve email që mund të përmbajnë përmbajtje të përziera (si tekst dhe bashkëngjitje).
from email.mime.text import MIMEText   # Importon klasën MIMEText, e cila përdoret për të krijuar përmbajtjen e emailit si tekst të thjeshtë.
import mysql.connector   
from mysql.connector import Error    #Importon klasën Error, e cila përdoret për të kapur dhe trajtuar gabimet që ndodhin gjatë ndërveprimit me bazën e të dhënave MySQL.
import os         #iguron funksionalitete menaxhimi i variablave të ambientit.

# Funksioni për të dërguar email për një klient të caktuar
def send_email_to_customer(first_name, last_name, recipient_email):
    # Konfigurimi i serverit SMTP dhe kredencialet për dërgimin e emailit
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'h@gmail.com'  # Emaili i dërguesit
    sender_password = os.getenv('EMAIL_PASSWORD')  # Fjalëkalimi nga variabla e ambientit
    
    # Krijimi i mesazhit të emailit
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = f"Mireseerdhet ne dyqanin tone, {first_name}!"

    # Trupi i emailit
    body = f"Pershendetje {first_name} {last_name},\n\nFaleminderit që jeni bërë pjesë e komunitetit tonë! Ne e vlerësojmë besimin tuaj dhe duam t’ju shpërblejmë me një ofertë të veçantë, të krijuar posaçërisht për ju.\n\nPër regjistrimin tuaj, përfitoni: 15% zbritje për porosinë tuaj të ardhshme! Prioritet për aksesin në produktet dhe shërbimet më të reja. Aksesi ekskluziv në ngjarje speciale dhe promocione të kufizuara.\n\nPër të përfituar nga kjo ofertë, thjesht përdorni kodin MIRESEVINI15 kur bëni porosinë tuaj të ardhshme. Ky kod është i vlefshëm deri më 31 Tetor 2024. Nëse keni ndonjë pyetje ose kërkesë, mos hezitoni të na kontaktoni. Ekipi ynë është këtu për t'ju ndihmuar me çdo nevojë që mund të keni. Faleminderit që na besuat dhe mezi presim të vazhdojmë t’ju ofrojmë shërbimet tona të shkëlqyera.\n\nMe Respekt,\nElda"
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Lidhja me serverin SMTP dhe dërgimi i emailit
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Fillimi i kriptimit TLS
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print(f"Emaili u dërgua me sukses tek {first_name} {last_name} ({recipient_email})")

    except Exception as e:
        print(f"Emaili dështoi të dërgohej tek {recipient_email}: {str(e)}")

# Funksioni për të marrë klientët nga baza e të dhënave dhe për t'ju dërguar email
def send_emails_to_customers(db_config):
    try:
        # Lidhja me bazën e të dhënave MySQL
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)

            # Marrja e të gjithë klientëve nga tabela 'customers' që kanë email të vlefshëm
            cursor.execute("SELECT first_name, last_name, email FROM customers WHERE email IS NOT NULL")
            customers = cursor.fetchall()

            # Dërgo email për çdo klient
            for customer in customers:
                send_email_to_customer(
                    customer['first_name'],
                    customer['last_name'],
                    customer['email']
                )

    except Error as e:  # Kapja e gabimeve gjatë lidhjes me bazën e të dhënave
        print(f"Gabim gjatë lidhjes me MySQL: {str(e)}")
    finally:
        if connection.is_connected():  # Mbyll lidhjen nëse është ende e hapur
            cursor.close()
            connection.close()

if __name__ == "__main__":
    # Konfigurimi i bazës së të dhënave MySQL
    db_config = {
        'host': 'localhost',        # Vendosja e hostit 
        'database': 'corebos80',     # emrin e bazës së të dhënave
        'user': 'root',              #  përdoruesin e bazës së të dhënave
        'password': ''               # V fjalëkalimin e bazës së të dhënave
    }

    # Sigurohuni që fjalëkalimi i Gmail të jetë vendosur në variablat e ambientit
    if not os.getenv('EMAIL_PASSWORD'):
        print("Gabim: Fjalëkalimi i Gmail nuk është vendosur në variablin e ambientit 'EMAIL_PASSWORD'")
    else:
        # Filloni procesin e dërgimit të emaileve tek të gjithë klientët
        send_emails_to_customers(db_config)