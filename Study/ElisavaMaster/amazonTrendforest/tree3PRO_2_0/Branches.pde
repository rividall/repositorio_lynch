void generateNewTree(int newBranchPosX, int newBranchPosY) {
  branches.clear();
  leaves.clear();
  branches.add(new Branch(newBranchPosX, newBranchPosY, newBranchPosX, newBranchPosY-sz, 0, null));
  subDivide(branches.get(0));
}

class Branch {
  PVector start;
  PVector end;
  PVector vel = new PVector(0, 0);
  PVector acc = new PVector(0, 0);
  int level;
  Branch parent = null;
  PVector restPos;
  float restLength;

  Branch(float _x1, float _y1, float _x2, float _y2, int _level, Branch _parent) {
    this.start = new PVector(_x1, _y1);
    this.end = new PVector(_x2, _y2);
    this.level = _level;
    this.restLength = dist(_x1, _y1, _x2, _y2);
    this.restPos = new PVector(_x2, _y2);
    this.parent = _parent;
  }

  void display() {
    //println(this.level);
    //stroke(10, 57, 20+this.level*4);
    stroke(93+(this.level*12), 48+(this.level*7), 38+(this.level*7)); // PDF exporter prints RGB values, so green changes after printing
    strokeWeight(maxLevel*2.5-this.level*2);

    if (this.parent != null) {
      line(this.parent.end.x, this.parent.end.y, this.end.x, this.end.y);
    } else {
      line(this.start.x, this.start.y, this.end.x, this.end.y);
    }
  }

  Branch newBranch(float angle, float mult) {
    // Calculate new branch's direction and length
    PVector direction = new PVector(this.end.x, this.end.y);
    direction.sub(this.start);
    float branchLength = direction.mag()*0.8;

    float worldAngle = degrees(atan2(direction.x, direction.y))+angle;
    direction.x = sin(radians(worldAngle));
    direction.y = cos(radians(worldAngle));
    direction.normalize();
    direction.mult(branchLength*mult);

    PVector newEnd = new PVector(this.end.x, this.end.y);
    newEnd.add(direction);

    return new Branch(this.end.x, this.end.y, newEnd.x, newEnd.y, this.level+1, this);
  }
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
