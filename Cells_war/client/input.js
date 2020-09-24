function createInputListener(inputMethod) {
    const state = {
        observers: []
    }

    let client;

    const input = inputMethod();

    function onNewInput() {
        const command = input.createInput(this.client);

        notifyAll(command);
    };

    

    function subscribe(observerFunction) {
        state.observers.push(observerFunction);
    }

    function notifyAll(command) {
        // debugm(`notificando ${state.observers.length} observers`);
        for (let observerFunction of state.observers) {
            observerFunction(command);
        }
    }

    function setClient(client) {
        this.client = client;
    }

    // input.onNewInput = function() {
    //     //...
    //     // const keyPressed = this.nicknamesTable[event.key];
        
    // }

    return {
        subscribe,
        onNewInput,
        setClient
    };
}



