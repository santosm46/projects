
// function abstractMovement(celula) {
//     const cell = celula;

//     function move(command) {
//         //...
//     }

//     return { move };
// }

// receive inpuct and update on the state of the game
function createActions() {
    // const cell = celula;

    function getFieldSize() {
        return {x:width, y:height};
    }

    // returns a new valid position
    function newPosition(cell, movement) {
        const field = getFieldSize();
        // debuga('actions.js field',field);
        const radius = cell.radius;

        let x = cell.x + movement.x;
        let y = cell.y + movement.y;

        x = x-radius < 0 ? radius : x;
        x = x+radius > field.x ? field.x - radius : x;

        y = y-radius < 0 ? radius : y;
        y = y+radius > field.y ? field.y - radius : y;

        return {x, y};
    }

    // the inputs are a vector to move or some key
    const acceptedInputs = {
        move: function (command) {
            // if(command.key != 'w') return;
            const movement = createVector(command.movement.x, command.movement.y);
            movement.limit(3);
            const cell = game.state.cells[command.cellId];
            const newPos = newPosition(cell, movement);
            cell.x = newPos.x;
            cell.y = newPos.y;
            // debugm('moving...');
        },
        shoot: function(command) {
            const movement = createVector(command.movement.x, command.movement.y);
            const cell = game.state.cells[command.cellId];
            movement.setMag();
        }
        // down: function (cell) {
        //     debugm('moving down');
        // },
        // left: function (cell) {
        //     debugm('moving left');
        // },
        // right: function (cell) {
        //     debugm('moving right');
        // },
    };

    function reactToInput(command) {
        const inputType = command.inputType;
        // debugm(`update de ${command.cellId} com ${inputType}`);
        // debugm(acceptedInputs);
        const inputAction = acceptedInputs[inputType];
        if (inputAction) {
            inputAction(command);
        }
    }

    return {
        reactToInput
    };
}