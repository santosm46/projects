package cookiegame;

//import common.Debug;
import common.ShortNum;
import cookiegame.handlers.*;
import decider.*;

public class Game {
	public TimeHandler time;
    public BankHandler bank;
    public BuildingHandler buildings;
    public boolean succeededBuying = true;
    
    private Decider decider;
    private Building chosen;

    private Game(int hoursLeft) {
    	this.buildings = new BuildingHandler(this);
        this.time = new TimeHandler(this, hoursLeft);
        this.bank = new BankHandler(this);
    }
    
    public static Game newGame(long initialCookiesInBank, int hoursLeft, String deciderMethodName) {
    	Decider auxDecider;
    	Game game = new Game(hoursLeft);
    	
    	auxDecider = Decider.newDecider(game, deciderMethodName);
    	
    	if(auxDecider == null) {
        	System.out.println("Invalid Decider type: " + deciderMethodName);
        	return null;
        }
    	else {
    		game.setDeciderMethod(auxDecider);
    	}
    	
    	if(initialCookiesInBank < 100) {
    		System.out.println("Inicial cookies in bank too small. Set at least 100");
    		return null;
    	}
    	else {
    		game.bank.changeCookiesInBankBy(initialCookiesInBank);
    	}
    	
    	return game;
    }
    
    public String getMethodName() {
    	return this.decider.getMethodName();
    }
    
    private void setDeciderMethod(Decider decider) {
    	this.decider = decider;
    }
    
    public void loop() {
    	while(true) {
    		this.chosen = decider.whatToBuy();
    		
    		if(chosen == null) {
    			// if null is returned, it couldn't buy or wait to buy any building
    			// so just wait the remaining time
    			this.waitTime(this.time.getRemainingSeconds());
    			break;
    		}
    		
			if(!this.bank.canBuy(chosen)) {
				// if can't buy, then wait to get more money
				this.waitTime(this.time.timeToBuy(chosen));
			}
			
			this.succeededBuying = this.bank.buyBuilding(chosen);
    	}
    }

    public boolean waitTime(long seconds) {
    	if(this.time.advanceTime(seconds)) {
    		this.bank.changeCookiesInBankBy(seconds * this.buildings.getTotalCpS());
    		return true;
    	} else {
    		return false;
    	}
    }
    
    public void printStatus(boolean printBuildings) {
    	System.out.println("\n========== [" + this.decider.getMethodName() + " method] ==========");
    	System.out.println("Cookies baked: " + ShortNum.format(this.bank.getCookiesBaked()));
    	System.out.println("Cookies in bank: " + ShortNum.format(this.bank.getCookiesInBank()));
    	System.out.println("Production: " + ShortNum.format(this.buildings.getTotalCpS()) + " cps");
    	this.time.printTimeStatus();
    	if(printBuildings)
    		this.buildings.printBuildings();
    	System.out.println("\n\n\n");
    	
    }
}
