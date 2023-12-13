/*  Phills PMX emulator
    © Phillip A Carter 2019, 2020, 2023
*/

// INCLUDES
#include <string.h>
#include <LiquidCrystal.h>

// INITIALIZE LCD (RS, En, D4, D5, D6, D7)
LiquidCrystal lcd(8, 9, 4, 5, 6, 7);

// OUPUT PINS
const byte receiving  = 2;
const byte currentOut = 3; // pwm output to set current

// INPUT PINS
const byte arcOn = 12;
const byte arcOk = 11;

// GLOBAL CONSTANTS
          const int coilOff         = 0x0000; // coil off
const unsigned long coilOn          = 0xFF00; // coil on
         const byte coilRead        = 0x01;   // read coil command
         const byte coilWrite       = 0x05;   // write coil command
         const byte numChars        = 225;    // maximum number of characters
          const int rArcTimeHigh    = 0x209F; // arc time high register
          const int rArcTimeLow     = 0x209E; // arc time low register
          const int rCurrent        = 0x2094; // current register
          const int rCurrentMax     = 0x209A; // current max register
          const int rCurrentMin     = 0x2099; // current min register
          const int rGasTest        = 0x0832; // gas test coil
          const int rLeadHigh       = 0x0809; // lead length high coil
          const int rLeadLow        = 0x0808; // lead length low coil
         const byte regRead         = 0x04;   // read register command
         const byte regWrite        = 0x06;   // read register command
         const byte regWriteMult    = 0x10;   // write multiple registers command
          const int rFault          = 0x2098; // fault code register
          const int rMode           = 0x2093; // cut mode register
          const int rMotionSwitch   = 0x0811; // motion switch signal status
          const int rPressure       = 0x2096; // pressure register
          const int rPressureActual = 0x204C; // actual pressure at valve
          const int rPressureMin    = 0x209C; // pressure min register
          const int rPressureMax    = 0x209D; // pressure max register
          const int rStartSwitch    = 0x0810; // start switch signal status

// PRETEND WE ARE A Powermax 65
float currentMax       = 65.0;
float currentMin       = 20.0;
float pressureMax      = 78.0;
float pressureMin      = 63.0;
float pressureMaxGouge = 58.0;
float pressureMinGouge = 43.0;

// GLOBAL VARIABLES
        float actualPressure;
         byte address            = 0;
          int button             = 0;
         bool buttonOff          = true;
         bool changing           = false;
          int inAddress;
         char inCheckLRC[numChars - 5];
unsigned long inData[5];
          int inFunction;
         char inLRC[3];
          int inNumBytes         = 2;
          int inNumRegs          = 1;
         char inRaw[numChars];
          int inRegister;
         byte lrc                = 0;
         char lrc_hex[5];
         bool newData            = false;
          int presentFault       = 0;
        float presentCurrent     = 45.0;
        float presentCurrentMax  = currentMax;
        float presentCurrentMin  = currentMin;
         bool presentGasTest     = 0;
          int presentMode        = 1;
        float presentPressure    = 75.0;
        float presentPressureMax = pressureMax;
        float presentPressureMin = pressureMin;
         bool pressureType       = 0;           // 0=psi, 1=bar
         bool remoteMode         = false;
          int remoteStart[3];
         char reply[numChars];
          int setting            = 0;
         char settings[9];
unsigned long startMillis;
         bool validCurrent       = false;
         bool validMode          = false;
         bool validPressure      = false;

          int lastMode           = presentMode;
        float lastCurrent        = presentCurrent;
        float lastPressure       = presentPressure;
        float currentUnit        = 255 / (currentMax - currentMin);
