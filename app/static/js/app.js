const API_PREFIX = "/api/v1";

const healthStatus = document.querySelector("#healthStatus");
const imageInput = document.querySelector("#imageInput");
const previewBox = document.querySelector("#previewBox");
const uploadBtn = document.querySelector("#uploadBtn");
const uploadResult = document.querySelector("#uploadResult");
const searchForm = document.querySelector("#searchForm");
const queryInput = document.querySelector("#queryInput");
const designerInput = document.querySelector("#designerInput");
const chatWindow = document.querySelector("#chatWindow");
const generateForm = document.querySelector("#generateForm");
const promptInput = document.querySelector("#promptInput");
const generateDesignerInput = document.querySelector("#generateDesignerInput");
const generatedText = document.querySelector("#generatedText");

function prettyJson(data) {
  return JSON.stringify(data, null, 2);
}

function setBusy(button, busyText) {
  const originalText = button.textContent;
  button.disabled = true;
  button.textContent = busyText;
  return () => {
    button.disabled = false;
    button.textContent = originalText;
  };
}

function appendMessage(role, title, body) {
  const message = document.createElement("div");
  message.className = `message ${role}`;

  const strong = document.createElement("strong");
  strong.textContent = title;
  message.appendChild(strong);

  if (typeof body === "string") {
    const span = document.createElement("span");
    span.textContent = body;
    message.appendChild(span);
  } else {
    message.appendChild(body);
  }

  chatWindow.appendChild(message);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

function renderSearchResults(results) {
  const list = document.createElement("div");
  list.className = "result-list";

  results.forEach((item, index) => {
    const row = document.createElement("div");
    row.className = "result-item";
    row.innerHTML = `
      <b>#${index + 1} ${item.image_url}</b>
      <span>designer: ${item.designer_id} · score: ${item.score}</span>
    `;
    list.appendChild(row);
  });

  return list;
}

async function checkHealth() {
  try {
    const response = await fetch("/health");
    if (!response.ok) throw new Error("health check failed");
    healthStatus.textContent = "Online";
    healthStatus.classList.add("ok");
  } catch (error) {
    healthStatus.textContent = "Offline";
    healthStatus.classList.remove("ok");
  }
}

imageInput.addEventListener("change", () => {
  const file = imageInput.files?.[0];
  if (!file) return;

  const previewUrl = URL.createObjectURL(file);
  previewBox.innerHTML = "";
  const img = document.createElement("img");
  img.src = previewUrl;
  img.alt = file.name;
  previewBox.appendChild(img);
});

uploadBtn.addEventListener("click", async () => {
  const file = imageInput.files?.[0];
  if (!file) {
    uploadResult.textContent = prettyJson({ error: "请先选择图片" });
    return;
  }

  const done = setBusy(uploadBtn, "上传中...");
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch(`${API_PREFIX}/upload`, {
      method: "POST",
      body: formData,
    });
    const data = await response.json();
    uploadResult.textContent = prettyJson(data);
  } catch (error) {
    uploadResult.textContent = prettyJson({ error: error.message });
  } finally {
    done();
  }
});

searchForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const submitButton = searchForm.querySelector("button");
  const query = queryInput.value.trim();
  const designerId = designerInput.value.trim() || null;
  if (!query) return;

  appendMessage("user", "你", designerId ? `${query}，设计师：${designerId}` : query);
  const done = setBusy(submitButton, "检索中...");

  try {
    const response = await fetch(`${API_PREFIX}/search`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query,
        designer_id: designerId,
        top_k: 5,
      }),
    });
    const data = await response.json();
    appendMessage("assistant", "Vision RAG", renderSearchResults(data.results || []));
  } catch (error) {
    appendMessage("assistant", "Vision RAG", `检索失败：${error.message}`);
  } finally {
    done();
  }
});

generateForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const submitButton = generateForm.querySelector("button");
  const prompt = promptInput.value.trim();
  const designerId = generateDesignerInput.value.trim() || null;
  if (!prompt) return;

  const done = setBusy(submitButton, "生成中...");

  try {
    const response = await fetch(`${API_PREFIX}/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        prompt,
        designer_id: designerId,
      }),
    });
    const data = await response.json();
    generatedText.textContent = `${data.message}: ${data.prompt}`;
  } catch (error) {
    generatedText.textContent = `生成失败：${error.message}`;
  } finally {
    done();
  }
});

checkHealth();
