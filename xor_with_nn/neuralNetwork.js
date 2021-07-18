
function sigmoid(x) {
    return 1 / (1 + Math.exp(-x));
}

function dsigmoid(y) {
    // y já passou por sigmoid
    return y * (1 - y);
}


class NeuralNetwork {
    constructor(numInputs, numHidden, numOutputs) {
        this.input_nodes = numInputs;
        this.hidden_nodes = numHidden;
        this.output_nodes = numOutputs;

        this.weights = [];
        this.bias = [];
        this.weights.push(new Matrix(this.hidden_nodes[0], this.input_nodes, true));
        this.bias.push(new Matrix(this.hidden_nodes[0], 1, true));
        
        for(let i=1; i<this.hidden_nodes.length; i++) {
            let rows = this.hidden_nodes[i];
            let cols = this.hidden_nodes[i-1];
            this.weights.push(new Matrix(rows, cols, true));

            let rows_b = this.hidden_nodes[i];
            this.bias.push(new Matrix(rows_b, 1, true));
        }
        let cols_ho = this.hidden_nodes[this.hidden_nodes.length-1];
        this.weights.push(new Matrix(this.output_nodes, cols_ho, true));
        this.bias.push(new Matrix(this.output_nodes, 1, true));

        this.activate = sigmoid;
        this.learning_rate = 0.2;
    }


    feedForward(inputs) {
        // H = W * I + B
        if(! (inputs instanceof Matrix)) {
            inputs = Matrix.fromArray(inputs);
        }

        let results = [];

        let hidden;
        for(let i=0; i<this.weights.length; i++) {
            hidden = Matrix.multiply(this.weights[i], inputs);
            hidden.add(this.bias[i]);
            hidden.map(this.activate);
            results.push(hidden);
            inputs = hidden;
        }

        return {
            output: hidden.toArray(),
            results: results,
            hidden: hidden
        };
    }

    train(inputs, targets) {
        inputs = Matrix.fromArray(inputs);
        targets = Matrix.fromArray(targets);

        let results = this.feedForward(inputs).results;
        let errors;

        for(let i=this.weights.length-1; i>=0; i--) {
            if(i === this.weights.length-1) {
                errors = Matrix.subtract(targets, results[i]);
            }
            else {
                let weights_t = Matrix.transpose(this.weights[i+1]);
                errors = Matrix.multiply(weights_t, errors);
            }

            // (O *(1 - O))
            let gradients = Matrix.map(results[i], dsigmoid);
            gradients.elementWise(errors);
            gradients.multiply(this.learning_rate);

            let hidden_t;
            if(i===0) {
                hidden_t = Matrix.transpose(inputs);
            }
            else {
                hidden_t = Matrix.transpose(results[i-1]);
            }

            let deltas = Matrix.multiply(gradients, hidden_t);
            // twicks
            this.weights[i].add(deltas);
            this.bias[i].add(gradients);
        }
    }
}


//      Eo = targets - O
// Wh² deltas = lr * Eo * (O *(1 - O)) . t(H²)

//      Eh² = t(Wh²) . Eo
// Wh¹ deltas = lr * Eh² * (H² *(1 - H²)) . t(H¹)

//      Eh¹ = t(Wh¹) . Eh²
// Wih deltas = lr * Eh¹ * (H¹ *(1 - H¹)) . t(I)

