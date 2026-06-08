# AI 圖片生成器

這是一個純前端 web app。使用者輸入文字敘述後，app 會呼叫 Pollinations 的文字轉圖片 API 生成圖片。

## 使用的免費模型

建議使用 `FLUX.1-schnell` / `flux`。Black Forest Labs 在 Hugging Face model card 標示 `FLUX.1-schnell` 採 `apache-2.0` 授權，可用於個人、研究與商業用途。它是文字轉圖片模型，但本機直接跑完整模型通常需要較好的 GPU。

本專案預設使用 Pollinations 的 hosted API：

```text
https://gen.pollinations.ai/image/{prompt}?model=flux
```

Pollinations 2026 文件顯示正式 API 需要 key。可到 https://enter.pollinations.ai 申請免費 key，再貼到網頁中的 API key 欄位。key 只會存在使用者自己的瀏覽器 localStorage。

## 如何執行

直接用瀏覽器開啟 `index.html`。

如果你想用本機伺服器，也可以在此資料夾執行：

```powershell
python -m http.server 5173
```

然後開啟：

```text
http://localhost:5173
```

## Streamlit Cloud 部署

本專案也提供 Streamlit 版本，入口檔是：

```text
streamlit_app.py
```

在 Streamlit Community Cloud 建立 app 時，請選擇此 GitHub repo，並將 main file path 設為 `streamlit_app.py`。

部署前請在 Streamlit Cloud 的 Secrets 設定加入：

```toml
POLLINATIONS_API_KEY = "你的 Pollinations API key"
```

請不要把 `.env` 或 `.streamlit/secrets.toml` 提交到 GitHub。若要在本機測試 Streamlit 版本，可先安裝依賴：

```powershell
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## 功能

- 輸入文字 prompt 生成圖片
- 選擇模型、比例、seed
- 可開啟 prompt enhance
- 顯示生成圖片與圖片 URL
- 複製 URL、下載圖片
- API key 儲存在瀏覽器，不寫入專案檔案

## 參考資料

- FLUX.1-schnell model card: https://huggingface.co/black-forest-labs/FLUX.1-schnell
- Pollinations API docs: https://gen.pollinations.ai/docs
