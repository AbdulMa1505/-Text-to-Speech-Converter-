import pyttsx3
import time
import pyperclip
import tkinter as tk
from tkinter import filedialog

# Initialize pyttsx3 engine
engine = pyttsx3.init()

def list_voices():
    voices = engine.getProperty('voices')
    print("Available voices:")
    for index, voice in enumerate(voices):
        print(f"{index}: {voice.name}")
    return voices

def set_voice():
    voices = list_voices()
    voice_choice = int(input("Choose a voice (enter number): "))
    engine.setProperty('voice', voices[voice_choice].id)

def set_speech_rate():
    rate = engine.getProperty('rate')
    print(f"Current rate: {rate}")
    new_rate = int(input("Enter new speech rate (default is 200): "))
    engine.setProperty('rate', new_rate)

def save_speech_to_file(text):
    filename = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("Audio files", "*.mp3")])
    if filename:
        engine.save_to_file(text, filename)
        engine.runAndWait()
        print(f"Audio saved as {filename}")

def convert_text_to_speech(text):
    engine.say(text)
    engine.runAndWait()

def convert_file_to_speech():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            file_text = file.read()
            convert_text_to_speech(file_text)

def read_clipboard():
    clipboard_text = pyperclip.paste()
    print(f"Clipboard content: {clipboard_text}")
    convert_text_to_speech(clipboard_text)

def handle_user_input():
    user_input = input("Enter text to convert to speech, or type 'file', 'clipboard', 'quit': ").strip().lower()
    
    if user_input == 'file':
        convert_file_to_speech()
    elif user_input == 'clipboard':
        read_clipboard()
    elif user_input == 'quit':
        print("Exiting...")
    else:
        if user_input:
            convert_text_to_speech(user_input)
            save_speech_to_file(user_input)
        else:
            print("No text entered. Exiting.")

def gui_mode():
    #  a simple GUI with tkinter
    window = tk.Tk()
    window.title("Text to Speech")

    def on_convert_button():
        text = text_input.get("1.0", tk.END).strip()
        if text:
            convert_text_to_speech(text)

    def on_save_button():
        text = text_input.get("1.0", tk.END).strip()
        if text:
            save_speech_to_file(text)

    frame = tk.Frame(window)
    frame.pack()

    text_input = tk.Text(frame, height=10, width=40)
    text_input.pack()

    convert_button = tk.Button(frame, text="Convert to Speech", command=on_convert_button)
    convert_button.pack(side=tk.LEFT)

    save_button = tk.Button(frame, text="Save as Audio", command=on_save_button)
    save_button.pack(side=tk.LEFT)

    quit_button = tk.Button(frame, text="Quit", command=window.quit)
    quit_button.pack(side=tk.LEFT)

    window.mainloop()

if __name__ == "__main__":
    print("Welcome to the Text to Speech Converter!")
    set_voice()          # Set voice
    set_speech_rate()    # Set speech rate

    mode = input("Choose mode: 'gui' for graphical interface or 'cli' for command-line interface: ").strip().lower()

    if mode == 'gui':
        gui_mode()  # Launch the GUI mode
    else:
        handle_user_input()  # CLI mode for manual input or file processing
