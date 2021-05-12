import smtplib
import email.message
import os
from utils import Utils

debug = False

def send_mail(email_address, passwd, html_string, code):
    global debug

    if debug:
        url = "http://localhost:5000/verificacion/" + code
    else:
        url = "http://http://https://eco-asistente.herokuapp.com/verificacion/" + code
    
    print(url)
    #Datos de la cuenta.
    gmail_user = 'soporte.ecoasistente@gmail.com'
    gmail_password = 'proyectoFinal123'

    #Instanciación del objeto email.message
    message = email.message.Message()

    #Parámetros para el envío del email.
    sent_from = gmail_user
    to = [email_address]
    message['Subject']  = "EcoAsistente - Activá tu cuenta"

    #Importo el archivo html.
    

    #Formateo del email.
    message.add_header('Content-Type','text/html')
    message.set_payload(html_string)

    #Envío del email.
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, message.as_string().replace("URL_TO_REPLACE",url))
    server.close()


