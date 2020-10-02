// function abstractInput(cell) {
//     return () => { };
// }

const nicknamesTable = {
    w: 'move',
};

function keyAndMouseIM() {

    // function will be triggered by input
    function readInput(client) {
        if(nicknamesTable[key] != 'move') {return null};
        if(keyIsPressed === false) {return null};

        let command = {};
        let updatedState = client.getUpdatedState();
        // debugm('client.state.id', client.state.id);
        let cell = updatedState.cells[client.getClientId()];

        // debugm('valor de cell', cell);

        let vel = {
            x: mouseX - cell.x,
            y: mouseY - cell.y
        };
        command.inputType = nicknamesTable[key];
        command.movement = vel;
        command.key = key;
        // debuga('mandando id cliente', client..getClientId());
        command.cellId = client.getClientId();

        // debugm(`KeyAndMouse -> foi pressionado ${command.key}`);

        return command;

    }

    return {readInput};
}


function randomIM() {

    function readInput(client) {
        let command = {};
        let updatedState = client.getUpdatedState();
        // debugm('client.state.id', client.state.id);

        // debugm('valor de cell', cell);
        const maxVel = 5;

        const rx = random(-maxVel, maxVel);
        const ry = random(-maxVel, maxVel);

        let vel = {
            x: rx,
            y: ry
        };
        command.inputType = nicknamesTable['w'];
        command.movement = vel;
        command.key = key;
        // debuga('mandando id cliente', client..getClientId());
        command.cellId = client.getClientId();

        return command;
    }

    return {readInput};
}

