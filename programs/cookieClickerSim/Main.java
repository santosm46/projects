package cookieClickerSim;

public class Main {
    public static void main(String[] args) {
        Game game = new Game(1000.0);

        game.printBuildings();
        game.buildings.get(1).buyBuilding();
        game.printBuildings();

    }
}
