document.getElementById("f").addEventListener("submit", async (e) => {
  e.preventDefault();
  const fd = new FormData(e.target);
  const body = {
    name: fd.get("name"),
    contact: fd.get("contact"),
    role: fd.get("role"),
    years_exp: Number(fd.get("years_exp") || 0),
    skills: String(fd.get("skills")||"").split(",").map(s=>s.trim()).filter(Boolean),
    job_description: fd.get("job_description")
  };
  const r = await fetch("/api/builder", {
    method:"POST",
    headers:{ "Content-Type":"application/json" },
    body: JSON.stringify(body)
  });
  const j = await r.json();
  document.getElementById("out").classList.remove("hidden");
  document.getElementById("cl").textContent = j.cover_letter || JSON.stringify(j,null,2);
  document.getElementById("cv").textContent = JSON.stringify(j.resume || j, null, 2);
});
