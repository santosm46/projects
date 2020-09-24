
function createCellHandler() {
    let state;
    let game;

    function createCell(command) {//chunks, movement) {
        let cell = {};

        const cellId = command.cellId || 'r' + Math.floor(random(10, 99)); //command.cellId
        const x = command.x || Math.floor(random(width));
        const y = command.y || Math.floor(random(height));
        const raio = command.raio || Math.floor(random(10, 60));

        // attributes
        cell.id = cellId;
        cell.x = x;
        cell.y = y;
        cell.raio = raio;
        cell.cor = command.cor || {
            r: Math.floor(random(255)),
            g: Math.floor(random(255)),
            b: Math.floor(random(255))
        };
        // debugm(command.game);
        // command.game.state.cells[cellId] = cell;
        return cell;

    }

    function removeCell(command) {
        const cellId = command.cellId;
        delete game.state.cells[cellId];
    }

    function createCells(command) {//numCells, chunks, movement) {
        for (let i = 0; i < command.numCells; i++) {
            createCell(command);
        }
    }

    function getChunkPos(cell) {
        return {
            x: Math.floor(cell.x / cell.chunks.size),
            y: Math.floor(cell.y / cell.chunks.size)
        };
    }

    function inSight(cell, other) {

        let posT = cell.getChunkPos();
        let tX = posT.x;
        let tY = posT.y;
        let posO = other.getChunkPos();
        let oX = posO.x;
        let oY = posO.y;
        let inside =
            tX >= oX - 1 &&
            tX <= oX + 1 &&
            tY >= oY - 1 &&
            tY <= oY + 1;

        return inside;
    }

    function setup(game) {
        // debugm('setado cellHandler.game');
        // debugm(game);
        this.game = game;
    }

    return {
        createCell,
        removeCell,
        createCells,
        getChunkPos,
        inSight,
        draw,
        state,
        setup
    };
}