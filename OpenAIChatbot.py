import openai
from dotenv import load_dotenv
import os

load_dotenv()

class OpenAIChatbot():
    def __init__(self):
        self.model_name = "gpt-3.5-turbo"
        openai.api_key = os.environ["OPENAI_API_KEY"]
        openai.organization = os.environ["OPENAI_ORGANIZATION"]
        self.running = True
        self.bot_name = "llamachop_bot"
        self.bot_interests = "video games, anime, and programming"
        self.system_message = {"role": "system", "content": f"You are {self.bot_name}, and you like {self.bot_interests}. I want you to act like a person in every way. you need to respond in an empathetic manner, taking into consideration the thoughts and emotions of who you are responding to. you are exceptionally sarcastic and with show sarcasm in your responses."}
        self.conversation = []
        print("Chatbot initialized")

    def text_input(self):
        utterance = input("You: ")
        return utterance
    
    def text_output(self, utterance):
        if utterance == "bye":
            self.running = False
            print("Chatbot: Bye!")
            return
        
        # add conversation messages to conversation list up to 5 messages.
        # to do, figure out how to get the conversation history to work correctly. 
        # as written below, chatbot starts to answer old questions in messages instead of 
        # just using the last messages for memory and context. 
        # if len(self.conversation) < 5:
        #     self.conversation.insert(0, self.system_message)
        #     self.conversation.append({"role": "user", "content": utterance})
        # else:
        #     self.conversation.pop(0)
        #     self.conversation.insert(0, self.system_message)
        #     self.conversation.append({"role": "user", "content": utterance})

        self.conversation = [
            self.system_message,
            {"role": "user", "content": utterance}
        ]

        print(self.conversation)

        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=self.conversation,
            max_tokens=200,
            temperature=1,
            # top_p=1,
            # frequency_penalty=0.0,
            # presence_penalty=0.6,
            stop=["\n"]
        )
        # print("Chatbot: ", response['choices'][0]['message']['content'])
        # print("whole response: ")
        # print(response)
        self.conversation.pop(0)
        with open('output.txt', 'w') as f:
            f.write(str(response['choices'][0]['message']['content']))
        return response['choices'][0]['message']['content']
    
    def run(self):
        while self.running:
            self.text_output(self.text_input())

# ai = OpenAIChatbot()
# ai.run()
