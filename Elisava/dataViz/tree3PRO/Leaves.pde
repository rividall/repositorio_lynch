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

  Leaf(float _x, float _y, Branch _parent) {
    this.pos = new PVector(_x, _y);
    this.diameter = random(ldiam, ldiam+8);
    this.opacity = random(opa, opa+20);
    this.parent = _parent;
    this.offset = new PVector(_parent.restPos.x-this.pos.x, _parent.restPos.y-this.pos.y);

    if (leaves.size() % 5 == 0) {
      this.hue = hval;
      this.sat = 100;
    } else {
      this.hue = random(hval, hval+20);
      this.sat = 50;
    }
  }

  void display() {
    stroke(this.hue,sat,100, this.opacity*3);
    fill(this.hue, sat, 100, this.opacity);
    line(this.pos.x-10, this.pos.y-5, this.pos.x+10, this.pos.y+5);
    noStroke();
    ellipse(this.pos.x, this.pos.y, this.diameter, this.diameter/2);
  }
}
