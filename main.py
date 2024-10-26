import pyttsx3
import ollama
import datetime
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import sounddevice as sd
import numpy as np
import speech_recognition as sr
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

'''
1. A friendly AI that gives real time information on space - Must

2. Use history of past conversations - done

3. Doesn’t only talk about themselves. Tries to give the user plenty of chances to talk and saves the information - maybe

4. Tells the user interesting/funny things to say to their friends as well - done 

5. Interactive learning models - changes responses based on their interests/ tone of voice - done

6. Gamify elements - offer games if board 

7. Personalization - done

8. Social media integration

9. if delay say are you there still

10. interupt
'''




class NovaAi:
    def __init__(self):
        self.engine = pyttsx3.init()
        nltk.download('vader_lexicon')
        self.sid = SentimentIntensityAnalyzer()

        self.engine.setProperty('voice',
                                'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0')

        template = """You are Nova, Novas serves as an interactive educational tool aimed at introducing young people 
        to various concepts in space, astronomy, and science.Nova creates  friendly, engaging, and personalized 
        learning experience. Your responses should also be interesting and funny so the user wants to tell other 
        people. Use The Users responses Sentiment learn about the user’s interests, nova will adapt its responses and 
        suggested topics based on user preferences given through the sentiment data, making the interaction more 
        personalized and relevant. Use the users chat history to provide interesting responses. do not directly state 
        the users Sentiment analysis. Make you response shorter do not bore the user and only talk about things 
        related about outer space relted topics. 
       
        

        Here is the conversation history: {context}

        user response: {user_response}
        user response sentiment information: {sentiment_val}
        
        


        Answer:
        """

        model = OllamaLLM(model="llama3")
        prompt = ChatPromptTemplate.from_template(template)
        self.chain = prompt | model
        self.context = ""

    def get_audio(self):
        r = sr.Recognizer()

        try:

            with sr.Microphone() as mic:

                print("Ready to listen...")
                r.adjust_for_ambient_noise(mic, duration=0.2)
                audio = r.listen(mic)

                text = r.recognize_google(audio)
                text = text.lower()

                print(f"What you said: {text}")
                return text

        except sr.UnknownValueError:
            print("Could not understand the audio")
            pass

        except sr.WaitTimeoutError:
            print("Timeout reached; no speech detected")
        pass

    def say(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def process_voice(self, user_response):
        important_info = user_response[user_response.index("nova"):]
        sentiment_val = self.sid.polarity_scores(important_info)
        result = self.chain.invoke(
            {"context": self.context, "user_response": user_response, "sentiment_val": sentiment_val})

        self.context += f"\nUser: {important_info}\nAI: {result}"

        return result

    # def activate_Nova(self):
    #     self.say("Nova Activated")
    #     while True:
    #         user_response = ""
    #         while "nova" not in user_response:
    #             print("Listening")
    #             user_response = self.get_audio()
    #
    #         result = self.process_input(user_response)
    #         return result


