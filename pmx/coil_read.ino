void coil_read() {  // READ COIL

  char hex2[3] = "";
  int integer = 0;
  int numBytes = 0;
  unsigned i = 0;

  // create the base data for LRC calculation
  int_to_hex(hex2, inAddress, 2);
  strcpy(inCheckLRC, hex2);
  int_to_hex(hex2, inFunction, 2);
  strcat(inCheckLRC, hex2);
  numBytes = (inNumRegs + 7) / 8;
  int_to_hex(hex2, numBytes, 2);
  strcat(inCheckLRC, hex2);
  for (int i = 0; i < inNumRegs; ++i) {
    lcd.print(inRegister + i);
    if (inRegister + i == rLeadLow) {
      //integer = integer | (1 << i);  // pretend we have a 35'~50' torch lead
    } else if (inRegister + i == rLeadHigh) {
      //integer = integer | (1 << i); // pretend we have a 70' torch lead
    } else if (inRegister + i == rStartSwitch) {
      if (digitalRead(arcOn)) {
        integer = integer & ~(1 << i);
      } else {
        integer = integer | (1 << i);
      }
    } else if (inRegister + i == rMotionSwitch) {
      if (digitalRead(arcOk)) {
        integer = integer & ~(1 << i);
      } else {
        integer = integer | (1 << i);
      }
    } else if (inRegister + i == rGasTest) {
      integer = presentGasTest;
    }
  }
  int_to_hex(hex2, integer, 2);
  strcat(inCheckLRC, hex2);
  strcat(inCheckLRC, "\0");

}  // END READ COIL
