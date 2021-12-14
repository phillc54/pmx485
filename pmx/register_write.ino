bool register_write(){ // WRITE REGISTER

  if((int)strtol(inRegister, NULL, 16) == rMode){
    cMode = (int)strtol(inData, NULL, 16);

    if(cMode == 3){
      cPressureMax = gPressureMax;
      cPressureMin = gPressureMin;
    }else{
      cPressureMax = nPressureMax;
      cPressureMin = nPressureMin;
    }
    if(pressureType){
      cPressure    = cPressure    * 0.0689476;
      cPressureMax = cPressureMax * 0.0689476;
      cPressureMin = cPressureMin * 0.0689476;
    }
    if(cPressure > cPressureMax){
      cPressure = cPressureMax;
    }else if(cPressure < cPressureMin && cPressure != 0){
      cPressure = cPressureMin;
    }

  
  }else if((int)strtol(inRegister, NULL, 16) == rCurrent){
    cCurrent = ((float)strtol(inData, NULL, 16)) / 64;
  }else if((int)strtol(inRegister, NULL, 16) == rPressure){
    cPressure = ((float)strtol(inData, NULL, 16)) / 128;
  }

  strcpy(reply, inRaw);
  return true;  

} // END WRITE REGISTER
