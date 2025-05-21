from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

class PromptRequest(BaseModel):
    prompt: str
    max_new_tokens: int = 4000
    temperature: float = 0.2
    top_p: float = 0.9

app = FastAPI()

checkpoint = "Qwen/Qwen3-0.6B"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForCausalLM.from_pretrained(checkpoint)

generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device=0 if model.device.type == "cuda" else -1)
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

@app.get("/")
def hello():
    return {
        "Hello world!"
    }