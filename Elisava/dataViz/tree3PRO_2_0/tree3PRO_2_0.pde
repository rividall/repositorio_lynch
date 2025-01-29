// Global variables
ArrayList<Branch> branches = new ArrayList<Branch>();
ArrayList<Leaf> leaves = new ArrayList<Leaf>();
Table table;

int sel = 12; // SELECT DATA TO LOAD

int maxMoney = 1019403;
int minMoney = 9130;
int cats = 18;
int catColors = 360/cats;

float maxLevel = 6.9; // cantidad hojas
int ldiam = 30; // tamaño hojas
int hval = 20; // color
int sz = 100; // tamaño arbol

int treePX = 600;
int treePY = 1000;

PImage leaveImage;
color col1;
color col2;
color col3;

void setup() {
  size(1200, 1000, P2D);
  table = loadTable("categoryValue.csv", "header");
  TableRow row = table.getRow(sel);
  hval = row.getInt("cat")*catColors;  // set color based on csv
  maxLevel = map(row.getInt("val"), minMoney, maxMoney, 6, 10);
  println(hval + " " + maxLevel);
  colorMode(HSB, 360, 100, 100);
  frameRate(5);
  callTrees();
  col1 = color(hval-9, 100, 41);
  col2 = color(hval-1, 100, 59);
  col3 = color(hval, 100, 72);
  leaveImage = createLeaveImage();
}

void draw() {
  background(360);
  fill(col3);
  noStroke();
  rect(0,0,100,100);


  for (int i = 0; i < branches.size(); i++) {
    Branch branch = branches.get(i);
    branch.display();
  }
  for (int i = leaves.size()-1; i > -1; i--) {
    Leaf leaf = leaves.get(i);
    leaf.display();
  }
}

void callTrees() {
  col1 = color(hval-9, 100, 41);
  col2 = color(hval-1, 100, 59);
  col3 = color(hval, 100, 72);
  leaveImage = createLeaveImage();
  generateNewTree(treePX, treePY);
}

void generateNewTree(int newBranchPosX, int newBranchPosY) {
  branches.clear();
  leaves.clear();
  branches.add(new Branch(newBranchPosX, newBranchPosY, newBranchPosX, newBranchPosY-sz, 0, null));

  subDivide(branches.get(0));
}

void subDivide(Branch branch) {
  ArrayList<Branch> newBranches = new ArrayList<Branch>();

  int newBranchCount = (int)random(1, 4);

  float minLength = 1.1;
  float maxLength = 1.2;

  switch(newBranchCount) {
  case 2:
    newBranches.add(branch.newBranch(random(-35.0, -10.0), random(minLength, maxLength)));
    newBranches.add(branch.newBranch(random(10.0, 35.0), random(minLength, maxLength)));
    break;
  case 3:
    newBranches.add(branch.newBranch(random(-35.0, -15.0), random(minLength, maxLength)));
    newBranches.add(branch.newBranch(random(-10.0, 10.0), random(minLength, maxLength)));
    newBranches.add(branch.newBranch(random(15.0, 35.0), random(minLength, maxLength)));
    break;
  default:
    newBranches.add(branch.newBranch(random(-35.0, 35.0), random(minLength, maxLength)));
    break;
  }

  for (Branch newBranch : newBranches) {
    branches.add(newBranch);

    if (newBranch.level < maxLevel) {
      subDivide(newBranch);
    } else {
      // Randomly generate leaves position on last branch
      for (int i = 0; i < 5; i++) {
        leaves.add(new Leaf(newBranch.end.x, newBranch.end.y, newBranch));
      }
    }
  }
}

PImage createLeaveImage() {
  PGraphics buffer = createGraphics(12, 18, P2D);
  buffer.beginDraw();
  buffer.stroke(col1); // mas oscuro
  buffer.line(6, 0, 6, 6);
  buffer.noStroke();
  buffer.fill(col2); //  claro
  buffer.beginShape();
  buffer.vertex(6, 6);
  buffer.bezierVertex(0, 12, 0, 12, 6, 18);
  buffer.bezierVertex(12, 12, 12, 12, 6, 6);
  buffer.endShape();
  buffer.fill(col3); // mas claro
  buffer.beginShape();
  buffer.vertex(6, 9);
  buffer.bezierVertex(0, 13, 0, 13, 6, 18);
  buffer.bezierVertex(12, 13, 12, 13, 6, 9);
  buffer.endShape();
  buffer.stroke(col2); //  oscuro
  buffer.noFill();
  buffer.bezier(6, 9, 5, 11, 5, 12, 6, 15);
  buffer.endDraw();
  return buffer.get();
}

void mousePressed() {
  callTrees();
}
void keyPressed() {
  if (key == 'a') {
    if (hval>=30)hval -= 20;
  }
  if (key == 's') {
    if (hval<=340)hval += 20;
  }
  if (key == 'q') {
    ldiam += 2;
  }
  if (key == 'w') {
    if (ldiam>=3)ldiam -= 2;
  }
  if (key == 'z') {
    if(sel>=1)sel-=1;
  }
  if (key == 'x') {
    if(sel<=16)sel+=1;
  }
}
