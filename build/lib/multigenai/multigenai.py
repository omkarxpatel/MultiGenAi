import os
import time
import openai
import threading
from bardapi import Bard
from tiktoken import encoding_for_model
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

COMBINED_PROMPT = """In the following paragraph I will be showing you some results generated by AI for the following prompt: {}. Your job is to combine these peices of information into a 
combined version of a sentence or paragraph. Make sure that the two original sentences are not fully part of the new sentence or paragraph but instead, parts from both are included.
I will be sharing with you a response from Bard, and a response from ChatGPT. You have to concatinate these responses into a singular response and then after the response, give a list of 
bulletpoints of what the differences and similarities were between the two different outputs from Bard and ChatGPT.
\nHere are the responses below:

\n\nBard's response: {}


\n\nChatGPT's response:{}


\n\nPlease make sure to follow all instructions above."""

class GenAI:
    def __init__(self, bard_token, openai_token, chatgpt_model):
        # Set variables needed for Bard + Chatgpt API
        self.bard_token = bard_token
        self.bard = Bard(token=self.bard_token)
        
        self.openai_token = openai_token
        self.gpt_tokenizer = encoding_for_model(chatgpt_model)
        
        self.responses = {
            "bard_content": None,
            "chatgpt_content": None,
            "combined_content": None
        }
        
        # Timing variables to see the speed
        self.bard_time = None
        self.chatgpt_time = None
        self.combined_time = None
        self.combined_start_time = time.time()
        
        
    # CLEAR SCREEN
    def clear(self) -> None:
        os.system('cls' if os.system == 'nt' else 'clear')
                    
    # BARD    
    def get_bard_response(self, prompt: str, name: str) -> str:
        bard_start_time = time.time()
        response = self.bard.get_answer(prompt)['content']
        self.bard_time = time.time()-bard_start_time
        
        print(f"{name}: {response}")
        self.responses["bard_content"] = response
        
        return response
    
    # CHATGPT
    def set_gpt_token(self) -> None:
        openai.api_key = self.openai_token
        return
    
    
    def get_gpt_tokens(self, text: str) -> int:
        return len(self.gpt_tokenizer.encode(text))
        
        
    def get_chatgpt_response(self, prompt: str, name: str) -> str:
        chatgpt_start_time = time.time()
        self.set_gpt_token()

        while True:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )

                assert isinstance(response.choices[0].message.content, str), "API response is not a string"
                response = response.choices[0].message.content

                self.chatgpt_time = time.time() - chatgpt_start_time

                print(f"\n{name}: {response}")
                
                val = 'chatgpt_content'
                if name == 'combined': val = 'combined_content'
                self.responses[val] = response

                return response

            except openai.error.RateLimitError:
                print("Rate limit exceeded. Retrying after a delay...")
                time.sleep(5)  # Wait for 5 seconds before retrying
    
    
    def get_combined_prompt(self, prompt) -> None:
        self.combined_time = time.time()
        new_prompt = COMBINED_PROMPT.format(prompt, self.responses["bard_content"], self.responses["chatgpt_content"])
        
        # self.get_bard_response(new_prompt, "Bard Combined")
        self.get_chatgpt_response(new_prompt, "combined")
        
        self.combined_time = time.time() - self.combined_start_time
        
    
    
    def get_responses(self, prompt):
        self.clear()
        print(f"Prompt: {prompt}")
        # Create threads for Bard and ChatGPT
        bard_thread = threading.Thread(target=self.get_bard_response, args=(prompt, "Bard"))
        chatgpt_thread = threading.Thread(target=self.get_chatgpt_response, args=(prompt, "ChatGPT"))
        
        # Start both threads
        bard_thread.start()
        chatgpt_thread.start()
        
        # Wait for both threads to finish
        bard_thread.join()
        chatgpt_thread.join()
        
        # Get newly generated prompt
        self.get_combined_prompt(prompt)
        
        # print(f"\n\nTiming Stats:\nBard: {self.bard_time}\nChatGPT: {self.combined_time-self.chatgpt_time}\nCombined: {self.combined_time}")


# multigenai = GenAI(bard_token=os.environ['BARD_TOKEN'], openai_token=os.environ['OPENAI_TOKEN'], chatgpt_model="gpt-3.5-turbo")


# multigenai.get_responses("what does the name omkar mean in one sentence")
# app = Flask(__name__)

# @app.route('/api', methods=['POST'])
# def api():
#     prompt = request.json['prompt']
#     multigenai.get_responses(prompt)
    
#     return jsonify(multigenai.responses)

# def run_api():
#     app.run()

# if __name__ == '__main__':
#     run_api()
# curl -X POST -H "Content-Type: application/json" -d '{"prompt":"Your prompt goes here"}' http://localhost:5000/api