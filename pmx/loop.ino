void loop() {  // MAIN LOOP

  char hex2[3] = "";
  char hex4[5] = "";

  if (newData == false) {
    get_data();
  } else {
    if (get_lrc()) {
      if (inFunction == coilRead) {
        coil_read();
      } else if (inFunction == regRead) {
        register_read();
      } else if (inFunction == regWrite || inFunction == regWriteMult) {
        for (int i = 0; i < inNumRegs; ++i) {
          if (remoteMode) {
            register_write(inRegister + i, inData[i]);  //, i);
          }
          if (inRegister + i == rMode || inRegister + i == rCurrent || inRegister + i == rPressure) {
            set_mode(inRegister + i, i);
          }
        }
        // create the base data for LRC calculation
        int_to_hex(hex2, inAddress, 2);
        strcpy(inCheckLRC, hex2);
        int_to_hex(hex2, inFunction, 2);
        strcat(inCheckLRC, hex2);
        int_to_hex(hex4, inRegister, 4);
        strcat(inCheckLRC, hex4);
        if (inFunction == regWrite) {
          int_to_hex(hex4, inData[0], 4);
        } else {
          int_to_hex(hex4, inNumRegs, 4);
        }
        strcat(inCheckLRC, hex4);
        strcat(inCheckLRC, "\0");
      } else if (inFunction == coilWrite) {
        coil_write();
      } else {
        send_bad("unknown function");
        return;
      }
      // create the reply packet
      strcpy(reply, ":");
      strcat(reply, strupr(inCheckLRC));
      get_lrc();
      strcat(reply, strupr(lrc_hex));
      strcat(reply, "\r\n");
      send_data();
    } else {
      send_bad("bad lrc");
    }
    newData = false;
  }
  analogWrite(currentOut, int((presentCurrent - currentMin) * currentUnit));
  actualPressure = presentPressure ? presentPressure : 75.0;
  buttons();
  display();

}  // END MAIN LOOP
