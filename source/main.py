import speech_recognition as sr
from tkinter import *
from tkinter import ttk
import os
import pyaudio
import openai
import pyttsx3
openai.api_key = "OPENAI-SECRET-API-KEY"
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)
root = Tk()
style = ttk.Style(root)
root.title("VoiceGPT")
if os.name == 'nt':  # Windows
    root.iconbitmap('devdan.ico')
else:
    img = PhotoImage(file='devdan.png')
    root.tk.call('wm', 'iconphoto', root._w, img)
root.geometry('600x400')
root.resizable(False,True)
texte = ""
responsew = ""

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def listen_audio(event):
    global texte, listen_audio_called, responsew
    print("Clicked")
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Recording...")
        audio = r.listen(source, phrase_time_limit=5,timeout=3)
        try:
            listen_audio_called = True
            texte = r.recognize_google(audio)
            print(texte)
            model = "gpt-3.5-turbo"
            response = openai.ChatCompletion.create(
                model=model,
                messages = [{"role":"assistant","content":texte,}]
                )
            responsew = response.choices[0].message.content
            print(responsew)
            speak_text(responsew)
            popup = Toplevel()
            popup.title("ChatGPT's Response")
            popup.geometry('500x100')
            response_label = Label(popup, text=responsew, font=('Helvetica', 12), wraplength=400)
            response_label.pack(padx=20, pady=20)
        except sr.UnknownValueError:
            print("Speech recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Error: {e}")

    c.itemconfig("button", outline="")

def update_text():
    global texte, responsew
    if listen_audio_called: 
        c.itemconfig(sumn, text=f"You said: {texte}")
    else:
        c.itemconfig(sumn, text="Say Something!")
    root.after(100, update_text)

x0 = 220
y0 = 30
x1 = 360
y1 = 170
r = sr.Recognizer()
c = Canvas(root, width=890, height=480)
c.pack()
listen_audio_called = False
c.create_oval(x0,y0,x1,y1,fill="Black")
c.create_text((x0 + x1) // 2, (y0 + y1) // 2, text="Speak", fill="white", font=("Helvetica", 20, "bold"))
sumn = c.create_text((x0 + x1) // 2, y1 + 20, text="", font=("Helvetica", 12))
c.tag_bind("button", "<Button-1>", listen_audio)
c.create_oval(x0, y0, x1, y1, outline="", tags="button")

update_text()
root.mainloop()