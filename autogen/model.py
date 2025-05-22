from fastapi import FastAPI
import torch
import time
import uuid
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from typing import List, Optional, Literal

checkpoint = "Qwen/Qwen3-0.6B"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForCausalLM.from_pretrained(checkpoint)
device = "cuda" if torch.cuda.is_available() else "cpu"

class PromptRequest(BaseModel):
    prompt: str
    max_new_tokens: int = 4000
    temperature: float = 0.2
    top_p: float = 0.9

class ChatMessage(BaseModel):
    role: Literal["user", "system", "assistant"]
    content: str

class ChatCompletionRequest(BaseModel):
    model: str = checkpoint
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.9
    max_tokens: Optional[int] = 1024

app = FastAPI()

generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device=device)
@app.post("/generate")
def generate_text(req: PromptRequest):
    messages = [
    {"role": "user", "content": req.prompt}
    ]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False # Switches between thinking and non-thinking modes. Default is True.
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    # conduct text completion
    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=32768
    )
    output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist() 

    # parsing thinking content
    try:
        # rindex finding 151668 (</think>)
        index = len(output_ids) - output_ids[::-1].index(151668)
    except ValueError:
        index = 0

    thinking_content = tokenizer.decode(output_ids[:index], skip_special_tokens=True).strip("\n")
    content = tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")

    print("content:", content)

    return {"choices": [
            {
                "message": {
                    "content": content
                }
            }

            ]}

@app.post("/chat/completions")
def chat_completions(req: ChatCompletionRequest):
    # Apply chat template
    prompt_text = tokenizer.apply_chat_template(
        req.messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False
    )

    inputs = tokenizer([prompt_text], return_tensors="pt").to(device)
    generated_ids = model.generate(
        **inputs,
        max_new_tokens=req.max_tokens or 1024,
        temperature=req.temperature,
        top_p=req.top_p,
        do_sample=True
    )

    # Get output text
    output_ids = generated_ids[0][len(inputs.input_ids[0]):].tolist() 

    # parsing thinking content
    try:
        # rindex finding 151668 (</think>)
        index = len(output_ids) - output_ids[::-1].index(151668)
    except ValueError:
        index = 0

    content = tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")

    # Create OpenAI-compatible response
    return {
        "id": f"chatcmpl-{str(uuid.uuid4())}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": req.model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": content
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": len(inputs.input_ids[0]),
            "completion_tokens": len(output_ids),
            "total_tokens": len(inputs.input_ids[0]) + len(output_ids)
        }
    }

@app.get("/")
def hello():
    return {
        "Hello world!"
    }