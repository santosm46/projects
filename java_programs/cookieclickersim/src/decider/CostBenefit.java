package decider;

import java.util.ArrayList;
import java.util.Comparator;

import cookiegame.Building;
import cookiegame.Game;

public class CostBenefit extends Decider {
	public final static String methodType = "CostBenefit";
	private ArrayList<Building> buildings;
	
	public CostBenefit(Game game) {
		super(game, CostBenefit.methodType);
	}
	
	@SuppressWarnings("unchecked")
	public Building whatToBuy() {
		if(this.game.succeededBuying) {
			buildings = (ArrayList<Building>) this.game.buildings.GetBuildings().clone();
			buildings.sort(Comparator.comparingLong(Building::getCostBenefit));
		}
		else {
			if(buildings.size() <= 1) {
				return null;
			}
			buildings.remove(0);
		}
		
		return buildings.get(0);
	}
}
