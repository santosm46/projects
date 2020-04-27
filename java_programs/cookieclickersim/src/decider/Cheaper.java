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
		ArrayList<Building> buildings = this.game.buildings.GetBuildings();
		if(buildings.size() == 0) {
			return new Exit("These isn't buildings");
		}
		this.chosen = buildings.get(0);
		for(Building i : buildings) {
			if(i.getPrice() < this.chosen.getPrice()) {
				this.chosen = i;
			}
		}
		
		if(this.game.bank.canBuy(this.chosen)) {
			return new Buy(this.chosen);
		}
		else {
			timetobuy = this.game.time.timeToBuy(this.chosen);
			return new Wait(timetobuy);
		}
		
	}
}
