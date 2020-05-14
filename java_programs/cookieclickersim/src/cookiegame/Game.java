package cookiegame;

import common.Debug;
import common.ShortNum;
import cookiegame.handlers.*;
import decider.*;
import decider.choice.*;

public class Game {
	public TimeHandler time;
    public BankHandler bank;
    public BuildingHandler buildings;
    
    private Decider decider;
    private Choice choice;

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
    		this.choice = decider.decide();
    		
    		if(choice instanceof Buy) {
    			if(!this.bank.buyBuilding(((Buy) choice).getChosen())) {
    				break;
    			}
    		} else if(choice instanceof Wait) {
    			if(!this.waitTime(((Wait) choice).getWaitingTime())) {
    				// wait the remaining time
    				this.waitTime(this.time.getRemainingSeconds());
    				break;
    			}
    		} else if(choice instanceof Exit) {
    			((Exit) this.choice).printExitMessage();
    			break;
    		} else {
    			System.out.println("Unknown class type of choice: " + this.choice.getClass());
    			break;
    		}
    	}
    }

    public boolean waitTime(long seconds) {
    	if(this.time.advanceTime(seconds)) {
    		this.bank.changeCookiesInBankBy(seconds * this.buildings.getTotalCpS());
    		return true;
    	}
    	else {
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


//
