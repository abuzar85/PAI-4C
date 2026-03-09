class ChessBoard {
    constructor(elementId, size) {
        this.element = document.getElementById(elementId);
        this.size = size;
        this.squares = [];
        this.queens = new Map(); // key: row, value: column
        this.init();
    }

    init() {
        this.element.innerHTML = '';
        this.element.style.gridTemplateColumns = `repeat(${this.size}, 1fr)`;
        this.element.style.gridTemplateRows = `repeat(${this.size}, 1fr)`;

        // Calculate max size based on parent container
        const container = this.element.parentElement;
        const maxSize = Math.min(container.clientWidth, container.clientHeight) * 0.9;
        this.element.style.width = `${maxSize}px`;
        this.element.style.height = `${maxSize}px`;

        for (let r = 0; r < this.size; r++) {
            this.squares[r] = [];
            for (let c = 0; c < this.size; c++) {
                const square = document.createElement('div');
                square.className = `square ${(r + c) % 2 === 0 ? 'light' : 'dark'}`;
                square.dataset.row = r;
                square.dataset.col = c;
                this.element.appendChild(square);
                this.squares[r][c] = square;
            }
        }
    }

    placeQueen(row, col) {
        // Remove existing queen in this row if any
        this.removeQueen(row);

        const square = this.squares[row][col];
        const queen = document.createElement('span');
        queen.className = 'queen';
        queen.innerHTML = '♛';
        square.appendChild(queen);
        this.queens.set(row, col);

        // GSAP Animation
        gsap.fromTo(queen,
            { scale: 0, opacity: 0, rotation: -45 },
            { scale: 1, opacity: 1, rotation: 0, duration: 0.4, ease: "back.out(1.7)" }
        );

        this.highlightSquare(row, col, 'active');
    }

    removeQueen(row) {
        if (this.queens.has(row)) {
            const col = this.queens.get(row);
            const square = this.squares[row][col];
            const queen = square.querySelector('.queen');

            if (queen) {
                gsap.to(queen, {
                    scale: 0,
                    opacity: 0,
                    duration: 0.3,
                    onComplete: () => queen.remove()
                });
            }
            this.queens.delete(row);
            this.clearHighlights(row);
        }
    }

    showConflict(row, col) {
        this.highlightSquare(row, col, 'conflict');
        // Shake animation
        gsap.to(this.squares[row][col], {
            x: 5,
            repeat: 5,
            yoyo: true,
            duration: 0.05,
            onComplete: () => {
                gsap.to(this.squares[row][col], { x: 0, duration: 0.1 });
            }
        });
    }

    highlightSquare(row, col, className) {
        this.squares[row][col].classList.add(className);
    }

    clearHighlights(row) {
        if (row !== undefined) {
            for (let c = 0; c < this.size; c++) {
                this.squares[row][c].classList.remove('active', 'conflict');
            }
        } else {
            this.squares.flat().forEach(sq => sq.classList.remove('active', 'conflict'));
        }
    }

    reset() {
        this.queens.clear();
        this.init();
    }

    setBoard(board) {
        // board is an array [col0, col1, col2, ...]
        this.reset();
        board.forEach((col, row) => {
            if (col !== -1) {
                this.placeQueen(row, col);
            }
        });
    }
}
