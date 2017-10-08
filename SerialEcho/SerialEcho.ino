void setup() 
{
  Serial.begin(115200);
  Serial.println("Hello from RX");
}

void loop() 
{
  if (Serial.available())
    Serial.println(sizeof(Serial.read()));
}
