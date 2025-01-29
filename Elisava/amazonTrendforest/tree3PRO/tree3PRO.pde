// Global variables
ArrayList<Branch> branches = new ArrayList<Branch>();
ArrayList<Leaf> leaves = new ArrayList<Leaf>();

float maxLevel = 5.9; // Tamaño arbol
int ldiam = 40; // tamaño hojas
int hval = 0; // color
int opa = 5;

int treePX = 400;
int treePY = 600;

void setup() {
  size(800, 700);
  colorMode(HSB, 360,100,100);
  callTrees();
}

void draw() {
  background(360);

  for (int i = 0; i < branches.size(); i++) {
    Branch branch = branches.get(i);
    branch.display();
  }
  for (int i = leaves.size()-1; i > -1; i--) {
    Leaf leaf = leaves.get(i);
    leaf.display();
  }
}

void callTrees(){
 generateNewTree(treePX, treePY);
}

void generateNewTree(int newBranchPosX, int newBranchPosY) {
  branches.clear();
  leaves.clear();
  float rootLength = random(80.0, 120.0);
  branches.add(new Branch(newBranchPosX, newBranchPosY, newBranchPosX, newBranchPosY-rootLength, 0, null));

  subDivide(branches.get(0));
}

void subDivide(Branch branch) {
  ArrayList<Branch> newBranches = new ArrayList<Branch>();

  int newBranchCount = (int)random(1, 4);

  float minLength = 0.7;
  float maxLength = 0.85;

  switch(newBranchCount) {
  case 2:
    newBranches.add(branch.newBranch(random(-45.0, -10.0), random(minLength, maxLength)));
    newBranches.add(branch.newBranch(random(10.0, 45.0), random(minLength, maxLength)));
    break;
  case 3:
    newBranches.add(branch.newBranch(random(-45.0, -15.0), random(minLength, maxLength)));
    newBranches.add(branch.newBranch(random(-10.0, 10.0), random(minLength, maxLength)));
    newBranches.add(branch.newBranch(random(15.0, 45.0), random(minLength, maxLength)));
    break;
  default:
    newBranches.add(branch.newBranch(random(-45.0, 45.0), random(minLength, maxLength)));
    break;
  }

  for (Branch newBranch : newBranches) {
    branches.add(newBranch);

    if (newBranch.level < maxLevel) {
      subDivide(newBranch);
    } else {
      // Randomly generate leaves position on last branch
      float offset = 5.0;
      for (int i = 0; i < 5; i++) {
        leaves.add(new Leaf(newBranch.end.x+random(-offset, offset), newBranch.end.y+random(-offset, offset), newBranch));
      }
    }
  }
}

void mousePressed() {
  callTrees();
}

void keyPressed() {

  if (key == 'a') {
    maxLevel+=1; // cantidad hojas
  }
  if (key == 's') {
    ldiam+=1; // tamaño hojas
  }
  if (key == 'd') {
    if(hval<= 340)hval += 20; // color
  }
  if (key == 'A') {
    if(maxLevel >= 2) maxLevel-=1; // cantidad hojas
  }
  if (key == 'S') {
    if (ldiam>=2)ldiam-=1; // tamaño hojas
  }
  if (key == 'D') {
    if (hval>=20)hval -= 20; // color
  }
}
