void set_mode(){ // SET OPERATING MODE

  if(!validMode && (int)strtol(inRegister, NULL, 16) == rMode){
    if((int)strtol(inData, NULL, 16) != 0){
      validMode = true;
//      oldMode = cMode;
    }else{
      validMode = false;
    }
  }

  if(!validCurrent && (int)strtol(inRegister, NULL, 16) == rCurrent){
    if((int)strtol(inData, NULL, 16) != 0){
      validCurrent = true;
//      oldCurrent = cCurrent;
    }else{
      validCurrent = false;
    }
  }

  if(!validPressure && (int)strtol(inRegister, NULL, 16) == rPressure){
    if((int)strtol(inData, NULL, 16) != 0){
      validPressure = true;
//      oldPressure = cPressure;
    }else if(validMode && validCurrent){
      validPressure = true;
//      oldPressure = cPressure;
    }else{
      validPressure = false;
    }
  }

  if(address == 0 && (validMode || validCurrent || validPressure)){    
    address = (int)strtol(inAddress, NULL, 16);
  }

  if(validMode && validCurrent && validPressure){    
    remoteMode = true;
  }

} // END OPERATING MODE
