/* Amazon Trendforest - Ricardo Vidal Lynch, Jose Claramonte
 
 Creating different trees through data from Amazon sold products.
 
 Clicking will load a new tree.
 'z' and 'x' keys allow to navigate through categories. 'p' key to save that frame.
 
 Branches are based on 'Cherry Blossom Tree' by Jponcemath on https://openprocessing.org/sketch/441998
 Leaves are based on 'growingTree' by unknown source on https://openprocessing.org/sketch/1589590
 
 */

import processing.pdf.*;

boolean UI = false; // set to true for navigation aid
boolean record;

// Global variables
ArrayList<Branch> branches = new ArrayList<Branch>();
ArrayList<Leaf> leaves = new ArrayList<Leaf>();
Table table;

int sel = 0; // SELECT DATA TO LOAD

int maxMoney = 1019403;
int minMoney = 9130;
int cats = 18;
int catColors = 360/cats;

float maxLevel = 10; // cantidad hojas
float ldiam = 16; // tamaño hojas
int hval = 20; // color
int sz = 100; // tamaño arbol

int treePX = 700;
int treePY = 1000;

PImage leaveImage;
color col1;
color col2;
color col3;
TableRow row;

void setup() {
  size(1400, 1100, P2D);
  table = loadTable("categoryValue.csv", "header");
  row = table.getRow(sel);
  hval = row.getInt("cat")*catColors;  // set color based on csv
  colorMode(HSB, 360, 100, 100);
  frameRate(3);
  callTrees();
  col1 = color(hval-9, 100, 41);
  col2 = color(hval-1, 100, 59);
  col3 = color(hval, 100, 72);
  leaveImage = createLeaveImage();
  callTrees();
}

void draw() {
  if (record) {
    beginRecord(PDF, "trees/arbol"+(sel+1)+".pdf");
  }
  if (UI)iface();
  for (int i = 0; i < branches.size(); i++) {
    Branch branch = branches.get(i);
    branch.display();
  }
  for (int i = leaves.size()-1; i > -1; i--) {
    Leaf leaf = leaves.get(i);
    leaf.display();
  }
  if (record) {
    endRecord();
    record = false;
    println("PRINTED");
  }
}

void callTrees() {
  background(360, 0, 100, 0);
  row = table.getRow(sel);
  hval = row.getInt("cat")*catColors;  // set color based on csv
  maxLevel = map(row.getInt("val"), minMoney, maxMoney, 5, 12);
  col1 = color(hval-9, 100, 41);
  col2 = color(hval-1, 100, 59);
  col3 = color(hval, 100, 72);
  leaveImage = createLeaveImage();
  generateNewTree(treePX, treePY);
}

void mousePressed() {
  callTrees();
  println(sel+1 + " " + maxLevel);
}

void iface() {
  fill((sel+1)*20, 100, 72);
  noStroke();
  rect(0, 0, 100, 100);
  fill(0, 0, 100);
  textSize(40);
  text(sel+1, 35, 55);
}
void keyPressed() {
  if (key == 'z') {
    if (sel>=1) {
      sel-=1;
      fill(20, 100, 100);
      noStroke();
      triangle(100, 50, 150, 0, 150, 100);
    }
  }
  if (key == 'x') {
    if (sel<=16) {
      sel+=1;
      fill(90, 100, 100);
      noStroke();
      triangle(150, 0, 150, 100, 200, 50);
    }
  }
  if (key == 'p') {
    record = true;
  }
}
