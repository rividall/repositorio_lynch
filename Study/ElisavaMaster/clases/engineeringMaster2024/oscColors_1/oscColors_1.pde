import oscP5.*;
import netP5.*;
int added = 1;
OscP5 oscP5;
NetAddress myRemoteLocation;
int szFactor = 30;
float oscAlpha = 10;
color oscCol = color(255, 255, 255);
color oscBg = color(0, 0, 0, oscAlpha);
static    float coordX = 0;
static    float coordY = 0;
static  float prevX = 0;
static  float prevY = 0;
static float oscSize = 5;

void setup() {

  size(1000, 1000);
  frameRate(25);
  /* start oscP5, listening for incoming messages at port 12000 */
  oscP5 = new OscP5(this, 57120);

  /* myRemoteLocation is a NetAddress. a NetAddress takes 2 parameters,
   * an ip address and a port number. myRemoteLocation is used as parameter in
   * oscP5.send() when sending osc packets to another computer, device,
   * application. usage see below. for testing purposes the listening port
   * and the port of the remote location address are the same, hence you will
   * send messages back to this sketch.
   */
  myRemoteLocation = new NetAddress("172.152.3.87", 9000);
}


void draw() {
  noStroke();
  fill(oscCol);
  ellipse(coordX, coordY, oscSize, oscSize);

  drawline();
  prevX = coordX;
  prevY = coordY;

  oscBg = color(0, 0, 0, oscAlpha);
  fill(oscBg);
  noStroke();
  rect(0, 0, width, height);
}

void mousePressed() {
  /* in the following different ways of creating osc messages are shown by example */
  OscMessage myMessage = new OscMessage("/test");

  myMessage.add(added); /* add an int to the osc message */
  added++;
  /* send the message */
  oscP5.send(myMessage, myRemoteLocation);
  //println("sent");
}
