int isalnum(int c) {
  return (c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z') ||
         (c >= '0' && c <= '9');
}
int isalpha(int c) { return (c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z'); }
int iscntrl(int c) { return (c >= 0 && c <= 0x1f) || c == 0x7f; }
int isdigit(int c) { return (c >= '0' && c <= '9'); }
int isgraph(int c) { return (c >= 0x21 && c <= 0x7e); }
int islower(int c) { return (c >= 'a' && c <= 'z'); }
int isprint(int c) { return (c >= 0x20 && c <= 0x7e); }
int ispunct(int c) { return isgraph(c) && !isalnum(c); }
int isspace(int c) {
  return (c == ' ' || c == '\t' || c == '\v' || c == '\n' || c == '\r' ||
          c == '\f');
}
int isupper(int c) { return (c >= 'A' && c <= 'Z'); }
int isxdigit(int c) {
  return (c >= 'A' && c <= 'F') || (c >= 'a' && c <= 'f') ||
         (c >= '0' && c <= '9');
}
int tolower(int c) {
  if (isupper(c)) {
    return c - 'A' + 'a';
  } else {
    return c;
  }
}
int toupper(int c) {
  if (islower(c)) {
    return c - 'a' + 'A';
  } else {
    return c;
  }
}
