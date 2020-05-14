package decider;

import cookiegame.Building;
import cookiegame.Game;
import decider.choice.Choice;

public abstract class Decider {
	protected Game game;
	protected Building chosen;
	protected long timetobuy;
	private String methodName = "Undefined";
	
	protected Decider(Game game, String methodName) {
		this.methodName = methodName;
		this.game = game;
	}
	
	public static Decider newDecider(Game game, String deciderMethodName) {
		if(deciderMethodName.equals(Cheaper.methodType)) {
			return new Cheaper(game);
		}
		else if(deciderMethodName.equals(CostBenefit.methodType)) {
			return new CostBenefit(game);
		}
		else if(deciderMethodName.equals(BuySellCB.methodType)) {
			return new BuySellCB(game);
		}
		else {
			System.out.println("Unknown decider method name: " + deciderMethodName);
			return null;
		}
	}
	
	public String getMethodName() {
		return this.methodName;
	}
	
	public abstract Choice decide();
}
