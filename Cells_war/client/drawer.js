function createDrawer() {

    // function stateFromServer(command) {
    //     if (command.type === 'draw') {
    //         gameState = command.state;
    //     }
    // }


    function drawGameState(client) {
        let state = client.getUpdatedState();

        // if(state == null) {
        //     debugm('nothing to draw...');
        //     return;
        // }
        
        drawGridChunks(state.chunks);
        drawRangeArea(client);
        drawCells(client);
    }

    function drawGridChunks(chunks) {
        for (let j = 0; j <= chunks.cols; j++) {
            line(j * chunks.size, 0,
                j * chunks.size, height);
        }

        for (let i = 0; i <= chunks.rows; i++) {
            line(0, i * chunks.size,
                width, i * chunks.size);
        }
    }

    function drawCell(cell) {
        fill(cell.cor.r, cell.cor.g, cell.cor.b);
        circle(cell.x, cell.y, cell.raio);
    }

    function drawCells(client) {
        const celulas = client.getUpdatedState().cells;

        for(cellId in celulas) {
            drawCell(celulas[cellId]);
        }
    }

    function drawRangeArea(client) {
        // debugm('chamando drawRangeArea');
        let state = client.getUpdatedState();
        let chunkSize = state.chunks.size;
        let cell = client.getClientCell();

        let tam = chunkSize * 3;
        let chunkX = Math.floor(cell.x / chunkSize) - 1;
        let chunkY = Math.floor(cell.y / chunkSize) - 1;
    
        fill(0, 200, 50, 150);
        rect(chunkX * chunkSize,
            chunkY * chunkSize,
            tam, tam);
    }

    return {
        drawGameState,
        drawCells,
        drawRangeArea
    }

}



