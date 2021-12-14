bool get_checksum(){ // CHECKSUM

  char tmp[3];
  char tmp1[3];
  unsigned i = 0;

  lrc = 0;
  for(; i < strlen(inCheck); i = i + 2){
    strncpy(tmp, &inCheck[i], 2);
    lrc = (lrc + (int)strtol(tmp, NULL, 16)) & 255;
  }

  utoa(unsigned(((lrc ^ 255) + 1) & 255), tmp1, 16);

  if(strlen(tmp1) == 1){
    strcpy(hex, "0");
    strcat(hex,tmp1);
  }else{
    strcpy(hex,tmp1);
  }

  if(!strcmp(strupr(inLRC), strupr(hex))){
    return true;
  }

  return false;

} // END CHECKSUM
