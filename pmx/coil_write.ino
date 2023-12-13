void coil_write() {  // WRITE COIL

  char hex2[3] = "";
  char hex4[5] = "";

  // create the base data for LRC calculation
  int_to_hex(hex2, inAddress, 2);
  strcpy(inCheckLRC, hex2);
  int_to_hex(hex2, inFunction, 2);
  strcat(inCheckLRC, hex2);
  int_to_hex(hex4, inRegister, 4);
  strcat(inCheckLRC, hex4);

  if (remoteMode) {
    if (inRegister == rGasTest) {
      if (inData[0] == coilOff) {
        presentGasTest = false;
      } else if (inData[0] == coilOn) {
        presentGasTest = true;
      }
    }
  }
  int_to_hex(hex4, inData[0], 4);
  strcat(inCheckLRC, hex4);  //coil);
  strcat(inCheckLRC, "\0");

}  // END WRITE COIL
