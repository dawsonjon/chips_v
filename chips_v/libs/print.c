#include <stdio.h>

// Print an unsigned int to stdout in hex format
void fprint_uhex(unsigned uhex, unsigned width, FILE handle) {
  char digits[] = "0123456789abcdef";
  unsigned digitval = 1000000000;
  char digit;
  int position = 10;
  int seen_non_zero = 0;

  // print value starting with most significant digit
  while (digitval) {
    digit = uhex / digitval;
    if (digit || seen_non_zero || position == 1) {
      fputc(digits[digit], handle);
      seen_non_zero = 1;
    } else if (width >= position) {
      fputc(digits[digit], handle);
    }
    uhex %= digitval;
    digitval /= 16;
    position--;
  }
}

// Print an unsigned int to stdout in decimal format
// leading 0s will be suppressed
void fprint_udecimal(unsigned udecimal, unsigned width, FILE handle) {
  unsigned digitval = 1000000000;
  char digit;
  int position = 10;
  int seen_non_zero = 0;

  // print value starting with most significant digit
  while (digitval) {
    digit = udecimal / digitval;
    if (digit || seen_non_zero || position == 1) {
      fputc(digit + '0', handle);
      seen_non_zero = 1;
    } else if (width >= position) {
      fputc(digit + '0', handle);
    }
    udecimal %= digitval;
    digitval /= 10;
    position--;
  }
}

// Print a signed int to stdout in hex format
void fprint_hex(int hex, int width, FILE handle) {
  if (hex >= 0) {
    fprint_uhex(hex, width, handle);
  } else {
    fputc('-', handle);
    fprint_uhex(-hex, width, handle);
  }
}

// Print a signed int to stdout in decimal format
// leading 0s will be suppressed
void fprint_decimal(int decimal, int width, FILE handle) {
  if (decimal >= 0) {
    fprint_udecimal(decimal, width, handle);
  } else {
    fputc('-', handle);
    fprint_udecimal(-decimal, width, handle);
  }
}

void fprint_float(float f, FILE handle) {
  unsigned digit;
  unsigned print = 0;
  float significance = 100000000.0f;

  if (f < 0.0f) {
    fputc('-', handle);
    f = -f;
  }

  while (significance >= 1.0f) {
    digit = f / significance;
    if (significance < 10.0f) {
      print = 1;
    } else {
      print |= digit;
    }
    if (print) {
      fputc(digit + '0', handle);
    }
    f = f - (digit * significance);
    significance /= 10.0f;
  }

  fputc('.', handle);

  while (significance > 0.00000001f) {
    digit = f / significance;
    fputc(digit + '0', handle);
    f = f - (digit * significance);
    significance /= 10.0f;
    if (f == 0.0f)
      break;
  }
}

void fprint_double(double f, FILE handle) {
  unsigned digit;
  unsigned print = 0;
  double significance = 100000000000000.0;

  if (f < 0) {
    fputc('-', handle);
    f = -f;
  }

  while (significance >= 1.0) {
    digit = f / significance;
    if (significance < 10.0) {
      print = 1;
    } else {
      print |= digit;
    }
    if (print) {
      fputc(digit + '0', handle);
    }
    f = f - (digit * significance);
    significance /= 10.0;
  }

  fputc('.', handle);

  while (significance > 0.0000000001) {
    digit = f / significance;
    fputc(digit + '0', handle);
    f = f - (digit * significance);
    significance /= 10.0;
    if (f == 0.0)
      break;
  }
}

void print_uhex(int hex, int width) { fprint_uhex(hex, width, stdout); }

void print_udecimal(int decimal, int width) {
  fprint_udecimal(decimal, width, stdout);
}

void print_hex(int hex, int width) { fprint_hex(hex, width, stdout); }

void print_decimal(int decimal, int width) {
  fprint_decimal(decimal, width, stdout);
}

void print_float(float f) { fprint_float(f, stdout); }

void print_double(double f) { fprint_double(f, stdout); }
