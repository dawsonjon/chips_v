#include <ctype.h>
#include <float.h>
#include <stdarg.h>
#include <stdio.h>

// helper function writes either to a file or a buffer
static int _put(char c, FILE file, char bufp[], int idx) {
  if ((int)file) {
    fputc(c, file);
    idx++;
  } else {
    bufp[idx++] = c;
    bufp[idx] = 0;
  }
  return idx;
}

// prints octal/decimal/hex digits
static char _radix_digit(int digit, int upper) {
  if (digit <= 9)
    return digit + '0';
  else if (upper)
    return digit - 10 + 'A';
  else
    return digit - 10 + 'a';
}

// helper function prints numbers in an arbitrary radix
static int _fprint_udecimal(FILE output, char buffer[], int idx,
                            unsigned udecimal, unsigned width, char fill_char,
                            int radix, int upper) {
  unsigned digitval;
  char digit;
  int position;
  int seen_non_zero = 0;

  // setup initial values based on radix
  switch (radix) {
  case 16:
    digitval = 0x10000000;
    position = 8;
    break;
  case 10:
    digitval = 1000000000;
    position = 10;
    break;
  case 8:
    digitval = 01000000000;
    position = 10;
    break;

  // default to 10
  default:
    digitval = 1000000000;
    radix = 10;
    position = 10;
  }

  // print value starting with most significant digit
  while (digitval) {
    digit = udecimal / digitval;
    if (digit || seen_non_zero || position == 1) {
      idx = _put(_radix_digit(digit, upper), output, buffer, idx);
      seen_non_zero = 1;
    } else if (width >= position) {
      idx = _put(fill_char, output, buffer, idx);
    }
    udecimal %= digitval;
    digitval /= radix;
    position--;
  }

  return idx;
}

static int is_special(double f) {
  return (f != f || f > DBL_MAX || f < -DBL_MAX);
}

static int _print_special(FILE output, char buffer[], int idx, double f,
                          int width, int upper) {

  if (((long long)f) & 0x8000000000000000) {
    idx = _put('-', output, buffer, idx);
    width--;
  }

  while (width > 3) {
    idx = _put(' ', output, buffer, idx);
  }

  if (f != f) {
    if (upper) {
      idx = _put('N', output, buffer, idx);
      idx = _put('A', output, buffer, idx);
      idx = _put('N', output, buffer, idx);
    } else {
      idx = _put('n', output, buffer, idx);
      idx = _put('a', output, buffer, idx);
      idx = _put('n', output, buffer, idx);
    }
  } else if (f > DBL_MAX || f < -DBL_MAX) {
    if (upper) {
      idx = _put('I', output, buffer, idx);
      idx = _put('N', output, buffer, idx);
      idx = _put('F', output, buffer, idx);
    } else {
      idx = _put('i', output, buffer, idx);
      idx = _put('n', output, buffer, idx);
      idx = _put('f', output, buffer, idx);
    }
  }
}

static int _print_double(FILE output, char buffer[], int idx, double f,
                         int precision, int width, char fill_char, int upper) {
  int digitval;
  double digit;
  int position;
  int negative = 0;

  if (is_special(f)) {
    return _print_special(output, buffer, idx, f, width, upper);
  }

  if (f < 0.0) {
    f = -f;
    negative = 1;
    width--;
  }

  /*Find out how many digits are needed*/
  digit = 1.0;
  position = 1;
  while (digit * 10.0 <= f) {
    digit *= 10.0;
    position++;
  }

  /*pad with extra chars if needed*/
  if (precision)
    width -= (precision + 1);
  while (width-- > position) {
    idx = _put(fill_char, output, buffer, idx);
  }

  /*print the '-' character*/
  if (negative)
    idx = _put('-', output, buffer, idx);

  /*print integer part*/
  while (position--) {
    digitval = (int)(f / digit);
    idx = _put('0' + digitval, output, buffer, idx);
    f -= (digitval * digit);
    digit /= 10.0;
  }

  /*print fraction part*/
  if (precision) {
    idx = _put('.', output, buffer, idx);
  }
  for (int i = 0; i < precision; i++) {
    digitval = (int)(f / digit);
    f -= (digitval * digit);
    digit /= 10.0;

    /* round last digit */
    if (i == precision - 1) {
      if (f / digit >= 5) {
        digitval++;
      }
    }
    idx = _put('0' + digitval, output, buffer, idx);
  }

  return idx;
}

