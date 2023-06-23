from multigenai.genai import GenAI


# Create an instance of GenAI
# multigenai = GenAI(bard_token="YOUR_BARD_TOKEN", openai_token="YOUR_OPENAI_TOKEN", chatgpt_model="gpt-3.5-turbo")
multigenai = GenAI(bard_token="Xwj0SVWRsKCGT4tvkeKqeeVyqvaOJUvREneOZ1164ITxcyH7pNTo4bMNElC7yxF7CjxG_Q.", openai_token="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", chatgpt_model="gpt-3.5-turbo")
# Get responses for a prompt
prompt = "What does the name Omkar mean in one sentence?"
multigenai.get_content(prompt)

# Print the responses
print("Bard's Response:", multigenai.content["bard_content"])
print("ChatGPT's Response:", multigenai.content["chatgpt_content"])
print("Combined Response:", multigenai.content["combined_content"])