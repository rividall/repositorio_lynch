// Ricardo Vidal, Data. 2025 Elisava.

int posXeg = 150; // posicion en X de las elipses grises en cuadrado blanco
int posYeg = 200;

int sepXeg = 20; // separación en X de las elipses grises en cuadrado blanco
int sepYeg = 20;

int tamEr = 90; // tamaño ellipse rosa arriba derecha

void setup() {
  size(500, 500);
}

void draw() {
  background(#54a0ff);

  noStroke();


  rect(10, 10, 10, 10);
  rect(30, 10, 10, 10);
  rect(480, 60, 10, 10);
  rect(40, 380, 10, 10);

// ELIPSE ROSA 

  fill(#ff9ff3);
  circle(350, 120, tamEr); // ellipse rosa arriba derecha

// FIN ELIPSE ROSA


  fill(#f368e0); //circulos atras
  ellipse(250, 400, 100, 100); // circulo rosado abajo
  ellipse(420, 400, 100, 100); // circulo rosado abajo derecha
  ellipse(420, 270, 100, 100); // circulo rosado abajo medio derecha

// TRIANGULO 

  fill(46, 134, 222); // triangulo atras
  triangle(150, 150, 500, 150, 150, 450);
  
// FIN TRIANGULO

  fill(#222f3e); // rect gris oscuro medio
  rect(230, 220, 190, 100);
  rect(420, 350, 190, 100);

  fill(255);
  rect(50, 50, 300, 200); // cuadrado blanco

  fill(#2c3e50);
  triangle(50, 50, 250, 50, 50, 200); // triangulo azul

  fill(255); //Lineas sobre triangulo azul
  rect(50, 100, 70, 3);
  rect(50, 90, 70, 3);
  rect(160, 70, 70, 3);
  rect(180, 60, 70, 3);

// CIRCULOS GRISES

  fill(#6c5ce7); //circulos grises en cuadrado blanco
  ellipse(posXeg, posYeg, 10, 10);
  ellipse(posXeg + sepXeg, posYeg, 10, 10);
  ellipse(posXeg + sepXeg*2, posYeg, 10, 10);
  ellipse(posXeg + sepXeg*3, posYeg, 10, 10);
  ellipse(posXeg + sepXeg*4, posYeg, 10, 10);

  ellipse(posXeg, posYeg + sepYeg, 10, 10);
  ellipse(posXeg + sepXeg, posYeg + sepYeg, 10, 10);
  ellipse(posXeg + sepXeg*2, posYeg + sepYeg, 10, 10);
  ellipse(posXeg + sepXeg*3, posYeg + sepYeg, 10, 10);
  ellipse(posXeg + sepXeg*4, posYeg + sepYeg, 10, 10);

  ellipse(posXeg, posYeg + sepYeg*2, 10, 10);
  ellipse(posXeg + sepXeg, posYeg + sepYeg*2, 10, 10);
  ellipse(posXeg + sepXeg*2, posYeg + sepYeg*2, 10, 10);
  ellipse(posXeg + sepXeg*3, posYeg + sepYeg*2, 10, 10);
  ellipse(posXeg + sepXeg*4, posYeg + sepYeg*2, 10, 10);
        
  
// FIN DE CIRCULOS GRISES QUE VAN Y VUELVEN  

  fill(#34495e); // triangulos azules 
  triangle(60, 120, 60, 150, 100, 150);
  triangle(140, 90, 140, 120, 110, 120);
  triangle(30, 320, 30, 350, 60, 350);

  fill(#7f8c8d); // elementos extra
  rect(200, 135, 110, 12);
  rect(200, 120, 110, 12);
  rect(60, 230, 10, 10);
  ellipse(85, 235, 10, 10);
  triangle(100, 230, 100, 240, 110, 235);

  fill(#e74c3c); // Poder
  rect(200, 160, 110, 6);
  rect(200, 170, 110, 6);
  rect(160, 270, 110, 6);
  rect(160, 280, 110, 6);
  rect(160, 290, 110, 6);

  print(mouseX); 
  print(',');
  println(mouseY);
}
