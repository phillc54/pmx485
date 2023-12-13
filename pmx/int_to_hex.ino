void int_to_hex(char *hex, int integer, int length) {  // CONVERT INTEGER TO HEX

  char tmp[length + 1] = "";
  int diff;

  utoa(integer, tmp, 16);
  if (strlen(tmp) < length) {
    diff = length - strlen(tmp);
    memset(hex, '0', diff);
    for (int i = 0; i < strlen(tmp); i++) {
      hex[i + diff] = tmp[i];
    }
  } else {
    strcpy(hex, tmp);
  }

}  // END CONVERT INTEGER TO HEX
