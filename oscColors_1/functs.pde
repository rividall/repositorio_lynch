void oscEvent(OscMessage theOscMessage) {
  /* check if theOscMessage has the address pattern we are looking for. */
  if (theOscMessage.checkAddrPattern("/syntien/basic/1/touchpad1/press")==true) {
    coordX = theOscMessage.get(0).floatValue()*1000;
    coordY = theOscMessage.get(1).floatValue()*1000;
  }
  if (theOscMessage.checkAddrPattern("/syntien/basic/1/button1")==true) {
    oscCol = color(52, 152, 219);
  }
  if (theOscMessage.checkAddrPattern("/syntien/basic/1/button2")==true) {
    oscCol = color(46, 204, 11);
  }
  if (theOscMessage.checkAddrPattern("/syntien/basic/1/button3")==true) {
    oscCol = color(231, 76, 60);
  }
  if (theOscMessage.checkAddrPattern("/syntien/basic/1/button4")==true) {
    oscCol = color(241, 196, 15);
  }
    if (theOscMessage.checkAddrPattern("/syntien/basic/1/slider1")==true) {
    oscSize = theOscMessage.get(0).floatValue()*szFactor;
  }
      if (theOscMessage.checkAddrPattern("/syntien/basic/1/slider2")==true) {
    oscAlpha = theOscMessage.get(0).floatValue()*255;
  }
  println("#received address: "+theOscMessage.addrPattern());
}
void drawline() {
  strokeWeight(oscSize);
  stroke(oscCol);
  line(prevX, prevY, coordX, coordY);
  println(prevX + " " + prevY +" "+ coordX +" "+ coordY);
}
