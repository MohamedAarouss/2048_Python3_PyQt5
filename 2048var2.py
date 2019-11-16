#!/usr/bin/python3

import sys
import copy
from random import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *

class PyQtGame(QWidget):
	def __init__(self):
		super(PyQtGame,self).__init__()
		self.randomInit()
		self.colors = {
			0:QColor(0xCDC1B4),
			1:QColor(0x646464),
			2:QColor(0xFDFDAB),
			4:QColor(0xF7DB6E),
			8:QColor(0xFAC84B),
			16:QColor(0xFEB42D),
			32:QColor(0xFF9930),
			64:QColor(0xFC311A),
			128:QColor(0xFA3619),
			256:QColor(0xFB0D03),
			512:QColor(0xE30702),
			1024:QColor(0xB20700),
			2048:QColor(0x8C0606),
			4096:QColor(0x740402),
			8192:QColor(0x630700),
			16384:QColor(0x560303),
			32768:QColor(0x240101),
			65536:QColor(0x030002),
			131072:QColor(0x000000),
		}
		self.best = 0
		self.condVictoire = False
		self.initUI()

# Définition de la fenêtre
	def initUI(self):
		self.setFixedSize(350,400)
		self.center()
		self.setWindowTitle("2048")
		self.show()

	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

# Initialisation de la grille
	def randomInit(self) :
		self.blocs = [[0]*4 for i in range(4)]
		self.createLock(1)
		for m in range(2) :
			self.createColor(10)
		self.score = 0
		self.overed = 0
		self.availableBlocs = range(16)

# Attribution des touches
	def keyPressEvent(self,e) :
		if e.key() == Qt.Key_Escape :
			self.resetGame()
		elif e.key() == Qt.Key_Up :
			self.up()
		elif e.key() == Qt.Key_Down :
			self.down()
		elif e.key() == Qt.Key_Left :
			self.left()
		elif e.key() == Qt.Key_Right :
			self.right()
		self.movesAvailable()

	def up(self) :
		moved = False
		for i in range(1,4) :
			for j in range(0,4) :
				if self.blocs[i][j] != 0 and self.blocs[i][j] != 1 :
					k = i
					while k-1 >= 0 and self.blocs[k-1][j] == 0 :
						k -= 1
					if k-1 >= 0 and self.blocs[k-1][j] == self.blocs[i][j] :
						self.score += self.blocs[i][j] *2
						self.blocs[k-1][j] *= 2
						self.blocs[i][j] = 0
						moved = True
					elif k < i :
						self.blocs[k][j] = self.blocs[i][j]
						self.blocs[i][j] = 0
						moved = True
		if moved :
			if not self.condVictoire :
				QSound.play("sons/deplacement1.wav")
			self.updateBlocs()

	def down(self) :
		moved = False
		for i in range(2,-1,-1):
			for j in range(0,4):
				if self.blocs[i][j] != 0 and self.blocs[i][j] != 1 :
					k = i
					while k+1 < 4 and self.blocs[k+1][j] == 0 :
						k += 1
					if k+1 < 4 and self.blocs[k+1][j] == self.blocs[i][j] :
						self.score += self.blocs[i][j] *2
						self.blocs[k+1][j] *= 2
						self.blocs[i][j] = 0
						moved = True
					elif k > i :
						self.blocs[k][j] = self.blocs[i][j]
						self.blocs[i][j] = 0
						moved = True
		if moved :
			if not self.condVictoire :
				QSound.play("sons/deplacement1.wav")
			self.updateBlocs()

	def left(self) :
		moved = False
		for i in range(0,4) :
			for j in range(0,4) :
				if self.blocs[i][j] != 0 and self.blocs[i][j] != 1 :
					k = j
					while k-1 >= 0 and self.blocs[i][k-1] == 0 :
						k -= 1
					if k-1 >= 0 and self.blocs[i][k-1] == self.blocs[i][j] :
						self.score += self.blocs[i][j] *2
						self.blocs[i][k-1] *= 2
						self.blocs[i][j] = 0
						moved = True
					elif k < j :
						self.blocs[i][k] = self.blocs[i][j]
						self.blocs[i][j] = 0
						moved=True
		if moved :
			if not self.condVictoire :
				QSound.play("sons/deplacement2.wav")
			self.updateBlocs()

	def right(self) :
		moved = False
		for i in range(0,4) :
			for j in range(2,-1,-1) :
				if self.blocs[i][j] != 0 and self.blocs[i][j] != 1 :
					k = j
					while k+1 < 4 and self.blocs[i][k+1] == 0 :
						k += 1
					if k+1 < 4 and self.blocs[i][k+1] == self.blocs[i][j] :
						self.score += self.blocs[i][j] *2
						self.blocs[i][k+1] *= 2
						self.blocs[i][j] = 0
						moved = True
					elif k > j :
						self.blocs[i][k] = self.blocs[i][j]
						self.blocs[i][j] = 0
						moved = True
		if moved :
			if not self.condVictoire :
				QSound.play("sons/deplacement2.wav")
			self.updateBlocs()

