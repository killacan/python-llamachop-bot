from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
import torch

# class ChatBot():
#     def __init__(self):
#         # self.model_name = "facebook/blenderbot-400M-distill"
#         # self.model_name = "facebook/blenderbot-3B"]
#         self.model_name = "facebook/blenderbot-1B-distill"
#         self.model = BlenderbotForConditionalGeneration.from_pretrained(self.model_name)
#         self.tokenizer = BlenderbotTokenizer.from_pretrained(self.model_name)
#         self.running = True
#         print(torch.cuda.is_available())
#         print("Chatbot initialized")
#         self.persona = ""
#         self.context = []
#         self.prompts = [
#             "Tell me about yourself.",
#             "What are your hobbies?",
#             "What kind of music do you like?",
#             "How are you feeling today?",
#             "What's on your mind?",
#         ]
    
#     def text_input(self):
#         if self.context:
#             prompt = self.context.pop(0)
#         else:
#             prompt = self.prompts[0]
#         utterance = input("You: {} ".format(prompt))
#         return utterance
    
#     def text_output(self, utterance):
#         if utterance == "bye":
#             self.running = False
#             print("Chatbot: Bye!")
#             return
#         if not self.persona:
#             self.persona = utterance
#             self.prompts.append("What's your favorite movie?")
#             return
#         inputs = self.tokenizer(self.persona + " " + utterance, return_tensors='pt')
#         result = self.model.generate(
#             **inputs, 
#             max_new_tokens=1000,
#         )
#         response = self.tokenizer.decode(result[0])
#         if not self.context and response.startswith(self.persona):
#             response = response[len(self.persona):].strip()
#             if response.startswith(","):
#                 response = response[1:].strip()
#         if "  " in response:
#             response = response.replace("  ", " ")
#         if self.context and response in self.context:
#             self.context.remove(response)
#         # print("Chatbot: ", response)
#         return response

#     def run(self):

#         persona = "I'm a video game enthusiast and love to talk about games."
#         conversation = [persona]
#         while self.running:
#             self.text_output(self.text_input())

class ChatBot():
    def __init__(self):
        # self.model_name = "facebook/blenderbot-400M-distill"
        # self.model_name = "facebook/blenderbot-3B"]
        self.model_name = "facebook/blenderbot-1B-distill"
        self.model = BlenderbotForConditionalGeneration.from_pretrained(self.model_name)
        self.tokenizer = BlenderbotTokenizer.from_pretrained(self.model_name)
        self.running = True
        print(torch.cuda.is_available())
        print("Chatbot initialized")
    
    def text_input(self):
        utterance = input("You: ")
        return utterance
    
    def text_output(self, utterance):
        if utterance == "bye":
            self.running = False
            print("Chatbot: Bye!")
            return
        inputs = self.tokenizer([utterance], return_tensors='pt')
        result = self.model.generate(
            **inputs, 
            max_new_tokens=1000,
        )
        response = self.tokenizer.decode(result[0])
        # print("Chatbot: ", response)
        return response

    def run(self):
        while self.running:
            self.text_output(self.text_input())



