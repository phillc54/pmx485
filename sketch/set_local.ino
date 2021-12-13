void set_local(){ // SET LOCAL VALUES

//  int param = 0;

  switch(button){
    case 1:
      if(setting < 4){
        setting ++;
      }else{
        setting = 0;
      }
      break;
    case 4:
      if(setting == 1){
        if(cMode == 3){
          cMode = 1;
        }else{
          cMode ++;
        }
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
      }else if(setting == 2){
        cCurrent += 0.1;
        if(cCurrent > cCurrentMax){
          cCurrent = cCurrentMin;
        }
      }else if(setting == 3){
        cPressure += 0.1;
        if(cPressure > cPressureMax){
          cPressure = cPressureMin;
        }
      }else if(setting == 4){
        pressureType = !pressureType;
        if(pressureType){
          cPressure    = cPressure    * 0.0689476;
          cPressureMax = cPressureMax * 0.0689476;
          cPressureMin = cPressureMin * 0.0689476;
        }else{
          cPressure    = cPressure    * 14.5038;
          cPressureMax = cPressureMax * 14.5038;
          cPressureMin = cPressureMin * 14.5038;
        }
      }
      break;
    case 5:
      if(setting == 1){
        if(cMode == 1){
          cMode = 3;
        }else{
          cMode --;
        }
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
      }else if(setting == 2){
        cCurrent -= 0.1;
        if(cCurrent < cCurrentMin){
          cCurrent = cCurrentMax;
        }
      }else if(setting == 3){
        cPressure -= 0.1;
        if(cPressure < cPressureMin && cPressure != 0){
          cPressure = cPressureMax;
        }
      }else if(setting == 4){
        pressureType = !pressureType;
        if(pressureType){
          cPressure    = cPressure    * 0.0689476;
          cPressureMax = cPressureMax * 0.0689476;
          cPressureMin = cPressureMin * 0.0689476;
        }else{
          cPressure    = cPressure    * 14.5038;
          cPressureMax = cPressureMax * 14.5038;
          cPressureMin = cPressureMin * 14.5038;
        }
      }
      break;
  }
  oldMode = cMode;
  oldCurrent = cCurrent;
  oldPressure = cPressure;  
} // END SET LOCAL VALUES
