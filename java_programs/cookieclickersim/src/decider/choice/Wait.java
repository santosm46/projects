package decider.choice;

public class Wait implements Choice {
	private long waitingTime;
	
	public Wait(long waitingTime) {
		this.waitingTime = waitingTime;
	}

	public long getWaitingTime() {
		return waitingTime;
	}
}