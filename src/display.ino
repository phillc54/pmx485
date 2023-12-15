void display() {  // DISPLAY

  // TOP LINE
  // show mode
  lcd.setCursor(0, 0);
  switch (presentMode) {
    case 0:
      lcd.print("Local ");
      break;
    case 1:
      lcd.print("Normal");
      break;
    case 2:
      lcd.print("CPA   ");
      break;
    case 3:
      lcd.print("Gouge ");
      break;
  }

  // show current
  lcd.setCursor(8, 0);
  if (presentCurrent < 10) {
    lcd.print("  ");
  } else if (presentCurrent < 100) {
    lcd.print(" ");
  }
  lcd.print(presentCurrent, 1);
  lcd.print("amp");

  // BOTTOM LINE
  //  show settings mode
  lcd.setCursor(0, 1);
  lcd.print(settings);
  // show pressure
  lcd.setCursor(8, 1);
  if (presentPressure < 10) {
    lcd.print("  ");
  } else if (presentPressure < 100) {
    lcd.print(" ");
  }
  lcd.print(presentPressure, 1);
  if (pressureType) {
    lcd.print("bar");
  } else {
    lcd.print("psi");
  }

}  // END DISPLAY
