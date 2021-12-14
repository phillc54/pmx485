/*  Phills PMX emulator
    © Phillip A Carter 2019, 2020
*/

// INCLUDES
#include <string.h>
#include <LiquidCrystal.h>

// INITIALIZE LCD (RS, En, D4, D5, D6, D7)
LiquidCrystal lcd(8, 9, 4, 5, 6, 7);

// OUPUT PINS
const byte led       = 13;
const byte receiving = 2;

// GLOBAL CONSTANTS

const byte  numChars     = 18;
const byte  regRead      = 4;     // write register command
const byte  regWrite     = 6;     // read register command
const int   rCurrent     = 8340;  // current register #
const int   rCurrentMax  = 8346;  // current max register #
const int   rCurrentMin  = 8345;  // current min register #
const int   rFault       = 8344;  // fault code register #
const int   rMode        = 8339;  // cut mode register #
const int   rPressure    = 8342;  // pressure register #
const int   rPressureMax = 8349;  // pressure max register #
const int   rPressureMin = 8348;  // pressure min register #

// TEMP GLOBAL FOR TEST
byte bob;
//float bob;

// GLOBAL VARIABLES
unsigned long startMillis;
bool  newData       = false;
bool  remoteMode    = false;
bool  validCurrent  = false;
bool  validMode     = false;
bool  validPressure = false;
bool  changing      = false;
bool  buttonOff     = true;
byte  address       = 0;
byte  lrc           = 0;
int   cFault        = 0;
int   cMode         = 1;
int   oldMode       = cMode;
int   button        = 0;
int   setting       = 0;
char  hex[5];
char  inAddress[3];
char  inCheck[13];
char  inData[5];
char  inFunction[3];
char  inLRC[3];
char  inRaw[numChars];
char  inRegister[5];
char  reply[18];
char  settings[9];

bool  pressureType  = 0; // default to psi

//Powermax 65 - setup is always psi
float nPressureMax = 78.0;
float nPressureMin = 63.0;
float gPressureMax = 58.0;
float gPressureMin = 43.0;

float cCurrentMax  = 65.0;
float cCurrentMin  = 20.0;
float cPressureMax = nPressureMax;
float cPressureMin = nPressureMin;
float cCurrent     = 41;
float cPressure    = 75;
float oldCurrent   = cCurrent;
float oldPressure  = cPressure;
