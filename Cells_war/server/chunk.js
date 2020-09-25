function newChunkList(chunks) {
    const a = [];

    for (let i = 0; i < chunks.rows; i++) {
        let b = [];
        for (let j = 0; j < chunks.cols; j++) {
            b.push([]);
        }
        a.push(b);
    }
    return a;
}

function createChunks() {
    let chunks = {
        size: 100
    };

    chunks.rows = height / chunks.size;
    chunks.cols = width / chunks.size;

    

    chunks.chunk = newChunkList(chunks);

    return chunks;
}



