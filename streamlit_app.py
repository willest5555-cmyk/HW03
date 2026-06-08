import os
from urllib.parse import quote

import requests
import streamlit as st
from dotenv import load_dotenv


load_dotenv()

API_BASE_URL = "https://gen.pollinations.ai/image"
MODEL_OPTIONS = {
    "FLUX": "flux",
    "Z-Image Turbo": "zimage",
    "Seedream": "seedream",
    "GPT Image": "gptimage",
}
RATIO_OPTIONS = {
    "1:1 正方形": (1024, 1024),
    "16:9 橫式": (1280, 720),
    "9:16 直式": (720, 1280),
    "4:3 橫式": (1024, 768),
}


def get_configured_api_key():
    try:
        secret_key = st.secrets.get("POLLINATIONS_API_KEY", "")
    except Exception:
        secret_key = ""

    return secret_key or os.getenv("POLLINATIONS_API_KEY", "")


def build_image_url(prompt, model, width, height, seed, enhance, api_key):
    params = {
        "model": model,
        "width": str(width),
        "height": str(height),
        "seed": str(seed or 0),
        "enhance": str(enhance).lower(),
        "safe": "true",
        "key": api_key,
    }
    query = "&".join(f"{key}={quote(value, safe='')}" for key, value in params.items())
    return f"{API_BASE_URL}/{quote(prompt, safe='')}?{query}"


def generate_image(image_url):
    response = requests.get(image_url, timeout=90)
    content_type = response.headers.get("content-type", "")

    if response.status_code != 200:
        raise RuntimeError(f"API 回傳 HTTP {response.status_code}: {response.text[:300]}")

    if not content_type.startswith("image/"):
        raise RuntimeError(f"API 未回傳圖片: {response.text[:300]}")

    return response.content, content_type


st.set_page_config(page_title="AI 圖片生成器", page_icon="AI", layout="wide")

st.title("文字轉圖片生成器")
st.caption("使用 Pollinations hosted API 生成圖片。部署到 Streamlit Cloud 時，API key 會保留在後端 secrets。")

configured_api_key = get_configured_api_key()

with st.sidebar:
    st.header("生成設定")
    model_label = st.selectbox("模型", list(MODEL_OPTIONS.keys()))
    ratio_label = st.selectbox("比例", list(RATIO_OPTIONS.keys()))
    seed = st.number_input("Seed", min_value=0, value=0, step=1)
    enhance = st.checkbox("強化 prompt", value=False)

    st.divider()
    pasted_key = st.text_input(
        "Pollinations API key",
        type="password",
        value="",
        placeholder="部署時建議改用 Streamlit secrets",
    )
    st.caption("本機測試可暫時貼 key；正式部署請使用 Streamlit Cloud 的 Secrets。")

api_key = pasted_key.strip() or configured_api_key.strip()

prompt = st.text_area(
    "圖片敘述",
    height=180,
    placeholder="例如：一座未來感台北城市，雨後夜晚，霓虹燈倒映在街道上，電影感光影",
)

left, right = st.columns([1, 1])

with left:
    submitted = st.button("生成圖片", type="primary", use_container_width=True)

with right:
    if not api_key:
        st.warning("尚未設定 Pollinations API key。請在側欄貼 key，或於 Streamlit Cloud 設定 secrets。")

if submitted:
    if not prompt.strip():
        st.error("請先輸入圖片敘述。")
    elif not api_key:
        st.error("請先設定 Pollinations API key。")
    else:
        width, height = RATIO_OPTIONS[ratio_label]
        image_url = build_image_url(
            prompt=prompt.strip(),
            model=MODEL_OPTIONS[model_label],
            width=width,
            height=height,
            seed=seed,
            enhance=enhance,
            api_key=api_key,
        )

        with st.spinner("圖片生成中，通常需要幾秒到一分鐘。"):
            try:
                image_bytes, content_type = generate_image(image_url)
            except Exception as exc:
                st.error(f"生成失敗：{exc}")
            else:
                st.image(image_bytes, caption="AI 生成圖片結果", use_container_width=True)
                st.download_button(
                    "下載圖片",
                    data=image_bytes,
                    file_name="ai-image.jpg",
                    mime=content_type,
                    use_container_width=True,
                )
