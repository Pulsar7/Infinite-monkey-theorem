import os,random,string,time,sys
from datetime import datetime
import matplotlib.pyplot as plt

def datum():
	t = datetime.now()
	return ("%s-%s-%s"%(t.day,t.month,t.year))

def uhrzeit():
	t = datetime.now()
	return ("%s:%s:%s"%(t.hour,t.minute,t.second))

class AFFE:
	def __init__(self,wort,max_letters,blatt_dateipfad):
		self.buchstaben = string.ascii_lowercase
		self.max_letters = max_letters
		self.blatt_dateipfad = blatt_dateipfad+".affe"
		self.gefunden_status = False
		self.wort = wort

	def datenvisualisierung(self,daten):
		datei = open(self.blatt_dateipfad,'r')
		Lines = datei.readlines()
		datei.close()
		buchstaben_daten = {}
		for buchstabe in self.buchstaben:
			for line in Lines:
				zeile = line.strip()
				try:
					argumente = zeile.split(buchstabe)
					buchstaben_daten[buchstabe] = {
						'anzahl': len(argumente)-1
					}	
				except Exception as error:
					pass

		font1 = {'family':'serif','color':'blue','size':15}
		font2 = {'family':'sans-serif','color':'black','size':13}

		plt.suptitle(
		"'%s' - %s Anschläge - %s Durchläufe"%(
				daten['gesuchtes_wort'],
				daten['anschläge_insgesamt'],
				daten['durchläufe_insgesamt']
			)
		)

		#Plot 1 (Anzahl der Buchstaben Insgesamt): 

		__anzahl = []
		__buchstaben = []
		for element in buchstaben_daten:
			__buchstaben.append(element)
			__anzahl.append(buchstaben_daten[element]['anzahl'])

		plt.subplot(2, 1, 1)
		plt.plot(__buchstaben,__anzahl,marker = 'o')
		plt.title("Anzahl der Buchstaben Insgesamt",fontdict = font1)
		plt.xlabel("Alle Buchstaben",fontdict = font2)
		plt.ylabel("Anzahl der Buchstaben",fontdict = font2)
		plt.grid(color = 'black', linestyle = '-', linewidth = 0.5)

		#Plot 2 (Dauer der Durchläufe):

		dauer = []
		dauer_daten = daten['dauer_durchläufe_insgesamt']
		for element in dauer_daten:
			dauer.append(element)
		durchläufe = []
		for i in range(1,len(dauer)+1):
			durchläufe.append(str(i))
		plt.subplot(2, 1, 2)
		plt.plot(durchläufe,dauer,marker = 'o')
		plt.title("\n\n Dauer der Durchläufe",fontdict = font1)
		plt.xlabel("Durchläufe",fontdict = font2)
		plt.ylabel("Dauer in Sekunden",fontdict = font2)
		plt.grid(color = 'black', linestyle = '-', linewidth = 0.5)

		plt.show()

	def blatt_schreiben(self,durchlauf_counter):
		datei = open(self.blatt_dateipfad,'a')
		datei.writelines(self.BLATT[durchlauf_counter])
		datei.close()

	def write(self):
		self.BLATT = {}
		durchlauf_counter,anschläge_counter = 1,0
		start = time.time()
		dauer_durchläufe_insgesamt = []
		print("+ Affe beginnt zu schreiben.")
		while (self.gefunden_status == False):
			try:
				__start = time.time()
				self.BLATT[durchlauf_counter] = []
				for n in range(0,self.max_letters):
					buchstabe = self.buchstaben[
						random.randint(0,len(self.buchstaben)-1)]
					anschläge_counter += 1
					self.BLATT[durchlauf_counter].append(buchstabe)
					sys.stdout.write("\r+ %s Buchstaben; Durchlauf = %s"%(
						len(self.BLATT[durchlauf_counter]),
						durchlauf_counter
					))
					sys.stdout.flush()
				self.blatt_schreiben(durchlauf_counter)
				bisher_geschrieben = "".join(self.BLATT[durchlauf_counter])
				__end = time.time()
				dauer_durchläufe_insgesamt.append(__end-__start)
				if (self.wort in bisher_geschrieben):
					self.gefunden_status = True
					break
				else:
					pass
				del self.BLATT[durchlauf_counter]
				durchlauf_counter += 1
			except KeyboardInterrupt:
				break
		end = time.time()
		dauer = end-start
		print("\n\n+ Affe hat aufgehört zu schreiben.")
		if (self.gefunden_status == False):
			print("! '%s' konnte nach %s Anschlägen nicht gefunden werden."%(
				self.wort, anschläge_counter
			))
		else:
			print("+ '%s' wurde nach %s Anschlägen gefunden!"%(
				self.wort,anschläge_counter
			))
			daten = {
				"anschläge_insgesamt": anschläge_counter,
				"gesuchtes_wort": self.wort,
				"dauer_durchläufe_insgesamt": dauer_durchläufe_insgesamt,
				"durchläufe_insgesamt": durchlauf_counter,
				"maximale_buchstaben_pro_durchlauf": self.max_letters
			}
			self.datenvisualisierung(daten)
		print("""
* Dauer = %s Sekunden mit %s Druchläufen (%s maximale Buchstaben pro Durchlauf)
		"""%(dauer,durchlauf_counter,self.max_letters))

#
wort = "haar".lower()
max_letters = 10000
blatt_dateipfad = "BLATT/%s_%s_%s"%(datum(),uhrzeit(),wort)
#

if (__name__ == '__main__'):
	os.system("clear") #Linux
	affe = AFFE(wort,max_letters,blatt_dateipfad)
	affe.write()