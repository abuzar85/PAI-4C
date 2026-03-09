document.addEventListener('DOMContentLoaded', () => {
    // Initialize Visualizers
    const jugVisualizer = new WaterJug3D('three-container');
    const graphVisualizer = new StateGraph('graph-container');

    // UI Elements
    const solveBtn = document.getElementById('solve-btn');
    const jug1Input = document.getElementById('jug1-cap');
    const jug2Input = document.getElementById('jug2-cap');
    const targetInput = document.getElementById('target-val');
    const algoSelect = document.getElementById('algo-select');

    const prevBtn = document.getElementById('prev-btn');
    const playPauseBtn = document.getElementById('play-pause-btn');
    const nextBtn = document.getElementById('next-btn');
    const resetBtn = document.getElementById('reset-btn');
    const speedSlider = document.getElementById('speed-slider');

    const ruleDisplay = document.getElementById('rule-display');
    const stateDisplay = document.getElementById('state-display');
    const currentStepSpan = document.getElementById('current-step');
    const totalStepsSpan = document.getElementById('total-steps');
    const stepCounterDiv = document.getElementById('step-counter');
    const visitedCountSpan = document.getElementById('visited-count');
    const pathLengthSpan = document.getElementById('path-length');
    const efficiencyPercent = document.getElementById('efficiency-percent');
    const efficiencyBar = document.getElementById('efficiency-bar');
    const downloadBtn = document.getElementById('download-report-btn');

    // State
    let solutionData = null;
    let currentStepIndex = 0;
    let isPlaying = false;
    let playInterval = null;

    // --- EVENT LISTENERS ---

    solveBtn.addEventListener('click', async () => {
        const jug1 = parseInt(jug1Input.value);
        const jug2 = parseInt(jug2Input.value);
        const target = parseInt(targetInput.value);
        const algorithm = algoSelect.value;

        if (target > Math.max(jug1, jug2)) {
            alert("Target cannot be greater than the largest jug capacity.");
            return;
        }

        solveBtn.disabled = true;
        solveBtn.innerText = "Solving...";

        try {
            const response = await fetch('http://localhost:5000/solve', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ jug1, jug2, target, algorithm })
            });

            const data = await response.json();

            if (data.error) {
                alert(data.error);
                solveBtn.disabled = false;
                solveBtn.innerText = "Solve & Simulate";
                return;
            }

            solutionData = data;
            initSimulation();
        } catch (error) {
            console.error("Error solving:", error);
            alert("Failed to connect to backend. Make sure Flask app is running.");
        } finally {
            solveBtn.disabled = false;
            solveBtn.innerText = "Solve & Simulate";
        }
    });

    function initSimulation() {
        currentStepIndex = 0;
        isPlaying = false;
        clearInterval(playInterval);

        // Reset Visuals
        graphVisualizer.reset();
        jugVisualizer.updateWaterLevels(0, parseInt(jug1Input.value), 0, parseInt(jug2Input.value));

        // Update Stats
        visitedCountSpan.innerText = solutionData.visited.length;
        pathLengthSpan.innerText = solutionData.solution.length - 1; // -1 for initial state

        const efficiency = Math.round((solutionData.solution.length / solutionData.visited.length) * 100);
        efficiencyPercent.innerText = `${efficiency}%`;
        efficiencyBar.style.width = `${efficiency}%`;

        // Update UI Controls
        prevBtn.disabled = true;
        nextBtn.disabled = false;
        playPauseBtn.disabled = false;
        resetBtn.disabled = false;
        downloadBtn.disabled = false;
        stepCounterDiv.classList.remove('hidden');
        totalStepsSpan.innerText = solutionData.solution.length - 1;

        updateStep();
    }

    function updateStep() {
        const step = solutionData.solution[currentStepIndex];
        const [j1, j2] = step.state;

        ruleDisplay.innerText = step.rule;
        stateDisplay.innerText = `Current State: (${j1}, ${j2})`;
        currentStepSpan.innerText = currentStepIndex;

        // 3D Update
        jugVisualizer.updateWaterLevels(j1, parseInt(jug1Input.value), j2, parseInt(jug2Input.value));

        // Graph Update
        // Add all visited nodes up to here or step by step? 
        // Let's add the current path nodes
        const prevState = currentStepIndex > 0 ? solutionData.solution[currentStepIndex - 1].state : null;
        graphVisualizer.addState(step.state, prevState, (j1 === parseInt(targetInput.value) || j2 === parseInt(targetInput.value)));
        graphVisualizer.highlightState(step.state);

        // Button States
        prevBtn.disabled = (currentStepIndex === 0);
        nextBtn.disabled = (currentStepIndex === solutionData.solution.length - 1);

        if (currentStepIndex === solutionData.solution.length - 1) {
            pause();
            ruleDisplay.innerText = "Target Reached!";
            ruleDisplay.classList.add('text-emerald-400');
        } else {
            ruleDisplay.classList.remove('text-emerald-400');
        }
    }

    prevBtn.addEventListener('click', () => {
        if (currentStepIndex > 0) {
            currentStepIndex--;
            updateStep();
        }
    });

    nextBtn.addEventListener('click', () => {
        if (currentStepIndex < solutionData.solution.length - 1) {
            currentStepIndex++;
            updateStep();
        }
    });

    playPauseBtn.addEventListener('click', () => {
        if (isPlaying) pause();
        else play();
    });

    function play() {
        isPlaying = true;
        playPauseBtn.querySelector('#play-icon').classList.add('hidden');
        playPauseBtn.querySelector('#pause-icon').classList.remove('hidden');

        playInterval = setInterval(() => {
            if (currentStepIndex < solutionData.solution.length - 1) {
                currentStepIndex++;
                updateStep();
            } else {
                pause();
            }
        }, speedSlider.max - speedSlider.value + 200);
    }

    function pause() {
        isPlaying = false;
        playPauseBtn.querySelector('#play-icon').classList.remove('hidden');
        playPauseBtn.querySelector('#pause-icon').classList.add('hidden');
        clearInterval(playInterval);
    }

    resetBtn.addEventListener('click', () => {
        currentStepIndex = 0;
        updateStep();
        pause();
    });

    speedSlider.addEventListener('input', () => {
        if (isPlaying) {
            pause();
            play();
        }
    });

    // --- PDF REPORT GENERATION ---
    downloadBtn.addEventListener('click', () => {
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();

        doc.setFontSize(22);
        doc.text("AI Water Jug Search Solution Report", 20, 20);

        doc.setFontSize(12);
        doc.text(`Jug 1 Capacity: ${jug1Input.value}`, 20, 35);
        doc.text(`Jug 2 Capacity: ${jug2Input.value}`, 20, 42);
        doc.text(`Target Value: ${targetInput.value}`, 20, 49);
        doc.text(`Algorithm Used: ${algoSelect.value.toUpperCase()}`, 20, 56);

        doc.setFontSize(16);
        doc.text("Solution Path:", 20, 70);

        doc.setFontSize(10);
        let y = 80;
        solutionData.solution.forEach((step, index) => {
            if (y > 270) {
                doc.addPage();
                y = 20;
            }
            const text = `${index}. ${step.rule} -> (${step.state[0]}, ${step.state[1]})`;
            doc.text(text, 25, y);
            y += 7;
        });

        doc.save(`water_jug_solution_${algoSelect.value}.pdf`);
    });
});