typedef struct {
  double f;
  int e;
} exp_float;

exp_float get_exp(double f) {

  exp_float result;
  double abs_f = f;

  result.e = 0;
  result.f = f;

  if (f < 0.0)
    abs_f = -f;

  if (f == 0) {
    result.e = 0;
    result.f = 0.0;
    return result;
  }
  result.e = 0.0;
  while (abs_f >= 10.0) {
    result.f /= 10.0;
    abs_f /= 10.0;
    result.e++;
  }

  while (abs_f < 1.0) {
    result.f *= 10.0;
    abs_f *= 10.0;
    result.e--;
  }

  return result;
}

static int _print_e_double(FILE output, char buffer[], int idx, double f,
                           int precision, int width, char fill_char,
                           int upper) {

  if (is_special(f)) {
    return _print_special(output, buffer, idx, f, width, upper);
  }

  int digitval;
  exp_float expval = get_exp(f);

  /*total width includes exponent*/
  width -= 4;
  if (expval.e >= 100)
    width--;
  if (expval.e <= -100)
    width--;

  /*print mantissa*/
  idx = _print_double(output, buffer, idx, expval.f, precision, width,
                      fill_char, upper);

  /*print exponent*/
  if (upper) {
    idx = _put('E', output, buffer, idx);
  } else {
    idx = _put('e', output, buffer, idx);
  }
  if (expval.e < 0.0) {
    idx = _put('-', output, buffer, idx);
    expval.e = -expval.e;
  } else {
    idx = _put('+', output, buffer, idx);
  }
  if (expval.e >= 100) {
    digitval = expval.e / 100;
    expval.e -= digitval * 100;
  }
  digitval = expval.e / 10;
  expval.e -= digitval * 10;
  idx = _put(digitval + '0', output, buffer, idx);
  digitval = expval.e / 1;
  idx = _put(digitval + '0', output, buffer, idx);

  return idx;
}

static int _print_g_double(FILE output, char buffer[], int idx, double f,
                           int precision, int width, char fill_char,
                           int upper) {

  if (is_special(f)) {
    return _print_special(output, buffer, idx, f, width, upper);
  }

  exp_float expval = get_exp(f);
  if (expval.e < -4 || expval.e > precision) {
    return _print_e_double(output, buffer, idx, f, precision, width, fill_char,
                           upper);
  } else {
    return _print_double(output, buffer, idx, f, precision, width, fill_char,
                         upper);
  }
}

