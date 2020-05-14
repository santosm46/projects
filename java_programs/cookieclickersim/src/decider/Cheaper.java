package decider;
import java.util.ArrayList;

import cookiegame.Building;
import cookiegame.Game;
import decider.choice.*;

public class Cheaper extends Decider {
	
	public final static String methodType = "Cheaper";
	
	public Cheaper(Game game) {
		super(game, Cheaper.methodType);
	}

	public Choice decide() {
		
		if(!this.game.buildings.hasBuildings()) {
			return new Exit("These isn't buildings");
		}
		
		this.findCheapest();
		
		if(this.game.bank.canBuy(this.chosen)) {
			return new Buy(this.chosen);
		}
		else {
			timetobuy = this.game.time.timeToBuy(this.chosen);
			return new Wait(timetobuy);
		}
		
	}
	
	private void findCheapest() {
		ArrayList<Building> buildings = this.game.buildings.GetBuildings();
		
		this.chosen = buildings.get(0);
		
		for(Building i : buildings) {
			if(i.getPrice() < this.chosen.getPrice()) {
				this.chosen = i;
			}
		}
	}
}
