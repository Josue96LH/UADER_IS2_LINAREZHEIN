// EJEMPLO BLINK

// la función setup se ejecuta una vez cuando presionas reset o enciendes la placa
void setup() {
  // inicializa el pin digital LED_BUILTIN como una salida.
  pinMode(LED_BUILTIN, OUTPUT);
}

// la función loop se ejecuta una y otra vez para siempre
void loop() {
  digitalWrite(LED_BUILTIN, HIGH);  // enciende el LED
  delay(1000);                      // espera un segundo
  digitalWrite(LED_BUILTIN, LOW);   // apaga el LED
  delay(5000);                      // espera cinco segundo
}