function createDrawer() {
    let gameState;

    // function stateFromServer(command) {
    //     if (command.type === 'draw') {
    //         gameState = command.state;
    //     }
    // }


    function drawGameState(state) {
        state.chunks.drawGridChunks();
    }

    function drawCell(cell) {
        fill(cell.cor.r, cell.cor.g, cell.cor.b);
        circle(cell.x, cell.y, cell.raio);
    }

    function drawCells(state) {
        const celulas = state.cells;

        for(cellId in celulas) {
            drawCell(celulas[cellId]);
        }
    }

    return {
        gameState,
        drawGameState,
        drawCells
    }

}



// function vizinhos(cell) {
//     let tam = chunks.size * 3;
//     let chunkX = Math.floor(cell.x / chunks.size) - 1;
//     let chunkY = Math.floor(cell.y / chunks.size) - 1;

//     fill(0, 200, 50, 150);
//     rect(chunkX * chunks.size,
//         chunkY * chunks.size,
//         tam, tam);
// }