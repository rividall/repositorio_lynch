color grisOsc = #7f8c8d; // Creación de variables de color.
color verde = #1abc9c;
color gris = #ecf0f1;
color grisAzul = #95a5a6;
color celeste = #48dbfb;
color cyan = #0abde3;
color nar = #e74c3c;
int posX = 30;
int posY = 30;
int tam = 50;
float var1 = 0;
float var2 = 0;
float posMX = 100;
float posMY = 200;

int pts = 0;

boolean col1 = true;
boolean col2 = true;

boolean enemy1 = true;


PImage pika;
PImage charm;

void setup() {
  size(500, 500);

  charm = loadImage("char.png");
  pika = loadImage("pika.png");
}

void draw() {
  
  var1 = random(-5,7);
  var2 = random(-5,5);
  posMX += var1;
  posMY += var2;

  background(verde);
  image(pika, posX, posY, tam, tam);
  text("Puntos: ", 10, 10);
  text(pts, 60, 10);

  if (posX <= 0) posX=0;
  if (posX >= width-35)posX=width-35;
  if (posY <= 0) posY=0;
  if (posY >= height-35)posY=height-35;

  if (col1 == true) {
    fill(nar);
    ellipse(100, 100, 40, 40);
    if (dist(100, 100, posX, posY) < 30) {
      pts+=1; 
      tam+=25;
      col1 = false;
    }
  }

  if (col2 == true) {
    fill(nar);
    ellipse(200, 200, 40, 40);
    if (dist(200, 200, posX, posY) < 30) {
      pts+=1; 
      tam+=25;
      col2 = false;
    }
  }

  if (enemy1 == true) {
    fill(gris);
    rect(posMX, posMY, 40, 40);
    if (dist(posMX, posMY, posX, posY) < 30) {
      pts-=1; 
      tam-=25;
      enemy1 = false;
    }
  }

  if (pts < 0) {
    background(verde);
    text("PERDISTE", width/2, height/2);
  }
    if (pts > 1) {
    background(verde);
    text("GANASTE", width/2, height/2);
  }
}



void keyPressed() {
  if (key == 'a') {
    posX -= 5;
  }
  if (key == 'd') {
    posX += 5;
  }
  if (key == 'w') {
    posY -= 5;
  }
  if (key == 's') {
    posY += 5;
  }
}
