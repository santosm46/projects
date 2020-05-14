package cookiegame.handlers;

import cookiegame.Building;
import cookiegame.Game;

public class BankHandler {
	private Game game;
	private long cookiesInBank = 0;
    private long cookiesBaked = 0;
	
	public BankHandler(Game game) {
		this.game = game;
	}
	
	public long getCookiesInBank() {
        return this.cookiesInBank;
    }
	
	public long getCookiesBaked() {
        return this.cookiesBaked;
    }
	
	public boolean changeCookiesInBankBy(long change) {
        if((this.cookiesInBank + change) < 0) {
            return false;
        }
        if(change > 0) {
//        	Debug.out("produced " + change + " cookies"); //
            this.increaseCookiesBakedBy(change);
        }
        this.cookiesInBank += change;
        return true;
    }
	
	public boolean buyBuilding(Building building) {
        // returns True if it bought, and False otherwise
        if(!this.canBuy(building)) { // checks if has enough money
            return false;
        }
        if(building.isLocked()) {
            return false;
        }
        
        this.changeCookiesInBankBy(-building.getPrice());
        building.changeAmountBy(1);
        
        return true;
    }
    
    public boolean sellBuilding(Building building) {
        // returns True if it bought, and False otherwise
        if(building.getAmount() < 1) { // checks if has buildings
            return false;
        }
        if(building.isLocked()) {
            return false;
        }
        
        this.changeCookiesInBankBy((long)(building.getPrice() / 4.6));
        building.changeAmountBy(-1);
        
        return true;
    }
	
	public boolean canBuy(Building b) {
		return this.getCookiesInBank() >= b.getPrice();
	}
	
	private void increaseCookiesBakedBy(long change) {
        this.cookiesBaked += change;
        this.game.buildings.unlockBuildings();
    }
	
}
