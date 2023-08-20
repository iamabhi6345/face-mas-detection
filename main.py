from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
import sys
import numpy as np
import cv2
from deepLearning import face_mask_prediction



class VideoCapture(qtc.QThread):
    change_pixmap_signal = qtc.pyqtSignal(np.ndarray)
    
    def __init__(self):
        super().__init__()
        self.run_flag = True
    
    def run(self):
        cap = cv2.VideoCapture(0)
        
        while self.run_flag:
            ret,frame=cap.read() 
            prediction = face_mask_prediction(frame)
            
            
            if ret==True:
                self.change_pixmap_signal.emit(prediction)
        
        cap.release()
    
    
    def   stop(self):
        self.run_flag =False
        self.wait()
            
            








class minWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(qtg.QIcon('D:\\project\\7-face-mask-detection\\3_app\\icon.png'))
        self.setWindowTitle('Face Mask Recognition Software')
        self.setFixedSize(700,600)
        
        
        
        label = qtw.QLabel('<h2>Face Mask Recognition App </h2>')
        self.cameraButton = qtw.QPushButton('Open Camera',clicked=self.cameraButtonClick, checkable =True)
        
        
        
        self.screen = qtw.QLabel()
        self.img = qtg.QPixmap(700,500)
        self.img.fill(qtg.QColor('darkGrey'))
        self.screen.setPixmap(self.img)
        
        
        layout = qtw.QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.cameraButton)
        layout.addWidget(self.screen)
        
        self.setLayout(layout)
        self.show()
        
        
        
    def cameraButtonClick(self):
        print('clicked')
        status =self.cameraButton.isChecked()
        
        if status == True:
            self.cameraButton.setText('close Camera')
            
           
            self.capture=VideoCapture()
            self.capture.change_pixmap_signal.connect(self.updateImage)
            self.capture.start()
 
         
        elif status == False:
            self.cameraButton.setText('open Camera')
            
        
    
    @qtc.pyqtSlot(np.ndarray)
    def updateImage(self,image_array):
        rgb_img = cv2.cvtColor(image_array , cv2.COLOR_BGR2RGB)
        h,w,ch = rgb_img.shape
        bytes_per_line = ch*w
        convertedImage = qtg.QImage(rgb_img.data , w , h , bytes_per_line ,qtg.QImage.Format_RGB888 )
        scaledImage = convertedImage.scaled(600,580,qtc.Qt.KeepAspectRatio)
        qt_img = qtg.QPixmap.fromImage(scaledImage)
       
       
        self.screen.setPixmap(qt_img)
        
        
        
        
        
        
        
        
        
        
        


if __name__=='__main__':
    app = qtw.QApplication(sys.argv)
    mw=minWindow()
    sys.exit(app.exec())
    








            
 
 
 
 
 


                  
