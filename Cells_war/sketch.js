let game; // para conexões. temporário

let client;
let drawer;
let inputListener;
// let randomInput;
const numClientesBot = 2;
const botClients = {};

// generic observers with no parameter to their function
let observers = [];

function setup() {
    createCanvas(1500, 1000); // width, height

    game = createGame(); // temporário 
    game.setup();
    client = createClient(game); // cliente faz conexão com servidor
    // debuga('client aaaaaa ' + (client == null), client);
    inputListener = createInputListener(keyAndMouseIM, client);

    client.setup({
        // server: game.server,
        client,
        inputListener
    });

    drawer = createDrawer();

    
    inputListener.setup();

    for(let i = 0; i<numClientesBot; i++) {
        const c = createClient(game); // cliente faz conexão com servidor
        const randomInput = createInputListener(randomIM, c);
        randomInput.setup();

        // randomInput.setClient(c);
        c.setup({inputListener:randomInput});

        botClients[i] = {c, randomInput};
    }
    
    
    
    
    
    
    
    // drawer = createDrawer();
}


function draw() {

    background(220);

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
    // return;
    let msgf;
    print(msg);
    if(obg !== null) print(obg);
}

function debuga(msg, obg) {
    // return;
    print(msg);
    print(obg);
}

function debugNull(value, message) {
    if(value == null) {
        console.error(message);
    }
}

