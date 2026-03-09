// Main App Controller
class App {
    constructor() {
        this.boardSizeInput = document.getElementById('boardSize');
        this.solveBtn = document.getElementById('solveBtn');
        this.resetBtn = document.getElementById('resetBtn');
        this.playPauseBtn = document.getElementById('playPauseBtn');
        this.prevBtn = document.getElementById('prevBtn');
        this.nextBtn = document.getElementById('nextBtn');
        this.speedSlider = document.getElementById('speedSlider');
        this.solutionSelect = document.getElementById('solutionSelect');
        this.downloadBtn = document.getElementById('downloadReportBtn');
        this.loader = document.getElementById('loader');

        // State displays
        this.visitedDisplay = document.getElementById('visitedCount');
        this.backtrackDisplay = document.getElementById('backtrackCount');
        this.solutionDisplay = document.getElementById('solutionCount');
        this.runtimeDisplay = document.getElementById('runtimeDisplay');
        this.explanationText = document.getElementById('stepExplanation');
        this.statusIndicator = document.getElementById('statusIndicator');

        // App variables
        this.board = null;
        this.tree = null;
        this.steps = [];
        this.solutions = [];
        this.currentStepIndex = -1;
        this.isPlaying = false;
        this.animationTimer = null;
        this.apiResult = null;

        this.init();
    }

    init() {
        this.setupBoard();
        this.setupTree();
        this.attachEventListeners();
    }

    setupBoard() {
        const size = parseInt(this.boardSizeInput.value);
        this.board = new ChessBoard('chessboard', size);
    }

    setupTree() {
        this.tree = new SearchTree('treeSvg', 'treeContainer');
    }

    attachEventListeners() {
        this.solveBtn.addEventListener('click', () => this.solve());
        this.resetBtn.addEventListener('click', () => this.reset());
        this.playPauseBtn.addEventListener('click', () => this.togglePlay());
        this.nextBtn.addEventListener('click', () => this.stepForward());
        this.prevBtn.addEventListener('click', () => this.stepBackward());
        this.speedSlider.addEventListener('input', () => {
            if (this.isPlaying) {
                this.pause();
                this.play();
            }
        });

        this.boardSizeInput.addEventListener('change', () => {
            this.reset();
            this.setupBoard();
        });

        this.solutionSelect.addEventListener('change', (e) => {
            const index = parseInt(e.target.value);
            if (index >= 0) {
                this.board.setBoard(this.solutions[index]);
            }
        });

        this.downloadBtn.addEventListener('click', () => this.generateReport());
    }

