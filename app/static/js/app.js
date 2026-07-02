const API_PREFIX = "/api/v1";

const healthStatus = document.querySelector("#healthStatus");
const imageInput = document.querySelector("#imageInput");
const uploadDesignerInput = document.querySelector("#uploadDesignerInput");
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
const generatedPreview = document.querySelector("#generatedPreview");

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

  if (!results.length) {
    const empty = document.createElement("div");
    empty.className = "result-item";
    empty.textContent = "No matching reference images found.";
    list.appendChild(empty);
    return list;
  }

  results.forEach((item, index) => {
    const row = document.createElement("div");
    row.className = "result-item";
    row.innerHTML = `
      <b>#${index + 1} ${item.image_url}</b>
      <span>designer: ${item.designer_id} | score: ${Number(item.score || 0).toFixed(4)} | distance: ${Number(item.distance || 0).toFixed(4)}</span>
    `;
    list.appendChild(row);
  });

  return list;
}

async function parseResponse(response) {
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || data.message || "Request failed");
  }
  return data;
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
  const designerId = Number(uploadDesignerInput.value);
  if (!file || !designerId) {
    uploadResult.textContent = prettyJson({ error: "Choose an image and enter a designer ID." });
    return;
  }

  const done = setBusy(uploadBtn, "Uploading...");
  const formData = new FormData();
  formData.append("designer_id", designerId);
  formData.append("file", file);

  try {
    const response = await fetch(`${API_PREFIX}/upload`, {
      method: "POST",
      body: formData,
    });
    const data = await parseResponse(response);
    uploadResult.textContent = prettyJson(data);
    designerInput.value = designerId;
    generateDesignerInput.value = designerId;
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
  const designerId = Number(designerInput.value);
  if (!query || !designerId) return;

  appendMessage("user", "You", `${query} | designer ${designerId}`);
  const done = setBusy(submitButton, "Searching...");

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
    const data = await parseResponse(response);
    appendMessage("assistant", "Vision RAG", renderSearchResults(data.results || []));
  } catch (error) {
    appendMessage("assistant", "Vision RAG", `Search failed: ${error.message}`);
  } finally {
    done();
  }
});

generateForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const submitButton = generateForm.querySelector("button");
  const prompt = promptInput.value.trim();
  const designerId = Number(generateDesignerInput.value);
  if (!prompt || !designerId) return;

  const done = setBusy(submitButton, "Generating...");
  generatedText.textContent = "Retrieving references and generating image...";
  generatedPreview.innerHTML = "Generating";

  try {
    const response = await fetch(`${API_PREFIX}/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        prompt,
        designer_id: designerId,
        top_k: 3,
      }),
    });
    const data = await parseResponse(response);
    generatedText.textContent = data.generated_image_url
      ? `Saved locally: ${data.generated_image_url}`
      : prettyJson(data.generation || data);

    if (data.generated_image_url) {
      generatedPreview.innerHTML = "";
      const img = document.createElement("img");
      img.src = data.generated_image_url;
      img.alt = "Generated result";
      generatedPreview.appendChild(img);
    }
  } catch (error) {
    generatedText.textContent = `Generation failed: ${error.message}`;
    generatedPreview.textContent = "Generation failed";
  } finally {
    done();
  }
});

checkHealth();
