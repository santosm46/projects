package decider;

import java.util.ArrayList;
import java.util.Comparator;

import cookiegame.Building;
import cookiegame.Game;
import decider.choice.*;

public class CostBenefit extends Decider {
	public final static String methodType = "CostBenefit";
	
	public CostBenefit(Game game) {
		super(game, CostBenefit.methodType);
	}
	
	public Choice decide() {
		@SuppressWarnings("unchecked")
		ArrayList<Building> buildings = (ArrayList<Building>) this.game.buildings.GetBuildings().clone();
		buildings.sort(Comparator.comparingLong(Building::getCostBenefit));
		
		while(true) {
			if(buildings.size() == 0) {
				return new Exit("");
			}
			
			this.chosen = buildings.get(0);
			
			if(this.game.bank.canBuy(this.chosen)) {
				return new Buy(this.chosen);
			}
			else if(this.game.time.canWaitToBuy(this.chosen)){
				timetobuy = this.game.time.timeToBuy(this.chosen);
				return new Wait(timetobuy);
			} else {
				buildings.remove(0);
			}
		}
	}
}
