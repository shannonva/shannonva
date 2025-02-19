import os
import tkinter as tk
from tkinter import messagebox, filedialog
import whisper
import sounddevice as sd
import wave
import numpy as np

# Set FFmpeg path explicitly
#idhu vandhu different audio files ah read pannum okk
os.environ["FFMPEG_BINARY"] = r"C:\ffmpeg\bin\ffmpeg.exe"

print("stage 1 ok")

# Morse Code Dictionary
#idhu vandhu letters ah morse alternatives ah mattum ?? text letters gets convereterd to morse using this dictionerys every sinlge letters and considers them as akey so it will bring its key value when running which is the more codes
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
    '9': '----.', '0': '-----', ', ': '--..--', '.': '.-.-.-', '?': '..--..',
    '/': '-..-.', '-': '-....-', '(': '-.--.', ')': '-.--.-', ' ': '/'
}

# Function to convert text to morse code
def text_to_morse(text):
    # Ensure the text is in uppercase
    text = text.upper()
    print(text)
    morse_code = []
    for char in text:
        if char in MORSE_CODE_DICT:
            morse_code.append(MORSE_CODE_DICT[char])
        else:
            morse_code.append('/')
    return ' '.join(morse_code)

# Function to transcribe speech to text using Whisper
def speech_to_text():
    model = whisper.load_model("base")  # Load the Whisper model
    #idhula andha base means power and accuracy level 
    
    # Record audio from microphone using sounddevice
    record_audio()
    
    # Transcribe the recorded audio file
    result = model.transcribe("recorded_audio.wav")
    transcription = result["text"]
    
    # Convert the transcription to Morse code
    morse_code = text_to_morse(transcription)
    
    # Display the transcription and Morse code
    transcription_text.set(transcription)
    morse_code_text.set(morse_code)
    
    # Show a message box with the result
    messagebox.showinfo("Speech to Text", "Transcription and Morse code conversion complete!")

# Function to record audio from microphone using sounddevice
def record_audio():
    # Set up audio parameters
    rate = 44100
    duration =  20 # seconds
    channels = 2
    
    # Notify the user to speak
    messagebox.showinfo("Recording", "Recording started! Speak now...")
    
    # Record audio using sounddevice
    audio_data = sd.rec(int(rate * duration), samplerate=rate, channels=channels, dtype='int16')
    sd.wait()  # Wait for the recording to finish
    
    # Save the recorded audio to a file
    with wave.open("recorded_audio.wav", 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)  # 2 bytes (16-bit audio)
        wf.setframerate(rate)
        wf.writeframes(audio_data.tobytes())
    
    # Notify the user that the recording is done
    messagebox.showinfo("Recording", "Recording saved as 'recorded_audio.wav'")

# Function to save transcribed text to a file
def save_text():
    # Ask the user for a file location to save the transcription
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(transcription_text.get())
        messagebox.showinfo("Save", "File saved successfully!")























# Create the main window
root = tk.Tk()
root.title("Speech to Text & Morse Code Converter")

# Set window size
root.geometry("600x500")

# Create a button to start speech-to-text and Morse code conversion
speech_to_text_button = tk.Button(root, text="Record and Transcribe Speech", font=("Arial", 14), command=speech_to_text)
speech_to_text_button.pack(pady=10)

# Create a label to display the transcription result
transcription_text = tk.StringVar()
transcription_label = tk.Label(root, textvariable=transcription_text, font=("Arial", 14), height=2, wraplength=500)
transcription_label.pack(pady=20)

# Create a label to display the Morse code result
morse_code_text = tk.StringVar()
morse_code_label = tk.Label(root, textvariable=morse_code_text, font=("Arial", 14), height=2, wraplength=500)
morse_code_label.pack(pady=20)

# Create a button to save the transcribed text
save_button = tk.Button(root, text="Save Transcribed Text", font=("Arial", 14), command=save_text)
save_button.pack(pady=10)

# Run the GUI
root.mainloop()