    async solve() {
        const n = this.boardSizeInput.value;
        this.loader.classList.remove('hidden');
        this.reset();

        try {
            const response = await fetch('http://localhost:5000/solve', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ n })
            });

            const data = await response.json();
            if (data.status === 'success') {
                this.apiResult = data;
                this.steps = data.steps;
                this.solutions = data.solutions;

                this.visitedDisplay.innerText = data.visited_states;
                this.backtrackDisplay.innerText = data.total_backtracks;
                this.solutionDisplay.innerText = data.total_solutions;
                this.runtimeDisplay.innerText = data.runtime;

                this.populateSolutions();
                this.enableControls();
                this.statusIndicator.innerText = 'SOLVED';
                this.statusIndicator.classList.add('text-emerald-400');

                this.play();
            } else {
                alert('Error: ' + data.error);
            }
        } catch (error) {
            console.error('Fetch error:', error);
            alert('Could not connect to backend. Make sure app.py is running.');
        } finally {
            this.loader.classList.add('hidden');
        }
    }

    populateSolutions() {
        const nav = document.getElementById('solutionsNav');
        nav.classList.remove('hidden');
        this.solutionSelect.innerHTML = '<option value="-1">Browse Solutions...</option>';
        this.solutions.forEach((_, i) => {
            const opt = document.createElement('option');
            opt.value = i;
            opt.innerText = `Solution ${i + 1}`;
            this.solutionSelect.appendChild(opt);
        });
    }

    enableControls() {
        this.playPauseBtn.disabled = false;
        this.nextBtn.disabled = false;
        this.prevBtn.disabled = false;
    }

    reset() {
        this.pause();
        this.steps = [];
        this.solutions = [];
        this.currentStepIndex = -1;
        this.apiResult = null;

        this.board.reset();
        this.tree.reset();

        this.visitedDisplay.innerText = '0';
        this.backtrackDisplay.innerText = '0';
        this.solutionDisplay.innerText = '0';
        this.runtimeDisplay.innerText = '0';
        this.explanationText.innerHTML = '<p class="text-slate-400 italic">Board reset. Press Solve to start.</p>';

        this.statusIndicator.innerText = 'IDLE';
        this.statusIndicator.classList.remove('text-emerald-400');

        document.getElementById('solutionsNav').classList.add('hidden');
        this.playPauseBtn.disabled = true;
        this.nextBtn.disabled = true;
        this.prevBtn.disabled = true;
    }

    togglePlay() {
        if (this.isPlaying) this.pause();
        else this.play();
    }

    play() {
        if (this.currentStepIndex >= this.steps.length - 1) {
            this.currentStepIndex = -1; // Loop or just stop? Let's reset for fresh play
            this.board.reset();
            this.tree.reset();
        }

        this.isPlaying = true;
        document.getElementById('playIcon').classList.add('hidden');
        document.getElementById('pauseIcon').classList.remove('hidden');

        const speed = 1050 - parseInt(this.speedSlider.value);
        this.animationTimer = setInterval(() => {
            if (!this.stepForward()) {
                this.pause();
            }
        }, speed);
    }

    pause() {
        this.isPlaying = false;
        document.getElementById('playIcon').classList.remove('hidden');
        document.getElementById('pauseIcon').classList.add('hidden');
        clearInterval(this.animationTimer);
    }

    stepForward() {
        if (this.currentStepIndex < this.steps.length - 1) {
            this.currentStepIndex++;
            this.applyStep(this.steps[this.currentStepIndex], 'forward');
            return true;
        }
        return false;
    }

    stepBackward() {
        if (this.currentStepIndex > 0) {
            this.currentStepIndex--;
            this.applyStep(this.steps[this.currentStepIndex], 'backward');
            return true;
        }
        return false;
    }

    applyStep(step, direction) {
        this.explanationText.innerHTML = `<p class="text-indigo-300 font-medium">${step.description}</p>`;

        switch (step.type) {
            case 'visit':
                this.tree.addNode(step.id, step.parent_id, { type: 'visit', description: step.description });
                this.tree.setActiveNode(step.id);
                this.board.setBoard(step.board);
                break;
            case 'attempt':
                this.tree.addNode(step.id, step.parent_id, { type: 'attempt', description: step.description });
                this.tree.setActiveNode(step.id);
                this.board.setBoard(step.board);
                break;
            case 'success':
                this.tree.setActiveNode(step.id, 'success');
                this.board.placeQueen(step.row, step.col);
                break;
            case 'conflict':
                this.tree.setActiveNode(step.id, 'conflict');
                this.board.showConflict(step.row, step.col);
                break;
            case 'backtrack':
                this.board.removeQueen(step.row);
                // When backtracking, we don't remove node from tree for visual history, 
                // but we could mark it as "inactive"
                break;
            case 'solution':
                this.tree.setActiveNode(this.steps[this.currentStepIndex - 1].id, 'solution');
                this.board.setBoard(step.board);
                this.statusIndicator.innerText = 'SOLUTION FOUND!';
                break;
        }

        // Logic for backwards might need full state reconstruction if steps are delta-only.
        // Since we have 'board' snapshot in 'visit' and 'attempt', it helps.
    }

    generateReport() {
        if (!this.apiResult) return;

        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();
        const n = this.boardSizeInput.value;

        // Title
        doc.setFontSize(22);
        doc.setTextColor(99, 102, 241);
        doc.text("N-Queens AI Visualization Report", 20, 30);

        // Stats
        doc.setFontSize(14);
        doc.setTextColor(0, 0, 0);
        doc.text(`Board Size: ${n}x${n}`, 20, 50);
        doc.text(`Total Solutions: ${this.apiResult.total_solutions}`, 20, 60);
        doc.text(`Visited States: ${this.apiResult.visited_states}`, 20, 70);
        doc.text(`Total Backtracks: ${this.apiResult.total_backtracks}`, 20, 80);
        doc.text(`Computation Time: ${this.apiResult.runtime} ms`, 20, 90);

        // Algorithm Description
        doc.setFontSize(16);
        doc.text("Algorithm Details", 20, 110);
        doc.setFontSize(12);
        const description = "The solver uses a Dynamic Backtracking approach. It tries to place a queen in each row, ensuring no two queens threaten each other (same column or diagonal). If a conflict occurs, it backtracks to the previous row and tries the next available column.";
        const splitDescription = doc.splitTextToSize(description, 170);
        doc.text(splitDescription, 20, 120);

        // Example Solution
        if (this.solutions.length > 0) {
            doc.setFontSize(16);
            doc.text("Optimal Solution (Example 1)", 20, 150);
            let yPos = 160;
            this.solutions[0].forEach((col, row) => {
                let rowStr = "";
                for (let i = 0; i < n; i++) {
                    rowStr += (i === col ? "[Q]" : "[ ]") + " ";
                }
                doc.setFont("courier");
                doc.text(rowStr, 30, yPos);
                yPos += 8;
            });
        }

        doc.save(`n-queens-${n}-report.pdf`);
    }
}

// Start the app
window.addEventListener('DOMContentLoaded', () => {
    window.app = new App();
});
