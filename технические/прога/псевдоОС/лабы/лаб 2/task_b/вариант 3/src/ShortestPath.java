public class ShortestPath {
    int from;
    int vertex;
    int dist;
    ShortestPath(int from, int vertex, int dist) {
        this.from = from;
        this.vertex = vertex;
        this.dist = dist;
    }

    @Override
    public String toString() {
        return from + " " + vertex + " " + dist;
    }
}