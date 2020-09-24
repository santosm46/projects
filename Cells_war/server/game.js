function createState() {
    return {
        cells: {},
        energyOrbs: {}
    };
}


function createGame() {

    const state = createState();
    const chunks = createChunks();
    let actions = null;

    state.chunks = chunks;

    const server = createServerNetwork();
    
    const cellHandler = createCellHandler();


    
    function tickClock() {
        server.sendQuadState();
    }

    function createCell(command) {
        let cell = game.cellHandler.createCell(command);
        game.state.cells[cell.id] = cell;
    }
    // function callCreateCells(game) {

    // }
    function setupGame(game) {
        server.setup(game);
        cellHandler.setup(game);
        this.actions = createActions();
        for(let i=0; i<30; i++) {
            game.createCell({});
        }
        // cellHandler.createCells({game:game, numCells: 10}); //50, chunks, randomMovement);
    }

    return {
        cellHandler,
        server,
        tickClock,
        state,
        chunks,
        setupGame,
        createCell
    };
}

