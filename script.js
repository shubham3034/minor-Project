/* ------------------------------------------------
   QUIZ QUESTIONS
---------------------------------------------------*/
const questions = [
  { q: "Which of the following is a biotic component?", choices: ["Water", "Soil", "Plants", "Sunlight"], a: 2 },
  { q: "Which abiotic factor is essential for photosynthesis?", choices: ["Animals", "Bacteria", "Sunlight", "Fungi"], a: 2 },
  { q: "Which option includes only biotic components?", choices: ["Plants, Animals, Bacteria", "Rocks, Soil, Air", "Sunlight, Water, Wind", "Clouds, Rain, Light"], a: 0 },
  { q: "Why is environmental awareness important?", choices: ["To increase pollution", "To promote sustainable living", "To damage ecosystems", "To avoid education"], a: 1 },
  { q: "Which factor is *not* abiotic?", choices: ["Temperature", "Wind", "Animals", "Water"], a: 2 }
];

/* ------------------------------------------------
   DOM ELEMENTS (QUIZ ONLY)
---------------------------------------------------*/
const container = document.getElementById("quizContainer");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");
const submitBtn = document.getElementById("submitBtn");
const resultBox = document.getElementById("result");

let index = 0;
let answers = Array(questions.length).fill(null);

/* ------------------------------------------------
   RENDER QUESTION
---------------------------------------------------*/
function renderQuestion() {
  if (!container) return; // Prevent errors on other pages

  const obj = questions[index];

  container.innerHTML = `
    <div class="qcard" style="animation:fadeUp 0.6s ease;">
      <h3>Q${index + 1}. ${obj.q}</h3>
      <div class="options">
        ${obj.choices
          .map((c, i) => `
            <label class="option">
              <input type="radio" name="q" value="${i}" ${answers[index] === i ? "checked" : ""}/>
              ${c}
            </label>
          `)
          .join("")}
      </div>
    </div>
  `;

  if (prevBtn) prevBtn.disabled = index === 0;
  if (nextBtn) nextBtn.style.display = index === questions.length - 1 ? "none" : "inline-block";
  if (submitBtn) submitBtn.style.display = index === questions.length - 1 ? "inline-block" : "none";

  const opts = container.querySelectorAll('input[name="q"]');
  opts.forEach(o =>
    o.addEventListener("change", e => {
      answers[index] = Number(e.target.value);
      localStorage.setItem("env_quiz", JSON.stringify(answers));
    })
  );
}

/* ------------------------------------------------
   BUTTON EVENTS (QUIZ)
---------------------------------------------------*/
if (prevBtn)
  prevBtn.addEventListener("click", () => {
    index = Math.max(0, index - 1);
    renderQuestion();
  });

if (nextBtn)
  nextBtn.addEventListener("click", () => {
    index = Math.min(questions.length - 1, index + 1);
    renderQuestion();
  });

if (submitBtn)
  submitBtn.addEventListener("click", () => {
    let score = 0;

    for (let i = 0; i < questions.length; i++) {
      if (answers[i] === questions[i].a) score++;
    }

    resultBox.innerHTML = `
      <div style="animation:fadeIn 0.8s;">
        You scored <strong>${score}</strong> out of <strong>${questions.length}</strong>.
      </div>
    `;
      
    localStorage.removeItem("env_quiz");
  });

/* ------------------------------------------------
   LOAD SAVED PROGRESS
---------------------------------------------------*/
const saved = localStorage.getItem("env_quiz");
if (saved) {
  try {
    const parsed = JSON.parse(saved);
    if (Array.isArray(parsed)) answers = parsed;
  } catch {}
}

/* ------------------------------------------------
   INIT QUIZ
---------------------------------------------------*/
renderQuestion();

/* ------------------------------------------------
   ABIOTIC MODEL (PLANT GROWTH INDEX)
---------------------------------------------------*/
document.addEventListener("DOMContentLoaded", () => {
  const temp = document.getElementById("temp");
  const rain = document.getElementById("rain");
  const tempVal = document.getElementById("tempVal");
  const rainVal = document.getElementById("rainVal");
  const growth = document.getElementById("growth");

  // Run only on abiotic.html
  if (temp && rain && tempVal && rainVal && growth) {
    function updateGrowth() {
      const t = parseInt(temp.value);
      const r = parseInt(rain.value);

      tempVal.textContent = t;
      rainVal.textContent = r;

      // Simple ecological growth index
      let tempFactor = 1 - Math.abs(t - 25) / 25; // ideal temp = 25
      let rainFactor = r / 200; // 0–200 rainfall scale

      let index = ((tempFactor + rainFactor) / 2).toFixed(2);
      if (index < 0) index = 0;

      growth.textContent = index;
    }

    temp.addEventListener("input", updateGrowth);
    rain.addEventListener("input", updateGrowth);

    updateGrowth(); // initial
  }
});

/* ------------------------------------------------
   SMALL BUTTON ANIMATION
---------------------------------------------------*/
(function () {
  const style = document.createElement("style");
  style.textContent = `
    .pulse { animation: pulse 0.4s ease; }
    @keyframes pulse {
      0% { transform: translateY(0); }
      50% { transform: translateY(-5px); }
      100% { transform: translateY(0); }
    }
  `;
  document.head.appendChild(style);
})();
