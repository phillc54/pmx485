void setup() {  // SETUP

  pinMode(arcOk, INPUT_PULLUP); // floating inputs are unstable
  pinMode(arcOn, INPUT_PULLUP);
  pinMode(receiving, OUTPUT);
  pinMode(currentOut, OUTPUT);
  Serial.begin(19200, SERIAL_8E1);
  lcd.begin(16, 2);
  lcd.setCursor(2, 0);
  lcd.print("booting....");
  lcd.setCursor(2, 1);
  lcd.print("please wait");
  delay(2000);
  lcd.clear();
  digitalWrite(receiving, LOW);

}  // END SETUP
