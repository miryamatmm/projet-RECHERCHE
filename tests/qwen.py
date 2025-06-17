import torch
import time
from transformers import AutoTokenizer, AutoModelForCausalLM

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
    "List all scientific disciplines of this offer as a comma-separated list: "
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
