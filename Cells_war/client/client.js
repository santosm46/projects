/**
 * faz conexão com o servidor
 * inicia inputs
 * repassa input para o servidor (inserve observador)
 */

var debug = 0;


function createClient(gameRef) {

    // constructor(gameRef) {
    //     game = gameRef;
    //     state = createClientState();
    //     server = null;
    //     receivedState = null;

    // }

    const game = gameRef;
    // server to connect
    let state = createClientState();

    let server;
    let receivedState;

    function createClientState() {
        const state = {};
        
        state.id = 'c' + Math.floor(random(1000, 9999));
        state.observers = [];
        
        return state;
    }

    function inputFromClient(command) {
        server.inputToServer(command);
    }

    // só pode ser chamado após setupClient
    function createServerConnection(serverToConnect, clientInstance) {
        server = serverToConnect;
        // print('server', server);
        server.receiveConnection({ 
            instance: clientInstance, 
            id: state.id
        });
        return server; // might not be needed
    }

    function getUpdatedState() {
        return receivedState;
        // return game.state;
    }

    function receiveQuadState(command) {
        // ... implementar, alguém vai receber o estado
        receivedState = command.state;

    }

    function getClientCell() {
        const us = getUpdatedState();
        // debuga('client.js cliente deve estar aí', us);
        const clientCell = us.cells[state.id];
        // debuga('client.js: updated state', us);
        debugNull(clientCell, `client.js: couldn't find client cell`);
        return clientCell;
    }

    // because can only connect to server when creation of this object is complete
    function setup(command) {
        command.inputListener.subscribe(inputFromClient);
        createServerConnection(game.server, this);//command.client);
    }

    function getClientId() {
        return state.id;
    }

    // function warnDrawer() {
    //     
    // }

    return {
        // input,
        getClientId,
        // subscribe,
        receiveQuadState,
        createServerConnection,
        setup,
        getUpdatedState,
        getClientCell
    };
}

