package cookieClickerSim;
import java.util.ArrayList;
import java.util.List;

public class Game {
    private double cookiesInBank = 0.0;
    private double cookiesBaked = 0.0;
    private List<Building> allBuildings = new ArrayList<Building>();
    public List<Building> buildings = new ArrayList<Building>();

    public Game(double initialCookiesInBank) {
        this.instantiateBuildings();
        this.changeCookiesInBankBy(initialCookiesInBank);
    }

    public double getCookiesInBank() {
        return this.cookiesInBank;
    }

    public void printBuildings() {
        System.out.println("\n\n---- " + this.getCookiesInBank() +"$ ----------------------------");
        System.out.println("Disponiveis");
        for(Building i : this.buildings) {
            System.out.println(i.getInfo());
        }

        System.out.println("\nTravados");
        for(Building i : this.allBuildings) {
            if(i.isLocked()) {
                System.out.println(i.getInfo());
            }
        }
    }

    private void unlockBuildings() {
        for(Building i : this.allBuildings) {
            if(i.unlock()) { // if unlock then add to buildings array
                buildings.add(i);
            }
        }
    }

    private void increaseCookiesBakedBy(double change) {
        this.cookiesBaked += change;
        this.unlockBuildings();
    }

    public boolean changeCookiesInBankBy(double change) {
        if((this.cookiesInBank + change) < 0) {
            return false;
        }
        if(change > 0) {
            this.increaseCookiesBakedBy(change);
        }
        this.cookiesInBank += change;
        return true;
    }

    public double getCookiesBaked() {
        return this.cookiesBaked;
    }

    private void instantiateBuildings() {
        this.allBuildings.add(new Building("grandma",this, 10.0, 1));
        this.allBuildings.add(new Building("mine",this, 500.0, 1));
        this.allBuildings.add(new Building("mouse",this, 1700.0, 1));
    }
}
