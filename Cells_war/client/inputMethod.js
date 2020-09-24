// function abstractInput(cell) {
//     return () => { };
// }


function keyAndMouse() {

    const nicknamesTable = {
        w: 'move',
    };

    // function will be triggered by input
    function createInput(client) {
        // if(key != 'w') {return null};
        
        let command = {};
        let updatedState = client.getUpdatedState();
        // debugm('client.state.id', client.state.id);
        let cell = updatedState.cells[client.state.id];

        // debugm('valor de cell', cell);

        let vel = {
            x: mouseX - cell.x,
            y: mouseY - cell.y
        };
        command.inputType = nicknamesTable[key];
        command.movement = vel;
        command.key = key;
        command.cellId = client.state.id;

        // debugm(`KeyAndMouse -> foi pressionado ${command.key}`);

        return command;

    }

    return {createInput};
}


function randomMovement(cell) {
    let mover = {};

    mover.cell = cell;
    mover.vel = 2;


    mover.move = function () {
        this.cell.x += random(-this.vel, this.vel);
        this.cell.y += random(-this.vel, this.vel);
    };

    return mover;
}

