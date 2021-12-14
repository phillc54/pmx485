void loop(){ // MAIN LOOP

  bool result = false;
  
  if(newData == false){
    get_data();
  }else{
    if(get_checksum()){
//      if(remoteMode == true){
      if(remoteMode){
        if(address == (int)strtol(inAddress, NULL, 16)){
          if((int)strtol(inFunction, NULL, 16) == regRead){
            result = register_read();
          }else if((int)strtol(inFunction, NULL, 16) == regWrite){
            result = register_write();
            if(cMode == 0 && cCurrent == 0 && cPressure == 0){
                address = 0;
                validMode = false;
                validCurrent = false;
                validPressure = false;
                cMode = oldMode;
                cCurrent = oldCurrent;
                cPressure = oldPressure;
//                cMode = 0;
//                cCurrent = 0;
//                cPressure = 0;
                remoteMode = false;
            }
          }
        }
        if(result == true){
          send_data();
        }
      }else{
        if(address == 0 || (address != 0 && address == (int)strtol(inAddress, NULL, 16))){
          if((int)strtol(inFunction, NULL, 16) == regWrite){
            result = register_write();
            if(result == true){
              set_mode();
              send_data();
            }
          }
        }
      }
    }else{
      send_bad();
    }
    newData = false;
  }

  buttons();
  
  display();

} // END MAIN LOOP
