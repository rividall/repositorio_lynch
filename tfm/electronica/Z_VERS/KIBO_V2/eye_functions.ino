void initEyes(void) {
  Serial.println("Initialise eye objects");
  // Initialise eye objects based on eyeInfo list in config.h:
  for (uint8_t e = 0; e < NUM_EYES; e++) {
    Serial.print("Create display #");
    Serial.println(e);

    eye[e].tft_cs = eyeInfo[e].select;
    eye[e].blink.state = NOBLINK;
    eye[e].xposition = eyeInfo[e].xposition;

    pinMode(eye[e].tft_cs, OUTPUT);
    digitalWrite(eye[e].tft_cs, LOW);
  }
}

void updateEye(void) {
  frame(37);
}

// EYE-RENDERING FUNCTION --------------------------------------------------
void drawEye(  // Renders one eye.  Inputs must be pre-clipped & valid.
  // Use native 32 bit variables where possible as this is 10% faster!
  uint8_t e,         // Eye array index; 0 or 1 for left/right
  uint32_t iScale,   // Scale factor for iris
  uint32_t scleraX,  // First pixel X offset into sclera image
  uint32_t scleraY,  // First pixel Y offset into sclera image
  uint32_t uT,       // Upper eyelid threshold value
  uint32_t lT) {     // Lower eyelid threshold value

  uint32_t screenX, screenY, scleraXsave;
  int32_t irisX, irisY;
  uint32_t p, a;
  uint32_t d;

  uint32_t pixels = 0;

  // Set up raw pixel dump to entire screen.  Although such writes can wrap
  // around automatically from end of rect back to beginning, the region is
  // reset on each frame here in case of an SPI glitch.
  digitalWrite(eye[e].tft_cs, LOW);
  // tft.startWrite();
  tft.setAddrWindow(eye[e].xposition, 0, 128, 128);

  // Now just issue raw 16-bit values for every pixel...

  scleraXsave = scleraX;  // Save initial X value to reset on each line
  irisY = scleraY - (SCLERA_HEIGHT - IRIS_HEIGHT) / 2;

  // Eyelid image is left<>right swapped for two displays
  uint16_t lidX = 0;
  uint16_t dlidX = -1;
  if (e) dlidX = 1;
  for (screenY = 0; screenY < SCREEN_HEIGHT; screenY++, scleraY++, irisY++) {
    scleraX = scleraXsave;
    irisX = scleraXsave - (SCLERA_WIDTH - IRIS_WIDTH) / 2;
    if (e) lidX = 0;
    else lidX = SCREEN_WIDTH - 1;
    for (screenX = 0; screenX < SCREEN_WIDTH; screenX++, scleraX++, irisX++, lidX += dlidX) {
      if ((pgm_read_byte(lower + screenY * SCREEN_WIDTH + lidX) <= lT) || (pgm_read_byte(upper + screenY * SCREEN_WIDTH + lidX) <= uT)) {  // Covered by eyelid
        p = 0;
      } else if ((irisY < 0) || (irisY >= IRIS_HEIGHT) || (irisX < 0) || (irisX >= IRIS_WIDTH)) {  // In sclera
        p = pgm_read_word(sclera + scleraY * SCLERA_WIDTH + scleraX);
      } else {                                                           // Maybe iris...
        p = pgm_read_word(polar + irisY * IRIS_WIDTH + irisX);           // Polar angle/dist
        d = (iScale * (p & 0x7F)) / 128;                                 // Distance (Y)
        if (d < IRIS_MAP_HEIGHT) {                                       // Within iris area
          a = (IRIS_MAP_WIDTH * (p >> 7)) / 512;                         // Angle (X)
          p = pgm_read_word(iris + d * IRIS_MAP_WIDTH + a);              // Pixel = iris
        } else {                                                         // Not in iris
          p = pgm_read_word(sclera + scleraY * SCLERA_WIDTH + scleraX);  // Pixel = sclera
        }
      }
      *(&pbuffer[dmaBuf][0] + pixels++) = p >> 8 | p << 8;

      if (pixels >= BUFFER_SIZE) {
        yield();
#ifdef USE_DMA
        tft.pushPixelsDMA(&pbuffer[dmaBuf][0], pixels);
        dmaBuf = !dmaBuf;
#else
        tft.pushPixels(pbuffer, pixels);
#endif
        pixels = 0;
      }
    }
  }

  if (pixels) {
#ifdef USE_DMA
    tft.pushPixelsDMA(&pbuffer[dmaBuf][0], pixels);
#else
    tft.pushPixels(pbuffer, pixels);
#endif
  }
  tft.endWrite();
  digitalWrite(eye[e].tft_cs, HIGH);
}
// EYE ANIMATION -----------------------------------------------------------
const uint8_t ease[] = {                                                           // Ease in/out curve for eye movements 3*t^2-2*t^3
  0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 3,                                  // T
  3, 3, 4, 4, 4, 5, 5, 6, 6, 7, 7, 8, 9, 9, 10, 10,                                // h
  11, 12, 12, 13, 14, 15, 15, 16, 17, 18, 18, 19, 20, 21, 22, 23,                  // x
  24, 25, 26, 27, 27, 28, 29, 30, 31, 33, 34, 35, 36, 37, 38, 39,                  // 2
  40, 41, 42, 44, 45, 46, 47, 48, 50, 51, 52, 53, 54, 56, 57, 58,                  // A
  60, 61, 62, 63, 65, 66, 67, 69, 70, 72, 73, 74, 76, 77, 78, 80,                  // l
  81, 83, 84, 85, 87, 88, 90, 91, 93, 94, 96, 97, 98, 100, 101, 103,               // e
  104, 106, 107, 109, 110, 112, 113, 115, 116, 118, 119, 121, 122, 124, 125, 127,  // c
  128, 130, 131, 133, 134, 136, 137, 139, 140, 142, 143, 145, 146, 148, 149, 151,  // J
  152, 154, 155, 157, 158, 159, 161, 162, 164, 165, 167, 168, 170, 171, 172, 174,  // a
  175, 177, 178, 179, 181, 182, 183, 185, 186, 188, 189, 190, 192, 193, 194, 195,  // c
  197, 198, 199, 201, 202, 203, 204, 205, 207, 208, 209, 210, 211, 213, 214, 215,  // o
  216, 217, 218, 219, 220, 221, 222, 224, 225, 226, 227, 228, 228, 229, 230, 231,  // b
  232, 233, 234, 235, 236, 237, 237, 238, 239, 240, 240, 241, 242, 243, 243, 244,  // s
  245, 245, 246, 246, 247, 248, 248, 249, 249, 250, 250, 251, 251, 251, 252, 252,  // o
  252, 253, 253, 253, 254, 254, 254, 254, 254, 255, 255, 255, 255, 255, 255, 255
};  // n
#ifdef AUTOBLINK
uint32_t timeOfLastBlink = 0L, timeToNextBlink = 0L;
#endif
// Process motion for a single frame of left or right eye
void frame(uint16_t iScale)  // Iris scale (0-1023)
{
  static uint32_t frames = 0;   // Used in frame rate calculation
  static uint8_t eyeIndex = 0;  // eye[] array counter
  int16_t eyeX, eyeY;
  uint32_t t = micros();  // Time at start of function

  if (++eyeIndex >= NUM_EYES) eyeIndex = 0;  // Cycle through eyes, 1 per call


// XY MOTION

static bool eyeInMotion = false;
  static int16_t eyeOldX = 512, eyeOldY = 512, eyeNewX = 512, eyeNewY = 512;
  static uint32_t eyeMoveStartTime = 0L;
  static int32_t eyeMoveDuration = 0L;

  // New: pot tracking state
  static int lastPotValue = -1;
  static uint32_t potHoldStartTime = 0;
  static bool trackingPot = false;

  int currentPotValue = analogRead(POT_PIN);
  currentPotValue = map(currentPotValue, 0, 4096, 0, 1023);

  // Detect pot change (with threshold)
  if (abs(currentPotValue - lastPotValue) > 55) {
    trackingPot = true;
    potHoldStartTime = millis();
    eyeNewX = currentPotValue;
    eyeNewY = 32;  // You can adjust this or make Y responsive too
    lastPotValue = currentPotValue;
  }

  // If 10 seconds passed, stop tracking
  if (trackingPot && (millis() - potHoldStartTime > 6000)) {
    trackingPot = false;
  }

  int32_t dt = t - eyeMoveStartTime;  // uS elapsed since last eye event

  if (trackingPot) {
  eyeX = eyeNewX;
  eyeY = eyeNewY;
  eyeInMotion = false;  // Cancel any ongoing random movement
} else {
  if (eyeInMotion) {
    if (dt >= eyeMoveDuration) {
      eyeInMotion = false;
      eyeMoveDuration = random(3000000);  // 0-3 sec stop
      eyeMoveStartTime = t;
      eyeX = eyeOldX = eyeNewX;
      eyeY = eyeOldY = eyeNewY;
    } else {
      int16_t e = ease[255 * dt / eyeMoveDuration] + 1;
      eyeX = eyeOldX + (((eyeNewX - eyeOldX) * e) / 256);
      eyeY = eyeOldY + (((eyeNewY - eyeOldY) * e) / 256);
    }
  } else {
    eyeX = eyeOldX;
    eyeY = eyeOldY;
    if (dt > eyeMoveDuration) {
      int16_t dx, dy;
      uint32_t d;
      do {
        eyeNewX = random(1024);
        eyeNewY = random(1024);
        dx = (eyeNewX * 2) - 1023;
        dy = (eyeNewY * 2) - 1023;
      } while ((d = dx * dx + dy * dy) > (1023 * 1023));  // Stay within circle
      eyeMoveDuration = random(72000, 144000);
      eyeMoveStartTime = t;
      eyeInMotion = true;
    }
  }
}

// Blinking

#ifdef AUTOBLINK
  // Similar to the autonomous eye movement above -- blink start times
  // and durations are random (within ranges).
  if ((t - timeOfLastBlink) >= timeToNextBlink) {  // Start new blink?
    timeOfLastBlink = t;
    uint32_t blinkDuration = random(36000, 72000);  // ~1/28 - ~1/14 sec
    // Set up durations for both eyes (if not already winking)
    for (uint8_t e = 0; e < NUM_EYES; e++) {
      if (eye[e].blink.state == NOBLINK) {
        eye[e].blink.state = ENBLINK;
        eye[e].blink.startTime = t;
        eye[e].blink.duration = blinkDuration;
      }
    }
    timeToNextBlink = blinkDuration * 3 + random(4000000);
  }
#endif
  if (eye[eyeIndex].blink.state) {  // Eye currently blinking?
    // Check if current blink state time has elapsed
    if ((t - eye[eyeIndex].blink.startTime) >= eye[eyeIndex].blink.duration) {
      // Yes -- increment blink state, unless...
      if ((eye[eyeIndex].blink.state == ENBLINK) && (  // Enblinking and...
#if defined(BLINK_PIN) && (BLINK_PIN >= 0)
            (digitalRead(BLINK_PIN) == LOW) ||  // blink or wink held...
#endif
            ((eyeInfo[eyeIndex].wink >= 0) && digitalRead(eyeInfo[eyeIndex].wink) == LOW))) {
        // Don't advance state yet -- eye is held closed instead
      } else {                                        // No buttons, or other state...
        if (++eye[eyeIndex].blink.state > DEBLINK) {  // Deblinking finished?
          eye[eyeIndex].blink.state = NOBLINK;        // No longer blinking
        } else {                                      // Advancing from ENBLINK to DEBLINK mode
          eye[eyeIndex].blink.duration *= 2;          // DEBLINK is 1/2 ENBLINK speed
          eye[eyeIndex].blink.startTime = t;
        }
      }
    }
  } else {  // Not currently blinking...check buttons!
#if defined(BLINK_PIN) && (BLINK_PIN >= 0)
    if (digitalRead(BLINK_PIN) == LOW) {
      // Manually-initiated blinks have random durations like auto-blink
      uint32_t blinkDuration = random(36000, 72000);
      for (uint8_t e = 0; e < NUM_EYES; e++) {
        if (eye[e].blink.state == NOBLINK) {
          eye[e].blink.state = ENBLINK;
          eye[e].blink.startTime = t;
          eye[e].blink.duration = blinkDuration;
        }
      }
    } else
#endif
      if ((eyeInfo[eyeIndex].wink >= 0) && (digitalRead(eyeInfo[eyeIndex].wink) == LOW)) {  // Wink!
      eye[eyeIndex].blink.state = ENBLINK;
      eye[eyeIndex].blink.startTime = t;
      eye[eyeIndex].blink.duration = random(45000, 90000);
    }
  }

  // Process motion, blinking and iris scale into renderable values

  // Scale eye X/Y positions (0-1023) to pixel units used by drawEye()
  eyeX = map(eyeX, 0, 1023, 0, SCLERA_WIDTH - 128);
  eyeY = map(eyeY, 0, 1023, 0, SCLERA_HEIGHT - 128);

  // Horizontal position is offset so that eyes are very slightly crossed
  // to appear fixated (converged) at a conversational distance.  Number
  // here was extracted from my posterior and not mathematically based.
  // I suppose one could get all clever with a range sensor, but for now...
  if (NUM_EYES > 1) {
    if (eyeIndex == 1) eyeX += 4;
    else eyeX -= 4;
  }
  if (eyeX > (SCLERA_WIDTH - 128)) eyeX = (SCLERA_WIDTH - 128);

  // Eyelids are rendered using a brightness threshold image.  This same
  // map can be used to simplify another problem: making the upper eyelid
  // track the pupil (eyes tend to open only as much as needed -- e.g. look
  // down and the upper eyelid drops).  Just sample a point in the upper
  // lid map slightly above the pupil to determine the rendering threshold.
  static uint8_t uThreshold = 128;
  uint8_t lThreshold, n;
#ifdef TRACKING
  int16_t sampleX = SCLERA_WIDTH / 2 - (eyeX / 2),  // Reduce X influence
    sampleY = SCLERA_HEIGHT / 2 - (eyeY + IRIS_HEIGHT / 2);
  // Eyelid is slightly asymmetrical, so two readings are taken, averaged
  if (sampleY < 0) n = 0;
  else n = (pgm_read_byte(upper + sampleY * SCREEN_WIDTH + sampleX) + pgm_read_byte(upper + sampleY * SCREEN_WIDTH + (SCREEN_WIDTH - 1 - sampleX))) / 2;
  uThreshold = (uThreshold * 3 + n) / 4;  // Filter/soften motion divide by more to minimize upper lid?
  // Lower eyelid doesn't track the same way, but seems to be pulled upward
  // by tension from the upper lid.
  lThreshold = 254 - uThreshold;
#else  // No tracking -- eyelids full open unless blink modifies them
  uThreshold = lThreshold = 0;
#endif

  // The upper/lower thresholds are then scaled relative to the current
  // blink position so that blinks work together with pupil tracking.
  if (eye[eyeIndex].blink.state) {  // Eye currently blinking?
    uint32_t s = (t - eye[eyeIndex].blink.startTime);
    if (s >= eye[eyeIndex].blink.duration) s = 255;   // At or past blink end
    else s = 255 * s / eye[eyeIndex].blink.duration;  // Mid-blink
    s = (eye[eyeIndex].blink.state == DEBLINK) ? 1 + s : 256 - s;
    n = (uThreshold * s + 254 * (257 - s)) / 256;
    lThreshold = (lThreshold * s + 254 * (257 - s)) / 256;
  } else {
    n = uThreshold;
  }

  // Pass all the derived values to the eye-rendering function:
  drawEye(eyeIndex, iScale, eyeX, eyeY, n, lThreshold);

  if (eyeIndex == (NUM_EYES - 1)) {
    user_loop();  // Call user code after rendering last eye
  }
}