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
    stroke(10, 57, 20+this.level*4);
    strokeWeight(maxLevel-this.level+1);

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
    float branchLength = direction.mag();

    // Javascript doesn't have PVector.rotate() method
    // so need to manually get its new angle.
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
