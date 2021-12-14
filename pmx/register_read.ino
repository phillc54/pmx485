bool register_read(){ // READ REGISTER

  const char start[] = "010402"; 
  char data[5];
  char tmpD[5];
  byte tmpB = 0;
  float tmpF = 0;
  int tmpI = 0;
  char outCheck[13];
  int i = 0;
  
  if((int)strtol(inRegister, NULL, 16) == rMode){
    tmpI = cMode;
   }else if((int)strtol(inRegister, NULL, 16) == rCurrent){
    tmpI = cCurrent * 64;
  }else if((int)strtol(inRegister, NULL, 16) == rPressure){
    tmpI = cPressure * 128;
  }else if((int)strtol(inRegister, NULL, 16) == rFault){
    tmpI = cFault;
  }else if((int)strtol(inRegister, NULL, 16) == rCurrentMin){
    tmpI = cCurrentMin * 64;
  }else if((int)strtol(inRegister, NULL, 16) == rCurrentMax){
    tmpI = cCurrentMax * 64;
  }else if((int)strtol(inRegister, NULL, 16) == rPressureMin){
    tmpI = cPressureMin * 128;
  }else if((int)strtol(inRegister, NULL, 16) == rPressureMax){
    tmpI = cPressureMax * 128;
  }
  
  utoa(tmpI, tmpD, 16);

  if(strlen(tmpD) < 4){
    int difference = 4 - strlen(tmpD);
    memset(data, '0', difference);
    for(i; i < strlen(tmpD); i++){
      data[i+difference] = tmpD[i];
    }
  }else{
    strcpy(data, tmpD);
  }

  data[4] = '\0';
  strcpy(inCheck, start);
  strcat(inCheck, strupr(data));
  strcat(inCheck, '\0');
  get_checksum();
  strcpy(reply, ":");
  strcat(reply, inCheck);
  strcat(reply, strupr(hex));
  strcat(reply, "\r\n");
  return true;

} // END READ REGISTER
