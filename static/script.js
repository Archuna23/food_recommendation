// Frontend logic - Flask backend (/api/recommend) ku request anuppum

const $ = (id) => document.getElementById(id);
const SLIDERS = ["spicy", "healthy", "protein", "fast_food"];
let vegetarian = 1;
let timer = null;

function getPreferences() {
  const prefs = { vegetarian };
  SLIDERS.forEach((key) => (prefs[key] = Number($(key).value)));
  return prefs;
}

async function fetchRecommendations() {
  try {
    const res = await fetch("/api/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(getPreferences()),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Server error");
    render(data);
  } catch (err) {
    $("top3").innerHTML = `<p class="error">Error: ${err.message}</p>`;
  }
}

function mini(label, value) {
  return `<div>${label} ${value}<div class="bar"><i style="width:${value * 10}%"></i></div></div>`;
}

function render(data) {
  $("hint").textContent = `User profile: [${data.user_profile.join(", ")}]`;

  $("top3").innerHTML = data.top3
    .map(
      (f, i) => `
    <div class="card">
      <div class="rank">${i + 1}</div>
      <div>
        <h3>${f.name}<span class="dot ${f.vegetarian ? "veg" : "nonveg"}">● ${f.vegetarian ? "Veg" : "Non-veg"}</span></h3>
        <div class="mini">
          ${mini("Spicy", f.spicy)}${mini("Healthy", f.healthy)}
          ${mini("Protein", f.protein)}${mini("Fast", f.fast_food)}
        </div>
      </div>
      <div class="score"><b>${f.similarity.toFixed(2)}%</b><span>match</span></div>
    </div>`
    )
    .join("");

  $("all").innerHTML = data.all
    .map(
      (f) => `<div><span>${f.name}</span><span class="bar"><i style="width:${f.similarity}%"></i></span></div>`
    )
    .join("");
}

// Small delay so slider drag-la server-ku too many requests pogaadhu
function schedule() {
  clearTimeout(timer);
  timer = setTimeout(fetchRecommendations, 120);
}

function setVeg(value) {
  vegetarian = value;
  $("vYes").classList.toggle("on", value === 1);
  $("vNo").classList.toggle("on", value === 0);
  fetchRecommendations();
}

$("vYes").onclick = () => setVeg(1);
$("vNo").onclick = () => setVeg(0);

SLIDERS.forEach((key) => {
  $(key).oninput = () => {
    $("v-" + key).textContent = $(key).value;
    schedule();
  };
});

$("reset").onclick = () => {
  SLIDERS.forEach((key) => {
    $(key).value = 5;
    $("v-" + key).textContent = 5;
  });
  setVeg(1);
};

fetchRecommendations();
