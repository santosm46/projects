package cookiegame;
// import cookieclickersim.Game;

import common.ShortNum;

public class Building {
    private Game game = null;
    private int amount = 0;
    private boolean locked = true; //unlocks when cookies baked reaches the building price
    private long initialPrice;
    private long initialCpS;
    private String name;

    private final double PRICE_INCREASE_RATE = 1.15;

    public Building(String name, Game game, long initialPrice, long initialCpS) {
        this.name = name;
        this.game = game;
        this.initialPrice = initialPrice;
        this.initialCpS = initialCpS;
    }

    public String getName() {
        return this.name;
    }

    public long getPrice() {
        return (long) (this.initialPrice) * (long) (Math.pow(this.PRICE_INCREASE_RATE, this.getAmount()));
    }

    public boolean isLocked() {
        return this.locked;
    }

    public boolean unlock() {
        if(this.game.bank.getCookiesBaked() >= this.getPrice() && this.isLocked()) {
            this.locked = false;
            return true;
        }
        return false;
    }

    public int getAmount() {
        return this.amount;
    }
    
    public long getCostBenefit() {
    	return this.getPrice() / (this.initialCpS);
    }

    public long getCpS() {
        return this.initialCpS * (long)(this.getAmount());
    }

    public boolean changeAmountBy(int increase) {
        if(this.amount + increase >= 0) {
            this.amount += increase;
            // this.price *= this.PRICE_INCREASE_RATE;
            return true;
        }
        else {
            return false;
        }
    }

    public String getInfo() {
        return  "Name: " + this.getName() + 
        		" | price: " + ShortNum.format(this.getPrice()) + 
        		" | CpS: " + ShortNum.format(this.initialCpS) + 
//        		" | CB: " + this.getRelativeCB() + 
        		" | amount: " + this.getAmount();
    }
}