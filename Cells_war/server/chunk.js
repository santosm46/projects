
function createChunks() {
    let chunks = {
        size: 100
    };

    chunks.rows = height / chunks.size;
    chunks.cols = width / chunks.size;

    let a = [];

    for (let i = 0; i < chunks.rows; i++) {
        let b = [];
        for (let j = 0; j < chunks.cols; j++) {
            b.push(null);
        }
        a.push(b);
    }

    chunks.chunk = a;

    chunks.drawGridChunks = function () {
        for (let j = 0; j <= this.cols; j++) {
            line(j * this.size, 0,
                j * this.size, height);
        }

        for (let i = 0; i <= this.rows; i++) {
            line(0, i * this.size,
                width, i * this.size);
        }
    }

    return chunks;
}



