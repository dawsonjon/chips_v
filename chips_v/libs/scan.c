#include <scan.h>

unsigned hex2nibble_(char hex) {
  if (hex >= '0' && hex <= '9')
    return hex - '0';
  if (hex >= 'a' && hex <= 'f')
    return hex - 'a' + 0xa;
  if (hex >= 'A' && hex <= 'F')
    return hex - 'A' + 0xa;
  return 10;
}

unsigned fscan_uhex(unsigned f) {
  unsigned value;
  char c;
  value = 0;
  while (1) {
    c = fgetc(f);
    if (!isxdigit(c))
      break;
    value <<= 4;
    value += hex2nibble_(c);
  }
  return value;
}

unsigned fscan_udecimal(unsigned f) {
  unsigned value;
  char c;
  value = 0;
  while (1) {
    c = fgetc(f);
    if (!isdigit(c))
      break;
    value *= 10;
    value += c - '0';
  }
  return value;
}

int fscan_hex(unsigned f) {
  int sign;
  char c;
  c = fgetc(f);
  if (c == '-') {
    sign = -1;
  } else if (c == '+') {
    sign = 1;
  } else {
    sign = 1;
  }
  return sign * fscan_uhex(f);
}

int fscan_decimal(unsigned f) {
  int sign;
  char c;
  c = fgetc(f);
  if (c == '-') {
    sign = -1;
  } else if (c == '+') {
    sign = 1;
  } else {
    sign = 1;
  }
  return sign * fscan_udecimal(f);
}

float fscan_float(unsigned f) {

  float value, significance, sign;
  char c;

  value = 0;
  significance = 0.1;

  c = fgetc(f);

  /*evaluate sign*/
  if (c == '-') {
    sign = -1;
  } else if (c == '+') {
    sign = 1;
  } else {
    sign = 1;
    value = c - '0';
  }

  /*evaluate integer part*/
  while (1) {
    c = fgetc(f);
    if (!isdigit(c))
      break;
    value *= 10;
    value += c - '0';
  }

  /*evaluate fractional part*/
  if (c == '.') {
    while (1) {
      c = fgetc(f);
      if (!isdigit(c))
        break;
      value += significance * (c - '0');
      significance /= 10.0;
    }
  }

  return sign * value;
}

double fscan_double(unsigned f) {

  double value, significance, sign;
  char c;

  value = 0;
  significance = 0.1;

  c = fgetc(f);

  /*evaluate sign*/
  if (c == '-') {
    sign = -1;
  } else if (c == '+') {
    sign = 1;
  } else {
    sign = 1;
    value = c - '0';
  }

  /*evaluate integer part*/
  while (1) {
    c = fgetc(f);
    if (!isdigit(c))
      break;
    value *= 10;
    value += c - '0';
  }

  /*evaluate fractional part*/
  if (c == '.') {
    while (1) {
      c = fgetc(f);
      if (!isdigit(c))
        break;
      value += significance * (c - '0');
      significance /= 10.0;
    }
  }

  return sign * value;
}

unsigned scan_uhex() { return fscan_uhex(stdin); }

unsigned scan_udecimal() { return fscan_udecimal(stdin); }

int scan_hex() { return fscan_hex(stdin); }

int scan_decimal() { return fscan_decimal(stdin); }

float scan_float() { return fscan_float(stdin); }

double scan_double() { return fscan_double(stdin); }
