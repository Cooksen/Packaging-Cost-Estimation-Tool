import streamlit as st
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

HUGGINGFACE_API_TOKEN = ""

@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
    model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
    model = model.to("cpu")
    return tokenizer, model


tokenizer, model = load_model()

st.title("FLAN-T5 model testing")

prompt = st.text_area(
    "Input your instructions here：", height=100, placeholder="Where is the capital of France？"
)

if st.button("Generate text", type="primary"):
    if not prompt.strip():
        st.warning("Please input prompt。")
    else:
        with st.spinner("Responding..."):
            try:
                inputs = tokenizer(prompt, return_tensors="pt")

                inputs = {key: val.to("cpu") for key, val in inputs.items()}

                outputs = model.generate(
                    **inputs, min_new_tokens=200, max_new_tokens=300
                )

                generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

                st.success("Results：")
                st.write(generated_text)
            except Exception as e:
                st.error(f"Error：{e}")
