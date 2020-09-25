/**
 * faz conexão com o servidor
 * inicia inputs
 * repassa input para o servidor (inserve observador)
 */

 var debug = 0;

function createClientState() {
    const state = {};
    
    state.id = 'c' + Math.floor(random(1000, 9999));
    state.observers = [];
    
    return state;
}


function createClient(gameRef) {
    const game = gameRef;
    // server to connect
    let state = createClientState();

    let server;
    let receivedState;
    

    // state.id = 'c' + Math.floor(random(1000, 9999));

    function inputFromClient(command) {
        // debuga('client f:inputFromClient mandando input pro server', command);
        this.server.inputToServer(command);
    }

    // só pode ser chamado após setupClient
    function createServerConnection(serverToConnect, clientInstance) {
        // debuga('client state',state);
        this.server = serverToConnect;
        // print('this.server', this.server);
        serverToConnect.receiveConnection({ 
            instance: clientInstance, 
            id: state.id
        });
        return serverToConnect;
    }

    function getUpdatedState() {
        // return this.server.game.state;
        // debuga('client -> retornando receivedState',receivedState);
        return receivedState;
        // return game.state;
    }

    function receiveQuadState(command) {
        // ... implementar, alguém vai receber o estado
        // this.drawer.gameState = command.game.state;
        // debuga('command recebido',command);
        receivedState = command.state;
        // debuga('esse é o receivedState agr',receivedState);

    }

    function getClientCell() {
        let clientCell = getUpdatedState().cells[state.id];
        return clientCell;
    }

    // because can only connect to server when creation of this object is complete
    function setup(command) {
        // debugm('setup de client, recebido command', command);
        // this.createServerConnection(command.server);
        // debugm('subscribe em inputFromClient', inputFromClient);
        command.inputListener.subscribe(inputFromClient);
        createServerConnection(game.server, command.client);
    }

    function getClientId() {
        return state.id;
    }

    return {
        drawer,
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

