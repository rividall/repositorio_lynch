# 3D Printed Plant Light Sculptures Workshop
## Teacher's Guide & Preparation Document

---

## Workshop Overview

**Duration:** 4 days  
**Age Group:** Elisava Master Students 
**Class Size:** 15 students
**Goal:** Students learn Arduino basics, sensor integration, WS2812 LED control, and 3D printing while creating interactive light sculptures

**Core Philosophy:** This workshop embraces the learning process over perfection. Students will encounter challenges, make mistakes, and problem-solve—these are features, not bugs. The showcase celebrates creativity, effort, and learning, and NOT polished final products.

---

## SECTION 1 - PRE-WORKSHOP PREPARATION (Critical for Success)

### Timeline: 2-3 Weeks Before Workshop

#### **Week 1-2: Hardware & Software Setup**

**Computer Setup (MANDATORY - Do not skip!)**
- [ ] Install Arduino IDE on ALL computers students will use
- [ ] Install FastLED library on each installation
- [ ] Test upload "Blink" sketch to Arduino on EACH computer

**Materials Procurement**
- [ ] Order/acquire all electronic components (see Bill of Materials section)
- [ ] Purchase spare components (10-20% overage recommended)
- [ ] Prepare component kits (one bag per student with all electronics)

**3D Printing Library Curation**
- [ ] Download 20-30 plant part STL files from Thingiverse/Printables
- [ ] Categorize by print time: Fast (<2hr), Medium (2-4hr), Slow (>4hr)
- [ ] Test print one of each type to verify quality
- [ ] Create photo gallery/catalog for students to browse
- [ ] Print 20 "emergency backup" generic parts

**Curated plant parts library:**

**Categories:**
- **Bases/Pots** (FAST: 1-2hr)
  - Must fit Arduino + breadboard
  - Include wire routing
  
- **Stems/Trunks** (FAST: 30min-1hr)
  - Hollow for LED strip routing
  - Modular sections
  
- **Leaves** (FAST: 15-30min each)
  - Various shapes and sizes
  - Can print multiples
  
- **Flowers/Decorative** (FAST: 20-45min)
  - Light diffusers
  - Artistic elements


**Instructor Preparation**
- [ ] Build 2-3 complete example projects yourself
- [ ] Document every problem you encounter (this is your troubleshooting guide!)

#### **Week 2-3: Student Pre-Work Assignment**

Send students this checklist **at least one week before Day 1:**

---

### **STUDENT PRE-WORKSHOP CHECKLIST**

Complete these tasks BEFORE arriving on Day 1. Bring proof of completion (screenshot or demo) to your instructor.

#### **Part 1: Arduino IDE Installation** (30-45 minutes)

**Step 1: Download Arduino IDE**
1. Go to https://www.arduino.cc/en/software
2. Download Arduino IDE 2.x for your operating system (Windows/Mac/Linux)
3. Install following the on-screen instructions
4. Open Arduino IDE - you should see a blank sketch window

**Step 2: Install FastLED Library**
1. In Arduino IDE, go to **Tools → Manage Libraries** (or click the library icon on left sidebar)
2. In the search box, type: `FastLED`
3. Find "FastLED by Daniel Garcia" in the results
4. Click **Install** (choose the latest version)
5. Wait for installation to complete
6. Close and restart Arduino IDE

---

#### **Part 2: Tinkercad Account Setup** (15-20 minutes)

**Step 1: Create Account**
1. Go to https://www.tinkercad.com
2. Click **Join Now** or **Sign Up**
3. Create account using:
   - **Option A:** Email address (recommended - use your school email)
   - **Option B:** Google account
   - **Option C:** Apple ID
4. Verify your email if required
5. Complete the profile setup

---

#### **Part 3: Workshop Preparation** (5 minutes)

