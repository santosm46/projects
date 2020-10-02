
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

        let x = cell.x + movement.x;
        let y = cell.y + movement.y;

        x = x-cell.raio < 0 ? cell.raio : x;
        x = x+cell.raio > field.x ? field.x - cell.raio : x;

        y = y-cell.raio < 0 ? cell.raio : y;
        y = y+cell.raio > field.y ? field.y - cell.raio : y;

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