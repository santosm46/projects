function createState() {
    const state = {};
    const chunks = createChunks();

    state.chunks = chunks;
    state.cells = {};
    state.energyOrbs = {};

    return state;
}


function createGame() {
    let actions = null;

    const state = createState();
    const server = createServerNetwork();
    const cellHandler = createCellHandler();
    
    function tickClock() {
        this.server.sendQuadState();
        this.server.updateLocalChunks();
    }

    function createCell(command) {
        let cell = this.cellHandler.createCell(command);
        this.state.cells[cell.id] = cell;
    }
    
    function setup() {
        this.server.setup(this);
        this.cellHandler.setup(this);
        this.actions = createActions();
        for(let i=0; i<10; i++) {
            this.createCell({});
        }
        // cellHandler.createCells({game:game, numCells: 10}); //50, chunks, randomMovement);
    }

    return {
        cellHandler,
        server,
        tickClock,
        state,
        setup,
        createCell
    };
}

