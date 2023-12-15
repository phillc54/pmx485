void get_data() {  // GET DATA

  static boolean recvInProgress = false;
  static byte index = 0;
  char startMarker = ':';
  char endMarker = '\n';
  char inChar;
  char tmp2[3] = "";
  char tmp4[5] = "";
  char readID[11] = "012B0E0401";
  char testID[11] = "";

  while (Serial.available() > 0 && newData == false) {
    inChar = Serial.read();
    if (recvInProgress == true) {
      if (inChar != endMarker) {
        inRaw[index] = inChar;
        index++;
        if (index >= numChars) {
          index = numChars - 1;
        }
      } else {
        inRaw[index] = inChar;
        index++;
        inRaw[index] = '\0';  // terminate the string
        recvInProgress = false;
        index = 0;
        newData = true;
      }
    } else if (inChar == startMarker) {
      //      inRaw[0] = 0;
      inRaw[index] = inChar;
      index++;
      recvInProgress = true;
    }
  }

  if (newData) {
    /* is this an identity request */
    strncpy(testID, &inRaw[1], 10);
    if (!strcmp(testID, readID)) {
      strcpy(reply, ":012B0E048100010101063038313231112B\r\n");
      send_data();
      newData = false;
      return;
    } else {
      lcd.print("n");
      inNumRegs = 1;
      memset(inCheckLRC, 0, sizeof inCheckLRC);
      strncpy(tmp2, &inRaw[1], 2);
      inAddress = (int)strtol(tmp2, NULL, 16);
      strncpy(tmp2, &inRaw[3], 2);
      inFunction = (int)strtol(tmp2, NULL, 16);
      strncpy(tmp4, &inRaw[5], 4);
      inRegister = (int)strtol(tmp4, NULL, 16);
      strncpy(tmp4, &inRaw[5], 4);
      if (inFunction == regRead || inFunction == coilRead) {
        strncpy(tmp4, &inRaw[9], 4);
        inNumRegs = (int)strtol(tmp4, NULL, 16);
      } else if (inFunction == regWrite || inFunction == coilWrite) {
        strncpy(tmp4, &inRaw[9], 4);
        inData[0] = strtoul(tmp4, NULL, 16);
      } else if (inFunction == regWriteMult) {
        strncpy(tmp4, &inRaw[9], 4);
        inNumRegs = (int)strtol(tmp4, NULL, 16);
        strncpy(tmp2, &inRaw[13], 2);
        inNumBytes = (int)strtol(tmp2, NULL, 16);
        for (int i = 0; i < inNumRegs; ++i) {
          strncpy(tmp4, &inRaw[15 + (i * 4)], 4);
          inData[i] = (int)strtol(tmp4, NULL, 16);
        }
      }
      strncpy(inLRC, &inRaw[strlen(inRaw) - 4], 2);
      strncpy(inCheckLRC, &inRaw[1], strlen(inRaw) - 5);
    }
  }

}  //END GET DATA
