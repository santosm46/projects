
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

    // the inputs are a vector to move or some key
    const acceptedInputs = {
        move: function (command) {
            // if(command.key != 'w') return;

            const movement = command.movement;
            const cell = game.state.cells[cellId];
            const vel = createVector(movement.x, movement.y);
            vel.limit(3);
            cell.x += vel.x;
            cell.y += vel.y;
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