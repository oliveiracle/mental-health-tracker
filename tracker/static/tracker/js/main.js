document.addEventListener("DOMContentLoaded", function() {
    initializeNavbarHoverEffects();
    initializeCardHoverEffects();
    initializeButtonHoverEffects();
    initializeMoodFormInteractions();
    initializeMoodTrendsChart();
});

function initializeNavbarHoverEffects() {
    const navButtons = document.querySelectorAll(
        ".nav-btn-primary, .nav-btn-secondary"
    );

    navButtons.forEach((button) => {
        button.addEventListener("mouseenter", function() {
            if (this.classList.contains("nav-btn-primary")) {
                this.style.transform = "translateY(-2px)";
                this.style.boxShadow =
                    "0 6px 16px rgba(92, 107, 192, 0.35)";
            }
        });

        button.addEventListener("mouseleave", function() {
            this.style.transform = "translateY(0)";
            if (this.classList.contains("nav-btn-primary")) {
                this.style.boxShadow =
                    "0 4px 12px rgba(92, 107, 192, 0.25)";
            }
        });
    });

    const signInLink = document.querySelector(".nav-link-primary");
    if (signInLink) {
        signInLink.addEventListener("mouseenter", function() {
            this.style.color = "#7e57c2";
        });

        signInLink.addEventListener("mouseleave", function() {
            this.style.color = "#5c6bc0";
        });
    }
}

function initializeCardHoverEffects() {
    const cards = document.querySelectorAll(".feature-card");

    cards.forEach((card) => {
        card.addEventListener("mouseenter", function() {
            this.style.transform = "translateY(-8px)";
            this.style.boxShadow =
                "0 12px 24px rgba(92, 107, 192, 0.15)";
        });

        card.addEventListener("mouseleave", function() {
            this.style.transform = "translateY(0)";
            this.style.boxShadow =
                "0 4px 12px rgba(0,0,0,0.08)";
        });
    });
}

function initializeButtonHoverEffects() {
    const primaryButtons = document.querySelectorAll(
        ".btn-primary-action"
    );
    const secondaryButtons = document.querySelectorAll(
        ".btn-secondary-action"
    );

    primaryButtons.forEach((button) => {
        button.addEventListener("mouseenter", function() {
            this.style.transform = "translateY(-2px)";
            this.style.boxShadow =
                "0 4px 12px rgba(67, 160, 71, 0.4)";
        });

        button.addEventListener("mouseleave", function() {
            this.style.transform = "translateY(0)";
            this.style.boxShadow =
                "0 2px 8px rgba(67, 160, 71, 0.3)";
        });
    });

    secondaryButtons.forEach((button) => {
        button.addEventListener("mouseenter", function() {
            this.style.transform = "translateY(-2px)";
            if (this.classList.contains("btn-update")) {
                this.style.boxShadow =
                    "0 4px 10px rgba(149, 117, 205, 0.4)";
            } else if (this.classList.contains("btn-archive")) {
                this.style.boxShadow =
                    "0 4px 10px rgba(255, 183, 77, 0.4)";
            }
        });

        button.addEventListener("mouseleave", function() {
            this.style.transform = "translateY(0)";
            if (this.classList.contains("btn-update")) {
                this.style.boxShadow =
                    "0 2px 6px rgba(149, 117, 205, 0.3)";
            } else if (this.classList.contains("btn-archive")) {
                this.style.boxShadow =
                    "0 2px 6px rgba(255, 183, 77, 0.3)";
            }
        });
    });
}

function initializeMoodFormInteractions() {
    const moodField = document.querySelector(
        ".mood-form-page .form-range"
    );
    const scoreValue = document.querySelector(
        ".mood-form-page #score-value"
    );
    const notesField = document.querySelector(
        ".mood-form-page textarea[name=\"notes\"]"
    );
    const counter = document.querySelector(
        ".mood-form-page #notes-counter"
    );

    if (moodField && scoreValue) {
        const lerp = (a, b, t) => Math.round(a + (b - a) * t);
        const colorForValue = (value) => {
            const t = value / 10;
            const r = lerp(239, 30, t);
            const g = lerp(68, 58, t);
            const b = lerp(68, 138, t);
            return `rgb(${r}, ${g}, ${b})`;
        };

        const updateScore = () => {
            const value = Number(moodField.value || 5);
            const color = colorForValue(value);
            scoreValue.textContent = value;
            scoreValue.style.color = color;
            moodField.style.setProperty("--mood-color", color);
        };

        moodField.addEventListener("input", updateScore);
        updateScore();
    }

    if (notesField && counter) {
        const updateCount = () => {
            const max = notesField.getAttribute("maxlength");
            const current = notesField.value.length;
            const display = max
                ? `${current}/${max}`
                : `${current} chars`;
            counter.textContent = display;
        };

        notesField.addEventListener("input", updateCount);
        updateCount();
    }
}

function loadChartJs() {
    return new Promise((resolve, reject) => {
        if (window.Chart) {
            resolve();
            return;
        }

        const script = document.createElement("script");
        script.src = "https://cdn.jsdelivr.net/npm/chart.js";
        script.onload = () => resolve();
        script.onerror = () => reject(
            new Error("Failed to load Chart.js")
        );
        document.head.appendChild(script);
    });
}

function initializeMoodTrendsChart() {
    const chartElement = document.getElementById("moodChart");
    if (!chartElement) return;

    const labelsRaw = chartElement.dataset.labels || "";
    const scoresRaw = chartElement.dataset.scores || "";
    const labels = labelsRaw.split(",").filter(Boolean);
    const scores = scoresRaw
        .split(",")
        .filter((value) => value.length)
        .map((value) => Number(value));

    loadChartJs()
        .then(() => {
            const ctx = chartElement.getContext("2d");
            if (!ctx) return;

            new Chart(ctx, {
                type: "line",
                data: {
                    labels,
                    datasets: [
                        {
                            label: "Mood Score",
                            data: scores,
                            borderColor: "#5c6bc0",
                            backgroundColor:
                                "rgba(92, 107, 192, 0.18)",
                            fill: true,
                            tension: 0.35,
                            pointRadius: 4,
                            pointBackgroundColor: "#5c6bc0",
                        },
                    ],
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            min: 0,
                            max: 10,
                            ticks: {
                                stepSize: 1,
                            },
                        },
                    },
                    plugins: {
                        legend: {
                            display: false,
                        },
                    },
                },
            });
        })
        .catch(() => {
            // Silently ignore chart errors to avoid blocking the page.
        });
}
