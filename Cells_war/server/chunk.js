
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

    return chunks;
}



