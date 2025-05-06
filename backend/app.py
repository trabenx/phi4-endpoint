from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer, pipeline
import torch
from PIL import Image
import io
import os

# Device setup
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load models
processor = ViTImageProcessor.from_pretrained("microsoft/Phi-4-multimodal-instruct")
tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-4-multimodal-instruct")
model = VisionEncoderDecoderModel.from_pretrained("microsoft/Phi-4-multimodal-instruct").to(device)
# Whisper for audio transcription
speech2text = pipeline(
    "automatic-speech-recognition",
    "openai/whisper-large-v2",
    device=0 if device=="cuda" else -1
)

def generate_response(text=None, image=None):
    # Prepare inputs
    inputs = {}
    if image:
        inputs["pixel_values"] = processor(images=image, return_tensors="pt").pixel_values.to(device)
    if text:
        inputs["input_ids"] = tokenizer(text, return_tensors="pt").input_ids.to(device)
    # Generate
    outputs = model.generate(**inputs, max_length=512)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
async def predict(
    text: str = Form(None),
    image: UploadFile = File(None),
    audio: UploadFile = File(None)
):
    prompt = text or ""
    # Handle audio
    if audio:
        audio_bytes = await audio.read()
        # use whisper pipeline directly on bytes
        transcription = speech2text(audio_bytes)["text"]
        prompt = transcription + " " + prompt
    # Handle image
    img = None
    if image:
        image_bytes = await image.read()
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    # Generate
    result = generate_response(text=prompt, image=img)
    return {"result": result}