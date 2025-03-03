#include <WiFi.h>
#include "time.h"
#include <ESP_Google_Sheet_Client.h>

#define WIFI_SSID "Futurity Systems"
#define WIFI_PASSWORD "BBFF2024"

// Google Project ID
#define PROJECT_ID "concise-torus-452312-q8"

// Service Account's client email
#define CLIENT_EMAIL "herbie-iot@concise-torus-452312-q8.iam.gserviceaccount.com"

// Service Account's private key
const char PRIVATE_KEY[] PROGMEM = "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDMd9bVTc71Qdhv\nOUFIGG7zkOAdVwIctbZlyrs3AkoOAHFSa66DuB0H18EDEiFbW0AT4TJKlcMUyIGn\nbYBCOIqF+U5/M7Wmop8tssd21um/Upvxph253PypMBG8dM71SLL0DRVdn86MMpWx\nIpeagkWx7ZFHblv6776puGQjUryuL6Wyd3rhtBYU1UvlZYPj++TcUFFQNuQORUms\njfHp0/+tcsGDTnIFiJ0A5DeR785blcXMEfDrg4JyA480Z4N4cCUSc4zIegf7lN7b\nbnJJatgvfSGlV+0O2RLmN6cfyCxxTiDdXhCZQzONRCYTrExlv+5AgMlZSnqTMKRZ\n7vLyOvA7AgMBAAECggEAR7HtvrWd0BnajoWBAoquvPEb5K3Rq8d7wY2ov80psmct\nVT004DL62vkoUK9WyvXgLhhUzhpdYTg9XjvjMVUqHXghsjCrjVaQgjGiB2WsaM3K\nqJ0a50U5wwl77pz2xMNNHI5J455ZiodiPc5nYmIzlgQ7YNSto/vU2yYw1sH4Lwsd\njsIZPKSJK1eTMbD+GQZgxFZNxXVqbJe3q8rR86b5IjUBHWqccvZXk4t+wMkBNzPF\njh97OQQZ0CbFH55S8P8RNhK7G9goDiuk2DByLenaByMTmYfrrs4Txn7p/Uints4a\nqyTzTVhsw6F0E7CMgwtzggbWgYBGwwy439Drn+y74QKBgQDpwarjxhSRtGp7XgwM\n/9/nbj6mkucZKrAKesL+6EeEbBMW+h8SMqWnJC2jjiy8ebjG5/VyyWvRoRowlAU1\nYghG4IQmVY3gDXrquptJgSc9CKODs9NzdR1iRqG2hyIKGpbgIrz/4u4mVJBDHw2A\n3VVrSHjS8XWPrErUYipvidlMxQKBgQDf7LQVAVtz+s+gbw/aU9ya4GCD+Xo3Jgsb\nPVnKba/PJk05xVhCkxbjv+SVZJg5lVeHUG0h18Xva7VPDFw3XobbgjvaUnIx7iY3\n/uZiD49+Q/r2WDwYYjxaFJ27hcU56tCL+k9yoW+4SeDZ8QxpXuLXTi9ZGnGW3k2j\nn8kFKJEY/wKBgQDFaTRcBiXK43Xl2AgPVmyOc5FfdcLLgzyGrSROyHXVhLwedH+X\nC8TQQgJ1FRX82kNNYAnuteJjeE245tj7O15IFUYlZa1aoafD4nJQgk1UAx6slEqo\nQCjfnUzm7Hq307rFcTDyXYDISDRJK0lpIgMIhnzbkOW6v0O212yFJAKrDQKBgQCT\nBSGTbQmzk2hA6MqayVbdZRZZcDI7BUJjhxtuGihFNNudY6G4TETKEdKt95cur4wB\nbt/ISZhOwwQOu4nMXMbkVpSfmmQZvkffmf9/QMIw38dleLc0N0NyzXhmh8Tfavmz\n/gutsqrcb70uuuIwSLldLZtOwFr1+E03chCUz3a81wKBgBb1LQ5Pqkq13vee8l1+\nXKTq4glS5LSWZyGy2WiM/0PT9R/IlCkCHeL2Ed5CQCuxTccLa7+nQTo9xGhbHwy5\nat+Pg+k+oMRy4rk5qRT4GoA/zfGGnkpoFHcaTVdkE5lY/LYR7nbOthabjVKTqU6s\n3hTfEcRb7lTw6Q3Rbw6uLOPA\n-----END PRIVATE KEY-----\n";

