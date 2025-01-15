int y1 = 0;
int x1 = 0;

int y2 = 0;
int x2 = 0;
int x3 = 0;

int y3 = 0;
int y4 = 0;
int x4 =0;

void setup() {
  size(600, 600);
  x1 = width/2;
  y2 = height/2;
  x2 = width/2;
  x3 = width/2;
  y3 = height;
  y4 = height;
  x4 = width/2;
  frameRate(15);
}

void draw() {
  if (frameCount<=31) {
    line(width/2, y1, x1, height/2);
    y1+=10;
    x1+=10;

    line(width/2, y1, x2, height/2);
    x2-=10;

    line(x3, height/2, width/2, y3);
    x3-=10;
    y3-=10;

    line(x4, height/2, width/2, y4);
    x4+=10;
    y4-=10;
  }
}
