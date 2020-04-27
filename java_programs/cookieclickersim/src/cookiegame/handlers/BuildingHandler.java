package cookiegame.handlers;

import java.util.ArrayList;

import cookiegame.Building;
import cookiegame.Game;

public class BuildingHandler {
	private Game game;
	private ArrayList<Building> allBuildings = new ArrayList<Building>();
    private ArrayList<Building> unlockedBuildings = new ArrayList<Building>();
	
	public BuildingHandler(Game game) {
		this.game = game;
		this.instantiateBuildings();
	}
	
	public ArrayList<Building> GetBuildings() {
    	return this.unlockedBuildings;
    }
	
	public void unlockBuildings() {
        for(Building i : this.allBuildings) {
            if(i.unlock()) { // if unlock successfully then add to unlockedBuildings array
                unlockedBuildings.add(i);
            }
        }
    }
	
	public long getTotalCpS() {
		long totalCpS = 0;
		for(Building i : this.unlockedBuildings) {
            totalCpS += i.getCpS();
        }
		return totalCpS;
	}
	
	private void instantiateBuildings() {
        this.allBuildings.add(new Building("Grandma",this.game, 		100L, 1L));
        this.allBuildings.add(new Building("Farm",this.game, 			1100L, 8L));
        this.allBuildings.add(new Building("Mine",this.game, 			12000L, 47L));
        this.allBuildings.add(new Building("Factory",this.game, 		130000L, 260L));
        this.allBuildings.add(new Building("Bank",this.game, 			1400000L, 1400L));
        this.allBuildings.add(new Building("Temple",this.game, 			20000000L, 7800L));
        this.allBuildings.add(new Building("Wizard tower",this.game, 	330000000L, 44000L));
        this.allBuildings.add(new Building("Shipment",this.game, 		5100000000L, 260000L));
        this.allBuildings.add(new Building("Alchemy lab",this.game, 	75000000000L, 1600000L));
        this.allBuildings.add(new Building("Portal",this.game, 			1000000000000L, 10000000L));
        this.allBuildings.add(new Building("Time machine",this.game, 	14000000000000L, 65000000L));
        this.allBuildings.add(new Building("Antimatter",this.game, 		170000000000000L, 430000000L));
        
    }
	
	public void printBuildings() {
        System.out.println("\n===== Buildings =====");
        for(Building i : this.unlockedBuildings) {
            System.out.println(i.getInfo());
        }
    }
}
