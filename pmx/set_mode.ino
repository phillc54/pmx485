void set_mode(int reg, int num) {  // SET OPERATING MODE

  if (remoteMode && presentMode == 0 && presentCurrent == 0 && presentPressure == 0) {
    address = 0;
    validMode = false;
    validCurrent = false;
    validPressure = false;
    presentMode = lastMode;
    presentCurrent = lastCurrent;
    presentPressure = lastPressure;
    remoteMode = false;
    return;
  }
  if (reg == rMode) {  //} && !validMode){
    if (inData[num] != 0) {
      validMode = true;
      remoteStart[0] = inData[num];
      //      lastMode = presentMode;
    } else {
      validMode = false;
      remoteStart[0] = 0;
    }
  } else if (reg == rCurrent) {  //} && !validCurrent){
    if (inData[num] != 0) {
      validCurrent = true;
      remoteStart[1] = inData[num];
      //      lastCurrent = presentCurrent;
    } else {
      validCurrent = false;
      remoteStart[1] = 0;
    }
  } else if (reg == rPressure) {  //} && !validPressure){
    if (inData[num] != 0) {
      validPressure = true;
      remoteStart[2] = inData[num];
      //      lastPressure = presentPressure;
    } else if (validMode && validCurrent) {
      validPressure = true;
      remoteStart[2] = inData[num];
      //      lastPressure = presentPressure;
    } else {
      validPressure = false;
      remoteStart[2] = 0;
    }
  }
  if (!remoteMode && validMode && validCurrent && validPressure) {
    remoteMode = true;
    register_write(rMode, remoteStart[0]);      //, 0);
    register_write(rCurrent, remoteStart[1]);   //, 0);
    register_write(rPressure, remoteStart[2]);  //, 0);
    if (address == 0) {
      address = inAddress;
    }
  }

}  // END OPERATING MODE
