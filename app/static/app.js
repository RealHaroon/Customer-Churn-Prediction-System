document.getElementById("btnPredict").addEventListener("click", async () => {
  const resultEl = document.getElementById("result");
  try {
    const text = document.getElementById("payload").value;
    const payload = JSON.parse(text);

    const resp = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await resp.json();
    resultEl.textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    resultEl.textContent = "Error: " + err.message;
  }
});
