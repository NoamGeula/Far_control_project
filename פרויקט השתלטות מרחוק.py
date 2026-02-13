    
import win32api
import pyautogui
import keyboard
import socket
import protocol
from pynput import mouse
from pynput.mouse import Listener
import time
from tkinter import *
import base64
SAVED_PHOTO_LOCATION = "d:\מועדון המתכנתים\screenshots_for_playing_screen"
IP = '192.168.7.6'
#TCP_PORT = 5000 

def new_key(event):
    #print("new event")
    button_pressed = event.name
    if button_pressed == "space":
        button_pressed = " "
    if button_pressed == "enter":
        button_pressed = "\n"
    if button_pressed == "shift 2":
        button_pressed = "@"
    return button_pressed  

def serverME():
    def keys(event):
        #שולח ללקוח את לחיצות המקלדת שלי דרך סוקט (צריך לוודא שיש לי גישה לקרנל כדי שזה יעבוד) 
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  ;  
        S_IP_PORT_TUPLE = (IP, 5000)  
        client_socket.connect(S_IP_PORT_TUPLE)   ;   print ("Established connection with the server.")
        packet = protocol.create_msg(new_key(event))
        client_socket.send(packet)

    def mousemove():        
        #שולח ללקוח את תזוזות ולחיצות העכבר שלי דרך סוקט (צריך לוודא שיש לי גישה לקרנל כדי שזה יעבוד) 
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  ;  
        S_IP_PORT_TUPLE = (IP, 5001)  
        client_socket.connect(S_IP_PORT_TUPLE)   ;   print ("Established connection with the server.")
        x, y = pyautogui.position()
        packet = protocol.create_msg([x,y])# יש סיכוי שלהעביר רשימה יעשה בעיה
        client_socket.send(packet)
    listener1 = mouse.Listener(on_move=mousemove) #לדעתי זה תוקע את הקוד כי זה לא ימשיך למטה, צריך נראה לי לעשות בטרד לבד
    listener1.start()#גם זה

    def mouseclick():
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  ;  
        S_IP_PORT_TUPLE = (IP, 5002)  
        client_socket.connect(S_IP_PORT_TUPLE)   ;   print ("Established connection with the server.")
        state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
        state_right = win32api.GetKeyState(0x02)  # Right button down = 0 or 1. Button up = -127 or -128
        a = win32api.GetKeyState(0x01)
        b = win32api.GetKeyState(0x02)
        if a != state_left:  # Button state changed
            state_left = a
            if a < 0:
                packet = protocol.create_msg(['left','p'])
            else:
                packet = protocol.create_msg(['left','r'])

        elif b != state_right:  # Button state changed
            state_right = b
            if b < 0:
                packet = protocol.create_msg(['right','p'])
            else:
                packet = protocol.create_msg(['right','r'])
        client_socket.send(packet)        
    with mouse.Listener(on_click=mouseclick) as listener2:
        listener2.join()

    keyboard.on_press(keys)
    keyboard.wait()

    def mousescroll(dy):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  ;  
        S_IP_PORT_TUPLE = (IP, 5003)  
        client_socket.connect(S_IP_PORT_TUPLE)   ;   print ("Established connection with the server.")
        client_socket.send(protocol.create_msg(dy))


    def on_scroll(x, y, dx, dy):
        mousescroll(dy)    

    listener3 = Listener(on_scroll=on_scroll)   
    listener3.start()         
    keyboard.wait()
    
    def screen():
        #מקבל תמונות מהלקוח דרך סוקט כל הזמן ומציב בעזרת טיקיי אינטר
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  ;  
        S_IP_PORT_TUPLE = (IP, 5004)  
        op, data = protocol.get_msgUDP(client_socket)
        with open(SAVED_PHOTO_LOCATION,'wb') as f:
            f.write(base64.b64decode(data))
        root = Tk()
    
        canvas = Canvas(root,  width=400, height=400)
        canvas.pack()
    
        img = PhotoImage(file = SAVED_PHOTO_LOCATION)
        canvas.create_image(10, 10, anchor=NW, image=img)
    
        mainloop()
    while True:
        screen()
        time.sleep(0.03125)
serverME()        

    
    



















