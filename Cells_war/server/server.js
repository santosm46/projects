function createServerNetwork() {
    let clients = [];
    let game;

    function receiveConnection(client) {
        clients.push(client);

        // criar player
        let command = {};
        command.cellId = client.id;
        this.game.createCell(command);
        debugm(`client ${client.id} connected to the server`);
        // debugm(client);
        return this;
    }

    function sendQuadState() {

        // let i = 0;
        // debugm(`calling client ${clients[i].name}`);
        // debuga('clients[i].instance', clients);

        // debugm(`about to send quadStates to ${clients.length} clients`);
        for (let i = 0; i < clients.length; i++) {
            const clientReceiveState = clients[i].instance.receiveQuadState;
            // debuga('clientReceiveState', clientReceiveState);
            const quadState = [];

            const yourobject = this.game.state.cells;
            for (let cellKey in yourobject) {
                // console.log(cellKey, yourobject[cellKey]);
            }
            clientReceiveState({ state: this.game.state });
        }

    }

    /**
     * Each cell is in a chunk, the chunk has a list of cells in it
     * The list is updated often
     */
    function updateLocalChunks() {
        // debuga('game.state', this.game);
        const allCells = this.game.state.cells;
        const oldChunks = this.game.state.chunks;
        // debuga('oldChunks', oldChunks);
        const newChunks = newChunkList(oldChunks);

        for (let cellId in allCells) {
            const cell = allCells[cellId];
            const ncc = this.game.cellHandler.getChunkPos(cell, oldChunks);
            cell.chunk = ncc;
            // debuga('cell',cell);
            // debuga('newChunks',newChunks);

            newChunks[ncc.y][ncc.x].push(cell); // put cell on the chunk
            
        }
        this.game.state.chunks.chunk = newChunks;
    }

    function setup(game) {
        this.game = game;
    }

    function inputToServer(command) {
        debugm(`received input ${command.key} from client ${command.cellId}`);
        this.game.actions.reactToInput(command);
    }

    return {
        receiveConnection,
        inputToServer,
        sendQuadState,
        setup,
        updateLocalChunks
    };

}