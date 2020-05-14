package decider;

import java.util.ArrayList;
import java.util.Comparator;

import common.Debug;
import cookiegame.Building;
import cookiegame.Game;
import decider.choice.*;

public class BuySellCB extends Decider {
	public final static String methodType = "BuySellCB";
	
	public BuySellCB(Game game) {
		super(game, CostBenefit.methodType);
	}
	
	public Choice decide() {
		@SuppressWarnings("unchecked")
		ArrayList<Building> gameBuildings = (ArrayList<Building>) this.game.buildings.GetBuildings();
		ArrayList<Building> buildings = new ArrayList<Building>();
		buildings.sort(Comparator.comparingLong(Building::getCostBenefit));
		
//		int[] b = new int[n]; 
//        int j = n; 
//        for (int i = 0; i < n; i++) { 
//            b[j - 1] = a[i]; 
//            j = j - 1; 
//        } 
		
		while(true) {
			if(buildings.size() == 0) {
				return new Exit("");
			}
			
			this.chosen = buildings.get(0);
			
			if(this.game.bank.canBuy(this.chosen)) {
				return new Buy(this.chosen);
			}
			else if(this.game.time.canWaitToBuy(this.chosen)){
//				Debug.out("> size: " + buildings.size());
				if(buildings.size() > 1) {
					for(int aux = buildings.size()-1; aux > 1; aux--) {
//						Debug.out("    > aux: " + aux);
						if(buildings.get(aux).sellBuilding()) {
							break;
						}
					}
				}
				
				timetobuy = this.game.time.timeToBuy(this.chosen);
				return new Wait(timetobuy);
			} else {
				buildings.remove(0);
			}
		}
	}
}
