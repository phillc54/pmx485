void send_data() {  // SEND DATA

  digitalWrite(receiving, HIGH);
  delay(1);
  Serial.write(reply);
  Serial.flush();
  digitalWrite(receiving, LOW);

}  // END SEND DATA