# Mise à jour des blocs
	def updateBlocs(self) :
		self.availableBlocs = []
		self.createColor(10)
		for i in range(4) :
			for j in range(4) :
				if self.blocs[i][j] ==0 :
					self.availableBlocs.append(i+j*4)
		self.update()
		self.win()
		self.best=max(self.score,self.best)
		if not self.movesAvailable():
			self.gameOver()

# Vérification de possibilité de jeu
	def movesAvailable(self):
		if len(self.availableBlocs) != 0 :
			return True
		for i in range(4) :
			for j in range(4) :
				if i < 3 and self.blocs[i][j] == self.blocs[i+1][j] :
					return True
				if j < 3 and self.blocs[i][j] == self.blocs[i][j+1] :
					return True	
		return False

# Victoire
	def win(self) :
		for i in range(4) :
			for j in range(4) :
				if self.blocs[i][j] == 2048 :
					if not self.condVictoire :
						self.condVictoire = True
						QSound.play("sons/victoire.wav")
						if QMessageBox.question(self,'Message',"<center><b>Congratulation !</b><br> Would you continue ?</center>",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)==QMessageBox.Yes:
							self.update()
							self.victoire = QSound("sons/apres2048.wav")
							self.victoire.play()
							self.victoire.setLoops(QSound.Infinite)
						else:
							self.close()
						return 1
		return 0

# Défaite
	def gameOver(self) :
		if QMessageBox.question(self,'Message',"<center><b>Game Over</b><br> Play again ?</center>",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)==QMessageBox.Yes:
			self.resetGame()
		else:
			self.close()

# Définition de la position d'un nouveau bloc
	def createColor(self,num) :
		while 1 :
			i = randint(0,3)
			j = randint(0,3)
			if self.blocs[i][j] == 0 :
				self.blocs[i][j] = self.randomColor(num)
				break

# Apparition d'un nouveau bloc
	def randomColor(self,taux) :
		i = randint(0,taux)
		if (i < taux) :
			return 2
		else :
			return 4

# Définition de la position d'un bloc noir
	def createLock(self,num):
		existeDeja = False
		for i in range(4) :
			for j in range(4) :
				if self.blocs[i][j] == 1 :
					existeDeja = True
					break
			if existeDeja == True :
				break
		if existeDeja == False :

			test= []
			for i in range(4) :
				for j in range(4) :
					if self.blocs[i][j] ==0 :
						test.append(i*4+j)
			if len(test)!=0:
				tmp = test[randint(0,len(test)-1)]
				i = tmp//4
				j = tmp%4

				self.blocs[i][j] = self.randomLock(num)


# Apparition d'un bloc noir
	def randomLock(self,taux) :
		i = randint(0,taux)
		if (i == taux) :
			return 1
		else :
			return 0

# Définition de la position d'un bloc noir existant
	def deleteLock(self,num) :
		for i in range(4) :
			for j in range(4) :
				if self.blocs[i][j] == 1 :
					self.blocs[i][j] = self.randomDelLock(num)

