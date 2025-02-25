import gradio as gr
import speech_recognition as sr
from pydub import AudioSegment
import re

def process_audio(audio_file, word):
    # Convert MP3 to WAV
    wav_file = "converted_audio.wav"
    audio = AudioSegment.from_file(audio_file)
    audio.export(wav_file, format="wav")

    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Convert speech to text with timestamps
    with sr.AudioFile(wav_file) as source:
        audio_duration = source.DURATION  # Get total audio duration
        audio_data = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            return "Could not understand the audio", "", []
        except sr.RequestError:
            return "Error connecting to speech recognition service", "", []

    # Process timestamps for word occurrences
    words = text.split()
    total_words = len(words)
    timestamps = []

    if word.lower() in text.lower():
        word_indices = [i for i, w in enumerate(words) if w.lower() == word.lower()]
        timestamps = [round((idx / total_words) * audio_duration, 2) for idx in word_indices]

    # Highlight word occurrences
    highlighted_text = re.sub(
        rf'\b({re.escape(word)})\b',
        r'<mark style="background-color: yellow; color: black;">\1</mark>',
        text,
        flags=re.IGNORECASE
    )

    return f"The word '{word}' appears {len(timestamps)} times.", highlighted_text, timestamps

# Create GUI
iface = gr.Interface(
    fn=process_audio,
    inputs=[
        gr.Audio(type="filepath", label="Upload MP3 File"),
        gr.Textbox(label="Enter Word to Search")
    ],
    outputs=[
        gr.Textbox(label="Word Count"),
        gr.HTML(label="Highlighted Transcript"),
        gr.JSON(label="Timestamps (seconds)")
    ],
    title="Audio Word Occurrence Tracker",
    description="Upload an MP3 file, enter a word to search, and get word count, highlighted text, and timestamps!"
)

iface.launch()

import gradio as gr
import speech_recognition as sr
from pydub import AudioSegment
import re
import os

def process_audio(audio_file, word):
    # Convert any audio format to WAV
    wav_file = "converted_audio.wav"
    try:
        audio = AudioSegment.from_file(audio_file)  # Auto-detect format
        audio.export(wav_file, format="wav")  # Convert to WAV
    except Exception as e:
        return f"Error processing audio file: {str(e)}", "", []

    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Convert speech to text with timestamps
    with sr.AudioFile(wav_file) as source:
        audio_duration = source.DURATION  # Get total audio duration
        audio_data = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            return "Could not understand the audio", "", []
        except sr.RequestError:
            return "Error connecting to speech recognition service", "", []

    # Process timestamps for word occurrences
    words = text.split()
    total_words = len(words)
    timestamps = []

    if word.lower() in text.lower():
        word_indices = [i for i, w in enumerate(words) if w.lower() == word.lower()]
        timestamps = [round((idx / total_words) * audio_duration, 2) for idx in word_indices]

    # Highlight word occurrences
    highlighted_text = re.sub(
        rf'\b({re.escape(word)})\b',
        r'<mark style="background-color: yellow; color: black;">\1</mark>',
        text,
        flags=re.IGNORECASE
    )

    return f"The word '{word}' appears {len(timestamps)} times.", highlighted_text, timestamps

# Create GUI
iface = gr.Interface(
    fn=process_audio,
    inputs=[
        gr.Audio(type="filepath", label="Upload Audio File"),  # Accepts any audio format
        gr.Textbox(label="Enter Word to Search")
    ],
    outputs=[
        gr.Textbox(label="Word Count"),
        gr.HTML(label="Highlighted Transcript"),
        gr.JSON(label="Timestamps (seconds)")
    ],
    title="Audio Word Occurrence Tracker",
    description="Upload any audio file, enter a word to search, and get word count, highlighted text, and timestamps!"
)

iface.launch()

