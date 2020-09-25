function createInputListener(inputMethodToUse, clientRef) {
    const observers = [];
    let client = clientRef;
    // client is created first  because inputListener needs to know who is the client

    const inputMethod = inputMethodToUse();

    // will be called by sketch draw notifyAll()
    function onNewInput(none) {
        if (client) {
            const command = inputMethod.readInput(client);
            if (command) {
                notifyAll(command);
            }
        } else {
            console.error(`client of inputListener is not set! Set the client with setClient`);
            throw "Undefined inputListener.client";
        }
    };

    function subscribe(observerFunction) {
        observers.push(observerFunction);
    }

    function notifyAll(command) {
        // debugm(`notificando ${state.observers.length} observers`);
        // debuga('observers ---->> ' + observers.length, observers);
        if (observers.length === 0) return;

        for (let observerFunction of observers) {
            observerFunction(command);
        }
    }

    function setClient(client) {
        this.client = client;
    }

    // can only be called after client is set
    function setup(command) {
        // this.setClient(command);
        sketchSubscribe(this.onNewInput);
    }

    // input.onNewInput = function() {
    //     //...
    //     // const keyPressed = this.nicknamesTable[event.key];

    // }

    return {
        subscribe,
        onNewInput,
        setClient,
        setup
    };
}



