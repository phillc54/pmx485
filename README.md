# pmx485

Uses an Arduino with a LCD Keypad Shield to emulate a Powermax for testing RS485 comms.

Comms Pins:
0 = RX Data             // MAX485 pin 1
1 = TX Data             // MAX485 pin 4
2 = RX Mode             // MAX485 pin 2 & 3 - RX when LOW, TX when HIGH

Input Pins:
11 = Arc OK             // GND to activate
12 = Arc On             // GND to activate

Output Pins:
3 = PWM Current Set     // 0% at minimum current, 100% at maximum current