void register_read() {  // READ REGISTER

  char hex2[3] = "";
  char hex4[5] = "";
  int value = 0;

  // create the base data for LRC calculation
  int_to_hex(hex2, inAddress, 2);
  strcpy(inCheckLRC, hex2);
  int_to_hex(hex2, inFunction, 2);
  strcat(inCheckLRC, hex2);
  int_to_hex(hex2, inNumRegs * 2, 2);
  strcat(inCheckLRC, hex2);
  // get the data from the register
  for (int i = 0; i < inNumRegs; ++i) {
    if (inRegister + i == rMode && remoteMode) {
      value = presentMode;
    } else if (inRegister + i == rCurrent && remoteMode) {
      value = presentCurrent * 64;
    } else if (inRegister + i == rPressure && remoteMode) {
      value = presentPressure * 128;
    } else if (inRegister + i == rFault) {
      value = presentFault;
    } else if (inRegister + i == rCurrentMin) {
      value = presentCurrentMin * 64;
    } else if (inRegister + i == rCurrentMax) {
      value = presentCurrentMax * 64;
    } else if (inRegister + i == rPressureMin) {
      value = presentPressureMin * 128;
    } else if (inRegister + i == rPressureMax) {
      value = presentPressureMax * 128;
    } else if (inRegister + i == rPressureActual) {
      value = actualPressure * 128;
    } else if (inRegister + i == rArcTimeLow) {
      value = 65535;
    } else if (inRegister + i == rArcTimeHigh) {
      value = 0;
    } else {
      value = 0; // return zero if register is unused
    }
    int_to_hex(hex4, value, 4);
    strcat(inCheckLRC, hex4);
  }
  strcat(inCheckLRC, "\0");

}  // END READ REGISTER
