void display(){ // DISPLAY

  char input[6];
  char output[7];

  // show mode
  lcd.setCursor(0, 0);
  switch (cMode) {
//    case 0:
//      lcd.print("Local ");
//      break;
    case 1:
      lcd.print("Normal");
      break;
    case 2:
      lcd.print("CPA   ");
      break;
    case 3:
      lcd.print("Gouge ");
      break;
//    default:
//      lcd.print("???   ");
//      break;
  }

  // show current
  lcd.setCursor(8, 0);
  dtostrf(cCurrent,5, 1, input);
  sprintf(output,"%samp",input);
  lcd.print(output);

  // show settings mode
  lcd.setCursor(0, 1);
  lcd.print(settings);

  // show pressure
  lcd.setCursor(8, 1);
  dtostrf(cPressure,5, 1, input);
  if(pressureType){
    sprintf(output,"%sbar",input);
  }else{
    sprintf(output,"%spsi",input);
  }
  lcd.print(output);

} // END DISPLAY
