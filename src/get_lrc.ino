bool get_lrc() {  // CHECKSUM

  char tmp[3] = "";

  lrc = 0;
  for (int i = 0; i < strlen(inCheckLRC); i = i + 2) {
    strncpy(tmp, &inCheckLRC[i], 2);
    lrc = (lrc + (int)strtol(tmp, NULL, 16)) & 255;
  }
  utoa(unsigned(((lrc ^ 255) + 1) & 255), tmp, 16);
  if (strlen(tmp) == 1) {
    strcpy(lrc_hex, "0");
    strcat(lrc_hex, tmp);
  } else {
    strcpy(lrc_hex, tmp);
  }
  if (!strcmp(strupr(inLRC), strupr(lrc_hex))) {
    return true;
  }
  return false;

}  // END CHECKSUM