**Materials to Bring:**
- [ ] Laptop (if you'll be using your own) with charger
- [ ] Notebook and pen for taking notes
- [ ] Enthusiasm and willingness to troubleshoot! 🔧

**Mindset Preparation:**
- **Expect challenges** - electronics never work the first time
- **Debugging is learning** - fixing problems teaches you the most
- **Ask questions** - the only "dumb" question is the one unasked
- **Help others** - teaching reinforces your own learning
- **Iteration is normal** - your first version won't be your best version

**✓ Final Checkpoint:** 
- Screenshot of Arduino IDE with FastLED installed
- Screenshot of Tinkercad dashboard
- Materials gathered

**Submit to:** [Instructor email/platform] by [deadline date]

---

### **Day-Before Final Checks**

**Technology**
- [ ] All computers booted and Arduino IDE launches successfully
- [ ] FastLED examples load on all computers
- [ ] Shared code folder is accessible to all students
- [ ] Backup USB drives with installers ready

---


## SECTION 2 - POWER SUPPLY DECISION (Choose ONE - Must decide before workshop)

### **Option A: USB Power Banks** ⭐ RECOMMENDED

**Pros:**
- Native 5V output (perfect for Arduino)
- Rechargeable (sustainable)
- Students familiar with them
- 2-4 hour runtime with LEDs
- Safe and simple

**Cons:**
- Cost: $10-20 per student
- Students must remember to charge
- Larger/heavier than batteries

**Implementation:**
- Purchase one 10,000mAh power bank per student
- Recommended brands: Anker, RAVPower, Aukey
- Include USB-A to USB-B cable (Arduino cable)
- Label each with student name
- Create charging station: power strip with 20 USB ports

---

### **Option B: Wall Adapters (5V 2A)**

**Pros:**
- Unlimited runtime
- Cheap ($3-5 each)
- Reliable and consistent power

**Cons:**
- Showcase limited to areas near outlets
- Trip hazard with many cables
- Not portable
- Less "professional" looking for student projects

**Implementation:**
- One 5V 2A wall adapter per student
- Use extension cords/power strips for showcase
- Clearly mark showcase area power layout
- Cable management critical (tape cables down)

## EMBRACE IMPERFECTION MESSAGING

**Philosophy:** This workshop is about learning, not perfection. Students WILL encounter problems - this is valuable! The goal is resilient problem-solvers, not flawless products.

### **How to Frame Challenges Positively**

**Instead of:** "Your project isn't working"  
**Say:** "You've discovered a debugging opportunity! Let's figure this out together."

**Instead of:** "That's wrong"  
**Say:** "Interesting! What happens if we try it this way instead?"

**Instead of:** "You should have..."  
**Say:** "Next time, consider trying..."

---

### **Showcase Award Categories** (Everyone wins something)

**🎨 Best Interaction Design**
- Most intuitive and engaging user experience
- Thoughtful mapping of input to output
- Clear and satisfying interaction model

**💡 Technical Excellence**
- Clean, well-structured code
- Robust implementation
- Efficient use of resources
- Good documentation

**🌈 Visual Aesthetics**
- Beautiful integration of light and form
- Compelling color choices
- Artistic use of LEDs
- Visual coherence

**🔧 Problem Solving**
- Creative solution to technical challenge
- Overcame significant obstacles
- Innovative workaround or adaptation

**🚀 Innovation**
- Novel approach or technique
- Pushed boundaries of the assignment
- Unexpected creative direction

**🏆 Instructor's Choice**
- Something special that doesn't fit other categories
- Exceptional growth or effort
- Hidden gem that deserves recognition

**Implementation:** Prepare certificates/ribbons for each category. Every student receives recognition for something specific they did well.

---

## PRE-WORKSHOP GO/NO-GO CHECKLIST

**Use this checklist 48 hours before Day 1. If ANY critical item is NO, delay the workshop.**

### **CRITICAL ITEMS** (Must be YES)

- [ ] **Computers:** Arduino IDE installed and tested on ALL student computers
- [ ] **Libraries:** FastLED library installed on all computers
- [ ] **Hardware:** Sufficient Arduinos for each student/pair
- [ ] **Components:** All electronic components received and inventoried
- [ ] **Power Supply:** Decision made and materials acquired
- [ ] **Staffing:** Minimum 1 instructor per 5 students confirmed
- [ ] **Safety:** First aid kit available, safety briefing prepared
- [ ] **3D Printers:** All printers tested and working
- [ ] **Backup Plan:** Spare parts and backup Arduinos ready

### **IMPORTANT ITEMS** (Strongly recommended)

- [ ] **Posters:** All 5 required posters created and laminated
- [ ] **Code Library:** All snippets tested and shared in accessible folder
- [ ] **STL Library:** Plant parts curated and print times calculated
- [ ] **Example Projects:** 2-3 complete examples built and working
- [ ] **Student Pre-work:** Majority of students completed checklist
- [ ] **TA Training:** Helpers briefed on troubleshooting procedures
- [ ] **Workspace:** Tables, power strips, tools organized
- [ ] **Timeline:** Daily schedule created with time buffers

### **NICE-TO-HAVE ITEMS** (Recommended but not blocking)

- [ ] **Spare Supplies:** Extra LEDs, wires, sensors ordered
- [ ] **Documentation:** Photo guides for assembly created
- [ ] **Showcase Plan:** Display area arranged, lighting tested
- [ ] **Parent Communication:** Workshop overview/schedule sent to families
- [ ] **Emergency Fund:** $200-300 budget available for last-minute purchases

---

**If GO:**
- [ ] Send reminder email to students with Day 1 arrival details
- [ ] Confirm TA attendance for all 4 days
- [ ] Final check of 3D printer filament levels
- [ ] Charge all power banks overnight

**If NO-GO:**
- Document which items are blocking
- Create action plan with new timeline
- Communicate delay to students/parents
- Reschedule for when all critical items are YES

---

## BILL OF MATERIALS

### **Per Student:**

**Electronics:**
- 1x Arduino Uno R3 (or compatible)
- 1x USB-A to USB-B cable
- 1x Breadboard (400 tie-point minimum)
- 1x WS2812 LED strip (10-15 LEDs, can cut from larger strip)
- 1x Light sensor module (photoresistor or BH1750)
- 1x Potentiometer (10kΩ optional, for manual control)
- 10x Jumper wires (assorted colors, pre-cut recommended)
- 1x Power supply (USB power bank, battery pack, or wall adapter)

**Consumables:**
- 3D printed plant parts (varies per student design)
- Hot glue sticks (5-10 per student)
- Electrical tape
- Zip ties or twist ties (wire management)

**Optional Enhancements:**
- Servo motor (for movement)
- Motion sensor (PIR sensor)
- Additional LED strips

### **Shared Materials (for class of 20):**

**Tools:**
- 5x Wire cutters/strippers
- 5x Small screwdrivers (Phillips and flathead)
- 5x Hot glue guns
- 2x Multimeters (for troubleshooting)
- 1x Label maker
- Scissors, tape, markers

**3D Printing:**
- 1kg filament per 3-4 students (PLA recommended)
- Blue painter's tape or glue stick (bed adhesion)
- Isopropyl alcohol (bed cleaning)

**Safety & Cleanup:**
- 1x First aid kit
- Safety glasses (if cutting/drilling)
- Paper towels
- Trash bags
- Hand sanitizer

---

## DAILY INSTRUCTOR PROTOCOLS

### **Start of Each Day:**

1. **Arrive 30 minutes before students**
2. **Boot all computers and verify Arduino IDE launches**
3. **Check 3D printer status** (overnight prints, filament levels)
4. **Review daily plan with TAs** (assign roles/stations)
5. **Prepare "kit of the day"** (specific components needed today)
6. **Set up emergency repair station** (spare parts, working Arduino)

### **End of Each Day:**

1. **Student checkout:**
   - Have students save all code to named files
   - Check that projects are stored safely
   - Verify batteries charging (if applicable)
   
2. **Workspace cleanup:**
   - Collect shared tools
   - Inventory remaining components
   - Secure 3D printers
   
3. **Instructor debrief:**
   - What went well today?
   - What took longer than expected?
   - Adjust tomorrow's plan accordingly
   - Update troubleshooting guide with new issues discovered

---

## INSTRUCTOR SURVIVAL TIPS

**Mental Preparation:**
- Plan for 2x your estimated time for everything
- Accept that not all projects will be complete/perfect
- Your role is facilitator, not "fixer" - teach students to debug
- Celebrate small wins loudly

**Physical Preparation:**
- Wear comfortable shoes (you'll be on your feet for hours)
- Stay hydrated
- Have snacks available (students and instructors!)
- Take breaks when possible

**Stress Management:**
- When overwhelmed, triage: Safety first, learning second, pretty results third
- It's okay to say "We're moving on" even if some students aren't done
- Have TAs handle routine questions so you can focus on complex issues
- Remember: Controlled chaos is still learning!

**Emergency Contacts:**
- [ ] Tech support (if school IT needs to help with computers)
- [ ] 3D printer supplier (for urgent part/filament orders)
- [ ] Electronics supplier (local store for same-day pickup)
- [ ] School facilities (if you need additional power/tables/space)

---

## CONCLUSION

This workshop will be challenging, rewarding, and occasionally chaotic. Your preparation is the key to success. By following this guide, you'll:

✅ Set students up for success with working tools  
✅ Prevent common technical disasters  
✅ Create a safe learning environment  
✅ Foster problem-solving skills over perfection  
✅ Celebrate learning and creativity  

**Remember:** The goal isn't 20 perfect light sculptures. The goal is 20 students who learned to build, debug, create, and persist through challenges. 

You've got this! 🚀

---

**Document Version:** 1.0  
**Last Updated:** January 19, 2026  
**Questions/Feedback:** [Your contact info]  

---

*Need help with a specific section? Have questions about implementation? Reach out - we're here to support you!*