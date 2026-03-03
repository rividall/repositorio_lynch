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
    angle = random(PI/2, PI+PI/2);
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
    image(leaveImage, -leaveImage.width/2, 0, ldiam, ldiam*2);
    popMatrix();
  }
}

PImage createLeaveImage() {
  PGraphics buffer = createGraphics(48, 72, P2D);
  buffer.beginDraw();
  buffer.scale(4);
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
