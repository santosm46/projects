package decider.choice;

public class Exit implements Choice {
	private String exitMessage;
	
	public Exit(String exitMessage) {
		this.exitMessage = exitMessage;
	}

	public String getExitMessage() {
		return this.exitMessage;
	}
	
	public void printExitMessage() {
		System.out.println(this.exitMessage);
	}
}