# 3D Printed Plant Light Sculptures Workshop
## Master's Level - Evening Schedule (5:00 PM - 9:00 PM)

---

## Workshop Overview

**Target Audience:** Master's students (AI-focused program, design background)  
**Duration:** 4 evening sessions, 4 hours each  
**Schedule:** 5:00 PM - 9:00 PM  

### What You'll Learn:
-  **Embedded systems** - Arduino microcontroller programming
-  **Physical computing** - Sensor integration and LED control
-  **Interaction design** - Creating responsive light behaviors
-  **Rapid prototyping** - 3D printing for functional enclosures
-  **Hardware/software integration** - Bridging digital and physical

**Final Deliverable:** An interactive plant light sculpture with custom code and 3D printed components

---

## Session Structure (Each Evening)

**5:00 - 5:10 PM:** Arrival & Setup (10 min)
**5:10 - 6:45 PM:** Main Session Block 1 (95 min)
**6:45 - 7:00 PM:** Break (15 min)
**7:00 - 9:00 PM:** Main Session Block 2 (120 min)

---

## SESSION 1: 3D Printing & Arduino Crash Course
*Evening 1: 5:00 PM - 9:00 PM*

### **5:00 - 5:10 PM: Setup & Introduction**

**Welcome & Context:**
- Workshop goals and deliverables
- Why physical computing matters for AI/design practitioners
- Safety briefing (electrical, hot tools, 3D printers)
- "Move fast, break things (safely), ask questions"

**Quick check:**
- Arduino IDE installed? ✓
- FastLED library installed? ✓
- Hardware kit received? ✓

---

### **5:10 - 5:30 PM: Ideation** (20 minutes)

**Co-create your plant using AI (or not):**

**What are we creating?** A plant with:
- Narrative → Design → Behavior → Light → Sound
- Each plant will have its own "Plant Soul Profile"

**Activities:**
1. **Plant Identity Generator** - Use AI prompts to generate your plant's personality, emotions, and name
2. **Extract Key Traits** - Plant name, personality (3 words), behavior when far/close
3. **Color Palette** - Primary, secondary, accent colors + mood
4. **Define Physical Constraints** - Max height 30cm, base 10-15cm, servo/LED/sensor locations
5. **Sketch** - Front view, side view, cavity for electronics
6. **Wrap-up prompt** - Generate exhibition label, sound description, interaction instruction

---

### **5:30 - 5:50 PM: 3D Printing Overview** (20 minutes)

