import torch
import time
from transformers import AutoTokenizer, AutoModelForCausalLM
from backtrack_sampler import BacktrackSampler, AntiSlopStrategy, AdaptiveTemperatureStrategy
from backtrack_sampler.provider.transformers_provider import TransformersProvider

torch.cuda.empty_cache()

model_name = "Qwen/Qwen2.5-0.5B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
device = torch.device('cuda:0')

slops = []



import re
import PyPDF2

def extract_text_from_pdf(pdf_path):
    """Improved text extraction with PDF formatting cleanup"""
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(min(len(pdf_reader.pages), 4)):  # Limit to 4 pages
            page = pdf_reader.pages[page_num]
            text += page.extract_text() + "\n"
    
    # Clean up PDF artifacts
    text = re.sub(r'-\n(\w)', r'\1', text)  # Join hyphenated words
    text = re.sub(r'\s+', ' ', text)        # Remove extra whitespace
    text = re.sub(r'\s([?.!](?:\s|$))', r'\1', text)  # Fix spacing before punctuation
    return text.strip()[:15000]  # Limit to ~4 pages


job_offer_text = extract_text_from_pdf('pdf/en/1.pdf')

questions = [
    "Give a short title for this job offer, answer only the exact title: " + job_offer_text,
    "Summarize this job offer in extactly two sentences: ",
    "List all scientific disciplines mentioned as a comma-separated list: "
]

messages = []

provider = TransformersProvider(model, tokenizer, device)
strategy = AntiSlopStrategy(provider, slops)
sampler = BacktrackSampler(provider, strategy)

ts = time.time()
print("\n____________________\n")
for question in questions:
    messages.append({"role": "user", "content": question})
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    token_stream = sampler.generate(
        prompt=prompt,
        max_new_tokens=4096,
        temperature=1
    )
    print("\n\n")
    answer = ""
    for token in token_stream:
        char = tokenizer.decode(token, skip_special_tokens=True)
        print(char, end="", flush=True)
        answer += char
    messages.append({"role": "assistant", "content": answer})

print("\n____________________\n")
print(f"\nDuration: {time.time()-ts} seconds")