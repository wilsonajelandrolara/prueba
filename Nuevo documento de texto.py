import datetime
import time
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
LED1=15
LED2=16
boton1=22
boton2=18
def on_message(client,obj,msg):
    print(msg.topic+" "+str(msg.qos)+" "+msg.payload.decode('utf-8'))

GPIO.setmode(GPIO.BOARD)

def main():
    MIFecha=""
    MIHora=""

    mqttc=mqtt.Client()
    mqttc.on_message=on_message
    mqttc.username_pw_set("wlara123@outlook.es","tomatitos1")
    mqttc.connect("maqiatto.com",1883)
    mqttc.subscribe("wlara123@outlook.es/prueba",0)

    GPIO.setup(boton1,GPIO.IN)
    GPIO.setup(boton2,GPIO.IN)
    GPIO.setup(LED1,GPIO.OUT)
    GPIO.setup(LED2,GPIO.OUT)
    cntInfo=0
    Arch=open("DGuardados.dat","w")
    Arch.close()
    while(1):
        mqttc.loop()
        MIFecha=str(datetime.date.today())
        MIHora=time.strftime("%H;%M;%S")

        GPIO.output(LED1,0)
        GPIO.output(LED2,0)

        if(GPIO.input(boton1)==1):
            Arch=open("DGuardados.dat","a")
            mqttc.publish("wlara123@outlook.es/prueba","1:0:-")
            GPIO.output(LED1,1)
            Arch.write(MIFecha+" "+MIHora+"---->UNO presionado \n")
            Arch.close()
            time.sleep(1) 
            cntInfo=1 
        if(GPIO.input(boton2)==1):
            Arch=open("DGuardados.dat","a")
            Arch.write(MIFecha+" "+MIHora+"---->DOS presionado \n")
            Arch.close()
            mqttc.publish("wlara123@outlook.es/prueba","0:1:-")
            GPIO.output(LED2,1)
            time.sleep(1)
            cntInfo=1
        if(cntInfo==1):
            Arch = open("DGuardados.dat","r")
            mqttc.publish("wlara123@outlook.es/prueba","0:0"+":"+Arch.read())
            Arch.close()
            time.sleep(1)
        cntInfo=0
  
        