**Quick primer (you know modeling, here's the hardware):**
- How FDM printing works (layer by layer)
- PLA material - easy to print, biodegradable
- Print time estimates and constraints

**Critical constraints:**
- **Print time:** Max 4-6 hours combined per student
- **⚠️ PRINTS MUST BE SUBMITTED BY 6:30 PM** (printer queue deadline)

---

### **5:50 - 6:30 PM: Part Selection & Design** (40 minutes)

**Curated plant parts library:**

**Categories:**
- **Bases/Pots** (FAST: 1-2hr) - Must fit Arduino + wires
- **Stems/Trunks** (FAST: 30min-1hr) - Hollow for LED routing
- **Leaves** (FAST: 15-30min each) - Print multiples!
- **Flowers/Decorative** (FAST: 20-45min) - Light diffusers

**Your assignment:**
Select parts totaling 4-6 hours print time:
- 1× Base (required)
- 2-3× Stems/structural
- 3-5× Leaves/decorative
- Optional: custom designed piece

**Activities:**
- Browse the parts catalog
- Plan your plant structure
- Check print time estimates
- Submit selections via form

---

### **📤 6:30 PM: PRINT SUBMISSION DEADLINE**

**Submit print queue via form:**
- Group name
- Part file names
- Any special notes (color, orientation)

---

### **6:30 - 6:45 PM: Q&A Buffer** (15 minutes)

- Final questions about 3D printing
- Prepare for electronics section
- Late submissions (if any issues)

---

### **6:45 - 7:00 PM: BREAK** ☕

---

### **7:00 - 7:20 PM: Arduino 101** (20 minutes)

**Quick overview:**
- Arduino = microcontroller + convenient IDE + vast ecosystem
- GPIO pins: Digital (HIGH/LOW), Analog (0-1023), PWM
- Programming model: `setup()` once, `loop()` forever

**First program - Blink**

**Upload and verify hardware works**

---

### **7:20 - 7:35 PM: Vibe Coding 101** (15 minutes)

**Your secret weapon: AI-assisted coding! 🤖**

You don't need to memorize syntax. You need to know *what's possible* and *how to ask*.

**The setup:**
1. Open your LLM of choice (Claude, ChatGPT, etc.)
2. Give it context about the library

**Starter prompt to copy:**
```
I'm using an Arduino Uno with WS2812 LED strips and the FastLED library.
Here's the library documentation: https://github.com/FastLED/FastLED

Help me write code to [describe what you want].
If you're unsure about something, check FastLED forums and GitHub issues for common solutions.
```

**Tips for good results:**
- Be specific: "rainbow that moves down the strip" > "cool colors"
- Describe the *behavior* you want, not the code
- If it doesn't work, paste the error message back
- Ask "what other effects can I do with FastLED?"

**🎯 Try it now:** Ask your LLM to explain what `CHSV` means and when to use it!

---

### **7:35 - 8:05 PM: WS2812 LEDs with FastLED** (30 minutes)

**Addressable LED introduction:**
- Each LED has a chip: individually controllable
- One data wire controls entire strip (daisy-chained)

**Basic wiring:**
- Red → 5V (power)
- White → GND (ground)
- Green → Pin 6 (data)
- **Arrow direction matters!** Data flows one way →

**First LED code: Turn LEDs on**

**Color exploration:**
- Named colors: `CRGB::Red`, `CRGB::Blue`, `CRGB::Purple`
- RGB values: `CRGB(255, 128, 0)` for orange
- HSV for easier color work: `CHSV(hue, 255, 255)`

---

### **8:05 - 8:50 PM: LED Patterns & Animation** (45 minutes)

**Core concepts to explore:**

**1. Rainbow generation:**
- Using CHSV for smooth hue transitions
- `fill_rainbow()` function

**2. Color palettes (built-in):**
- `RainbowColors_p`, `LavaColors_p`, `OceanColors_p`
- `ForestColors_p`, `PartyColors_p`, `HeatColors_p`
- Using `ColorFromPalette()`

**3. Temporal effects:**
- Breathing: `beatsin8()` for sine wave brightness
- Fading: `fadeToBlackBy()` for trailing effects
- Timing with `millis()` instead of `delay()`

**4. Spatial effects:**
- Waves: traveling patterns down the strip
- Chase: sequential LED activation
- Sparkles: random LED highlights

**🎯 Challenge:** Create 2-3 distinct "moods" for your plant!

---

### **8:50 - 9:00 PM: Wrap-up & Preview** (10 minutes)

**Save your work:**
- Use descriptive names ("session1_leds.ino")

**Your prints are running overnight!**

**Next Session Preview:**
- Adding sensors for interaction!
- Making your lights respond to the world
- 3D customization in Tinkercad
- Submit custom designs

---

## SESSION 2: 3D Customization & Code Refinement
*Evening 2: 5:00 PM - 9:00 PM*

### **5:00 - 5:15 PM: Print Reveal & Session Kickoff** (15 minutes)

**Print distribution:**
- Check print bin for your name
- Inspect print quality

**Session 2 goals:**
- Customize 3D parts in Tinkercad
- Submit custom designs for printing (before 6:30!)
- Refine and polish your code
- Test power supply integration

---

### **5:15 - 5:35 PM: Tinkercad Tutorial** (20 minutes)

**For those new to Tinkercad:**

**Basic operations:**
1. Navigation: Right-click drag (rotate), scroll (zoom), middle-click (pan)
2. Select objects: Click
3. Transform: Move, rotate, scale
4. Alignment tools: Align, group, ungroup
5. Export: Export → STL

**Key techniques:**
- **Scaling:** Maintain proportions (lock icon) or scale axes independently
- **Duplicating:** Ctrl+D (Cmd+D on Mac)
- **Grouping:** Select multiple → Group (critical before export!)

---

### **5:35 - 6:30 PM: 3D Design & Customization** (55 minutes)

**What to create/modify:**

**1. Structural parts:**
- Adjust stem heights to your desired plant size

**2. Decorative elements:**
- Customize leaf shapes
- Create custom flower/light diffuser shapes
- Consider translucency (thin walls = more light transmission)

**3. Advanced (optional):**
- Design completely original parts
- Integrated cable management systems

**Design review checkpoints:**
- Show your design on screen
- Explain how it will assemble
- Verify print time estimate
- Confirm you've checked all critical dimensions

---

### **📤 6:30 PM: CUSTOM DESIGN SUBMISSION DEADLINE**

- Export all parts as STL
- Upload to shared folder
- Prints start tonight

---

### **6:30 - 6:45 PM: Buffer / Power Supply Test** (15 minutes)

- Late design submissions (if any issues)
- Quick power supply test: Connect battery and verify LEDs work

---

### **6:45 - 7:00 PM: BREAK** ☕

---

### **7:00 - 7:30 PM: Adding Sensors!** (30 minutes)

**Now we make it interactive!**

#### **Sensor basics:**
- Ultrasound distance sensor wiring
- Reading analog values (0-1023)
- Serial Monitor for debugging (like print statements)

**Code example: Reading distance**

**Hands-on exercises:**
- Read sensor values in different conditions
- Calculate min/max ranges for your environment
- Understand the `map()` function

---

### **7:30 - 8:00 PM: Reactive Light Systems** (30 minutes)

**Combining sensor + LEDs:**

**Basic sensor-reactive brightness:**
- Connect sensor reading to LED brightness
- `map(sensorValue, minIn, maxIn, minOut, maxOut)`

**Challenges to explore:**

**🟢 Beginner: Brightness control**
- Distance controls LED brightness
- Close = bright, far = dim

**🟡 Intermediate: Color shift**
- Map sensor value to hue (0-255)
- Create smooth color transitions

**🔴 Expert: Multi-zone control**
- Different LED sections respond to different sensor ranges
- Create spatial patterns based on input

---

### **8:00 - 8:30 PM: Plant Reactions & Sound** (30 minutes)

**Give your plant a voice and behavior:**

**Define Reactions:** Complete a reaction table:
- No one nearby → Emotion → Action
- Someone approaches → Emotion → Action
- Very close → Emotion → Action

**Translate to Hardware:**
- Far away → soft light, no movement, slow breathing sound
- Close → brighter light, small movement, heartbeat sound
- Too close/threat → fast blinking, sharp sound, sudden movement

**Sound Menu - Choose Your Plant's Voice:**
- Pattern A: Breath/Wind (calm, friendly)
- Pattern B: Heartbeat (organic, emotional)
- Pattern C: Insect/Alert (nervous, defensive)
- Pattern D: Bloom/Reward (magical, joyful)

**Sound Rules:**
1. Garden Sound Hierarchy: 3 layers (Ambient, Interaction, Silence)
2. Each Plant Has ONE Main Sound: 1 dominant pattern + 1 special pattern

**Sound Motif Prompt:** Use AI to generate 3 short sound motifs, choose one as main identity

---

### **8:30 - 9:00 PM: Code Refinement** (30 minutes)

**Polish your code:**
- Clean up and add comments
- Create custom color palettes
- Optimize performance

#### **Instructor "Office Hours" - Mini Lectures on Demand:**

Available topics (5-10 min each):
- **"FastLED Performance Optimization"** - Achieve 60+ FPS
- **"Sensor Calibration"** - Auto-adjust to ambient conditions
- **"Power Budget"** - Calculate battery life, manage current draw
- **"Pattern Design"** - Creating compelling animations

**Expected outcomes by 9:00 PM:**
- Sensor-reactive LED system working!
- At least 2-3 distinct lighting behaviors
- Code saved with version control naming

---

**By 9:00 PM wrap-up:**
- Charge batteries overnight for Session 3
- Your custom prints are running overnight!

---

## SESSION 3: Integration & Assembly
*Evening 3: 5:00 PM - 9:00 PM*

### **5:00 - 5:15 PM: Print Collection & Quality Check** (15 minutes)

**Collect your prints:**
- Check print bin for your name
- Verify all parts printed successfully
- Inspect for quality issues

**Session 3 goal:** Complete functional assembly

---

### **5:15 - 6:30 PM: Dry Fit & Print Troubleshooting** (75 minutes)

#### **5:15 - 6:00 PM: DRY FIT - NO GLUE YET!** (45 min)

**Critical step:** Test everything before permanent assembly

**Checklist:**
- [ ] Arduino fits in base with room for wires
- [ ] Breadboard placement (if using)
- [ ] LED strip routes through stems/structure
- [ ] Power supply has mounting location
- [ ] All 3D parts fit together as intended
- [ ] Wire lengths are adequate
- [ ] Access to USB port for reprogramming

**Common issues to catch now:**
- Parts too tight (sand/file to fit)
- Parts too loose (add shims or rubber bands temporarily)
- Wires too short (extend before assembly)
- LEDs backward (check arrow direction!)

#### **6:00 - 6:30 PM: Print Troubleshooting** (30 min)

**If you have print failures or need modifications:**
- Quick fixes in Tinkercad
- Use backup parts from library
- Submit emergency reprints (small parts only!)

---

### **📤 6:30 PM: EMERGENCY REPRINT DEADLINE**

- Last chance for any quick reprints
- Small parts only (< 1 hour print time)

---

### **6:30 - 6:45 PM: Assembly Prep & Instructor Approval** (15 minutes)

**Organize your workspace:**
- All 3D printed parts laid out
- Electronics components ready
- Tools available: wire cutters, hot glue gun, zip ties
- Code uploaded and tested

**⚠️ GET INSTRUCTOR APPROVAL BEFORE GLUING**

---

### **6:45 - 7:00 PM: BREAK** ☕

---

### **7:00 - 9:00 PM: Assembly Sprint** (120 minutes)

#### **7:00 - 7:45 PM: Electronics Integration** (45 min)

**Test at each step:**
- Power on and verify LEDs work
- Check sensor readings
- Debug immediately if something breaks

#### **7:45 - 8:30 PM: Structural Assembly** (45 min)

**Now that electronics work, build the structure:**

**Hot glue station protocol:**
- Only at designated supervised station
- Let glue gun heat fully (3-5 minutes)
- Apply glue, press together, hold for 10-15 seconds
- Wait 30 seconds before handling
- Clean up glue strings immediately

**Cable management:**
- Use zip ties to bundle wires
- Leave some slack (stress relief)

**Checkpoints:**
- After each major glue operation
- Before final assembly (last chance to fix issues)
- Final functionality test

#### **8:30 - 9:00 PM: Testing & Troubleshooting** (30 min)

**Complete system test:**

**Upload final code:**
- Make sure latest version is on Arduino
- Test all lighting modes
- Verify sensor responsiveness
- Check brightness levels

**Power supply test:**
- Disconnect USB
- Connect battery/external power
- Turn on and verify full operation
- Note any changes in behavior (brightness, speed)

**Mechanical test:**
- Gently shake/move project
- Check for loose parts
- Verify stability (doesn't tip over)
- Stress test wire connections (wiggle base)

**"ER Clinic" for issues:**

Instructors available for:
- Code bugs that appeared during assembly
- Wiring problems (shorts, disconnections)
- Mechanical fit issues
- Power supply problems
- Behind schedule → prioritize core functionality

**If something's broken:**
1. Don't panic
2. Isolate the problem (code? wiring? mechanical?)
3. Test components individually
4. Ask for help immediately

---

**By 9:00 PM wrap-up:**
- Verify project is complete and stable
- Test on battery power one final time
- **Charge battery overnight!**
- Think about your 3-minute presentation for tomorrow
- Leave project at Elisava (if applicable)

---

## SESSION 4: Showcase & Critique
*Evening 4: 5:00 PM - 9:00 PM*

### **5:00 - 5:40 PM: Final Polish & Setup** (40 minutes)

**Last-minute adjustments:**
- Minor code tweaks (brightness, timing)
- Glue any loose parts
- Clean up appearance (remove glue strings)
- Test one final time

**Showcase display setup:**
- Arrange projects on tables
- Adequate spacing between projects
- Power strips/charging stations
- Lighting (dim enough to see LED effects)

---

### **5:40 - 6:20 PM: Presentation Preparation** (40 minutes)

**Structure your 3-minute presentation:**

**1. Concept (30 seconds)**
- What is it? What does it do?
- Demonstrate the interaction (turn it on!)
- What was your design intention?

**2. Technical Approach (30 seconds)**
- Code architecture (sensor → processing → LED output)

**3. Design Decisions (90 seconds)**
- Why these specific choices?
- What problems did you encounter?
- How did you solve them?
- What would you do differently?

**4. Future Improvements (30 seconds)**
- What would you add with more time?
- Possible applications or extensions
- What you learned that you'll apply next time

**Practice with a partner:**
- Take turns presenting
- Give feedback: clarity, timing, technical depth
- Refine your explanation
- Time yourself (3 minutes max)


---

### **6:20 - 6:35 PM: BREAK & FINAL SETUP** ☕

Turn on all projects, final tech check

---

### **6:35 - 8:00 PM: SHOWCASE & CRITIQUE** (85 minutes)

#### **6:35 - 7:10 PM: Round 1 - Lightning Presentations** (35 min)

**Format:** Each group presents at their station (3 min each)

**Presentation order:** [Alphabetical or random draw]

**While others present:**
- Listen actively
- Take notes on questions you want to ask
- Notice interesting technical approaches
- Think about connections to your own work

**Q&A after each presentation:**
- 1-2 questions from audience
- Keep it brief (more depth in Round 2)

---

#### **7:10 - 7:50 PM: Round 2 - Gallery Walk** (40 min)

**Open exploration format:**

**What to do:**
- Visit each project (spend 3-5 min at each)
- Engage in detailed technical discussions
- Ask the maker questions:
  - "How did you implement [specific feature]?"
  - "What was the hardest problem to solve?"
  - "Can you show me the code for [behavior]?"
- Test the interaction yourself
- Take photos/videos (with permission)

**For makers:**
- Be available at your project
- Encourage people to interact with it
- Explain technical details to those interested
- Discuss your process and decisions

**Instructors will circulate:**
- Observing interactions
- Noting innovations and excellence
- Preparing for awards decisions

---

#### **7:50 - 8:00 PM: Round 3 - Group Critique** (10 min)

**Reconvene as full group:**

**Discussion topics:**
- Common challenges everyone faced
- Creative solutions that emerged
- Technical innovations worth sharing
- Design patterns that worked well
- Lessons learned about physical computing

**Questions to consider:**
- How does working with physical constraints differ from software-only projects?
- What was surprising about embedded systems development?
- How might these techniques apply to your AI/design work?
- What would you want to explore further?

**Open floor:**
- Students can share insights
- Cross-pollinate ideas
- Reflect on the learning process

---

### **8:00 - 8:50 PM: Awards & Reflection** (50 minutes)

#### **8:00 - 8:25 PM: Award Ceremony** (25 min)

**Award categories & criteria:**

- 🎨 **Most Creative Design** - unique/artistic plant structure
- 🌈 **Best Light Effects** - coolest color patterns/animations
- 🔧 **Master Troubleshooter** - overcame significant technical challenges
- 💡 **Innovation Award** - unique feature or clever solution
- 🤝 **Best Collaborator** - helped others, shared knowledge
- 📈 **Most Improved** - biggest growth from Day 1 to Day 4
- ⚡ **Sensor Wizard** - best sensor integration
- 🏆 **Instructor's Choice** - something special the instructors noticed

**Award presentation:**
- Instructor explains why they won
- Certificates/recognition

---

#### **8:25 - 8:50 PM: Group Reflection** (25 min)

**Facilitated discussion:**

**What did you learn?**
- About embedded systems?
- About interaction design?
- About your own process?
- About integrating hardware + software?

**How does this connect to your field?**
- AI applications with physical sensors
- Edge computing and embedded ML
- Tangible interfaces for AI systems
- Physical computing in design practice

**What surprised you?**
- Challenges you didn't expect
- Things that were easier than anticipated
- Insights about physical vs digital

**Interest in future workshops?**
- ESP32/ESP8266 (WiFi, Bluetooth)
- TinyML (machine learning on microcontrollers)
- Advanced sensors (computer vision, audio)
- Robotics and actuation
- Wearable computing

---

#### **8:50 - 9:00 PM: Feedback & Farewell** (10 min)

**Quick wrap-up:**
- Fill out feedback form
- Take your project home carefully
- **Group photo!** 
