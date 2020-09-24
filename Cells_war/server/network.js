function createServerNetwork() {
    let clients = [];
    let game;

    function receiveConnection(client) {
        clients.push(client);

        // criar player
        let command = {};
        command.cellId = client.id;
        this.game.createCell(command);
        debugm(`client ${client.name} connected to the server`);
        // debugm(client);
        return this;
    }

    function sendQuadState() {
        // debugm(`about to send quadStates to ${clients.length} clients`);
        for(let i=0; i<clients.length; i++) {
            // debugm(`calling client ${clients[i].name}`);
            clients[i].instance.receiveQuadState({game:this.game});
        }
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
        setup
    };

}