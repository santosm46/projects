package cookiegame;

import decider.*;

public class Main {
	static int hours = 24 * 30 * 3;
	static int cookiesInBank = 200;
	
    public static void main(String[] args) {

    	Game[] games = {
    		Game.newGame(cookiesInBank, hours, Cheaper.methodType),
    		Game.newGame(cookiesInBank, hours, CostBenefit.methodType)
    	};
    	
    	for (Game game : games) {
	        if(game == null) {
	        	System.out.println("Error: game is null");
	        	continue;
	        }
	        
	        game.loop();
	        game.printStatus(false);
	        
    	}
    }
}
