HUGGINGFACE_API_TOKEN = ""
import streamlit as st
import torch

# 從 transformers 函式庫載入模型和分詞器
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


# --- 修正後的模型載入 ---
# 使用 Streamlit 的快取功能，避免每次操作都重新載入模型，提升效能。
@st.cache_resource
def load_model():
    """載入分詞器和模型。"""
    tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
    model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
    # 明確地將模型移動到 CPU 裝置，解決 meta device 的問題
    model = model.to("cpu")
    return tokenizer, model


# 載入模型
tokenizer, model = load_model()


# --- Streamlit 使用者介面 ---
st.title("FLAN-T5 模型測試應用")
st.write("這個應用程式使用 `google/flan-t5-base` 模型，根據您的提示生成文字。")

# 提示輸入框
prompt = st.text_area(
    "請在此輸入您的提示：", height=100, placeholder="例如：法國的首都是哪裡？"
)

# "生成" 按鈕
if st.button("生成文字", type="primary"):
    # 檢查提示是否為空
    if not prompt.strip():
        st.warning("請輸入提示文字。")
    else:
        # 顯示處理中的提示
        with st.spinner("正在生成回應..."):
            try:
                # 將輸入文字進行分詞，並轉換成 PyTorch 張量
                inputs = tokenizer(prompt, return_tensors="pt")

                # --- 裝置對齊 ---
                # 確保輸入張量也被明確地移動到 CPU，與模型所在的裝置一致
                inputs = {key: val.to("cpu") for key, val in inputs.items()}

                # 使用模型生成輸出
                # 現在模型和輸入都在同一個裝置上 (CPU)，可以無誤地運行
                outputs = model.generate(
                    **inputs, min_new_tokens=200, max_new_tokens=300
                )

                # 將生成的輸出解碼成文字
                generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

                # 顯示成功訊息和結果
                st.success("生成結果：")
                st.write(generated_text)
            except Exception as e:
                st.error(f"發生錯誤：{e}")
