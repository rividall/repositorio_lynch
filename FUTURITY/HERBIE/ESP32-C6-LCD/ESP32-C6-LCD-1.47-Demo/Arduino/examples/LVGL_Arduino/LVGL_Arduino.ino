//#include "SD_Card.h"
#include "Display_ST7789.h"
#include "LVGL_Driver.h"
#include "LVGL_Example.h"
void setup()
{       
  //Flash_test();
  LCD_Init();
  Lvgl_Init();
  //SD_Init();   

  //Lvgl_Example1();     
   lv_demo_widgets();               
 

  //Wireless_Test2();  
}

void loop()
{
  Timer_Loop();
  delay(5);
}
