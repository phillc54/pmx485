void set_local() {  // SET LOCAL VALUES

  //  int param = 0;

  switch (button) {
    case 1:
      if (setting < 4) {
        setting++;
      } else {
        setting = 0;
      }
      break;
    case 2:
      presentFault = 220;
      break;
    case 3:
      presentFault = 402;
      break;
    case 4:
      if (setting == 1) {
        if (presentMode == 3) {
          presentMode = 1;
        } else {
          presentMode++;
        }
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
      } else if (setting == 2) {
        presentCurrent += 0.1;
        if (presentCurrent > presentCurrentMax) {
          presentCurrent = presentCurrentMin;
        }
      } else if (setting == 3) {
        presentPressure += 0.1;
        if (presentPressure > presentPressureMax) {
          presentPressure = presentPressureMin;
        }
      } else if (setting == 4) {
        pressureType = !pressureType;
        if (pressureType) {  // convert to bar
          presentPressure = presentPressure * 0.0689476;
          presentPressureMax = presentPressureMax * 0.0689476;
          presentPressureMin = presentPressureMin * 0.0689476;
        } else {  // convert to psi
          presentPressure = presentPressure * 14.5038;
          presentPressureMax = presentPressureMax * 14.5038;
          presentPressureMin = presentPressureMin * 14.5038;
        }
      } else {
      presentFault = 2111;
      break;
      }
      break;
    case 5:
      if (setting == 1) {
        if (presentMode == 1) {
          presentMode = 3;
        } else {
          presentMode--;
        }
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
      } else if (setting == 2) {
        presentCurrent -= 0.1;
        if (presentCurrent < presentCurrentMin) {
          presentCurrent = presentCurrentMax;
        }
      } else if (setting == 3) {
        presentPressure -= 0.1;
        if (presentPressure < presentPressureMin && presentPressure != 0) {
          presentPressure = presentPressureMax;
        }
      } else if (setting == 4) {
        pressureType = !pressureType;
        if (pressureType) {  // convert to bar
          presentPressure = presentPressure * 0.0689476;
          presentPressureMax = presentPressureMax * 0.0689476;
          presentPressureMin = presentPressureMin * 0.0689476;
        } else {  // convert to psi
          presentPressure = presentPressure * 14.5038;
          presentPressureMax = presentPressureMax * 14.5038;
          presentPressureMin = presentPressureMin * 14.5038;
        }
      } else {
        presentFault = 3421;
        break;
      }
      break;
  }
  lastMode = presentMode;
  lastCurrent = presentCurrent;
  lastPressure = presentPressure;

}  // END SET LOCAL VALUES
