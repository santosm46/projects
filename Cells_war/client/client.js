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

    function inputFromClient(command) {
        server.inputToServer(command);
    }


    input.subscribe(inputFromClient);

    function createServerConnection(self) {
        return game.server.receiveConnection({ 
            instance: self, 
            id: state.id
        });
    }

    function getUpdatedState() {
        return drawer.gameState;
    }

    function receiveQuadState(command) {
        drawer.gameState = command.game.state;
    }

    // because can only connect to server when creation of this object is complete
    function setupClient(self) {
        server = createServerConnection(self);
        input.setClient(self);
    }

    state.id = 'player1';
    return {
        drawer,
        input,
        state,
        // subscribe,
        receiveQuadState,
        createServerConnection,
        setupClient,
        getUpdatedState
    };
}

