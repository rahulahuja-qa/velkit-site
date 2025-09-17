document.getElementById("f").addEventListener("submit", async (e) => {
  e.preventDefault();
  const fd = new FormData(e.target);
  const r = await fetch("/api/review", { method:"POST", body: fd });
  const j = await r.json();
  document.getElementById("out").classList.remove("hidden");
  document.getElementById("score").textContent = j.ats_score ?? "-";
  document.getElementById("kw").innerHTML = (j.missing_keywords||[]).map(k=>`<li>${k}</li>`).join("");
  document.getElementById("rw").innerHTML = (j.rewrite_suggestions||[]).map(s=>`<li>${s}</li>`).join("");
});
