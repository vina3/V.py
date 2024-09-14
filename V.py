import streamlit as st
from PIL import Image
import torch
from transformers import CLIPTextModel, CLIPTokenizer
from diffusers import StableDiffusionPipeline

# Initialize Stable Diffusion Pipeline
@st.cache_resource
def load_model():
    model_id = "CompVis/stable-diffusion-v1-4"
    pipe = StableDiffusionPipeline.from_pretrained(model_id)
    pipe.to("cuda" if torch.cuda.is_available() else "cpu")
    return pipe

pipe = load_model()

# Streamlit app layout
st.title("AI Image Generator with Stable Diffusion")

# Input from the user
prompt = st.text_input("Enter a prompt to generate an image:")

# Generate and display the image
if prompt:
    if st.button("Generate Image"):
        with st.spinner("Generating image..."):
            image = pipe(prompt).images[0]
            st.image(image, caption="Generated Image", use_column_width=True)
