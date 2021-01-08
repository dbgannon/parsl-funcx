import tkinter
import cv2
import PIL.Image # PIL.ImageTk
import PIL.ImageTk as ImageTk
import tkinter.scrolledtext as st
from tkinter import Frame
from tkinter import Label
import time
import os
import boto3
import json
import threading

accnts = {"az_name":"xxxxe",
          "az_key":"xxx4Dx9tOE5dSDaj/x+ug==;EndpointSuffix=core.windows.net",
          'aw_id':"xxxxx",
          'aw_sec_key':"xxxxxx"}
sqs = boto3.resource('sqs', 'us-west-2', aws_access_key_id=accnts['aw_id'],
                          aws_secret_access_key=accnts['aw_sec_key'])
q1 = sqs.get_queue_by_name(QueueName='funcx-queue1.fifo')
q2 = sqs.get_queue_by_name(QueueName='funcx-queue2.fifo')
# Create a window
window = tkinter.Tk()
frame1 = Frame(window)
frame2 = Frame(window)

window.title("talk to jetbot")


from PIL import Image, ImageDraw, ImageFont


# create Image object with the input image

 
#image = Image.open('xxxx.jpg')
#cv_img = cv2.cvtColor(cv2.imread("xxxx.jpg"), cv2.COLOR_BGR2RGB)
#canvas = tkinter.Canvas(frame2,  width = width+10, height = height+10)

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

def receive_message(queue, max_number, wait_time):
    try:
        messages = queue.receive_messages(
            MessageAttributeNames=['All'],
            MaxNumberOfMessages=max_number,
            WaitTimeSeconds=wait_time
        )
    except ClientError as error:
        raise error
    else:
        return messages
def send_message(queue, message_body):
    try:
        response = queue.send_message(
            MessageBody=message_body,
            MessageAttributes={},
            MessageGroupId='funcx',
            MessageDeduplicationId=str(time.time())
        )
    except ClientError as error:
        logger.exception("Send message failed: %s", message_body)
        raise error
    else:
        return response


text_area.insert(tkinter.INSERT, "ready.")
endt = 'end'

def run_listen_loop():
    done = False
    endt = 'end'
    while not done:
        m =receive_message(q1, 1, 3)
        if m != []:
            bod = m[0].body
            m[0].delete()
            bod = bod.replace("'", '"')
            bod = json.loads(bod)
            if "class" in bod:
                clas = bod["class"]
                t = bod["time"]
                localpath = 'c:/Users/ganno/Onedrive/docs13/xx.jpg'
                os.system('scp jetbot@10.0.0.6:'+'image-file.jpg'+' '+localpath)
                img2 = ImageTk.PhotoImage(Image.open('xx.jpg'))
                panel.configure(image=img2)
                panel.image = img2
                endt = 'end'
                text_area.insert(endt, clas+" "+str(t)+"\n" )              
            elif "info" in bod:
                text_area.insert(endt, bod["info"]+"\n" )
            elif "action" in bod:
                print(bod)
                done = True

t1 = threading.Thread(target=run_listen_loop, args=())

def ask_for_image():
    send_message(q2, '{"action":"take picture"}' )
    return ("asked for picture")    

def quit():
    send_message(q2, '{"action":"quit"}' )
    t1.join()
    print('thread jointed')
    #t1.stop()
    print('thread stopped')
    exit()

btn_blur=tkinter.Button(window, text="send image request", width=50, command=ask_for_image)
btn_blur.pack(anchor=tkinter.CENTER, expand=True)
btn_quit=tkinter.Button(window, text="quit", width=50, command=quit)
btn_quit.pack(anchor=tkinter.CENTER, expand=True)

frame1.pack(padx=1, pady=1)
frame2.pack(padx=10, pady=20)
# Run the window loop
#text_area.configure(state ='disabled')
t1.start()
window.mainloop() 
