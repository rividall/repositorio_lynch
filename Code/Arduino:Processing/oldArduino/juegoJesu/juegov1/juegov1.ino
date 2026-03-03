//    Juego sin nombre v1.1
// jugador azul vs morado
// primer color al azar
// todos buscan ese mismo color
// cuando uno gana, la luz queda pegada en el color de ese jugador

int bot1 = 13; // boton 1 en pin 1, variable bot1
int bot2 = 2;
int bot3 = 3;

int r1 = 6; // luz r, g ,b de bot1, variables r1, g1, b1
int g1 = 5; // en pines 4, 5 ,6.
int b1 = 4;

int r2 = 9;
int g2 = 8;
int b2 = 7;

int r3 = 12;
int g3 = 11;
int b3 = 10;

int l1 = 0; // variables para valor random de encendido
int l2 = 0;
int l3 = 0;

int dur = 100; // duración de pausa entre luces en test
int duraLuz = 500;

int pt1 = 0; // variables pàra contar puntaje
int pt2 = 0;
int pt3 = 0;
int ptWin = 3; // puntaje para conquistar base

unsigned long currentMillis = 1000; // variables para contar tiempo
unsigned long periodo; // tiempo al azar
int maxT = 2000; // tiempo maximo de espera entre luces
int minT = 600; // tiempo minimo

boolean win1 = false; // estado de bases, 1 2 y 3
boolean win2 = false;
boolean win3 = false;

void setup() { // funcion para setear los valores y modos de funcionamiento de pines y variables
  
  Serial.begin(9600); // com serial, para ver en el monitor 
  // put your setup code here, to run once:
  pinMode(bot1, INPUT_PULLUP); //seteo botones como entrada
  pinMode(bot2, INPUT_PULLUP);
  pinMode(bot3, INPUT_PULLUP);

  pinMode(r1, OUTPUT); // seteo luces como salida
  pinMode(g1, OUTPUT);
  pinMode(b1, OUTPUT);

  pinMode(r2, OUTPUT);
  pinMode(g2, OUTPUT);
  pinMode(b2, OUTPUT);

  pinMode(r3, OUTPUT);
  pinMode(g3, OUTPUT);
  pinMode(b3, OUTPUT);
  
  periodo = random(1000, 5000); // primera espera para luces en 1 y 4 segundos
}

void loop() { // loop infinito de funcionamiento
  
  int bot1st = digitalRead(bot1); // guardo estado de boton en variable bot#st
  int bot2st = digitalRead(bot2);
  int bot3st = digitalRead(bot3);

tiempo(); // lamo a funcion para contar tiempo

botones(); // llamo a funcion que controla botones

puntaje(); // llamo a la funcion que cuenta puntos

delay(20);
}

void tiempo(){ // funcion que cuenta tiempo
  
  if (millis() > currentMillis + periodo) { // si transcurre el tiempo del periodo
    currentMillis = millis(); // reinicio el tiempo
    periodo = random(minT, maxT); // nuevo valor de periodo, entre min y maxt

    if (!win1) { // mientras no haya ganado la base
      l1 = random(4, 7); // seleccionar color al azar
      digitalWrite(l1, HIGH); // prender ese color
    }
    if (!win2) { // bis, base 2
      l2 = random(7, 10);
      digitalWrite(l2, HIGH);
    }
    if (!win3) { // bis, base 3
      l3 = random(10, 13);
      digitalWrite(l3, HIGH);
    }
    Serial.print(l1); // escribir en monitor el estado de las luces (para debug)
    Serial.print(' ');
    Serial.print(l2);
    Serial.print(' ');
    Serial.println(l3);
  }

  if (millis() > currentMillis + duraLuz) { // si pasa el tiempo que dura prendidda la luz
    if (!win1) digitalWrite(l1, LOW); // mientras no haya conquistado la base, apagar luces
    if (!win2) digitalWrite(l2, LOW);
    if (!win3) digitalWrite(l3, LOW);
  }
}

void botones(){ // funcion que maneja los botones
  
  if (bot1st == LOW && l1 == r1) { // si apreto bot1, y esta prendido el rojo
    pt1 += 1; // sumo 1 punto
    digitalWrite(l1, LOW); // apago la luz
    l1 = 0;  // reinicio la luz
  }

  if (bot2st == LOW && l2 == r2) { // bis bot2
    pt2 += 1;
    digitalWrite(l2, LOW);
    l2 = 0;
  }

  if (bot3st == LOW && l3 == r3) { // bis bot3
    pt3 += 1;
    digitalWrite(l3, LOW);
    l3 = 0;
  }
}

void puntos(){ // función que cuenta los puntos
  
  if (pt1 == ptWin) { // si acumulo 3 puntos en base 1
    win1 = true; // activo el estado ganar
    digitalWrite(r1, HIGH); // mantengo prendida la luz roja
    Serial.println("ganaste la base 1"); // escribo en monitor
    pt1 += 1; // anulo el puntaje
  }

  if (pt2 == ptWin) { // bis base 2
    win2 = true;
    digitalWrite(r2, HIGH);
    Serial.println("ganaste la base 2");
    pt2 += 1;
  }

  if (pt3 == ptWin) { // bis base 3
    win3 = true;
    digitalWrite(r3, HIGH);
    Serial.println("ganaste la base 3");
    pt3 += 1;
  }

  if (win1 && win2 && win3) { // si conquisto las 3 bases, sale mensaje de ganador
    Serial.println("ALL YOUR BASE ARE BELONG TO US.");
  }
}
