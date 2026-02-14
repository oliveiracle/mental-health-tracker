/*jslint browser: true */
/*global window, document, Chart, Promise */

(function () {
    "use strict";

    /**
     * Adds hover effects to navigation buttons, creating a subtle lift and shadow
     * effect to provide visual feedback on interaction.
     */
    function initializeNavbarHoverEffects() {
        var navButtons = document.querySelectorAll(
            ".nav-btn-primary, .nav-btn-secondary"
        );
        var signInLink = document.querySelector(
            ".nav-link-primary"
        );

        navButtons.forEach(function (button) {
            button.addEventListener("mouseenter", function () {
                if (button.classList.contains("nav-btn-primary")) {
                    button.style.transform = "translateY(-2px)";
                    button.style.boxShadow = (
                        "0 6px 16px rgba(92, 107, 192, 0.35)"
                    );
                }
            });

            button.addEventListener("mouseleave", function () {
                button.style.transform = "translateY(0)";
                if (button.classList.contains("nav-btn-primary")) {
                    button.style.boxShadow = (
                        "0 4px 12px rgba(92, 107, 192, 0.25)"
                    );
                }
            });
        });

        if (signInLink) {
            signInLink.addEventListener("mouseenter", function () {
                signInLink.style.color = "#7e57c2";
            });

            signInLink.addEventListener("mouseleave", function () {
                signInLink.style.color = "#5c6bc0";
            });
        }
    }

    /**
     * Applies a lift-and-shadow hover effect to feature cards on the homepage,
     * making them feel more interactive and engaging.
     */
    function initializeCardHoverEffects() {
        var cards = document.querySelectorAll(".feature-card");

        cards.forEach(function (card) {
            card.addEventListener("mouseenter", function () {
                card.style.transform = "translateY(-8px)";
                card.style.boxShadow = (
                    "0 12px 24px rgba(92, 107, 192, 0.15)"
                );
            });

            card.addEventListener("mouseleave", function () {
                card.style.transform = "translateY(0)";
                card.style.boxShadow = (
                    "0 4px 12px rgba(0,0,0,0.08)"
                );
            });
        });
    }

    /**
     * Attaches hover effects to primary and secondary action buttons, providing
     * visual feedback through transformations and shadows.
     */
    function initializeButtonHoverEffects() {
        var primaryButtons = document.querySelectorAll(
            ".btn-primary-action"
        );
        var secondaryButtons = document.querySelectorAll(
            ".btn-secondary-action"
        );

        primaryButtons.forEach(function (button) {
            button.addEventListener("mouseenter", function () {
                button.style.transform = "translateY(-2px)";
                button.style.boxShadow = (
                    "0 4px 12px rgba(67, 160, 71, 0.4)"
                );
            });

            button.addEventListener("mouseleave", function () {
                button.style.transform = "translateY(0)";
                button.style.boxShadow = (
                    "0 2px 8px rgba(67, 160, 71, 0.3)"
                );
            });
        });

        secondaryButtons.forEach(function (button) {
            button.addEventListener("mouseenter", function () {
                button.style.transform = "translateY(-2px)";
                if (button.classList.contains("btn-update")) {
                    button.style.boxShadow = (
                        "0 4px 10px rgba(149, 117, 205, 0.4)"
                    );
                } else if (
                    button.classList.contains("btn-archive")
                ) {
                    button.style.boxShadow = (
                        "0 4px 10px rgba(255, 183, 77, 0.4)"
                    );
                }
            });

            button.addEventListener("mouseleave", function () {
                button.style.transform = "translateY(0)";
                if (button.classList.contains("btn-update")) {
                    button.style.boxShadow = (
                        "0 2px 6px rgba(149, 117, 205, 0.3)"
                    );
                } else if (
                    button.classList.contains("btn-archive")
                ) {
                    button.style.boxShadow = (
                        "0 2px 6px rgba(255, 183, 77, 0.3)"
                    );
                }
            });
        });
    }

    /**
     * Manages interactions within the mood entry form, including the dynamic
     * color change of the mood slider and the character counter for the notes field.
     */
    function initializeMoodFormInteractions() {
        var moodField = document.querySelector(
            ".mood-form-page .form-range"
        );
        var scoreValue = document.querySelector(
            ".mood-form-page #score-value"
        );
        var notesField = document.querySelector(
            ".mood-form-page textarea[name='notes']"
        );
        var counter = document.querySelector(
            ".mood-form-page #notes-counter"
        );
        var lerp;
        var colorForValue;
        var updateScore;
        var updateCount;

        if (moodField && scoreValue) {
            lerp = function (a, b, t) {
                return Math.round(a + (b - a) * t);
            };

            colorForValue = function (value) {
                var t = value / 10;
                var r = lerp(239, 30, t);
                var g = lerp(68, 58, t);
                var b = lerp(68, 138, t);
                return (
                    "rgb(" + r + ", " + g + ", " + b + ")"
                );
            };

            updateScore = function () {
                var value = Number(moodField.value || 5);
                var color = colorForValue(value);
                scoreValue.textContent = value;
                scoreValue.style.color = color;
                moodField.style.setProperty(
                    "--mood-color",
                    color
                );
            };

            moodField.addEventListener("input", updateScore);
            updateScore();
        }

        if (notesField && counter) {
            updateCount = function () {
                var max = notesField.getAttribute("maxlength");
                var current = notesField.value.length;
                counter.textContent = (
                    max
                    ? current + "/" + max
                    : current + " chars"
                );
            };

            notesField.addEventListener("input", updateCount);
            updateCount();
        }
    }

    /**
     * Asynchronously loads the Chart.js library if it's not already present,
     * ensuring the chart can be rendered without blocking the page load.
     * @returns {Promise} A promise that resolves when Chart.js is loaded.
     */
    function loadChartJs() {
        return new Promise(function (resolve, reject) {
            var script;

            if (window.Chart) {
                resolve();
                return;
            }

            script = document.createElement("script");
            script.src = (
                "https://cdn.jsdelivr.net/npm/chart.js"
            );
            script.onload = function () {
                resolve();
            };
            script.onerror = function () {
                reject(new Error("Failed to load Chart.js"));
            };
            document.head.appendChild(script);
        });
    }

    /**
     * Creates and configures a new Chart.js instance for the mood trends.
     * @param {CanvasRenderingContext2D} ctx - The rendering context of the canvas.
     * @param {string[]} labels - The labels for the x-axis (e.g., dates).
     * @param {number[]} scores - The mood scores for the y-axis.
     * @returns {Chart} The new Chart.js instance.
     */
    function createMoodChart(ctx, labels, scores) {
        return new Chart(ctx, {
            data: {
                datasets: [
                    {
                        backgroundColor: (
                            "rgba(92, 107, 192, 0.18)"
                        ),
                        borderColor: "#5c6bc0",
                        data: scores,
                        fill: true,
                        label: "Mood Score",
                        pointBackgroundColor: "#5c6bc0",
                        pointRadius: 4,
                        tension: 0.35
                    }
                ],
                labels
            },
            options: {
                plugins: {
                    legend: {
                        display: false
                    }
                },
                responsive: true,
                scales: {
                    y: {
                        max: 10,
                        min: 0,
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            },
            type: "line"
        });
    }

    /**
     * Initializes and renders the mood trends chart. It fetches data from the
     * DOM, loads Chart.js if needed, and then creates the chart.
     */
    function initializeMoodTrendsChart() {
        var chartElement = document.getElementById("moodChart");
        var labelsRaw;
        var scoresRaw;
        var labels;
        var scores;

        if (!chartElement) {
            return;
        }

        labelsRaw = chartElement.dataset.labels || "";
        scoresRaw = chartElement.dataset.scores || "";
        labels = labelsRaw.split(",").filter(Boolean);
        scores = scoresRaw.split(",").filter(function (value) {
            return value.length > 0;
        }).map(function (value) {
            return Number(value);
        });

        loadChartJs().then(function () {
            var ctx = chartElement.getContext("2d");
            if (!ctx) {
                return;
            }
            createMoodChart(ctx, labels, scores);
        }).catch(function () {
            return;
        });
    }

    /**
     * Main entry point. Initializes all interactive components and event
     * listeners after the DOM is fully loaded.
     */
    function main() {
        initializeNavbarHoverEffects();
        initializeCardHoverEffects();
        initializeButtonHoverEffects();
        initializeMoodFormInteractions();
        initializeMoodTrendsChart();
    }

    document.addEventListener("DOMContentLoaded", main);
}());