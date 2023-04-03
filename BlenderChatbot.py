from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
import torch

class ChatBot():
    def __init__(self):
        self.model_name = "facebook/blenderbot-400M-distill"
        # self.model_name = "facebook/blenderbot-3B"
        # self.model_name = "facebook/blenderbot-1B-distill"
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

# ai = ChatBot()
# ai.run()

