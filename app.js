const form = document.querySelector("#generatorForm");
const promptInput = document.querySelector("#prompt");
const modelInput = document.querySelector("#model");
const ratioInput = document.querySelector("#ratio");
const seedInput = document.querySelector("#seed");
const enhanceInput = document.querySelector("#enhance");
const apiKeyInput = document.querySelector("#apiKey");
const generateBtn = document.querySelector("#generateBtn");
const randomSeedBtn = document.querySelector("#randomSeedBtn");
const statusText = document.querySelector("#statusText");
const imageStage = document.querySelector("#imageStage");
const emptyState = document.querySelector("#emptyState");
const resultImage = document.querySelector("#resultImage");
const downloadLink = document.querySelector("#downloadLink");
const imageUrlInput = document.querySelector("#imageUrl");
const copyUrlBtn = document.querySelector("#copyUrlBtn");

const API_KEY_STORAGE_KEY = "pollinationsApiKey";

apiKeyInput.value = localStorage.getItem(API_KEY_STORAGE_KEY) || "";

apiKeyInput.addEventListener("input", () => {
  localStorage.setItem(API_KEY_STORAGE_KEY, apiKeyInput.value.trim());
});

randomSeedBtn.addEventListener("click", () => {
  seedInput.value = Math.floor(Math.random() * 1_000_000);
});

copyUrlBtn.addEventListener("click", async () => {
  if (!imageUrlInput.value) return;

  try {
    await navigator.clipboard.writeText(imageUrlInput.value);
    setStatus("已複製圖片 URL。");
  } catch {
    imageUrlInput.select();
    setStatus("已選取 URL，可手動複製。");
  }
});

form.addEventListener("submit", (event) => {
  event.preventDefault();

  const prompt = promptInput.value.trim();
  if (!prompt) {
    setStatus("請先輸入圖片敘述。", true);
    promptInput.focus();
    return;
  }

  const imageUrl = buildImageUrl(prompt);
  renderImage(imageUrl);
});

function buildImageUrl(prompt) {
  const [width, height] = ratioInput.value.split("x");
  const params = new URLSearchParams({
    model: modelInput.value,
    width,
    height,
    seed: seedInput.value.trim() || "0",
    enhance: String(enhanceInput.checked),
    safe: "true",
  });

  const key = apiKeyInput.value.trim();
  if (key) {
    params.set("key", key);
  }

  return `https://gen.pollinations.ai/image/${encodeURIComponent(prompt)}?${params.toString()}`;
}

function renderImage(imageUrl) {
  setLoading(true);
  setStatus("圖片生成中，通常需要幾秒到一分鐘。");
  imageUrlInput.value = imageUrl;
  downloadLink.href = imageUrl;
  downloadLink.classList.add("hidden");
  resultImage.classList.add("hidden");
  emptyState.classList.add("hidden");

  const image = new Image();
  image.alt = "AI 生成圖片結果";
  image.onload = () => {
    resultImage.src = imageUrl;
    resultImage.classList.remove("hidden");
    downloadLink.classList.remove("hidden");
    setLoading(false);
    setStatus("生成完成。");
  };
  image.onerror = () => {
    setLoading(false);
    emptyState.classList.remove("hidden");
    setStatus("生成失敗。請確認 API key 是否有效，或稍後再試。", true);
  };
  image.src = imageUrl;
}

function setLoading(isLoading) {
  generateBtn.disabled = isLoading;
  generateBtn.textContent = isLoading ? "生成中..." : "生成圖片";
  imageStage.classList.toggle("loading", isLoading);
}

function setStatus(message, isError = false) {
  statusText.textContent = message;
  statusText.classList.toggle("error", isError);
}
