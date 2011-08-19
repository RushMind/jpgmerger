#coding=utf-8
'''
Created on 2009-12-11

@author: ataosky
'''
from PyQt4.QtGui import *
from PyQt4.QtCore import *

import os,sys
from myutils import *
from jpgmerge import *

class PicMerger(QDialog,Ui_jpgmerge):
	def __init__(self,parent=None):
		super(PicMerger,self).__init__(parent)
		self.setupUi(self)
		self.pushButton.setEnabled(False)
		self.pushButton_4.setEnabled(False)
		self.pushButton_5.setEnabled(False)
		self.fname=''
		
	@pyqtSignature("")
	def on_pushButton_3_clicked(self):
		dirName = QFileDialog.getExistingDirectory(self,self.tr('select directory'),'E:\temp')
		self.progressBar.setValue(0)
		self.lineEdit.setText(dirName)
		os.chdir(unicode(dirName))
		self.pushButton.setEnabled(True)
		self.pushButton_4.setEnabled(False)
		self.pushButton_5.setEnabled(False)
		#QMessageBox.information(self,"Warning",fileName)
		
	@pyqtSignature("")
	def on_pushButton_2_clicked(self):
		sys.exit()
		
	@pyqtSignature("")
	def on_pushButton_4_clicked(self):
		os.startfile(self.fname)
		self.pushButton_5.setEnabled(True)
		
	@pyqtSignature("")
	def on_pushButton_5_clicked(self):
		if QMessageBox.question(self,u'Warning',u'Delete all the images?',QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
			removeJpg()
		
	@pyqtSignature("")
	def on_pushButton_clicked(self):
		l=[]
		cov=glob.glob('cov*.jpg')
		l=l+cov
		bok=glob.glob('bok*.jpg')
		l=l+bok
		leg=glob.glob('leg*.jpg')
		l=l+leg
		fow=glob.glob('fow*.jpg')
		l=l+fow
		c=glob.glob('!*.jpg')
		c.sort()
		l=l+c
		p=glob.glob('00*.jpg')
		p.sort()
		l=l+p
		ll=len(l)
		if ll==0:
			QMessageBox.information(self,"Warning","no pictures found in this directory!")
		else:                                            
			self.progressBar.setMaximum(ll)
			if not p:
				im=Image.open(cov[0])
			else:
				im=Image.open(p[0])
			imgsize=im.size
			pa=os.getcwd()
			na=(os.path.split(pa))[1]
			name=na.split('_')
			self.fname=name[0]+'.pdf'
			pdf=Canvas(name[0]+'.pdf',pagesize=imgsize)
			cl=0
			for i in l:
				try:
					pdf.drawImage(i,x=0,y=0)
					pdf.showPage()
					cl=cl+1
					self.progressBar.setValue(cl)
				except:
					print i
					QMessageBox.information(self,"Warning","page "+str(i)+" is bad,please download it again!")
					app.processEvents()
			pdf.save() 
			app.processEvents()
			self.pushButton_4.setEnabled(True)
			app.processEvents()
		

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainForm =PicMerger()
    mainForm.show()
    sys.exit(app.exec_())
