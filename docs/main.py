# !/usr/bin/python3
# -*- coding: utf-8 -*-
import sys 
import os
import numpy as np
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import cv2 as opencv2
import math
from AGV_ui import *
from ui_AcilisPencere import *
from ui_LoginPencere import *
from ui_SplashWindow import *
from PrinterFonksiyonlar import *
import pickle
from datetime import date
import glob
import actionlib
from geometry_msgs.msg  import Pose, Point, Quaternion, PoseStamped
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseActionGoal
from actionlib_msgs.msg import GoalID, GoalStatusArray, GoalStatus

class AnaPencere(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):

        super(AnaPencere, self).__init__(parent=parent)

        if True:
            self.anapencere = Ui_MainWindow()
            self.anapencere.setupUi(self)
            rospy.init_node("robot_arayuz")
            self.elemanadi_old =""
            self.hata_old=""
            self.logfile=open("log.txt", "a")
            self.stylesheet_yesil = "background-color: rgb(0, 255, 0); border:none; border-radius:15px"
            self.stylesheet_kirmizi = "background-color: rgb(255, 0, 0); border:none; border-radius:15px"
            self.stylesheet_sari = "background-color: rgb(255, 255, 0); border:none; border-radius:15px"
            self.stylesheet_turkuaz = "background-color: rgb(85, 170, 255); border:none; border-radius:15px"
            self.stylesheet_agv1="background-color: rgb(10,0,0)"
            self.stylesheet_agv_hovered="background-color: rgb(255, 255, 0);"
            self.stylesheet_agv_selected = "background-color: rgb(255, 0, 0);"

            self.anapencere.butonKapat.clicked.connect(self.programi_kapat)
            self.anapencere.butonKapat_3.clicked.connect(self.programi_kapat)
            self.anapencere.butonKapat_4.clicked.connect(self.programi_kapat)
            self.anapencere.butonKapat_5.clicked.connect(self.programi_kapat)
            self.anapencere.label_agv_goruntu.installEventFilter(self)
            self.anapencere.tabWidget.currentChanged.connect(self.amr_degistir)#baglama sırrrıııı
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.DRAW_ARROW = False
            self.anapencere.label_agv_goruntu.installEventFilter(self)
            self.mouse_label_uzerinde = False            

            self.anapencere.pushButtonGirisYap.clicked.connect(self.ana_sayfa_manuel_kontrol_ac)
            self.anapencere.pushButtonCikisYap.clicked.connect(self.ana_sayfa_manuel_kontrol_kapat)
            self.anapencere.pushButtonOperatorEkle.clicked.connect(self.operator_ekle)
            self.anapencere.pushButtonOperatorSil.clicked.connect(self.operator_sil)
            self.anapencere.pushButtonOperatorSilYenile.clicked.connect(self.operator_sil_yenile)
            self.anapencere.buton_dur.clicked.connect(self.robotDur)
            self.anapencere.buton_ileri.clicked.connect(self.ileriGit)
            self.anapencere.buton_geri.clicked.connect(self.geriGit)
            self.anapencere.buton_sol.clicked.connect(self.solaDon)
            self.anapencere.buton_sag.clicked.connect(self.sagaDon)
            self.anapencere.pushbuton_durak_liste_yenile.clicked.connect(self.durak_listesi_yenile)  
            self.anapencere.pushButton_durak_kaydet.clicked.connect(self.durak_kaydet)  
            self.anapencere.pushButton_durak_sil.clicked.connect(self.durak_sil)  
            self.anapencere.pushButtonRosAyarlariKaydet.clicked.connect(self.ROS_ayarlari_kaydet)

            self.konum_x=0
            self.konum_y=0
            self.agv_yaw_aci_2=0
            self.konum_x_2=0
            self.konum_y_2=20
            self.agv_yaw_aci_4=0

            self.portlar_dosyasi = "docs/datalar/PORTLAR.txt"


            try:
                self.portlar_dict = load_dict_from_file8bit(self.portlar_dosyasi)

                self.harita_1_name = self.portlar_dict["HARITA_1_NAME"]
                self.harita_2_name = self.portlar_dict["HARITA_2_NAME"]
                self.agv_icon_name = self.portlar_dict["AGV_ICON_NAME"]
                self.agv2_icon_name = self.portlar_dict["AGV2_ICON_NAME"]

                self.istasyon_kayit_dosyasi = self.portlar_dict["ISTASYON_KAYIT_DOSYASI"]

                self.anapencere.lineEditAyarlarHarita1.setText(str(self.harita_1_name))
                self.anapencere.lineEditAyarlarHarita2.setText(str(self.harita_2_name))
                self.anapencere.lineEditAyarlarAGVicon.setText(str(self.agv_icon_name))
                self.anapencere.lineEditAyarlarAGV2icon.setText(str(self.agv2_icon_name))
                self.anapencere.lineEditAyarlarDurakKayitDosyasi.setText(str(self.istasyon_kayit_dosyasi))

            except Exception as e:
                self.log_yaz("PORTS FORM ERROR", str(e))
                pass

            self.timer_1 =QTimer()
            self.timer_1.timeout.connect(self.radio_button_toggle)

            if not self.timer_1.isActive():
                self.timer_1.start(400)


            self.timer = QTimer()
            self.timer.timeout.connect(self.Haritaguncelle)
            if not self.timer.isActive():
                self.timer.start(100)
            self.image=opencv2.imread('/home/user/Desktop/autonomous_guided_vehicles_gui/docs/icons/endustriyel_harita_yok.png')
            self.harita=self.image
            self.harita_1=opencv2.imread('/home/user/Desktop/autonomous_guided_vehicles_gui/docs/icons/{}'.format(self.harita_1_name))
            self.harita_2=opencv2.imread('/home/user/Desktop/autonomous_guided_vehicles_gui/docs/icons/{}'.format(self.harita_2_name))
            self.pacman=opencv2.imread('/home/user/Desktop/autonomous_guided_vehicles_gui/docs/icons/{}'.format(self.agv_icon_name))
            self.pacman_1=opencv2.imread('/home/user/Desktop/autonomous_guided_vehicles_gui/docs/icons/{}'.format(self.agv2_icon_name))


            self.agv_ikon_gorunme_durumu=False
            self.agv_ikon_gorunme_durumu_1=False    

            self.pacman=opencv2.cvtColor(self.pacman,opencv2.COLOR_BGR2RGB)
            self.pacman_1=opencv2.cvtColor(self.pacman_1,opencv2.COLOR_BGR2RGB)
            self.durak_kayit_dizini='docs/datalar/{}'.format(self.istasyon_kayit_dosyasi)
            self.hiz_mesaji_1=Twist()
            self.hiz_mesaji_2=Twist()
            self.mevcut_konum_yaz=False

            self.odom_subscriber= rospy.Subscriber("robot_1/odom", Odometry,self.odomCallback)
            self.odom_subscriber_2=rospy.Subscriber("robot_2/odom", Odometry,self.odomCallback2) 
            self.manuel_control_pub = rospy.Publisher("robot_1/cmd_vel", Twist, queue_size=10)
            self.manuel_control_pub_2 = rospy.Publisher("robot_2/cmd_vel", Twist, queue_size=10)
            self.status_subscriber = rospy.Subscriber('amr1/move_base/status', GoalStatusArray, self.hedefDurumOgren)
            self.status_subscriber_2 = rospy.Subscriber('amr2/move_base/status', GoalStatusArray, self.hedefDurumOgren)
            self.hedef_yayini = rospy.Publisher('amr1/move_base_simple/goal', PoseStamped, queue_size=1)
            self.hedef_yayini_2 = rospy.Publisher('amr2/move_base_simple/goal', PoseStamped, queue_size=1)

            self.hedef_durak = PoseStamped()
            self.hedef_durak_2 =PoseStamped()
            self.hedef_durak.header.frame_id = "map_nav_link"
            self.hedef_durak_2.header.frame_id = "map_nav_link"
            self.durum_amr = "h"        

            self.durak_listesi_yenile()
             

    def amr_degistir(self):
        try:

            if self.anapencere.tabWidget.currentIndex()==0:
                self.harita=self.image
                self.agv_ikon_gorunme_durumu=False
                self.agv_ikon_gorunme_durumu_1=False
                #self.mevcut_konum_yaz=False

            if self.anapencere.tabWidget.currentIndex()==1:
                self.harita=self.harita_1
                self.agv_ikon_gorunme_durumu=True
                self.agv_ikon_gorunme_durumu_1=False
                #self.mevcut_konum_yaz=True

            if self.anapencere.tabWidget.currentIndex()==2:      
                self.harita=self.harita_2
                self.agv_ikon_gorunme_durumu=False
                self.agv_ikon_gorunme_durumu_1=True
                #self.mevcut_konum_yaz=True

            if self.anapencere.tabWidget.currentIndex()==3:
                self.harita=self.harita_1
                self.agv_ikon_gorunme_durumu=True
                self.agv_ikon_gorunme_durumu_1=True
                #self.mevcut_konum_yaz=True

        except Exception as e:
            self.log_yaz("AMR  CHANGE ERROR", str(e))
            pass


    def mousePressEvent(self, eventQMouseEvent):
        try:
            if self.mouse_label_uzerinde:
                self.originQPoint = self.anapencere.label_agv_goruntu.mapFromGlobal(self.mapToGlobal(eventQMouseEvent.pos()))
                self.currentQPoint = self.originQPoint
            else:
                pass

        except Exception as e:
            self.log_yaz("MAUSE PRESS EVENT ERROR", str(e))
            pass

    def mouseMoveEvent(self, event_q_mouse_event):
        try:
            if self.mouse_label_uzerinde:
                self.DRAW_ARROW = True
                self.currentQPoint = self.anapencere.label_agv_goruntu.mapFromGlobal(self.mapToGlobal(event_q_mouse_event.pos()))
            else:
                pass
        except Exception as e:
            self.log_yaz("MOUSE MOVE EVENT ERROR", str(e))
            pass

    def mouseReleaseEvent(self, event_q_mouse_event):
        if self.mouse_label_uzerinde:
            rectangle=[0,0]
            rectangle[0]= self.originQPoint.x()  
            rectangle[1]= self.originQPoint.y() 
            print("hedef", rectangle)
            self.DRAW_ARROW = False

            try:
                rectangle[0] = (rectangle[0])
                rectangle[1] = -(rectangle[1] - self.anapencere.label_agv_goruntu.height())
                rectangle[0]=rectangle[0]*0.05
                rectangle[1]=rectangle[1]*0.05
                print("hedef", rectangle)

                start_x = self.originQPoint.x() 
                start_y = self.originQPoint.y() 
                end_x = self.currentQPoint.x()
                end_y = self.currentQPoint.y() 

                lineB = ((start_x, start_y), (end_x, end_y))  
                angle = self.calcAngle(lineB)

                if  not rospy.is_shutdown():
                    aci_quat = self.euler_to_quaternion(0.0, 0.0, angle)
                    if self.anapencere.tabWidget.currentIndex()==0:
                         pass
                    print(type(aci_quat),aci_quat)

                    if self.anapencere.tabWidget.currentIndex()==1:
                        self.hedef_durak.pose = Pose(Point(rectangle[0], rectangle[1], 0.0), Quaternion(*aci_quat))
                    print(type(aci_quat),aci_quat)

                    if self.anapencere.tabWidget.currentIndex()==2:
                        self.hedef_durak_2.pose = Pose(Point(rectangle[0], rectangle[1], 0.0), Quaternion(*aci_quat))
                    print(type(aci_quat),aci_quat)

                    if self.anapencere.tabWidget.currentIndex()==3:
                        self.hedef_durak.pose = Pose(Point(rectangle[0], rectangle[1], 0.0), Quaternion(*aci_quat))
                        self.hedef_durak_2.pose = Pose(Point(rectangle[0], rectangle[1], 0.0), Quaternion(*aci_quat))               
                    print(type(aci_quat),aci_quat)

                    self.hedef_yayini.publish(self.hedef_durak)
                    self.hedef_yayini_2.publish(self.hedef_durak_2)

            except Exception as e:
                self.log_yaz("MOUSE RELEAS EVENT ERROR:", str(e))
                pass
        else:
            pass

    def eventFilter(self, object, event):
        try:
            if event.type() == QEvent.Enter:

                if object == self.anapencere.label_agv_goruntu:      
                    self.mouse_label_uzerinde = True
            if event.type() == QEvent.MouseButtonDblClick:
                if object == self.anapencere.label_agv_goruntu:
                    self.DRAW_ARROW = False
            if event.type() == QEvent.Leave:

                if object == self.anapencere.label_agv_goruntu:      
                    self.mouse_label_uzerinde = False

            return False

        except Exception as e:
            self.log_yaz("EVENT FİLTER ERROR", str(e))
            pass

    def put4ChannelImageOn4ChannelImage(self,back, fore, x, y):
        try:
            if x<=0:
                x=10
            if y<=0:
                y=10
            rows, cols, channels = fore.shape
            trans_indices = fore[...] != 0  # Where not transparent
            overlay_copy = back[y:y + rows, x:x + cols]
            overlay_copy[trans_indices] = fore[trans_indices]
            back[y:y + rows, x:x + cols] = overlay_copy
            return True, back                                             
        except Exception as e:
            self.log_yaz("PUT FOR CHANNEL IMAGE ERROR",str(e))
            False, False
            pass

    def rotate_image(self, rotateImage, angle):
        try:

            # Taking image height and width
            imgHeight, imgWidth = rotateImage.shape[0], rotateImage.shape[1]

            # Computing the centre x,y coordinates
            # of an image
            centreY, centreX = imgHeight//2, imgWidth//2

            # Computing 2D rotation Matrix to rotate an image
            rotationMatrix = opencv2.getRotationMatrix2D((centreX, centreY), angle, 1.0)

            # Now will take out sin and cos values from rotationMatrix
            # Also used numpy absolute function to make positive value
            cosofRotationMatrix = np.abs(rotationMatrix[0][0])
            sinofRotationMatrix = np.abs(rotationMatrix[0][1])

            # Now will compute new height & width of
            # an image so that we can use it in
            # warpAffine function to prevent cropping of image sides
            newImageHeight = int((imgHeight * sinofRotationMatrix) +
                                (imgWidth * cosofRotationMatrix))
            newImageWidth = int((imgHeight * cosofRotationMatrix) +
                                (imgWidth * sinofRotationMatrix))

            # After computing the new height & width of an image
            # we also need to update the values of rotation matrix
            rotationMatrix[0][2] += (newImageWidth/2) - centreX
            rotationMatrix[1][2] += (newImageHeight/2) - centreY

            # Now, we will perform actual image rotation
            rotatingimage = opencv2.warpAffine(
                rotateImage, rotationMatrix, (newImageWidth, newImageHeight))

            return rotatingimage
        except Exception as e:
            self.log_yaz("ROTATE IMAGE ERROR", str(e))
            pass

    def calcAngle(self, lineB):
        try:    
            lineA = ((50, 50), (100, 50))
            line1Y1 = lineA[0][1]
            line1X1 = lineA[0][0]
            line1Y2 = lineA[1][1]
            line1X2 = lineA[1][0]
            line2Y1 = lineB[0][1]
            line2X1 = lineB[0][0]
            line2Y2 = lineB[1][1]
            line2X2 = lineB[1][0]

            # calculate angle between pairs of lines
            angle1 = math.atan2(line1Y1 - line1Y2, line1X1 - line1X2)
            angle2 = math.atan2(line2Y1 - line2Y2, line2X1 - line2X2)
            angleDegrees = (angle1 - angle2) * 360 / (2 * math.pi)
            radians = math.radians(angleDegrees)

            return radians
        except Exception as e:
            self.log_yaz("CALCULATE ANGLE ERROR", str(e))
            pass

    def Haritaguncelle(self):
        self.anapencere.label_lineer_hiz.setText(str(self.hiz_mesaji_1.linear.x))
        self.anapencere.label_acisal_hiz.setText(str(self.hiz_mesaji_1.angular.z))
        self.anapencere.label_lineer_hiz_toplam.setText(str(self.hiz_mesaji_1.linear.x))
        self.anapencere.label_acisal_hiz_toplam.setText(str(self.hiz_mesaji_1.angular.z))
        self.anapencere.label_lineer_hiz_2.setText(str(self.hiz_mesaji_2.linear.x))
        self.anapencere.label_acisal_hiz_2.setText(str(self.hiz_mesaji_2.angular.z))
        self.anapencere.label_lineer_hiz_toplam_2.setText(str(self.hiz_mesaji_2.linear.x))
        self.anapencere.label_acisal_hiz_toplam_2.setText(str(self.hiz_mesaji_2.angular.z))     
        resim_birlestirme_durumu = False
        try:

            image=self.harita.copy()
            # image=opencv2.resize(src=image,dsize=(self.anapencere.label_agv_goruntu.width(), self.anapencere.label_agv_goruntu.height()))
            konum_y=image.shape[0]-self.konum_y 
            konum_y_2=image.shape[0]-self.konum_y_2
            #image=opencv2.rectangle(image,(self.konum_x,konum_y) ,(self.konum_x+10,konum_y-10), (255,0,0),2)
        
            if self.agv_ikon_gorunme_durumu:
                pacman=self.rotate_image(self.pacman.copy(),self.agv_yaw_aci_2)      
                resim_birlestirme_durumu, image = self.put4ChannelImageOn4ChannelImage(image, pacman,self.konum_x, konum_y-20)

            if self.agv_ikon_gorunme_durumu_1:
                pacman_1=self.rotate_image(self.pacman_1.copy(),self.agv_yaw_aci_4)      
                resim_birlestirme_durumu, image = self.put4ChannelImageOn4ChannelImage(image, pacman_1,self.konum_x_2, konum_y_2-20)


            if self.DRAW_ARROW: #and self.MOUSE_LABEL_UZERINDE:
                start_x = self.originQPoint.x() 
                start_y = self.originQPoint.y() 
                end_x = self.currentQPoint.x()  
                end_y = self.currentQPoint.y() 

                """
                image = cv2.line(image, (start_x, start_y), (end_x, end_y), (255, 0, 0), 5)
                image = cv2.circle(image, (end_x, end_y), 10, (255, 0, 0), -1)
                """

                if resim_birlestirme_durumu:
                    image = opencv2.arrowedLine(image, (start_x, start_y), (end_x, end_y), (255, 0, 0), 5)
            #opencv2.imwrite("resim.jpeg", image)
            if resim_birlestirme_durumu:
                height, width, channel = image.shape
                step = channel * width
                qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
                self.anapencere.label_agv_goruntu.setPixmap(QPixmap.fromImage(qImg))
            else:
                pass

        except Exception as e:
            self.log_yaz("MAP VISUALIZE ERROR",str(e))
            pass
        
    def quaternion_to_euler(self, x, y, z, w):
        try:
            t0 = +2.0 * (w * x + y * z)
            t1 = +1.0 - 2.0 * (x * x + y * y)
            X = math.degrees(math.atan2(t0, t1))

            t2 = +2.0 * (w * y - z * x)
            t2 = +1.0 if t2 > +1.0 else t2
            t2 = -1.0 if t2 < -1.0 else t2
            Y = math.degrees(math.asin(t2))

            t3 = +2.0 * (w * z + x * y)
            t4 = +1.0 - 2.0 * (y * y + z * z)
            Z = math.degrees(math.atan2(t3, t4))

            return X, Y, Z
        except Exception as e:
            self.log_yaz("QUATERNION TO EULER ERROR", str(e))
            pass

    def euler_to_quaternion(self, roll, pitch, yaw):
        try:
            qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
            qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
            qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
            qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)

            # return [0, 0, 0.992599579404, 0.121433417836]
            return [qx, qy, qz, qw]
        except Exception as e:
            self.log_yaz("EULER TO QUATERNION ERROR", str(e))
            pass

    def hedefDurumOgren(self, durum_hedef):
        try:
        
            if len(durum_hedef.status_list) !=0:
                temp_durum = durum_hedef.status_list[0].status
        
                if temp_durum == 1:       self.durum_amr = "m"
                elif temp_durum == 2:     self.durum_amr = "H"
                elif temp_durum == 3:     self.durum_amr = "h"
                elif temp_durum == 4:     self.durum_amr = "H"
            else:
                pass

                #rospy.loginfo(durum_hedef)
        except Exception as e:
            self.log_yaz("GOAL EVENT LEARN ERROR", str(e))
            pass

    def konum_veri_temizle(self):
        self.anapencere.label_durak_kaydet_mevcut_konum.setText("")
        self.anapencere.label_durak_kaydet_mevcut_konum_2.setText("") 

    def odomCallback(self,mesaj):
        try:
            self.anapencere.labelAMR1Status.setText("ONLINE")
            self.anapencere.labelAMR1Status.setStyleSheet(self.stylesheet_yesil)

            self.durak_kaydet_mesaj=mesaj

            if self.anapencere.comboBox_amr_secim.currentIndex()==0:
                self.anapencere.label_durak_kaydet_mevcut_konum.setText("SELECTED AGV DOESNT EXIST")
                self.anapencere.label_durak_kaydet_mevcut_konum_2.setText("SELECTED AGV DOESNT EXIST")
                
            if self.anapencere.comboBox_amr_secim.currentIndex()==1:
                self.konum_veri_temizle()
                self.anapencere.label_durak_kaydet_mevcut_konum.setText("x:{:.4f}, y:{:.4f}, z:{:.4f}".format(self.durak_kaydet_mesaj.pose.pose.position.x,
                                                                                                self.durak_kaydet_mesaj.pose.pose.position.y,
                                                                                                self.durak_kaydet_mesaj.pose.pose.position.z))
                                                                              
            # if self.mevcut_konum_yaz:
            #     self.anapencere.label_durak_kaydet_mevcut_konum.setText("x:{:.4f}, y:{:.4f}, z:{:.4f}".format(self.durak_kaydet_mesaj.pose.pose.position.x,
            #                                                                                     self.durak_kaydet_mesaj.pose.pose.position.y,
            #                                                                                     self.durak_kaydet_mesaj.pose.pose.position.z))
            # else:
            #     self.anapencere.label_durak_kaydet_mevcut_konum.setText("SECILI AGV YOK")


            self.konum_x=round(mesaj.pose.pose.position.x/0.05)
            self.konum_y=round(mesaj.pose.pose.position.y/0.05)

            self.anapencere.label_konum_x.setText(str(round(mesaj.pose.pose.position.x,4)))
            self.anapencere.label_konum_y.setText(str(round(mesaj.pose.pose.position.y,4)))
            self.anapencere.label_konum_x_toplam.setText(str(round(mesaj.pose.pose.position.x,4)))
            self.anapencere.label_konum_y_toplam.setText(str(round(mesaj.pose.pose.position.y,4)))      
            aci_x=round(mesaj.pose.pose.orientation.x, 4)
            aci_y=round(mesaj.pose.pose.orientation.y, 4)
            aci_z=round(mesaj.pose.pose.orientation.z, 4)
            aci_w=round(mesaj.pose.pose.orientation.w, 4)
            #dönüs acisi dahil edilecektir.
            _,_,self.agv_yaw_aci_2=self.quaternion_to_euler(aci_x,aci_y,aci_z,aci_w)
            self.anapencere.label_donus_acisi.setText("{:.2f}".format(self.agv_yaw_aci_2))
            _,_,self.agv_yaw_aci_2=self.quaternion_to_euler(aci_x,aci_y,aci_z,aci_w)
            self.anapencere.label_donus_acisi_toplam.setText("{:.2f}".format(self.agv_yaw_aci_2))

        except Exception as e:
            self.anapencere.labelAMR1Status.setText("OFFLINE")
            self.anapencere.labelAMR1Status.setStyleSheet(self.stylesheet_kirmizi)
            self.log_yaz("ODOM CALLBACK", str(e))
            pass


    def odomCallback2(self,mesaj):
        try:
            self.durak_kaydet_mesaj=mesaj
            self.anapencere.labelAMR2Status.setText("ONLINE")
            self.anapencere.labelAMR2Status.setStyleSheet(self.stylesheet_yesil)

            if self.anapencere.comboBox_amr_secim.currentIndex()==2:
                self.konum_veri_temizle()
                self.anapencere.label_durak_kaydet_mevcut_konum_2.setText("x:{:.4f}, y:{:.4f}, z:{:.4f}".format(self.durak_kaydet_mesaj.pose.pose.position.x,
                                                                                                self.durak_kaydet_mesaj.pose.pose.position.y,
                                                                                                self.durak_kaydet_mesaj.pose.pose.position.z))

            if self.mevcut_konum_yaz:            
                self.anapencere.label_durak_kaydet_mevcut_konum_2.setText("x:{:.4f}, y:{:.4f}, z:{:.4f}".format(self.durak_kaydet_mesaj.pose.pose.position.x,
                                                                                                    self.durak_kaydet_mesaj.pose.pose.position.y,
                                                                                                     self.durak_kaydet_mesaj.pose.pose.position.z))
            # else:
            #     self.anapencere.label_durak_kaydet_mevcut_konum_2.setText("SELECTED AGV DOESNT EXIST")
                                                                                                    
            self.konum_x_2=round(mesaj.pose.pose.position.x/0.05)
            self.konum_y_2=round(mesaj.pose.pose.position.y/0.05)
            self.anapencere.label_konum_x_2.setText(str(round(mesaj.pose.pose.position.x,4)))
            self.anapencere.label_konum_y_2.setText(str(round(mesaj.pose.pose.position.y,4)))
            self.anapencere.label_konum_x_toplam_2.setText(str(round(mesaj.pose.pose.position.y,4)))      
            self.anapencere.label_konum_y_toplam_2.setText(str(round(mesaj.pose.pose.position.y,4)))

            aci_x=round(mesaj.pose.pose.orientation.x, 4)
            aci_y=round(mesaj.pose.pose.orientation.y, 4)
            aci_z=round(mesaj.pose.pose.orientation.z, 4)
            aci_w=round(mesaj.pose.pose.orientation.w, 4)

            _,_,self.agv_yaw_aci_4=self.quaternion_to_euler(aci_x,aci_y,aci_z,aci_w)
            self.anapencere.label_donus_acisi_2.setText("{:.2f}".format(self.agv_yaw_aci_4))
            _,_,self.agv_yaw_aci_4=self.quaternion_to_euler(aci_x,aci_y,aci_z,aci_w)
            self.anapencere.label_donus_acisi_toplam_2.setText("{:.2f}".format(self.agv_yaw_aci_4))

        except Exception as e:
            self.anapencere.labelAMR2Status.setText("OFFLINE")
            self.anapencere.labelAMR2Status.setStyleSheet(self.stylesheet_kirmizi)
            self.log_yaz("ODOM CALLBACK", str(e))
            pass


    def robotDur(self):
        try:
            if self.anapencere.tabWidget.currentIndex()==0:
                pass

            if self.anapencere.tabWidget.currentIndex()==1:
                self.hiz_mesaji_1.linear.x=0.0
                self.hiz_mesaji_1.angular.z=0.0
                self.manuel_control_pub.publish(self.hiz_mesaji_1)        

            if self.anapencere.tabWidget.currentIndex()==2:

                self.hiz_mesaji_2.linear.x=0.0
                self.hiz_mesaji_2.angular.z=0.0
                self.manuel_control_pub_2.publish(self.hiz_mesaji_2)       

            if self.anapencere.tabWidget.currentIndex()==3:

                self.hiz_mesaji_1.linear.x=0.0
                self.hiz_mesaji_1.angular.z=0.0
                self.manuel_control_pub.publish(self.hiz_mesaji_1) 
                self.hiz_mesaji_2.linear.x=0.0
                self.hiz_mesaji_2.angular.z=0.0
                self.manuel_control_pub_2.publish(self.hiz_mesaji_2)  

        except Exception as e:
            self.log_yaz("ROBOT STOP",str(e))
            pass

    def ileriGit(self):
        try:
            if self.anapencere.tabWidget.currentIndex()==0:
                pass

            if self.anapencere.tabWidget.currentIndex()==1:
                self.hiz_mesaji_1.linear.x=1.0
                self.hiz_mesaji_1.angular.z=0.0
                self.manuel_control_pub.publish(self.hiz_mesaji_1)        

            if self.anapencere.tabWidget.currentIndex()==2:

                self.hiz_mesaji_2.linear.x=1.0
                self.hiz_mesaji_2.angular.z=0.0
                self.manuel_control_pub_2.publish(self.hiz_mesaji_2)       

            if self.anapencere.tabWidget.currentIndex()==3:

                self.hiz_mesaji_1.linear.x=1.0
                self.hiz_mesaji_1.angular.z=0.0
                self.manuel_control_pub.publish(self.hiz_mesaji_1) 
                self.hiz_mesaji_2.linear.x=1.0
                self.hiz_mesaji_2.angular.z=0.0
                self.manuel_control_pub_2.publish(self.hiz_mesaji_2)       

        except Exception as e:
            self.log_yaz("ROBOT FORWARD ERROR", str(e))
            pass

    def geriGit(self):
        try:
            if self.anapencere.tabWidget.currentIndex()==0:
                pass

            if self.anapencere.tabWidget.currentIndex()==1:
                self.hiz_mesaji_1.linear.x=-1.0
                self.hiz_mesaji_1.angular.z=0.0
                self.manuel_control_pub.publish(self.hiz_mesaji_1)        

            if self.anapencere.tabWidget.currentIndex()==2:

                self.hiz_mesaji_2.linear.x=-1.0
                self.hiz_mesaji_2.angular.z=0.0
                self.manuel_control_pub_2.publish(self.hiz_mesaji_2)       

            if self.anapencere.tabWidget.currentIndex()==3:

                self.hiz_mesaji_1.linear.x=-1.0
                self.hiz_mesaji_1.angular.z=0.0
                self.manuel_control_pub.publish(self.hiz_mesaji_1) 
                self.hiz_mesaji_2.linear.x=-1.0
                self.hiz_mesaji_2.angular.z=0.0
                self.manuel_control_pub_2.publish(self.hiz_mesaji_2) 

        except Exception as e:
            self.log_yaz("ROBOT GO BACK ERROR", str(e))
            pass

    def solaDon(self):
        try:
            if self.anapencere.tabWidget.currentIndex()==0:
                pass

            if self.anapencere.tabWidget.currentIndex()==1:
                self.hiz_mesaji_1.linear.x=0.0
                self.hiz_mesaji_1.angular.z=0.5
                self.manuel_control_pub.publish(self.hiz_mesaji_1)        

            if self.anapencere.tabWidget.currentIndex()==2:

                self.hiz_mesaji_2.linear.x=0.0
                self.hiz_mesaji_2.angular.z=0.5
                self.manuel_control_pub_2.publish(self.hiz_mesaji_2)       

            if self.anapencere.tabWidget.currentIndex()==3:

                self.hiz_mesaji_1.linear.x=1.0
                self.hiz_mesaji_1.angular.z=0.0
                self.manuel_control_pub.publish(self.hiz_mesaji_1) 
                self.hiz_mesaji_2.linear.x=1.0
                self.hiz_mesaji_2.angular.z=0.0
                self.manuel_control_pub_2.publish(self.hiz_mesaji_2) 

                                     
        except Exception as e:
            self.log_yaz("ROBOT TURN LEFT ERROR", str(e))
            pass
    def sagaDon(self):
        try:
            if self.anapencere.tabWidget.currentIndex()==0:
                pass

            if self.anapencere.tabWidget.currentIndex()==1:
                self.hiz_mesaji_1.linear.x=0.0
                self.hiz_mesaji_1.angular.z=-0.5
                self.manuel_control_pub.publish(self.hiz_mesaji_1)        

            if self.anapencere.tabWidget.currentIndex()==2:

                self.hiz_mesaji_2.linear.x=0.0
                self.hiz_mesaji_2.angular.z=-0.5
                self.manuel_control_pub_2.publish(self.hiz_mesaji_2)       

            if self.anapencere.tabWidget.currentIndex()==3:

                self.hiz_mesaji_1.linear.x=1.0
                self.hiz_mesaji_1.angular.z=0.0
                self.manuel_control_pub.publish(self.hiz_mesaji_1) 
                self.hiz_mesaji_2.linear.x=1.0
                self.hiz_mesaji_2.angular.z=0.0
                self.manuel_control_pub_2.publish(self.hiz_mesaji_2) 
                                 
        except Exception as e:
            self.log_yaz("ROBOT TURN RIGHT",str(e))
            pass

    def ana_sayfa_manuel_kontrol_ac(self):
        try:
            login = Login()
            if login.exec_() == QtWidgets.QDialog.Accepted:
                self.anapencere.widgetSifreli.setEnabled(True)
                self.log_yaz("ANASAYFA SIFRELI KISIMA ", "GIRIS YAPILDI")

            elif login.exec_() == QtWidgets.QDialog.Rejected:
                self.log_yaz("ANASAYFA SIFRELI KISIM", "SIFRE YANLIS GIRILDI")
        except Exception as e:
            self.log_yaz("ANASAYFA LOGIN ", str(e))
            pass

    def ana_sayfa_manuel_kontrol_kapat(self):
        try:
            self.log_yaz("ANASAYFA SIFRELI KISIM ", "CIKIS YAPILDI")
            self.anapencere.widgetSifreli.setEnabled(False)
        except Exception as e:
            self.log_yaz("HOMEPAGE MANUEL CONTROL ERROR", str(e))

    def radio_button_toggle(self):
        try:
            if self.anapencere.radioButtonBaglantiDurumlari.isChecked():
                self.anapencere.radioButtonBaglantiDurumlari.setChecked(False)
                pass
            elif not self.anapencere.radioButtonBaglantiDurumlari.isChecked():
                self.anapencere.radioButtonBaglantiDurumlari.setChecked(True)
        except Exception as e:
            self.log_yaz("RADIO BUTTON TOGGLE ERROR",str(e))
            pass

    def log_yaz(self, elemanadi, hata):
        if elemanadi != self.elemanadi_old and hata != self.hata_old:
            datestring = datetime.now().strftime("%d-%m-%Y-%H.%M.%S")
            self.anapencere.listWidgetLog.addItem("{} : {} {}".format(datestring, elemanadi, hata))
            self.logfile.write("{}: {} - {}  \n".format(datestring, str(elemanadi), str(hata)))
            self.logfile.flush()
        else:
            pass

        self.elemanadi_old = elemanadi
        self.hata_old = hata

    def dosyadan_liste_oku(self, kuyrukadi):
        try:
            return_list = []
            with open(kuyrukadi, "rb") as f:
                for _ in range(pickle.load(f)):
                    return_list.append(pickle.load(f))

            return True, return_list
        except Exception as e:
            self.log_yaz("LISTE OKUMA FONKSIYON", str(e))
            return False, str(e)
            pass

    def dosyaya_liste_kaydet(self, kuyrukadi, liste):
        try:
            with open(kuyrukadi, "wb") as f:
                pickle.dump(len(liste), f)
                for value in liste:
                    pickle.dump(value, f)
            return True
        except Exception as e:
            self.log_yaz("KUYRUK KAYDETME FONKSIYON", str(e))
            return False
            pass

    def operator_ekle(self):
        try:

            operator_adi = self.anapencere.lineEditOperatorisimEkle.text()

            operator_sifre = self.anapencere.lineEditOperatorSifreEkle.text()
            if len(operator_adi) == 0 or len(operator_sifre) == 0:
                QtWidgets.QMessageBox.warning(self, 'OPERATOR EKLEME HATA',
                                            'OPERATOR ADI VEYA ŞİFRE BOŞ. \n LÜTFEN BİLGİ GİRİNİZ')

            else:
                kullanicilar = load_dict_from_file8bit("datalar/Kullanicilar.txt")
                kullanicilar['{}'.format(operator_adi)] = str(operator_sifre)
                save_dict_to_file(kullanicilar, "datalar/Kullanicilar.txt")
                QtWidgets.QMessageBox.warning(self, 'OPERATOR EKLEME BAŞARILI', 'EKLENEN OPERATOR \n '
                                                                                'ADI: {} \n ŞİFRESİ: {} \n \n'
                                                                                'YENI OPERATOR ILE GIRIS YAPABILMEK ICIN '
                                                                                'PROGRAMI YENIDEN BASLATINIZ'
                                                                                ''.format(operator_adi, operator_sifre))
        except Exception as e:
            self.log_yaz("ADD OPERATOR ERROR", str(e))
            pass

    def operator_sil_yenile(self):
        try:
            self.anapencere.comboBoxOperatorSil.clear()
            kullanicilar = load_dict_from_file8bit("datalar/Kullanicilar.txt")

            for tag in kullanicilar:
                self.anapencere.comboBoxOperatorSil.addItem(tag)
        except Exception as e:
            self.log_yaz("OPERATOR REMOVE AND RENAME ERROR", str(e))
            pass

    def operator_sil(self):
        try:
            kullanicilar = load_dict_from_file8bit("datalar/Kullanicilar.txt")
            operator_adi = self.anapencere.comboBoxOperatorSil.currentText()
            kullanicilar.pop(operator_adi)
            QtWidgets.QMessageBox.warning(self, 'OPERATOR SILME BAŞARILI', 'SILINEN OPERATOR \n '
                                                                        'ADI: {} \n'.format(operator_adi))
            save_dict_to_file(kullanicilar, "datalar/Kullanicilar.txt")
        except Exception as e:
            self.log_yaz("OPERATOR DELETE ERROR", str(e))
            pass
    def programi_kapat(self):
            self.log_yaz("PROGRAM CLOSED ERROR", "")
            self.close()
    
    def durak_kaydet(self):
        kontrol=False
        try:    
            if self.anapencere.tabWidget.currentIndex()==0 or self.anapencere.tabWidget.currentIndex()==4:

                self.anapencere.label_durak_log.setText("\nAMR SEÇİNİZ\n")
                self.anapencere.label_durak_log.setStyleSheet(self.stylesheet_kirmizi)

            if self.anapencere.tabWidget.currentIndex()==1 or self.anapencere.comboBox_amr_secim.currentIndex()==1:

                station=self.anapencere.lineEdit_durak_kaydet_durak_ismi.text()
                durak_notu=self.anapencere.lineEdit_durak_kaydet_durak_notu.text()
                if len(durak_notu)==0: durak_notu=" "
                if len(station)>0:

                    self.anapencere.lineEdit_durak_kaydet_durak_ismi.setStyleSheet(self.stylesheet_yesil)
                    QtCore.QTimer.singleShot(2000, lambda: self.anapencere.lineEdit_durak_kaydet_durak_ismi.setStyleSheet("background-color:none; border:none;"))
                    durak_dict_list = load_dict_from_file8bit(self.durak_kayit_dizini)           
                    for i in durak_dict_list:
                        if station == i:
                            kontrol = True
                    if kontrol:
                        self.anapencere.label_durak_log.setText("\nAGV1 STATION ALREADY AVAIABLE \n")
                        self.anapencere.label_durak_log.setStyleSheet(self.stylesheet_sari)
                        QtCore.QTimer.singleShot(2000, lambda: self.anapencere.label_durak_log.setText(""))                       
                        QtCore.QTimer.singleShot(2000, lambda: self.anapencere.label_durak_log.setStyleSheet("background-color:none; border:none;"))
                    else:
                        durak_dict_list = load_dict_from_file8bit(self.durak_kayit_dizini)
                        durak_dict_list.update({"{}".format(station): {'x':self.durak_kaydet_mesaj.pose.pose.position.x,
                                                                            'y':self.durak_kaydet_mesaj.pose.pose.position.y,
                                                                            'z':self.durak_kaydet_mesaj.pose.pose.position.z,
                                                                            'not':durak_notu}})


                        save_dict_to_file(durak_dict_list, self.durak_kayit_dizini)        

                        self.anapencere.label_durak_log.setText("\nAGV1 STATION SAVED\n")
                        self.anapencere.label_durak_log.setStyleSheet(self.stylesheet_yesil)
                        QtCore.QTimer.singleShot(2000, lambda: self.anapencere.label_durak_log.setText(""))                       
                        QtCore.QTimer.singleShot(2000, lambda: self.anapencere.label_durak_log.setStyleSheet("background-color:none; border:none;"))
                        self.durak_listesi_yenile()
                else:
                    self.anapencere.label_durak_log.setText("\nAGV1 WRITE STATION NAME \n")
                    self.anapencere.label_durak_log.setStyleSheet(self.stylesheet_sari)
                    self.anapencere.lineEdit_durak_kaydet_durak_ismi.setStyleSheet(self.stylesheet_kirmizi)              
                    QtCore.QTimer.singleShot(2000, lambda: self.anapencere.lineEdit_durak_kaydet_durak_ismi.setStyleSheet("background-color:none; border:none;"))

            if self.anapencere.tabWidget.currentIndex()==2 or self.anapencere.comboBox_amr_secim.currentIndex()==2:

                station=self.anapencere.lineEdit_durak_kaydet_durak_ismi.text()
                durak_notu=self.anapencere.lineEdit_durak_kaydet_durak_notu.text()
                if len(durak_notu)==0: durak_notu=" "
                if len(station)>0:

                    self.anapencere.lineEdit_durak_kaydet_durak_ismi.setStyleSheet(self.stylesheet_yesil)
                    QtCore.QTimer.singleShot(2000, lambda: self.anapencere.lineEdit_durak_kaydet_durak_ismi.setStyleSheet("background-color:none; border:none;"))
                    durak_dict_list = load_dict_from_file8bit(self.durak_kayit_dizini)           
                    for i in durak_dict_list:
                        if station == i:
                            kontrol = True
                    if kontrol:
                        self.anapencere.label_durak_log.setText("\nAGV2 STATION ALREADY AVAIABLE \n")
                        self.anapencere.label_durak_log.setStyleSheet(self.stylesheet_sari)
                        QtCore.QTimer.singleShot(2000, lambda: self.anapencere.label_durak_log.setText(""))                       
                        QtCore.QTimer.singleShot(2000, lambda: self.anapencere.label_durak_log.setStyleSheet("background-color:none; border:none;"))
                    else:
                        durak_dict_list = load_dict_from_file8bit(self.durak_kayit_dizini)
                        durak_dict_list.update({"{}".format(station): {'x':self.durak_kaydet_mesaj.pose.pose.position.x,
                                                                            'y':self.durak_kaydet_mesaj.pose.pose.position.y,
                                                                            'z':self.durak_kaydet_mesaj.pose.pose.position.z,
                                                                            'not':durak_notu}})


                        save_dict_to_file(durak_dict_list, self.durak_kayit_dizini)        

                        self.anapencere.label_durak_log.setText("\nAGV2 STATION SAVED \n")
                        self.anapencere.label_durak_log.setStyleSheet(self.stylesheet_yesil)
                        QtCore.QTimer.singleShot(2000, lambda: self.anapencere.label_durak_log.setText(""))                       
                        QtCore.QTimer.singleShot(2000, lambda: self.anapencere.label_durak_log.setStyleSheet("background-color:none; border:none;"))
                        self.durak_listesi_yenile()
                else:
                    self.anapencere.label_durak_log.setText("\nAGV2 WRITE STATION NAME \n")
                    self.anapencere.label_durak_log.setStyleSheet(self.stylesheet_sari)
                    self.anapencere.lineEdit_durak_kaydet_durak_ismi.setStyleSheet(self.stylesheet_kirmizi) 
                    QtCore.QTimer.singleShot(2000, lambda: self.anapencere.lineEdit_durak_kaydet_durak_ismi.setStyleSheet("background-color:none; border:none;"))

            
        except Exception as e:

            self.anapencere.label_durak_log.setText(str(e))

            self.log_yaz("STATION SAVE ERROR", str(e))
            pass


    def durak_listesi_yenile(self):
        try:
            self.anapencere.comboBox_durak_sil_liste.clear()
            self.anapencere.tableWidget_durak_listesi.setRowCount(0)
            durak_dict_list = load_dict_from_file8bit(self.durak_kayit_dizini)

            self.anapencere.label_durak_sayici.setText(str(len(durak_dict_list)))
            for key, deger in durak_dict_list.items() :
                self.anapencere.comboBox_durak_sil_liste.addItem(key)

                durum, lot = self.del_none_keys(deger)
                if durum:
                    rowPosition = self.anapencere.tableWidget_durak_listesi.rowCount()
                    self.anapencere.tableWidget_durak_listesi.insertRow(rowPosition)


                    self.anapencere.tableWidget_durak_listesi.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(str(key)))
                    self.anapencere.tableWidget_durak_listesi.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem("{:.4f}".format(deger['x'])))
                    self.anapencere.tableWidget_durak_listesi.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem("{:.4f}".format(deger['y'])))
                    self.anapencere.tableWidget_durak_listesi.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem("{:.4f}".format(deger['z'])))
                    self.anapencere.tableWidget_durak_listesi.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(deger['not']))
                       
                else:
                    self.log_yaz("STAION LIST UPLOAD ERROR 1 ", str(lot))
                    pass
                

        except Exception as e:
            self.anapencere.label_durak_log.setText(str(e))
            self.anapencere.label_durak_log.setStyleSheet(self.stylesheet_kirmizi)
            self.log_yaz("STATION LIST RENAME ERROR",str(e))
            pass

    def del_none_keys(self, dict_gelen):
            try:
                for eleman in dict_gelen.keys():
                    if dict_gelen[eleman] is None:
                        dict_gelen[eleman] = ""
                return True, dict_gelen
            except Exception as e:
                self.log_yaz("DEL N0NE KEYS ERROR ", str(e))
                False, str(e)
                pass

    def durak_sil(self):
        try:
            kontrol=False
            station=self.anapencere.comboBox_durak_sil_liste.currentText()
            durak_dict_list = load_dict_from_file8bit(self.durak_kayit_dizini)           
            for i in durak_dict_list:
                if station == i:
                    kontrol = True       
            if  kontrol:
                del durak_dict_list["{}".format(station)]
                save_dict_to_file(durak_dict_list, self.durak_kayit_dizini)
                self.anapencere.label_durak_log.setText("{} NAMED STATION REMOVED ".format(station))
                self.durak_listesi_yenile()                

            else:
                self.anapencere.label_durak_log.setText("\THE STATION DOES NOT AVAIABLE.\n")                
        except Exception as e:
            self.anapencere.label_durak_log.setText(str(e))            
            self.log_yaz("STATION DELETE ERROR",str(e))

            pass

    def ROS_ayarlari_kaydet(self):
        style = "border: 5px solid  rgb(0, 0, 0);border-radius:15px;"
        try:
            harita_1_name = self.anapencere.lineEditAyarlarHarita1.text()
            harita_2_name = self.anapencere.lineEditAyarlarHarita2.text()
            agv_icon_name = self.anapencere.lineEditAyarlarAGVicon.text()
            agv2_icon_name = self.anapencere.lineEditAyarlarAGV2icon.text()
            istasyon_kayit_dosyasi = self.anapencere.lineEditAyarlarDurakKayitDosyasi.text()

            portlar_dict = load_dict_from_file8bit(self.portlar_dosyasi)

            portlar_dict["HARITA_1_NAME"] = harita_1_name
            portlar_dict["HARITA_2_NAME"] = harita_2_name
            portlar_dict["AGV_ICON_NAME"] = agv_icon_name
            portlar_dict["AGV2_ICON_NAME"] = agv2_icon_name
            portlar_dict["ISTASYON_KAYIT_DOSYASI"] = istasyon_kayit_dosyasi

            save_dict_to_file(portlar_dict, self.portlar_dosyasi)
            self.anapencere.labelRosAyarlariLog.setStyleSheet(self.stylesheet_yesil)
            QtCore.QTimer.singleShot(2000, lambda: self.anapencere.labelRosAyarlariLog.setStyleSheet(style))

            self.anapencere.labelRosAyarlariLog.setText("AYARLAR KAYDEDILDI.\nLUTFEN PROGRAMI YENIDEN BASLATIN")
        except Exception as e:
            self.anapencere.labelRosAyarlariLog.setText("HATA!\n{}".format(e))
            self.anapencere.labelRosAyarlariLog.setStyleSheet(self.stylesheet_kirmizi)
            QtCore.QTimer.singleShot(2000, lambda: self.anapencere.labelRosAyarlariLog.setStyleSheet(style))

            self.log_yaz("PLC ROS SETTINGS CHANGE ERROR", str(e))
            pass            