# Disparition d'un bloc noir existant
	def randomDelLock(self,taux) :
		i = randint(0,taux)
		if (i == taux) :
			return 0
		else :
			return 1

# Position du pointeur lors du dernier clic
	def mousePressEvent(self,e) :
		self.lastPoint=e.pos()

# Bouton reset
	def mouseReleaseEvent(self,e) :
		self.resetRect = QRect(240,15,80,60)
		if self.resetRect.contains(e.pos().x(),e.pos().y()) and self.resetRect.contains(self.lastPoint.x(),self.lastPoint.y()):
			if QMessageBox.question(self,'Message',"<center><b>Are you sure ?</b><br>You can also press <i>Escape</i> to reset directly</center>",QMessageBox.Ok|QMessageBox.Cancel,QMessageBox.Cancel)==QMessageBox.Ok:
				self.resetGame()

# Reset
	def resetGame(self) :
		self.randomInit()
		self.update()

# Affichage fixe
	def paintEvent(self,e) :
		painter = QPainter(self)
		painter.setPen(Qt.NoPen)
		painter.setBrush(QBrush(QColor(0xbbada0))) # Couleur fenêtre
		painter.drawRect(self.rect())
		painter.setBrush(QBrush(QColor(0x776e65))) # Couleur boutons score / reset
		painter.drawRoundedRect(QRect(20,15,80,60),5,5)
		painter.setFont(QFont("Century Gothic",12))
		painter.setPen(QColor(0xffffff)) # Couleur police texte "score"
		painter.drawText(QRectF(QRect(20,20,80,60)),"SCORE",QTextOption(Qt.AlignHCenter))
		painter.setFont(QFont("Century Gothic",18))
		painter.setPen(QColor(0xffffff)) # Couleur police nombre score
		painter.drawText(QRectF(QRect(20,15,80,55)),str(self.score),QTextOption(Qt.AlignHCenter|Qt.AlignBottom))
		painter.setPen(Qt.NoPen)
		painter.drawRoundedRect(QRect(130,15,80,60),5,5)
		painter.setFont(QFont("Century Gothic",12))
		painter.setPen(QColor(0xffffff)) # Couleur police texte "best"
		painter.drawText(QRectF(QRect(130,20,80,60)),"BEST",QTextOption(Qt.AlignHCenter))
		painter.setFont(QFont("Century Gothic",18))
		painter.setPen(QColor(0xffffff)) # Couleur police nombre best
		painter.drawText(QRectF(QRect(130,15,80,55)),str(self.best),QTextOption(Qt.AlignHCenter|Qt.AlignBottom))
		painter.setPen(Qt.NoPen)
		painter.drawRoundedRect(QRect(240,15,80,60),5,5)
		painter.setFont(QFont("Century Gothic",16))
		painter.setPen(QColor(0xffffff)) # Couleur police texte reset
		painter.drawText(QRectF(QRect(240,15,80,60)),"RESET",QTextOption(Qt.AlignHCenter|Qt.AlignVCenter))
		painter.setPen(Qt.NoPen)
		self.drawRectangles(painter)

# Affichage mobile
	def drawRectangles(self,painter):
		for i in range(4):
			for j in range(4):
				painter.setFont(QFont("Century Gothic",14,10))
				painter.setBrush(self.colors[self.blocs[i][j]])
				painter.drawRoundedRect(QRect(20+j*80,90+i*80,60,60),10,10)
				if self.blocs[i][j] != 0:
					if self.blocs[i][j]<15:
						painter.setPen(QColor(0x646464)) # Couleur police chiffre bloc < 16
					else :
						painter.setPen(QColor(0xffffff)) # Couleur police chiffre bloc >= 16
					painter.drawText(QRectF(QRect(20+j*80,90+i*80,60,60)),str(self.blocs[i][j]),QTextOption(Qt.AlignHCenter|Qt.AlignVCenter))
					painter.setPen(Qt.NoPen)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	game = PyQtGame()
app.exec_()
