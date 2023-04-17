from transformers import pipeline
import json
import torch

# to change the model, change the path in config.json
with open('config.json') as f:
    config = json.load(f)

class DolllyChatbot():
    def __init__(self):
        self.model_name = config["Dolly_model"]
        # self.model = AutoModelForCausalLM.from_pretrained("databricks/dolly-v2-12b", device_map="auto")
        # self.tokenizer = AutoTokenizer.from_pretrained("databricks/dolly-v2-12b", padding_side="left")
        self.running = True
        # print(torch.cuda.is_available())
        print("Chatbot initialized")
    
    def text_input(self):
        utterance = input("You: ")
        return utterance
    
    def text_output(self, utterance):
        if utterance == "bye":
            self.running = False
            print("Chatbot: Bye!")
            return
        generate_text = pipeline(model="databricks/dolly-v2-12b", torch_dtype=torch.bfloat16, trust_remote_code=True, device_map="auto")
        response = generate_text(utterance)
        # # inputs = self.tokenizer([utterance], return_tensors='pt')
        # result = self.model.generate(
        #     **inputs, 
        #     max_new_tokens=1000,
        # )
        # response = self.tokenizer.decode(result[0])
        # print("Chatbot: ", response)
        return response

    def run(self):
        while self.running:
            self.text_output(self.text_input())

ai = DolllyChatbot()
ai.run()
