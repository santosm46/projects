

const training_data_o = [
    {
        inputs: [0, 0],
        targets: [0]
    },
    {
        inputs: [0, 1],
        targets: [1]
    },
    {
        inputs: [1, 0],
        targets: [1]
    },
    {
        inputs: [1, 1],
        targets: [0]
    },

    {
        inputs: [0.1, 0.1],
        targets: [0]
    },
    {
        inputs: [0.1, 0.9],
        targets: [1]
    },
    {
        inputs: [0.9, 0.1],
        targets: [1]
    },
    {
        inputs: [0.9, 0.9],
        targets: [0]
    },

    {
        inputs: [0.4, 0.4],
        targets: [0]
    },
    {
        inputs: [0.4, 0.6],
        targets: [1]
    },
    {
        inputs: [0.6, 0.4],
        targets: [1]
    },
    {
        inputs: [0.6, 0.6],
        targets: [0]
    },


    {
        inputs: [0.4, 0.4],
        targets: [0]
    },
    {
        inputs: [0.4, 0.6],
        targets: [1]
    },
    {
        inputs: [0.6, 0.4],
        targets: [1]
    },
    {
        inputs: [0.6, 0.6],
        targets: [0]
    },
];

const training_data = [];




let rows, cols, res, nn;


function setup() {
    createCanvas(400, 400);

    for(let i=0; i<1000; i++) {
        let x = random(-1, 1);
        let y = random(-1, 1);
    
        let nx = x > 0.5 ? 1 : 0;
        let ny = y > 0.5 ? 1 : 0;
    
        let target = nx !== ny;
    
        training_data.push(
            {
                inputs: [x, y],
                targets: [target]
            }
        );
    }

    nn = new NeuralNetwork(2, [8], 1);
    
    res = 10;
    rows = Math.floor(width / res);
    cols = Math.floor(height / res);
    noStroke();

    nn.learning_rate = 0.05;

}

function draw() {
    background(255,0,0);
    
    for(let i=0; i<100000; i++) {
        let data = random(training_data);
        nn.train(data.inputs, data.targets);
    }

    for(let i=0; i<rows; i++) {
        for(let j=0; j<cols; j++) {
            let x1 = i / rows;
            let x2 = j / cols;
            let color = nn.feedForward([x1, x2]).output[0];
            fill((1-color) * 255, color * 255, 0);
            rect(res*i, res*j, res, res);
        }
    }

}



