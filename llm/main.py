from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time
import uuid
from unsloth import FastLanguageModel
import torch

import logging
logger = logging.getLogger('uvicorn')
logger.setLevel(logging.DEBUG)

# Load the model
max_seq_length = 8192
dtype = None  # Auto detection
load_in_4bit = True  # 4-bit quantization

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Qwen2.5-3B-Instruct",
    max_seq_length=max_seq_length,
    dtype=dtype,
    load_in_4bit=load_in_4bit,
)

FastLanguageModel.for_inference(model)
torch.cuda.empty_cache()
if torch.cuda.is_available():
    device = torch.device('cuda')
elif torch.backends.mps.is_available():  # For macOS with Metal support
    device = torch.device('mps')
elif torch.backends.rocm.is_available():  # For AMD GPUs
    device = torch.device('rocm')
else:
    logger.error('Unable to autodetect GPU!! Fallback to CPU.')
    device = torch.device('cpu')
model.to(device)

# FastAPI App
app = FastAPI(debug=True)



# Store chat sessions in memory
chat_sessions = {}
SESSION_TIMEOUT = 300  # 5 minutes

class Message(BaseModel):
    session_id: str
    message: str

@app.post("/start_session")
def start_session():
    session_id = str(uuid.uuid4())
    chat_sessions[session_id] = {"messages": [], "last_active": time.time()}
    return {"session_id": session_id}

@app.post("/chat")
def chat(msg: Message):
    session = chat_sessions.get(msg.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found or expired")
    
    session["last_active"] = time.time()
    
    messages = session["messages"]
    messages.append({"role": "user", "content": msg.message})
    logger.debug("USER REQUEST: " + msg.message)
    
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
    messages.append({"role": "assistant", "content": response})
    logger.debug("QWEN RESPONSE: " + response)
    return {"response": response}

@app.get("/session_status/{session_id}")
def session_status(session_id: str):
    session = chat_sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found or expired")
    return {"active": True, "messages": session["messages"]}

# Background cleanup task
import threading

def cleanup_sessions():
    while True:
        time.sleep(60)  # Check every minute
        now = time.time()
        expired_sessions = [sid for sid, s in chat_sessions.items() if now - s["last_active"] > SESSION_TIMEOUT]
        for sid in expired_sessions:
            del chat_sessions[sid]

threading.Thread(target=cleanup_sessions, daemon=True).start()
