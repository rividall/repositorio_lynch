int x = 0;
int y = 0;
int x1 = 0;
int y1, y2, y3;
int x2 = 0;
int x3 = 0;
float szChng = 10;

float l1x1, l1y1, l1x2, l1y2;

void setup() {
  size(800, 800);
  frameRate(10);
  background(256, 170, 0);
  y1 = width/2;
  y2 = height;
  y3 = width/2;
}

void draw() {
  noFill();
  translate(width/2, 0);
  quads();

  if (x1> width/2) {
    y=0;
    x1=0;
    y2=height;
    x3=0;
    background(256, 170, 0);
    szChng = random(10, 20);
    println(szChng);
  }
}

void quads() {
  quad(x, y, x1, y1, x2, y2, x3, y3);
  y+=szChng;
  x1+=szChng;
  y2-=szChng;
  x3-=szChng;
}
