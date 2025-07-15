    
import keyboard
import socket
import protocol
import pyautogui
import time
import mouse
import base64
import time
import threading
IP = '192.168.7.19'
#TCP_PORT = 5000 
PHOTO_PATH = "d:\מועדון המתכנתים\screenshots_for_playing_screen.png"

def new_key(event):
    #print("new event")
    button_pressed = event.name
    if button_pressed == "space":
        button_pressed = " "
    if button_pressed == "enter":
        button_pressed = "\n"
    if button_pressed == "shift 2":
        button_pressed = "@"
    return button_pressed.decode()    





def client():
    
    def keys(event):
        #שולח ללקוח את לחיצות המקלדת שלי דרך סוקט (צריך לוודא שיש לי גישה לקרנל כדי שזה יעבוד) 
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   ;   print ("server Socket created successfully.")
        S_IP_PORT_TUPLE = (IP, 5000)  
        server.bind(S_IP_PORT_TUPLE)                  
        server.listen(1)                   ;  print ("Waiting for a connection...")      
        client_socket, addr = server.accept()   ;   print ("Connected with " + addr[0] + " " + str(addr[1]))  
        op, click = protocol.get_msg(client_socket)
        pyautogui.write(click)


    def mousemove():        
        #שולח ללקוח את תזוזות ולחיצות העכבר שלי דרך סוקט (צריך לוודא שיש לי גישה לקרנל כדי שזה יעבוד) 
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   ;   print ("server Socket created successfully.")
        S_IP_PORT_TUPLE = (IP, 5001)  
        server.bind(S_IP_PORT_TUPLE)                  
        server.listen(1)                   ;  print ("Waiting for a connection...")      
        client_socket, addr = server.accept()   ;   print ("Connected with " + addr[0] + " " + str(addr[1]))  
        op, cords = protocol.get_msg(client_socket)
        pyautogui.moveTo(cords[0], cords[1])

    def mouseclick():  
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   ;   print ("server Socket created successfully.")
        S_IP_PORT_TUPLE = (IP, 5002)  
        server.bind(S_IP_PORT_TUPLE)                  
        server.listen(1)                   ;  print ("Waiting for a connection...")      
        client_socket, addr = server.accept()   ;   print ("Connected with " + addr[0] + " " + str(addr[1]))
        op, click = protocol.get_msg(client_socket) 
        if click[0] == 'right' and click[1] == 'p':
            mouse.click('right')
        elif click[0] == 'left' and click[1] == 'p':
            mouse.click('left')    
        elif click[0] == 'right' and click[1] == 'r':
            mouse.release('right')
        elif click[0] == 'left' and click[1] == 'r':
            mouse.release('left')    

    def mousescroll():
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   ;   print ("server Socket created successfully.")
        S_IP_PORT_TUPLE = (IP, 5003)  
        server.bind(S_IP_PORT_TUPLE)                  
        server.listen(1)                   ;  print ("Waiting for a connection...")      
        client_socket, addr = server.accept()   ;   print ("Connected with " + addr[0] + " " + str(addr[1]))
        op, data = protocol.get_msg(client_socket)
        mouse.scroll(data)

        
    def screen():
        #מקבל תמונות מהלקוח דרך סוקט כל הזמן ומציב בעזרת טיקיי אינטר
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   ;   print ("server Socket created successfully.")
        S_IP_PORT_TUPLE = (IP, 5004)  
        server.bind(S_IP_PORT_TUPLE)                     
        #client_socket, addr = server.accept()   ;   print ("Connected with " + addr[0] + " " + str(addr[1]))
        image = pyautogui.screenshot()
        image = image.resize((200, 100))
        image.save(PHOTO_PATH)
        with open(PHOTO_PATH, 'rb') as f:
            data = f.read()
        data = protocol.create_msg((base64.b64encode(data)).decode('ascii'))
        server.sendto(data,S_IP_PORT_TUPLE)
    threading.Thread(target=keys).start()
    threading.Thread(target=mousemove).start()
    threading.Thread(target=mouseclick).start()
    threading.Thread(target=mousescroll).start()    
    while True:
        screen()
        time.sleep(0.03125)
client()    
