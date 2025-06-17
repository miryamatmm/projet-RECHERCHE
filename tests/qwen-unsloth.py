from unsloth import FastLanguageModel
import torch
max_seq_length = 2048 # Choose any! We auto support RoPE Scaling internally!
dtype = None # None for auto detection. Float16 for Tesla T4, V100, Bfloat16 for Ampere+
load_in_4bit = True # Use 4bit quantization to reduce memory usage. Can be False.

model, tokenizer = FastLanguageModel.from_pretrained(
    # Can select any from the below:
    # "unsloth/Qwen2.5-0.5B", "unsloth/Qwen2.5-1.5B", "unsloth/Qwen2.5-3B"
    # "unsloth/Qwen2.5-14B",  "unsloth/Qwen2.5-32B",  "unsloth/Qwen2.5-72B",
    # And also all Instruct versions and Math. Coding verisons!
    model_name = "unsloth/Qwen2.5-3B-Instruct",
    max_seq_length = max_seq_length,
    dtype = dtype,
    load_in_4bit = load_in_4bit,
    # token = "hf_...", # use one if using gated models like meta-llama/Llama-2-7b-hf
)

FastLanguageModel.for_inference(model)
##

import torch
import time

torch.cuda.empty_cache()

device = torch.device('cuda:0')
model.to(device)

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
    "List all scientific subdisciplines of this offer as a comma-separated list like [\"Domain1 > SubDomain1\", \"Domain1 > SubDomain2\" ... ]: ",
    "Extract start and end month/year of this offer as a comma-separated pair like [\"MM-YYYY\", \"MM-YYYY\"] :"
]

messages = []


ts = time.time()
print("\n____________________\n")
for question in questions:
    messages.append({"role": "user", "content": question})
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=1024
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    print(response)
    print("\n\n")
   
    messages.append({"role": "assistant", "content": response})

print("\n____________________\n")
print(f"\nDuration: {time.time()-ts} seconds")
