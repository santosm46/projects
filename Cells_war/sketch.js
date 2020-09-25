let game; // para conexões. temporário

let client;
let drawer;
let inputListener;

// generic observers with no parameter to their function
let observers = [];

function setup() {
    createCanvas(1500, 1200); // width, height

    game = createGame(); // temporário 
    game.setup();
    client = createClient(game); // cliente faz conexão com servidor
    // debuga('client aaaaaa ' + (client == null), client);
    inputListener = createInputListener(keyAndMouse, client);

    client.setup({
        // server: game.server,
        client,
        inputListener
    });

    drawer = createDrawer();

    
    inputListener.setup();
}


function draw() {


    background(220);

    // if (keyIsPressed && keyIsDown(87)){
    // if (keyIsPressed){ 
    // // if (keyIsDown(87)) { 
    //     // w is pressed
    //     client.input.onNewInput();
    // }

    game.tickClock();

    drawer.drawGameState(client);

    // observers with use the clock of draw() to run function
    notifyAll({});

}


// inputListener will subscribe to run method to check for new inputs
function sketchSubscribe(observerFunction) {
    observers.push(observerFunction);
}

function notifyAll(command) {
    for(let observerFunction of observers) {
        observerFunction(command);
    }
}



// usefull functions

function debugm(msg, obg=null) {
    let msgf;
    print(msg);
    if(obg !== null) print(obg);
}

function debuga(msg, obg) {
    print(msg);
    print(obg);
}
