void send_bad(){ // SEND DATA

  char tmp[15];
  
  digitalWrite(receiving, HIGH);
  delay(1);
  strcpy(tmp,"E:");
  strcat(tmp,strupr(hex));
  strcat(tmp,",  G:");
  strcat(tmp,strupr(inLRC));
  strcat(tmp,+ "\r\n");
  Serial.write(tmp);
  Serial.flush();
  digitalWrite(receiving, LOW);

}  // END SEND DATA
