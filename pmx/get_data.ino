void get_data(){  // GET DATA

  static boolean recvInProgress = false;
  static byte index = 0;
  char startMarker = ':';
  char endMarker = '\n';
  char inChar;
//  static byte idx = 0;
  
  while(Serial.available() > 0 && newData == false){
    inChar = Serial.read();
//    if(idx < 15){     
//      idx ++;
//    }
    if(recvInProgress == true){
      if(inChar != endMarker){
        inRaw[index] = inChar;
        index++;
        if(index >= numChars){
          index = numChars - 1;
        }
      }else{
        inRaw[index] = inChar;
        index ++;
        inRaw[index] = '\0'; // terminate the string
        recvInProgress = false;
        index = 0;
        newData = true;
      }
    }else if(inChar == startMarker){
      inRaw[index] = inChar;
      index ++;
      recvInProgress = true;
    }
  }

  if(newData){
    strncpy(inAddress, &inRaw[1], 2);
    strncpy(inFunction, &inRaw[3], 2);
    strncpy(inRegister, &inRaw[5], 4);
    strncpy(inData, &inRaw[9], 4);
    strncpy(inCheck, &inRaw[1], 12);
    strncpy(inLRC, &inRaw[13], 2);
  }

}  //END GET DATA
