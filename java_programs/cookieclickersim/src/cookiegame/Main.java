package cookiegame;

import decider.*;

public class Main {
	static int hours = 24 * 20;
	static int cookiesInBank = 200;
	
    public static void main(String[] args) {
        Game game1 = Game.newGame(cookiesInBank, hours, Cheaper.methodType);
        Game game2 = Game.newGame(cookiesInBank, hours, CostBenefit.methodType);
        
        if(game1 == null || game2 == null) {
        	System.out.println("Error: game is null");
        	return;
        }

        game1.loop();
        game2.loop();
        
        game1.printStatus();
        game2.printStatus();

    }
}
