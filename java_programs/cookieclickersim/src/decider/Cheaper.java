package decider;
import java.util.ArrayList;

import cookiegame.Building;
import cookiegame.Game;

public class Cheaper extends Decider {
	public final static String methodType = "Cheaper";
	
	public Cheaper(Game game) {
		super(game, Cheaper.methodType);
	}

	public Building whatToBuy() {
		
		return (this.game.succeededBuying ? this.findCheapest() : null);
		
	}
	
	private Building findCheapest() {
		ArrayList<Building> buildings = this.game.buildings.GetBuildings();
		
		this.chosen = buildings.get(0);
		
		for(Building i : buildings) {
			if(i.getPrice() < this.chosen.getPrice()) {
				this.chosen = i;
			}
		}
		return this.chosen;
	}
}
