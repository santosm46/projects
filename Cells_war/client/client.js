/**
 * faz conexão com o servidor
 * inicia inputs
 * repassa input para o servidor (inserve observador)
 */

 var debug = 0;


function createClient(game) {
    let server;
    const input = createInputListener(keyAndMouse);
    const drawer = createDrawer();

    const state = {
        observers: []
    }
    state.id = 'c' + Math.floor(random(1000, 9999));

    function inputFromClient(command) {
        // debuga('client f:inputFromClient mandando input pro server', command);
        server.inputToServer(command);
    }


    input.subscribe(inputFromClient);

    function createServerConnection(self) {
        // só pode ser chamado após setupClient
        return game.server.receiveConnection({ 
            instance: self, 
            id: state.id
        });
    }

    function getUpdatedState() {
        // debuga('client -> server.state',server);
        return server.game.state;
    }

    function receiveQuadState(command) {
        drawer.gameState = command.game.state;
    }

    function getClientCell() {
        let clientCell = getUpdatedState().cells[state.id];
        return clientCell;
    }

    // because can only connect to server when creation of this object is complete
    function setupClient(self) {
        server = createServerConnection(self);
        input.setClient(self);
    }

    function getClientId() {
        return state.id;
    }

    
    return {
        drawer,
        input,
        getClientId,
        // subscribe,
        receiveQuadState,
        createServerConnection,
        setupClient,
        getUpdatedState,
        getClientCell
    };
}

