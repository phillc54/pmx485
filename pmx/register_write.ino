void register_write(int reg, int data) {  //}, int num){ // WRITE REGISTER

  if (reg == rMode) {
    presentMode = data;
    if (presentMode == 3) {  // set gouge pressures
      presentPressureMax = pressureMaxGouge;
      presentPressureMin = pressureMinGouge;
    } else {  // set normal pressures
      presentPressureMax = pressureMax;
      presentPressureMin = pressureMin;
    }
    if (pressureType) {  // convert to bar
      presentPressure = presentPressure * 0.0689476;
      presentPressureMax = presentPressureMax * 0.0689476;
      presentPressureMin = presentPressureMin * 0.0689476;
    }
    if (presentPressure > presentPressureMax) {
      presentPressure = presentPressureMax;
    } else if (presentPressure < presentPressureMin && presentPressure != 0) {
      presentPressure = presentPressureMin;
    }
  } else if (reg == rCurrent) {
    presentCurrent = (float)data / 64;
  } else if (reg == rPressure) {
    presentPressure = (float)data / 128;
  }

}  // END WRITE REGISTER
