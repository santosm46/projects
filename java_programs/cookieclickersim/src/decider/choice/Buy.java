package decider.choice;

import cookiegame.Building;

public class Buy implements Choice {
	private Building chosen;
	
	public Buy(Building chosen) {
		this.chosen = chosen;
	}

	public Building getChosen() {
		return this.chosen;
	}
}
