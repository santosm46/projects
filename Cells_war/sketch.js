let client;
let game;

function setup() {
    createCanvas(1600, 900); // width, height

    game = createGame(); // temporário 
    game.setupGame(game);

    // createState();

    client = createClient(game); // cliente faz conexão com servidor
    client.setupClient(client);

    //player = createCell(chunks, playerMovement);
    // player = createCell(chunks, mouseMovement);
    // cells.push(player);

    // document.addEventListener('keydown', function(event){
    //     console.log(`pressionado ${event.code}`);
    //     client.input.onNewInput();
    // });
}

function debugm(msg, obg=null) {
    let msgf;
    print(msg);
    if(obg !== null) print(obg);
}

function debuga(msg, obg) {
    print(msg);
    print(obg);
}

function draw() {


    background(220);

    // if (keyIsPressed && keyIsDown(87)){
    if (keyIsPressed){ 
    // if (keyIsDown(87)) { 
        // w is pressed
        client.input.onNewInput();
    }

    game.tickClock();

    client.drawer.drawGameState(client);
    // debugm('antes de chamar drawRangeArea');
    // fill(0, 200, 50);
    // rect(mouseX, mouseY, 30, 30);
    client.drawer.drawRangeArea(client);
    client.drawer.drawCells(client);


    // player.vizinhos();

    // for (let i = 0; i < cells.length; i++) {
    //     cells[i].move();
    //     cells[i].draw(player);
    // }
    // chunks.drawGridChunks();


}
