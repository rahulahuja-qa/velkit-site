document.getElementById("f").addEventListener("submit", async (e) => {
  e.preventDefault();
  const fd = new FormData(e.target);
  const body = {
    target_role: fd.get("target_role"),
    current_skills: String(fd.get("current_skills")||"").split(",").map(s=>s.trim()).filter(Boolean),
    interests: String(fd.get("interests")||"").split(",").map(s=>s.trim()).filter(Boolean)
  };
  const r = await fetch("/api/trainings", {
    method:"POST",
    headers:{ "Content-Type":"application/json" },
    body: JSON.stringify(body)
  });
  const j = await r.json();
  const el = document.getElementById("plan");
  el.innerHTML = (j.plan||[]).map(p=>`
    <div class="card">
      <div><strong>${p.title}</strong></div>
      <div class="sub">${p.provider} • ${p.level} • ~${p.estimated_hours}h</div>
      <p>${p.why}</p>
    </div>`).join("");
});
