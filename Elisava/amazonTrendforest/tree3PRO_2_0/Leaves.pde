class Leaf {
  PVector pos;
  PVector vel = new PVector(0, 0);
  PVector acc = new PVector(0, 0);
  float diameter;
  float opacity;
  float hue;
  float sat;
  PVector offset;
  boolean dynamic = false;
  Branch parent;
  float angle;

  Leaf(float _x, float _y, Branch _parent) {
    this.pos = new PVector(_x, _y);
    this.diameter = random(ldiam, ldiam+8);
    angle = random(PI/2,PI+PI/2);
    this.parent = _parent;
    this.offset = new PVector(_parent.restPos.x-this.pos.x, _parent.restPos.y-this.pos.y);

    if (leaves.size() % 5 == 0) {
      this.hue = hval;
      this.sat = 100;
    } else {
      this.hue = random(hval, hval*2);
      this.sat = 50;
    }
  }

  void display() {
    pushMatrix();
    translate(this.pos.x, this.pos.y);
    rotate(angle);
    image(leaveImage,  -leaveImage.width/2, 0, ldiam,ldiam*2);
    popMatrix();
  }
}
