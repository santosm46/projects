function createServerNetwork() {
    let clients = [];
    let game;

    // function newQuadState(c) {
    //     const state = {};
    //     const chunks = {}

    //     chunks.rows = c.rows;
    //     chunks.cols = c.cols;
    //     state.chunks = chunks;
    //     state.cells = {};
    //     state.energyOrbs = {};

    //     return state;
    // }

    function receiveConnection(client) {
        clients.push(client);

        // criar player
        let command = {};
        command.cellId = client.id;
        this.game.createCell(command);
        debugm(`client ${client.id} connected to the server`);
        return this;
    }

    // function validChunk(chunks, i, j) {
    //     if (i < 0) return false;
    //     if (j < 0) return false;
    //     if (i >= chunks.rows) return false;
    //     if (j >= chunks.cols) return false;
    //     return true;
    // }

    // function cellsOfNearChunk(clientChunk, chunks, quadState) {
    //     debuga(`server.js células na chunk[${clientChunk.y}][${clientChunk.x}] da célula`, chunks.getChunkList()[clientChunk.y][clientChunk.x]);
    //     // debuga('server.js clientChunk', clientChunk);
    //     debuga('server.js chunks.getChunkList()', chunks.getChunkList());
    //     // debuga('server.js chunks', chunks);
    //     for (let i = -1; i < 2; i++) {
    //         for (let j = -1; j < 2; j++) {
    //             // para não pegar valores inválidos
    //             const ni = clientChunk.y + i; const nj = clientChunk.x + j;
    //             if (validChunk(chunks, ni, nj)) {
    //                 // debugm(`server.js chunks[${ni}][${nj}]`);
    //                 // for some reason I can't create a reference  to the cells of a chunk,
    //                 //   so I access directly through chunks.getChunkList()
    //                 const chunkCells = chunks.getChunkList()[ni][nj]; 
    //                 // debuga(`server.js todas células na chunk[${ni}][${nj}]`, chunks.getChunkList()[ni][nj]);
    //                 for (let cell of chunkCells) {
    //                     // debuga(`server.js célula na chunk[${ni}][${nj}]`, cell);
    //                     const cellId = cell.id;
    //                     quadState.cells[cellId] = cell;
    //                 }
    //             }
    //         }
    //     }
    // }

    /**
     * this will be implemented to send only cells of near chunks of a client
     * for now it sends all cells for each client
     */
    function sendQuadState() {

        for (let i = 0; i < clients.length; i++) {
            // const clientCell = this.game.state.cells[clients[i].id];
            // const clientChunk = clientCell.chunk; // cell chunk
            // debuga('server.js: this.game.state.chunks ',this.game.state.chunks);
            // const chunksRef = this.game.state.chunks;
            // const quadState = newQuadState(chunksRef);
            // cellsOfNearChunk(clientChunk, chunksRef, quadState);
            // clientReceiveState({ state: quadState });
            
            const clientReceiveState = clients[i].instance.receiveQuadState;
            debugNull(clientReceiveState, `server.js: Couldn't get receive state funtion of client[${i}]: ${clients[i].id}`);
            clientReceiveState({ state: this.game.state });
            // clients[i].instance.receivedState = this.game.state;
        }

    }

    /**
     * Each cell is in a chunk, the chunk has a list of cells in it
     * The list is updated often
     */
    // function updateLocalChunks() {
    //     const allCells = this.game.state.cells;
    //     const oldChunks = this.game.state.chunks;
    //     const newCL = this.game.state.chunks.newChunkList(oldChunks);

    //     this.game.state.chunks.clearChunk
    //     debuga(`server.js: allCells (${allCells.length})`, allCells);
    //     for (let cellId in allCells) {
    //         const cell = allCells[cellId];
    //         const ncc = this.game.cellHandler.getChunkPos(cell, oldChunks);
    //         cell.chunk = ncc;

    //         // newCL[ncc.y][ncc.x].push(cell); // put cell on the chunk
    //         this.game.state.chunks.addCellToChunk(ncc, cell);

    //     }
    //     this.game.state.chunks.chunkList = newCL;
    // }

    function setup(game) {
        this.game = game;
    }

    function inputToServer(command) {
        debugm(`received input ${command.key} from client ${command.cellId}`);
        // an observer can be created to actions observe input to server
        this.game.actions.reactToInput(command);
    }

    return {
        receiveConnection,
        inputToServer,
        sendQuadState,
        setup,
        // updateLocalChunks
    };

}



