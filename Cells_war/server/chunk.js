
function createChunks() {

    const size = 100;
    const rows = height / size;
    const cols = width / size;

    // function newChunkList(chunks) {
    //     const a = [];
    //     // console.log('%c chunk.js: chunkList novinha','background: #222; color: #bada55');
    //     for (let i = 0; i < chunks.rows; i++) {
    //         let b = [];
    //         for (let j = 0; j < chunks.cols; j++) {
    //             b.push([]);
    //         }
    //         a.push(b);
    //     }
    //     return a;
    // }

    // let chunkList = newChunkList({rows, cols});

    // function getChunkList() {
    //     debuga(`chunk.js: pediram o chunkList, aqui está`,chunkList);
    //     return chunkList;
    // }

    // function addCellToChunk(pos, cell) {
    //     this.chunkList[pos.row][pos.col].push(cell);
    // }

    // function clearChunk(pos) {
    //     this.chunkList[pos.row][pos.col] = [];
    // }

    return {
        size,
        rows,
        cols,
        // getChunkList,
        // addCellToChunk,
        // clearChunk,
        // newChunkList
    };
}



