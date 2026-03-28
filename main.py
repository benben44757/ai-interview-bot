import os
import json
from dotenv import load_dotenv
import openai
import speech_recognition as sr
from elevenlabs import generate, stream

class InterviewBot:
    def __init__(self):
        load_dotenv()
        self.recognizer = sr.Recognizer()
        self.interview_types = ['general', 'technical', 'behavioral']
        self.transcript = []
        openai.api_key = os.getenv('OPENAI_API_KEY')

    def record_audio(self):
        with sr.Microphone() as source:
            print("Recording...")
            audio = self.recognizer.listen(source)
            return audio

    def speech_to_text(self, audio):
        try:
            text = self.recognizer.recognize_whisper(audio)
            print(f"Converted speech to text: {text}")
            return text
        except sr.UnknownValueError:
            print("Whisper could not understand audio")
            return None
        except sr.RequestError:
            print("Could not request results from Whisper service")
            return None

    def get_ai_response(self, prompt):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']

    def text_to_speech(self, text):
        audio = generate(text)
        stream(audio)

    def start_interview(self, interview_type='general'):
        print(f"Starting {interview_type} interview.")
        while True:
            audio = self.record_audio()
            if audio:
                question = self.speech_to_text(audio)
                if question:
                    self.transcript.append(question)
                    response = self.get_ai_response(question)
                    print(f"AI: {response}")
                    self.text_to_speech(response)

    def save_transcript(self, filename='transcript.json'):
        with open(filename, 'w') as f:
            json.dump(self.transcript, f)
        print(f"Transcript saved to {filename}.")

# Example usage:
# bot = InterviewBot()
# bot.start_interview('general')
# bot.save_transcript()