// The ID of the spreadsheet where you'll publish the data
const char spreadsheetId[] = "1T9gN984cuslzx1PG3GC3WY5886GqgPmQD9vI5curLWE";
const int readTimer = 300;
// Timer variables
unsigned long lastTime = 0;  
unsigned long timerDelay = readTimer *1000;
char datetime[30];

// Token Callback function
void tokenStatusCallback(TokenInfo info);

// NTP server to request epoch time
const char* ntpServer = "pool.ntp.org";

// Variable to save current epoch time
unsigned long epochTime; 

// Function that gets current epoch time
unsigned long getTime() {
  time_t now;
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    return(0);
  }
  time(&now);
  strftime(datetime,80,"%b %d %y %H:%M",&timeinfo);
  return now;
}

void wirelessSetup(){
    //Configure time
    configTime(0, 0, ntpServer);

    GSheet.printf("ESP Google Sheet Client v%s\n\n", ESP_GOOGLE_SHEET_CLIENT_VERSION);

    // Connect to Wi-Fi
    WiFi.setAutoReconnect(true);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  
    while (WiFi.status() != WL_CONNECTED) {
      Serial.print(".");
      delay(1000);
    }

    // Set the callback for Google API access token generation status (for debug only)
    GSheet.setTokenCallback(tokenStatusCallback);

    // Set the seconds to refresh the auth token before expire (60 to 3540, default is 300 seconds)
    GSheet.setPrerefreshSeconds(10 * 60);

    // Begin the access token generation for Google API authentication
    GSheet.begin(CLIENT_EMAIL, PROJECT_ID, PRIVATE_KEY);
}

void wirelessLoop(){
    // Call ready() repeatedly in loop for authentication checking and processing
    bool ready = GSheet.ready();

    if (ready && millis() - lastTime > timerDelay){
        lastTime = millis();

        FirebaseJson response;
        //nAppend spreadsheet values...");
        FirebaseJson valueRange;

        // Get timestamp
        epochTime = getTime();

        valueRange.add("majorDimension", "COLUMNS");
        valueRange.set("values/[0]/[0]", datetime);
        valueRange.set("values/[1]/[0]", h);
        valueRange.set("values/[2]/[0]", t);
        valueRange.set("values/[3]/[0]", gasValue);
        valueRange.set("values/[4]/[0]", soilMoistureValue);
        valueRange.set("values/[5]/[0]", lightLvl);

        // For Google Sheet API ref doc, go to https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/append
        // Append values to the spreadsheet
        bool success = GSheet.values.append(&response /* returned response */, spreadsheetId /* spreadsheet Id to append */, "hoja1!A1" /* range to append */, &valueRange /* data range to append */);
        if (success){
            response.toString(Serial, true);
            valueRange.clear();
        }
        else{
            Serial.println(GSheet.errorReason());
        }
        Serial.println();
        //Serial.println(ESP.getFreeHeap());
    }
}

void tokenStatusCallback(TokenInfo info){
    if (info.status == token_status_error){
        GSheet.printf("Token info: type = %s, status = %s\n", GSheet.getTokenType(info).c_str(), GSheet.getTokenStatus(info).c_str());
        GSheet.printf("Token error: %s\n", GSheet.getTokenError(info).c_str());
    }
    else{
        GSheet.printf("Token info: type = %s, status = %s\n", GSheet.getTokenType(info).c_str(), GSheet.getTokenStatus(info).c_str());
    }
}