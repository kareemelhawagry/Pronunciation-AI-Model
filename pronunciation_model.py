from difflib import SequenceMatcher
import sounddevice as sd
import speech_recognition as sr
from scipy.io.wavfile import write
from pydub import AudioSegment
from pydub.silence import split_on_silence

# Step 1: Collect audio input
duration = 5  # Duration of audio input in seconds
fs = 44100  # Sampling rate

print("Recording...")
myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
sd.wait()
print("Done recording...")

# Step 2: Preprocess audio input
audio = AudioSegment(
    myrecording.tobytes(),
    frame_rate=fs,
    sample_width=myrecording.dtype.itemsize,
    channels=2
)
chunks = split_on_silence(audio, min_silence_len=500, silence_thresh=-40)

for i, chunk in enumerate(chunks):
    chunk.export(f"chunk{i}.wav", format="wav")

# Step 3: Use speech recognition
r = sr.Recognizer()

text = ""
for i in range(len(chunks)):
    with sr.AudioFile(f"chunk{i}.wav") as source:
        audio = r.record(source)
        recognized_text = r.recognize_google(audio)
        text += recognized_text

# Step 4: Compare the text with the correct pronunciation
correct_pronunciation = "banana"
similarity_threshold = 0.8
similarity = SequenceMatcher(None, correct_pronunciation, text).ratio()

if similarity >= similarity_threshold:
    print("Correct pronunciation!")
else:
    print("Incorrect pronunciation!")

# Step 5: Give feedback
if similarity >= similarity_threshold:
    feedback = "Well done! You pronounced the word correctly."
else:
    feedback = "Sorry, you did not pronounce the word correctly. Please try again."

print(feedback)
