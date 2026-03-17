int sensorValue = 0;  // Variable para almacenar datos del sensor

void setup() {
  Serial.begin(9600);  // Permite la comunicación de los valores desde el Arduino al ordenador
  pinMode(A0, INPUT_PULLUP); // Utilización de pin analógico 
}

void loop() {
  sensorValue = analogRead(A0); // Lectura del sensor
  Serial.print("sensor = "); // Imprime los resultados en el monitor serial
  Serial.println(sensorValue);

  if (sensorValue < 28) {  // Condición de haber presionado el sensor
    Serial.println("Bajo el umbral");  // Imprime un aviso
  }
}