class LoginPencere(QtWidgets.QDialog, Ui_AcilisPage):

    def __init__(self, parent=None):
        
        super(LoginPencere, self).__init__(parent=parent)
        self.loginpencere = Ui_AcilisPage()
        self.loginpencere.setupUi(self)

        self.kullanicilar = load_dict_from_file8bit("datalar/Kullanicilar.txt")

        for tag in self.kullanicilar:
            self.loginpencere.comboBoxKullanicilar.addItem(tag)

        self.loginpencere.pushButtonCancel.clicked.connect(lambda: self.close())
        self.loginpencere.pushButtonLogin.clicked.connect(self.handle_login)

    def handle_login(self):
        kullanici_adi = self.loginpencere.comboBoxKullanicilar.currentText()
        if self.loginpencere.lineEditSifre.text() == self.kullanicilar[str(kullanici_adi)]:
            sozluk = load_dict_from_file8bit("datalar/GeciciVeriler.txt")
            sozluk["mevcut_kullanici"] = kullanici_adi
            save_dict_to_file(sozluk, "datalar/GeciciVeriler.txt")
            self.splashpencere = SplashScreen()
            self.splashpencere.show()
            self.close()
        else:
            QtWidgets.QMessageBox.warning(self, 'MANUEL KONTROL SAYFASI HATA', 'KULLANICI ADI VEYA SIFRE HATALI')


class Login(QtWidgets.QDialog, Ui_LoginPage):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)

        self.loginpencere = Ui_LoginPage()
        self.loginpencere.setupUi(self)

        self.loginpencere.pushButtonLogin.clicked.connect(self.handle_login)
        self.loginpencere.pushButtonCancel.clicked.connect(self.cancel)

    def handle_login(self):
        if self.loginpencere.lineEditKullanici.text() == 'stu' and self.loginpencere.lineEditSifre.text() == 'optimak123':
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self, 'ANASAYFA MANUEL KONTROL HATA', 'KULLANICI ADI VEYA SIFRE HATALI')

    def cancel(self):
        self.reject()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = AnaPencere()
    mainWindow.show()

    sys.exit(app.exec_())


