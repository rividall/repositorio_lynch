/*
Mapping category mean prices and rating to x and y coordinates on the poster
*/
Table table;
TableRow row;

int maxMoney = 425;
int minMoney = 93;
float maxRat = 4.52;
float minRat = 3.87;
float hval = 0; // color
float xCoord, yCoord;
color col1;
int offSet = 60;

void setup() {
  size(800, 800);
  colorMode(HSB, 360, 100, 100);
  // heads- newCat  avgPRice avgRat
  table = loadTable("amazon_avg_rating-price.csv", "header");
}

void draw() {
  background(360);
  for (int i=0; i < table.getRowCount(); i++) {
    row = table.getRow(i);
    hval = row.getInt("newCat")*20;  // set color based on csv
    xCoord = map(row.getFloat("avgPrice"), minMoney, maxMoney, 1, 6);
    yCoord = map(row.getFloat("avgRat"), minRat, maxRat, int(1), int(3));
    col1 = color(hval, 100, 90);
    fill(col1);
    noStroke();
    circle(xCoord*100, yCoord*100, 20);
    println("Created ellipse number " + row.getInt("newCat") + ", in coords x: " + xCoord + " and y: " + yCoord);
  }
  noLoop();
}