int _fprintf(FILE output, char *buffer, char fmt_str[], va_list ap) {
  int inp = 0;
  char fill_char;
  int width;
  int precision;
  char *str;
  int value;
  double dvalue;
  int idx = 0;

  if (!fmt_str[inp])
    return idx;
  while (1) {
    while (fmt_str[inp] != '%') {
      idx = _put(fmt_str[inp++], output, buffer, idx);
      if (!fmt_str[inp])
        return idx;
    }
    inp++; // discard %
    if (!fmt_str[inp])
      return idx;

    // flags
    if (fmt_str[inp] == '0') {
      fill_char = '0';
      inp++;
      if (!fmt_str[inp])
        return idx;
    } else {
      fill_char = ' ';
    }

    // width
    width = 0;
    while (isdigit(fmt_str[inp])) {
      width *= 10;
      width += fmt_str[inp++] - '0';
      if (!fmt_str[inp])
        return idx;
    }

    // precision
    precision = 6;
    if (fmt_str[inp] == '.') {
      inp++; /*discard .*/
      if (!fmt_str[inp])
        return idx;

      precision = 0;
      while (isdigit(fmt_str[inp])) {
        precision *= 10;
        precision += fmt_str[inp++] - '0';
        if (!fmt_str[inp])
          return idx;
      }
    }

    switch (fmt_str[inp]) {
    case '%':
      idx = _put(fmt_str[inp], output, buffer, idx);
      break;
    case 'c':
      idx = _put(va_arg(ap, int), output, buffer, idx);
      break;
    case 's':
      str = va_arg(ap, char *);
      while (*str) {
        idx = _put(*str, output, buffer, idx);
        *str++;
      }
      break;
    case 'i':
      value = va_arg(ap, int);
      if (value < 0) {
        idx = _put('-', output, buffer, idx);
        value = -value;
        idx = _fprint_udecimal(output, buffer, idx, value, width - 1, fill_char,
                               10, 0);
      } else {
        idx = _fprint_udecimal(output, buffer, idx, value, width, fill_char, 10,
                               0);
      }
      break;
    case 'd':
      value = va_arg(ap, int);
      if (value < 0) {
        idx = _put('-', output, buffer, idx);
        value = -value;
        idx = _fprint_udecimal(output, buffer, idx, value, width - 1, fill_char,
                               10, 0);
      } else {
        idx = _fprint_udecimal(output, buffer, idx, value, width, fill_char, 10,
                               0);
      }
      break;
    case 'u':
      idx = _fprint_udecimal(output, buffer, idx, va_arg(ap, int), width,
                             fill_char, 10, 0);
      break;
    case 'x':
      idx = _fprint_udecimal(output, buffer, idx, va_arg(ap, int), width,
                             fill_char, 16, 0);
      break;
    case 'X':
      idx = _fprint_udecimal(output, buffer, idx, va_arg(ap, int), width,
                             fill_char, 16, 1);
      break;
    case 'o':
      idx = _fprint_udecimal(output, buffer, idx, va_arg(ap, int), width,
                             fill_char, 8, 0);
      break;
    case 'f':
      idx = _print_double(output, buffer, idx, va_arg(ap, double), precision,
                          width, fill_char, 0);
      break;
    case 'e':
      idx = _print_e_double(output, buffer, idx, va_arg(ap, double), precision,
                            width, fill_char, 0);
      break;
    case 'E':
      idx = _print_e_double(output, buffer, idx, va_arg(ap, double), precision,
                            width, fill_char, 1);
      break;
    case 'g':
      idx = _print_g_double(output, buffer, idx, va_arg(ap, double), precision,
                            width, fill_char, 0);
      break;
    case 'G':
      idx = _print_g_double(output, buffer, idx, va_arg(ap, double), precision,
                            width, fill_char, 1);
      break;
    }
    inp++; // discard type field
    if (!fmt_str[inp])
      return idx;
  }
}

int vfprintf(FILE output, char fmt_str[], va_list ap) {
  _fprintf(output, 0, fmt_str, ap);
}

int vprintf(char fmt_str[], va_list ap) { _fprintf(stdout, 0, fmt_str, ap); }

int vsprintf(char *buffer, char fmt_str[], va_list ap) {
  _fprintf(0, buffer, fmt_str, ap);
}

int fprintf(FILE output, char fmt_str[], ...) {
  va_list(ap);
  va_start(ap, fmt_str);
  _fprintf(output, 0, fmt_str, ap);
}

int printf(char fmt_str[], ...) {
  va_list(ap);
  va_start(ap, fmt_str);
  _fprintf(stdout, 0, fmt_str, ap);
}

int sprintf(char *buffer, char fmt_str[], ...) {
  va_list(ap);
  va_start(ap, fmt_str);
  _fprintf(0, buffer, fmt_str, ap);
}
