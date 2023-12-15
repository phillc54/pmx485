void send_bad(char msg[20]) {  // SEND DATA

  char tmp[50] = "";

  digitalWrite(receiving, HIGH);
  delay(1);
  strcpy(tmp, "E:");
  strcat(tmp, strupr(lrc_hex));
  strcat(tmp, ", G:");
  strcat(tmp, strupr(inLRC));
  strcat(tmp, ", MSG:");
  strcat(tmp, msg);
  strcat(tmp, +"\r\n");
  Serial.write(tmp);
  Serial.flush();
  digitalWrite(receiving, LOW);

}  // END SEND DATA
