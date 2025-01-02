from transformers import pipeline
from transformers import AutoTokenizer
import transformers
import torch

print("MPS (Apple GPU) available:", torch.backends.mps.is_available())
# hf_token = "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"



# # Your Hugging Face access token goes here:

# # The model name:
# model_id = "meta-llama/Llama-2-13b-chat"

# tokenizer = AutoTokenizer.from_pretrained(model_id)
# llama_pipeline = pipeline(
#     "text-generation",  # LLM task
#     model=model_id,
#     torch_dtype=torch.float16,
#     device_map="auto",
# )

# def get_llama_response(prompt: str) -> None:
#     """
#     Generate a response from the Llama model.

#     Parameters:
#         prompt (str): The user's input/question for the model.

#     Returns:
#         None: Prints the model's response.
#     """
#     sequences = llama_pipeline(
#         prompt,
#         do_sample=True,
#         top_k=10,
#         num_return_sequences=1,
#         eos_token_id=tokenizer.eos_token_id,
#         max_length=256,
#     )
#     print("Chatbot:", sequences[0]['generated_text'])



# prompt = 'I liked "Breaking Bad" and "Band of Brothers". Do you have any recommendations of other shows I might like?\n'
# get_llama_response(prompt)

# print(prompt)