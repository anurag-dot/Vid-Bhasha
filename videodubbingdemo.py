# -*- coding: utf-8 -*-
"""VideoDubbingDemo.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1CMLzuyhUEb1U5vLeyxI_22yBkHCYIf_R
"""

!pip install moviepy
import moviepy.editor as mp

my_clip = mp.VideoFileClip(r"/content/Trim.mp4")
my_clip.audio.write_audiofile(r"my_result.wav")

!pip install SpeechRecognition

import speech_recognition as sr
r = sr.Recognizer()

with sr.AudioFile('my_result.wav') as source:
    audio = r.record(source)
    try:
        audio_text = r.recognize_google(audio)
        print(audio_text)
    except sr.UnknownValueError:
        print("404 error no input",UnknownValueError)
    except sr.RequestError:
        print("402 error from api",UnknownValueError)

!pip install gTTS
!pip install googletrans==4.0.0-rc1

import speech_recognition as spr
from googletrans import Translator
from gtts import gTTS
import os

recog1 = spr.Recognizer()

with spr.AudioFile('my_result.wav') as source:
  recog1.adjust_for_ambient_noise(source, duration=0.02)
  audio = recog1.record(source)
  try:
    audio_text = recog1.recognize_google(audio)
    audio_text = audio_text.lower()
  except recog1.UnknownValueError:
    print("404 error no input")
  except recog1.RequestError:
    print("402 error from api")

translator=Translator()

from_lang = 'en'
to_lang = 'hi'

tts = gTTS(text=translator.translate(audio_text, src=from_lang, dest=to_lang).text, lang=to_lang,  tld='co.in' , slow=False)
tts.save("insider.mp3")

translated_clip = mp.VideoFileClip(r"/content/demo.mp4")
translated_audio = mp.AudioFileClip(r"insider.mp3")
final_clip = translated_clip.set_audio(translated_audio)
final_clip.write_videofile(r"insider.mp4", codec="libx264", audio_codec="aac")

!pip install git+https://github.com/openai/whisper.git
!pip install -U openai-whisper

import os
import sys
import subprocess

import whisper
from whisper.utils import get_writer
model =whisper.load_model("tiny")

model.device

def audioconversion(my_clip, output_ext="mp3"):
  filename, ext=os.path.splitext(my_clip)
  subprocess.call(["ffmpeg", "-y", "-i", my_clip, f"{filename}.{output_ext}"], stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
  return f"{filename}.{output_ext}"

clip="/content/demo.mp4"
audio_file = audioconversion(clip)

result=model.transcribe(audio_file)
print(result)
output_directory = "./"

vtt_writer=whisper.utils.WriteVTT(output_directory)
options = {
    "highlight_words": True,
    "max_line_count": 2,
    "max_line_width": 50
}
vtt_writer(result, clip,options=options)

!pip install ipython
!pip install pybase64

from base64 import b64encode
from IPython.display import HTML

target_vd="/content/insider.mp4"
  subbtitled_path="/content/demo.vtt"

  with open(target_vd, 'rb') as f:
      video_data = f.read()
      video_base64 = b64encode(video_data).decode()

  with open(subbtitled_path, 'r') as f:
      captions_data = f.read()
      captions_base64 = b64encode(captions_data.encode('utf-8')).decode()

  video_html = f"""
  <video width="640" height="360" controls>
      <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
      <track src="data:text/vtt;base64,{captions_base64}" kind="captions" srclang="en" label="English" default>
  </video>
  """

  HTML(video_html)

def embed_video(video_file, subtitled_vtt, output_file):
  command=[ 'ffmpeg', '-i', video_file, '-i', subtitled_vtt, '-c', 'copy','-c:s', 'mov_text', '-metadata:s:s:0', 'language=eng', output_file]
  subprocess.run(command, check=True)