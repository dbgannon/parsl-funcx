import tkinter
import cv2
import PIL.Image # PIL.ImageTk
import PIL.ImageTk as ImageTk
import tkinter.scrolledtext as st
from tkinter import Frame
from tkinter import Label
import time
import os
import sys
import pika
import json
import threading
creds = pika.PlainCredentials('jetbot','jetbot')
parms = pika.ConnectionParameters('10.0.0.30', 5672, "/", creds)
connection = pika.BlockingConnection(parms)
# Create a window
window = tkinter.Tk()
frame1 = Frame(window)
frame2 = Frame(window)

window.title("talk to jetbot")


from PIL import Image, ImageDraw, ImageFont

img = ImageTk.PhotoImage(Image.open('xxxx.jpg'))
panel = Label(frame2, image=img)
panel.pack(side="bottom", fill="both", expand="yes")

# initialise the drawing context with
# the image object as backgroun
#photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv_img))
#canvas.create_image(1, 5, image=photo, anchor=tkinter.NW)
text_area = st.ScrolledText(frame1, 
                            width = 60,  
                            height = 4,  
                            font = ("Times New Roman", 
                                    9)) 
text_area.grid(column = 0, pady = 10, padx = 10) 
text_area.pack()

channel = connection.channel()
channel.queue_declare('hello')
channel.queue_declare('command')

def receive_message(channel, max_number, wait_time):
    #print('doing the call')
    method_frame, header_frame, body = channel.basic_get('hello')
    if method_frame:
        print(method_frame, header_frame, body)
        channel.basic_ack(method_frame.delivery_tag)
        return body
    else:
        #print('No message returned')
        #time.sleep(wait_time)
        return ''
def send_message(channel, message_body):
    channel.basic_publish(exchange='',
                      routing_key='command',
                      body=message_body)


endt =  'end'
text_area.insert(tkinter.INSERT, "ready.")
text_area.insert(endt, "\n" )
text_area.see(endt)

def got_message(ch, method, properites, body):
    endt = 'end'
    if body != '':
        bod = body.decode("utf-8")
        bod = bod.replace("'", '"')
        print('bod =', bod)
        bod = json.loads(bod)
        #print('decodeing', bod['info'])
        if "class" in bod:
            print(bod["class"],bod["time"])
            localpath = 'c:/Users/ganno/Onedrive/docs13/xx.jpg'
            #os.system('scp jetbot@[2601:603:f80:6310::bc67]:'+'image-file.jpg'+' '+localpath)
            os.system('scp jetbot@10.0.0.6:'+'image-file.jpg'+' '+localpath)
            img2 = ImageTk.PhotoImage(Image.open('xx.jpg'))
            panel.configure(image=img2)
            panel.image = img2
            endt = 'end'
            clas = bod["class"]
            t = bod["time"]
            text_area.insert(endt, clas+" "+str(t)+"\n" )
            text_area.see(endt)
            #channel.stop_consuming()
        elif "info" in bod:
            text_area.insert(endt, bod["info"]+"\n" )

def ask_for_image():
    send_message(channel, "take picture")  # '{"action":"take picture"}' )
    print ('asked')
    #channel.start_consuming()    

def rabit_tread(got_message):
    channel.basic_consume(queue='hello', on_message_callback=got_message, auto_ack=True)
    channel.start_consuming()

def quit():
    print('sending quit')
    send_message(channel, "quit") # '{"action":"quit"}' )
    channel.stop_consuming()
    t1.join()
    print('thread jointed')
    print('thread stopped')
    sys.exit()

btn_blur=tkinter.Button(window, text="send image request", width=50, command=ask_for_image)
btn_blur.pack(anchor=tkinter.CENTER, expand=True)
btn_quit=tkinter.Button(window, text="quit", width=50, command=quit)
btn_quit.pack(anchor=tkinter.CENTER, expand=True)

frame1.pack(padx=1, pady=1)
frame2.pack(padx=10, pady=20)

t1 = threading.Thread(target=rabit_tread, args=(got_message,))
# Run the window loop
t1.start()
window.mainloop() 
