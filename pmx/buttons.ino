void buttons(){ // READ BUTTONS
  int x;
  x = analogRead (0);
  if(x < 114) {
    button = 3;
  }else if(x < 300) {
    button = 4;
  }else if(x < 466){
    button = 5;
  }else if(x < 707){
    button = 2;
  }else if(x < 1003){
    button = 1;
  }else{
    button = 0;
  }

  if(remoteMode){
    if(x < 1003){
      switch(button){
        case 1:
          cFault = 120;
          break;
        case 2:
          cFault = 220;
          break;
        case 3:
          cFault = 402;
          break;
        case 4:
          cFault = 2111;
          break;
        case 5:
          cFault = 3421;
          break;
      }
    }else{
      cFault = 0;
    }
    setting = 0;
    strcpy(settings,"Remote  ");
  }else{
    if(button){
      if(buttonOff){
        buttonOff = false;
        startMillis = millis();
        set_local();
      }else if(setting > 1 && (button == 4 || button == 5) && startMillis){
        if(millis() > startMillis + 250){
          startMillis = millis();
          set_local();
        }
      }
    }else{
      buttonOff = true;
      startMillis = 0;
    }
    switch(setting){
      case 0:
        strcpy(settings, "Local   ");
        break;
      case 1:
        strcpy(settings, "Mode    ");
        break;
      case 2:
        strcpy(settings, "Current ");
        break;
      case 3:
        strcpy(settings, "Pressure");
        break;
      case 4:
        strcpy(settings, "Units   ");
        break;
    }
  }

} // END READ BUTTONS
