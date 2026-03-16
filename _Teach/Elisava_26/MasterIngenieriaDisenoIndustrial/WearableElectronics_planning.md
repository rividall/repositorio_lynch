# Arduino-Controlled Wearables
## Master in Industrial Design Engineering - ELISAVA 2026

---

## Course Overview

**Program:** Master in Industrial Design Engineering
**Focus:** Wearable development with Arduino, velostat & conductive thread
**Duration:** 12 hours across 5 class days (spread over ~2 months)
**Class Size:** ~15 students (Master's level, design engineering background)
**Goal:** Students learn to design and build functional wearable electronics that sense body input (pressure, stretch, touch) using soft/textile sensors and Arduino, culminating in a working wearable prototype

**Core Philosophy:** Wearables sit at the intersection of electronics, materials, and the body. Students won't just learn circuits; they'll learn to think about electronics as something that bends, stretches, and lives on skin and fabric. Mistakes and ugly prototypes are part of the process. A working ugly thing beats a beautiful dead thing every time.

**Format:** Classes are spread across two months. Students have significant time between sessions to work on their projects at home. In-class time focuses on delivering content, hands-on exercises, and monitoring progress. The homework gap is a feature, not a bug: students internalize concepts by wrestling with their projects independently.

---

## SESSION BREAKDOWN

| Day | Hours | Type | Focus |
|-----|-------|------|-------|
| **Day 1** | 2h | Theory | Intro, instructor's work, what is Arduino, electronics fundamentals, wearable materials |
| **Day 2** | 2h | Practical | First circuits, velostat sensors, conductive thread basics |
| **Day 3** | 4h | Practical | Wearable design thinking, reactive systems, actuators, building the wearable |
| **Day 4** | 2h | Follow-up | Troubleshooting, refinement, individual feedback |
| **Day 5** | 2h | Follow-up | Final troubleshooting, mini-showcase & critique |

**Total: 12 hours**

---

## DAY 1: THEORY (2 hours)
*"Why wearables? Why Arduino? Why you?"*

### Learning Objectives
- Understand where wearable electronics sit in industrial design practice
- Know what Arduino is, what it can and can't do
- Grasp fundamental electronics concepts (voltage, current, resistance, digital vs analog)
- Get inspired by real-world wearable projects and the instructor's own work
- Understand the key materials: velostat, conductive thread, conductive fabric

### Session Outline

#### **0:00 - 0:15 | Welcome & Context** (15 min)
- Who am I, what's my background
- Course goals and what we'll build over 12 hours
- How this connects to the Master's program and industrial design practice
- Expectations: this is hands-on, messy, iterative
- Course timeline: 5 sessions over 2 months, expect to work at home between classes

#### **0:15 - 0:40 | My Work & The Wearable Landscape** (25 min)
- Instructor's portfolio: relevant wearable/electronic projects
- State of wearable tech in design (beyond smartwatches)
- Key references and inspirations:
  - E-textile pioneers (Kobakant, Liza Stark, Plusea)
  - Fashion tech (CuteCircuit, Studio Roosegaarde)
  - Medical/sport wearables
  - Soft robotics crossover
- The design opportunity: what's NOT been done yet

#### **0:40 - 1:10 | What is Arduino? Electronics Fundamentals** (30 min)
- Arduino = microcontroller + IDE + ecosystem
- The programming model: `setup()` runs once, `loop()` runs forever
- Digital vs Analog: on/off vs a range of values
- **Key concepts for wearables:**
  - Voltage (5V world), Current (mA), Resistance (ohms)
  - Ohm's Law (V = I × R) -- just enough to not fry things
  - Pull-up and pull-down resistors (why they matter for sensors)
  - Analog read (0-1023) and how that maps to sensor data
  - PWM for controlling output intensity
- GPIO pins: which ones do what (digital, analog, PWM)

#### **1:10 - 1:35 | Wearable-Specific Materials** (25 min)
- **Velostat:** what it is, how it works (pressure-sensitive conductive sheet)
  - Resistance drops under pressure
  - How to build a pressure sensor with it
  - Applications: foot pressure, grip force, body contact
- **Conductive thread:** what it is, properties, limitations
  - It's thread that conducts electricity (stainless steel fiber)
  - Resistance per meter matters (varies by brand)
  - Sewing vs traditional wiring: trade-offs
  - Common failure points: knots, fraying, shorts from crossed paths
- **Other soft materials overview:** conductive fabric, copper tape, flex sensors
- **The body as context:** movement, sweat, stretch, comfort constraints

#### **1:35 - 1:55 | Course Roadmap & Project Brief** (20 min)
- What you'll build: a wearable that senses body input and responds
- Walk through the 5-day arc: theory → first circuits → big build day → refine → showcase
- Show 1-2 completed wearable examples (instructor-made)
- Brief project constraints: must use velostat or conductive thread, must be wearable, must sense and respond
- Open discussion: what excites you? What scares you?

#### **1:55 - 2:00 | Wrap-up & Homework** (5 min)
- **Before Day 2:**
  - Install Arduino IDE 2.x + test Blink sketch upload
  - Start thinking: what body input is interesting to sense? (pressure, stretch, touch, proximity)
  - Browse Kobakant's How To Get What You Want for inspiration
  - Bring laptop + charger to every session
- Q&A

### Day 1 Deliverable
- Arduino IDE installed and tested (homework)
- Initial ideas forming about wearable concept

---

## DAY 2: PRACTICAL - First Circuits & Soft Sensors (2 hours)
*"Get electricity flowing through thread and foam"*

### Learning Objectives
- Build a working circuit on a breadboard
- Construct a velostat pressure sensor from scratch
- Sew a basic conductive thread circuit
- Read analog sensor values on Arduino

### Session Outline

#### **0:00 - 0:10 | Setup & Quick Recap** (10 min)
- Verify Arduino IDE installs
- Distribute component kits
- Quick recap of key concepts from Day 1

#### **0:10 - 0:35 | Exercise 1: Hello Arduino** (25 min)
- Upload Blink sketch, verify hardware works
- Modify blink timing (understand delay, digital write)
- Read a potentiometer value via analogRead() + Serial Monitor
- **Key takeaway:** input goes in, numbers come out, you decide what to do with them

#### **0:35 - 1:05 | Exercise 2: Build a Velostat Pressure Sensor** (30 min)
- Materials: velostat sheet, conductive fabric/copper tape electrodes, wires
- Construction:
  1. Cut two electrode pieces (conductive fabric or copper tape)
  2. Place velostat between electrodes (sandwich)
  3. Attach wires to each electrode
  4. Connect as voltage divider with a fixed resistor
- Wire to Arduino analog pin
- Read pressure values in Serial Monitor
- Calibration: find your min/max range, use map() function
- **Hands-on challenge:** make an LED brightness respond to squeeze pressure

#### **1:05 - 1:15 | BREAK** (10 min)

#### **1:15 - 1:50 | Exercise 3: Conductive Thread Basics** (35 min)
- Threading a needle with conductive thread
- Basic running stitch on fabric
- Creating a simple LED circuit sewn onto fabric:
  1. Sew from battery holder (+) pad to LED (+) leg
  2. Sew from LED (-) leg back to battery holder (-)
  3. Keep thread paths separate (no shorts!)
- **Critical lessons:**
  - Tie secure knots (thread unravels easily)
  - Leave enough slack for fabric movement
  - Test continuity with multimeter as you sew
  - Insulate crossings with fabric glue or felt patches
- **Hands-on challenge:** sew a working LED circuit on a fabric swatch

#### **1:50 - 2:00 | Wrap-up & Homework** (10 min)
- Discuss: how could these sensors live on the body?
- **Before Day 3 (students have weeks to work on this):**
  - Sketch 2-3 ideas for your wearable project (where on body, what it senses, what it outputs)
  - Bring a garment or fabric piece you want to build on
  - Practice sewing with conductive thread at home if you have materials
  - Optional: experiment with your velostat sensor, try different pressure configurations

### Day 2 Deliverable
- Working velostat pressure sensor connected to Arduino
- Sewn LED circuit on fabric swatch
- 2-3 wearable project sketches (homework, due Day 3)

---

## DAY 3: PRACTICAL - Design, Systems & Build (4 hours)
*"From concept to wearable in one long session"*

This is the big day. Four hours to go from project concept through reactive electronics to actual construction on fabric. The longer session format lets students hit a flow state and make real progress.

### Learning Objectives
- Think critically about wearable placement, ergonomics, and interaction design
- Combine sensor input with meaningful output (LEDs, vibration, NeoPixels)
- Code conditional behaviors and sensor-to-output mapping
- Plan and begin building a wearable circuit on fabric/garment
- Transfer electronics from breadboard to textile

### Session Outline

#### **0:00 - 0:15 | Project Concept Share** (15 min)
- Quick round: each student shares their wearable concept (30 sec each)
- Show sketches from homework
- Instructor flags feasibility issues early
- Group students with similar concepts for peer support

#### **0:15 - 0:45 | Wearable Design Thinking** (30 min)
- **Where on the body?**
  - Ergonomics of sensor placement (joints, flat surfaces, pressure points)
  - High-movement vs low-movement zones
  - Comfort: weight distribution, friction, heat
- **The hard-soft interface:**
  - Connecting rigid electronics (Arduino, battery) to flexible textiles
  - Mounting strategies: pockets, velcro, clips, sewn sleeves
  - Strain relief at transition points
- **Interaction design for wearables:**
  - Intentional input vs passive sensing
  - Feedback modalities: visual (LEDs), haptic (vibration), audio
  - Social context: is it visible? Is it subtle?
- **Power for wearables:**
  - Battery options: LiPo, coin cell, small USB power bank
  - Weight and placement considerations
  - Runtime estimation
- **Case studies:** what works, what fails, why
- **Refine your concept** based on this discussion: update your sketch with specific sensor locations, Arduino placement, and output locations

#### **0:45 - 1:15 | Exercise 4: Sensor-to-Output Mapping** (30 min)
- Take your velostat sensor from Day 2
- Code reactive behaviors:
  - **Threshold triggering:** if pressure > 500, turn on LED
  - **Proportional mapping:** map pressure range to LED brightness (analogWrite + PWM)
  - **Multi-zone:** different pressure ranges trigger different behaviors
- Add a vibration motor:
  - Wiring: transistor as switch (NPN + diode for back-EMF)
  - Control with digitalWrite or analogWrite for intensity
- **Concept:** input → processing → output (the fundamental loop)

#### **1:15 - 1:45 | Exercise 5: NeoPixels on Wearables** (30 min)
- WS2812 / NeoPixel strips and rings for wearable output
- Wiring: 5V, GND, Data
- FastLED or Adafruit NeoPixel library
- Color modes that respond to body input:
  - Pressure → color shift (calm blue to alert red)
  - Touch → sparkle effect
  - Sustained pressure → breathing/pulsing pattern
- Discuss: sewing NeoPixels onto fabric (needle + conductive thread to pads)

#### **1:45 - 2:00 | BREAK** (15 min)

#### **2:00 - 2:25 | Plan Your Wearable Circuit** (25 min)
- Each student maps out their project:
  1. **Sensor plan:** what velostat/conductive thread sensors, where on body
  2. **Arduino placement:** where does the board live?
  3. **Output plan:** what actuators, where on the garment
  4. **Wiring diagram:** sketch the connections (on paper)
  5. **Thread routing:** plan sewn paths that don't cross
- **Instructor circulates for 1-on-1 feedback and approval**
- Identify any additional materials needed

#### **2:25 - 3:05 | Build Sprint Part 1: Sensors & Thread Paths** (40 min)
- **Priority 1:** Build and mount velostat sensors on garment
  - Cut sensor to size
  - Attach electrodes
  - Position on garment, secure with stitching or fabric glue
- **Priority 2:** Sew conductive thread paths
  - From sensors to Arduino connection point
  - Keep paths separated (insulate crossings!)
  - Test continuity as you go (multimeter is your best friend)
- **Common pitfalls to watch for:**
  - Thread too loose (intermittent connection)
  - Thread too tight (tears fabric when worn)
  - Crossed thread paths (short circuits)
  - Knots coming undone

#### **3:05 - 3:45 | Build Sprint Part 2: Electronics & Output** (40 min)
- Mount Arduino (velcro, pocket, armband sleeve, clip)
- Connect actuators (LEDs, NeoPixels, vibration motors)
- Wire sensor thread paths to Arduino pins (alligator clips to thread, or sew to breakout pads)
- Upload code, test on body
- **The hard-soft interface in practice:**
  - Alligator clips for prototyping (fast, removable)
  - Sewing directly to header pins (more permanent)
  - Snap connectors (ideal but need prep)
  - Conductive epoxy for permanent bonds

#### **3:45 - 4:00 | Testing & Wrap-up** (15 min)
- Put it on! First on-body test
- Calibrate sensor values for actual body use (different from table testing!)
- Quick code adjustments
- Document current state with photos
- **Before Day 4 (students have weeks):**
  - Continue building and refining at home
  - Come to Day 4 with a working prototype (even if rough)
  - Bring a specific list of problems/questions
  - Polish code: add comments, clean up, name constants

### Day 3 Deliverable
- Refined project concept with design rationale
- Working sensor → actuator system (at minimum on breadboard)
- Wearable construction started (at minimum sensors mounted)
- Clear build plan for continued work at home

---

## DAY 4: FOLLOW-UP - Troubleshooting & Refinement (2 hours)
*"Fix it, refine it, make it yours"*

By Day 4, students have had weeks to work on their wearables at home. They'll arrive at very different stages. Some will have polished prototypes, others will have hit walls. This session is about unblocking everyone and pushing quality forward.

### Learning Objectives
- Debug and resolve hardware/software issues
- Refine sensor calibration for real-world use
- Polish code and interaction behavior
- Improve physical construction and comfort

### Session Outline

#### **0:00 - 0:20 | Status Check & Triage** (20 min)
- Each student: what's working, what's broken, what do you need help with
- Quick show-and-tell: put it on, show what happens
- Instructor triages: quick fixes vs deep dives vs "let's rethink this"
- Pair students with similar issues for peer debugging

#### **0:20 - 1:00 | Guided Troubleshooting & Work Time** (40 min)
- **Instructor rotates between students/groups**
- Common issues and solutions:

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| Sensor reads 0 or 1023 constantly | Broken thread, loose connection | Check continuity, resew |
| Values are noisy/jumping | Poor contact, no smoothing | Add averaging in code, better electrode contact |
| LEDs flicker | Power issue, loose data wire | Check power, add capacitor, secure connections |
| Vibration motor doesn't start | Not enough current from pin | Use transistor circuit, check wiring |
| Conductive thread breaks | Too tight, friction point | Resew with slack, reinforce stress points |
| Short circuit | Crossed thread paths | Insulate with fabric glue, felt, or tape |
| Code compiles but behavior is wrong | Logic error, wrong pin number | Serial.println() debug, check pin assignments |
| Works on table, dies on body | Movement breaks connection | Add strain relief, test while wearing |

- **Mini-lectures on demand** (5-10 min each, if enough students need them):
  - "Smoothing noisy sensor data" (running average, median filter)
  - "Power management for wearables" (battery selection, sleep modes)
  - "Making it comfortable" (strain relief, soft enclosures, padding)
  - "Going wireless" (ESP32 as upgrade path, Bluetooth basics)

#### **1:00 - 1:10 | BREAK** (10 min)

#### **1:10 - 1:55 | Continued Work & Refinement** (45 min)
- Students continue building/fixing
- Focus areas:
  - Code polish: clean comments, named constants, smooth transitions
  - Physical polish: hide wires, secure components, improve fit
  - Behavior refinement: adjust thresholds, add states, improve responsiveness
- Instructor available for 1-on-1 consults

#### **1:55 - 2:00 | Wrap-up** (5 min)
- Status update: who's on track, who needs extra support before Day 5
- **Before Day 5:**
  - Finish your prototype. Day 5 = showcase day.
  - Prepare a 2-minute demo explanation
  - Charge batteries, test everything one last time at home

### Day 4 Deliverable
- Improved, more robust wearable prototype
- Cleaner code with comments
- Clear plan for final polish before Day 5

---

## DAY 5: FOLLOW-UP - Final Session & Mini-Showcase (2 hours)
*"Show what you built, share what you learned"*

### Learning Objectives
- Resolve any last remaining technical issues
- Present and demonstrate wearable projects
- Reflect on the design process and learnings
- Understand next steps for further development

### Session Outline

#### **0:00 - 0:30 | Final Build Time** (30 min)
- Last round of fixes, improvements, polish
- Instructor prioritizes students who are stuck
- Help with final calibration and testing on-body
- Everyone should have a functioning demo by 0:30

#### **0:30 - 0:40 | Prep for Showcase** (10 min)
- Structure your 2-minute demo:
  1. **What is it?** (10 sec) -- describe the wearable
  2. **Put it on and demo** (30 sec) -- show the interaction live
  3. **How does it work?** (30 sec) -- sensor/Arduino/output chain
  4. **Design decisions** (30 sec) -- why this placement, this material, this behavior
  5. **What would you improve?** (20 sec) -- honest reflection

#### **0:40 - 1:20 | Mini-Showcase** (40 min)
- Each student presents (~2-3 min + 1-2 min Q&A)
- Audience members try on/interact with projects (with permission)
- Instructor and peers give constructive feedback
- Document everything: photos, video

#### **1:20 - 1:30 | BREAK** (10 min)

#### **1:30 - 1:50 | Group Discussion & Reflection** (20 min)
- What was hardest about wearable electronics vs traditional circuits?
- What surprised you about working with the body as context?
- How does this connect to your industrial design practice?
- Where could this go? (medical, sport, fashion, safety, art)
- Next steps: ESP32, Bluetooth wearables, PCB design, e-textile advanced techniques

#### **1:50 - 2:00 | Feedback & Close** (10 min)
- Feedback form
- Share resources list (libraries, suppliers, communities)
- Group photo
- Take your wearable home!

### Day 5 Deliverable
- Demonstrated wearable prototype
- 2-minute presentation delivered
- Feedback form completed

---

## BILL OF MATERIALS

### Per Student Kit:

**Electronics:**
- 1x Arduino Uno R3 (or Nano for smaller wearable footprint)
- 1x USB cable (A-to-B for Uno, micro-USB for Nano)
- 1x Small breadboard (170 or 400 tie-point)
- 5-8x WS2812 NeoPixel LEDs (strip segment or individual)
- 1x Vibration motor (coin type, 3V)
- 1x NPN transistor (2N2222 or similar) + 1x 1N4001 diode (for motor)
- 2x 10kΩ resistors (pull-down for sensors)
- 10x Jumper wires (male-to-male)
- 5x Alligator clip wires (for thread-to-Arduino connection)
- 1x USB power bank (small, lightweight)

**Soft/Textile Materials:**
- 1x Velostat sheet (~15x15 cm per student, cut from larger sheet)
- 1x Conductive thread spool (shared, ~2-3m per student)
- 2x Conductive fabric patches (~5x5 cm, for electrodes)
- 1x Copper tape strip (~30 cm, for quick electrode prototyping)

**Consumables:**
- Sewing needles (sharp, with eyes large enough for conductive thread)
- Regular thread (for structural sewing)
- Fabric scraps (felt works great for prototyping)
- Fabric glue
- Velcro strips (for mounting Arduino)
- Safety pins, snap buttons
- Electrical tape, heat shrink tubing

### Shared Materials (for class of 15):

**Tools:**
- 5x Scissors (fabric scissors preferred)
- 3x Wire cutters/strippers
- 3x Multimeters (continuity testing is critical!)
- 2x Hot glue guns + sticks
- 1x Soldering iron + solder (optional, for permanent connections)
- Needle-nose pliers
- Rulers, markers

**Classroom:**
- Extension cords, power strips
- Paper towels, trash bags

---

## PRE-COURSE PREPARATION

### 2 Weeks Before Day 1:

**Instructor:**
- [ ] Build 1-2 complete wearable examples yourself
- [ ] Test all exercises end-to-end
- [ ] Prepare component kits (one bag per student)
- [ ] Cut velostat sheets to size
- [ ] Prepare conductive fabric electrode patches
- [ ] Test Arduino IDE on classroom computers
- [ ] Prepare code examples and starter sketches
- [ ] Print/prepare wiring diagrams for exercises

**Send to Students (1 week before Day 1):**
- [ ] Install Arduino IDE 2.x
- [ ] Test Blink sketch upload
- [ ] Bring laptop + charger to every session
- [ ] Optional: bring fabric scissors if you have them

---

## STUDENT PRE-COURSE CHECKLIST

### Part 1: Arduino IDE Installation (30 min)

1. Go to https://www.arduino.cc/en/software
2. Download Arduino IDE 2.x for your OS
3. Install and open it
4. Connect Arduino via USB
5. Select board (Arduino Uno) and port
6. Upload Examples → Basics → Blink
7. Verify the onboard LED blinks

### Part 2: Prepare Your Fabric (bring to Day 3)

Bring ONE of these:
- A glove you don't mind modifying
- An old t-shirt sleeve
- A fabric armband or wristband
- A piece of felt (at least 20x20 cm)
- Any garment piece you want to make "smart"

Think about: **where on the body** would be interesting to sense pressure or touch?

---

## KEY DIFFERENCES FROM PREVIOUS WORKSHOP

| Aspect | Plant Sculptures Workshop | Wearable Electronics |
|--------|--------------------------|---------------------|
| Context | Table-top, static display | Body-worn, moving |
| Sensors | Ultrasound (distance) | Velostat (pressure), conductive thread (touch) |
| Output | WS2812 LED strips | LEDs, NeoPixels, vibration motors |
| Construction | 3D printing + hot glue | Sewing + textile integration |
| Power | USB/wall adapter | Battery pack (portability required) |
| Challenges | Mechanical assembly | Soft circuit reliability, body ergonomics |
| Testing | On table | On body (completely different!) |
| Duration | 16h in 1 week | 12h over 2 months |
| Student work outside class | Minimal | Significant (projects evolve between sessions) |

---

## INSTRUCTOR NOTES

### Pacing & Format
- The 2-month spread is an advantage. Students absorb theory, then have time to experiment at home before the next class.
- Day 3 (4 hours) is the critical session. This is where design thinking, reactive systems, and actual construction all converge. Protect this session.
- Days 4-5 are for monitoring, not teaching. Your job is to unblock students and push quality. Expect wide variation in progress.
- Set clear homework expectations between sessions. Students who don't work at home will struggle on Day 4.

### Common Failure Modes (Wearable-Specific)
1. **Conductive thread shorts** -- Thread paths crossing = circuit death. Drill this into students early.
2. **Loose knots** -- Conductive thread is slippery. Teach secure knotting technique.
3. **Velostat inconsistency** -- Pressure response varies. Each sensor needs individual calibration.
4. **Body movement breaks connections** -- Everything works on the table, nothing works when worn. Build in test-while-wearing time.
5. **Power issues** -- Wearables need portable power. Don't let students rely on USB-to-laptop during build.

### What Success Looks Like
- **Minimum viable:** A velostat sensor sewn onto fabric, wired to Arduino, controlling an LED. Student can explain how it works.
- **Good outcome:** Multiple sensors, coded behaviors (thresholds/mapping), clean thread paths, comfortable to wear.
- **Exceptional:** Polished interaction design, multiple output modes, considered ergonomics, interesting concept.

---

## RESOURCES TO SHARE WITH STUDENTS

**References:**
- Kobakant: How To Get What You Want (e-textile encyclopedia) -- https://www.kobakant.at/DIY/
- Liza Stark's e-textile tutorials
- Adafruit wearable electronics guides
- Plusea's instructables

**Suppliers (EU-friendly):**
- Adafruit (via EU distributors)
- Sparkfun
- Kitronik (UK/EU)
- Statex (conductive textiles)

**Libraries:**
- FastLED (WS2812 control)
- Adafruit NeoPixel (alternative)

---

**Document Version:** 1.1
**Last Updated:** March 2026
**Course:** Master in Industrial Design Engineering - ELISAVA
