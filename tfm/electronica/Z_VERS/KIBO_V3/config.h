//     VCC ---------- 3.3V
//     SCL ---------- 18
//     SDA ---------- 23
//     RES ---------- 21
//.    RES2 --------- 27
//     DC  ---------- 26
//     BLK ---------- VIN

#include "ojoKibo.h"        // KIBO

// DISPLAY HARDWARE SETTINGS (screen type & connections) -------------------
#define TFT_COUNT 1         // Number of screens (Dual eye LCD is 1 display)
#define TFT1_CS 5           // TFT 1 chip select pin (set to -1 to use TFT_eSPI setup)
#define TFT2_CS 2           // TFT 2 chip select pin (set to -1 to use TFT_eSPI setup)
#define TFT_1_ROT 1         // TFT 1 rotation
#define TFT_2_ROT 3         // TFT 2 rotation
#define EYE_1_XPOSITION 20  // x shift for eye 1 image on display
#define EYE_2_XPOSITION 20  // x shift for eye 2 image on display

// EYE LIST ----------------------------------------------------------------
#define NUM_EYES 2  // Number of eyes to display (1 or 2)
//#define LH_WINK_PIN -1  // Left wink pin (set to -1 for no pin)
//#define RH_WINK_PIN -1  // Right wink pin (set to -1 for no pin)

eyeInfo_t eyeInfo[] = {
  { TFT1_CS, -1, TFT_1_ROT, EYE_1_XPOSITION },  // LEFT EYE chip select and wink pins, rotation and offset
  { TFT2_CS, -1, TFT_2_ROT, EYE_2_XPOSITION },  // RIGHT EYE chip select and wink pins, rotation and offset
};

//#define TRACKING   // If defined, eyelid tracks pupil
#define AUTOBLINK  // If defined, eyes also blink autonomously