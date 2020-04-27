package cookiegame.handlers;
import java.util.Date;
// import cookieclickersim.Game;

import common.Debug;
import cookiegame.Building;
import cookiegame.Game;

public class TimeHandler {
    private long time; // in seconds
    private Date inicialTime;
    private long deadline; // in seconds
    private Game game;

    public TimeHandler(Game game, long daysLeft) {
        this.game = game;
        this.time = 0;
        this.inicialTime = new Date();
        this.deadline = this.dayToSeconds(daysLeft);

    }
    
    public void printTimeStatus() {
    	System.out.println("Inicial time: " + this.inicialTime.toString() + "\ndeadline:     " + this.toDate(this.deadline));
    }
    
    public boolean advanceTime(long seconds) {
    	long newTime = this.time + seconds;

    	if(newTime <= this.deadline) {
    		this.time = newTime;
    		return true;
    	}
    	else {
    		return false;
    	}
    }
    
    public long timeToBuy(Building b) {
    	long cookiesNeeded = b.getPrice() - this.game.bank.getCookiesInBank();
    	long timetowait = (long) Math.ceil((float)cookiesNeeded / (float)this.game.buildings.getTotalCpS());

    	return timetowait;
    }
    
    public long getRemainingSeconds() {
    	return this.deadline - this.time;
    }
    
    public boolean canWaitToBuy(Building b) {
    	return this.timeToBuy(b) < this.getRemainingSeconds();
    }

    private long dayToSeconds(long days) {
        return days * 3600;
    }
    
    private String toDate(long seconds) {
    	return new Date(this.inicialTime.getTime() + (seconds * 1000)).toString();
    }
}