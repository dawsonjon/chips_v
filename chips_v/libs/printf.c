#include <stdio.h>
#include <stdarg.h>
#include <ctype.h>

//helper function writes either to a file or a buffer
static int _put(char c, FILE file, char bufp[], int idx){
    if(file){
        fputc(c, file);
        idx++;
    } else {
        bufp[idx++] = c;
        bufp[idx] = 0;
    }
    return idx;
}

//prints octal/decimal/hex digits
static char _radix_digit(int digit, int upper){
    if(digit<=9) return digit+'0';
    else if(upper) return digit-10+'A';
    else return digit-10+'a';
}


//helper function prints numbers in an arbitrary radix
static int _fprint_udecimal(FILE output, char buffer[], int idx, unsigned udecimal, unsigned width, char fill_char, int radix, int upper){
	unsigned digitval;
	char digit;
	int position;
	int seen_non_zero = 0;

    //setup initial values based on radix
    switch(radix){
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

        //default to 10
        default:
            digitval = 1000000000;
            radix = 10;
            position = 10;
    }

    //print value starting with most significant digit
	while(digitval){
		digit = udecimal/digitval;
		if(digit || seen_non_zero || position==1){
			idx = _put(_radix_digit(digit, upper), output, buffer, idx);
			seen_non_zero = 1;
		} else if(width >= position){
			idx = _put(fill_char, output, buffer, idx);
		}
		udecimal %= digitval;
		digitval /= radix;
		position--;
	}

    return idx;
}

int _fprintf(FILE output, char *buffer, char fmt_str[], va_list ap){
    int inp = 0; 
    char fill_char;
    int width;
    char *str;
    int value;
    int idx = 0;

    if(!fmt_str[inp]) return idx;
    while(1){
        while(fmt_str[inp] != '%'){
            idx = _put(fmt_str[inp++], output, buffer, idx);
            if(!fmt_str[inp]) return idx;
        }
        inp++; //discard %
        if(!fmt_str[inp]) return idx;

        //flags 
        if(fmt_str[inp] == '0'){
            fill_char = '0';
            inp++;
            if(!fmt_str[inp]) return idx;
        } else {
            fill_char = ' ';
        }

        //width 
        width = 0;
        while(isdigit(fmt_str[inp])){
            width *= 10;
            width += fmt_str[inp++]-'0';
            if(!fmt_str[inp]) return idx;
        }

        switch(fmt_str[inp]){
            case '%':
                idx = _put(fmt_str[inp], output, buffer, idx);
                break;
            case 'c':
                idx = _put(va_arg(ap, int), output, buffer, idx);
                break;
            case 's':
                str = va_arg(ap, char*);
                while(*str){
                    idx = _put(*str, output, buffer, idx);
                    *str++;
                }
                break;
            case 'i':
                value = va_arg(ap, int);
                if(value < 0){
                    idx = _put('-', output, buffer, idx);
                    value = -value;
                    idx = _fprint_udecimal(output, buffer, idx, value, width-1, fill_char, 10, 0);
                } else {
                    idx = _fprint_udecimal(output, buffer, idx, value, width, fill_char, 10, 0);
                }
                break;
            case 'd':
                value = va_arg(ap, int);
                if(value < 0){
                    idx = _put('-', output, buffer, idx);
                    value = -value;
                    idx = _fprint_udecimal(output, buffer, idx, value, width-1, fill_char, 10, 0);
                } else {
                    idx = _fprint_udecimal(output, buffer, idx, value, width, fill_char, 10, 0);
                }
                break;
            case 'u':
                idx = _fprint_udecimal(output, buffer, idx, va_arg(ap, int), width, fill_char, 10, 0);
                break;
            case 'x':
                idx = _fprint_udecimal(output, buffer, idx, va_arg(ap, int), width, fill_char, 16, 0);
                break;
            case 'X':
                idx = _fprint_udecimal(output, buffer, idx, va_arg(ap, int), width, fill_char, 16, 1);
                break;
            case 'o':
                idx = _fprint_udecimal(output, buffer, idx, va_arg(ap, int), width, fill_char, 8, 0);
                break;
        }
        inp++; //discard type field
        if(!fmt_str[inp]) return idx;
    }
}

int vfprintf(FILE output, char fmt_str[], va_list ap){
    _fprintf(output, 0, fmt_str, ap);
}

int vprintf(char fmt_str[], va_list ap){
    _fprintf(stdout, 0, fmt_str, ap);
}

int vsprintf(char * buffer, char fmt_str[], va_list ap){
    _fprintf(0, buffer, fmt_str, ap);
}

int fprintf(FILE output, char fmt_str[], ...){
    va_list(ap);
    va_start(ap, fmt_str);
    _fprintf(output, 0, fmt_str, ap);
}

int printf(char fmt_str[], ...){
    va_list(ap);
    va_start(ap, fmt_str);
    _fprintf(stdout, 0, fmt_str, ap);
}

int sprintf(char * buffer, char fmt_str[], ...){
    va_list(ap);
    va_start(ap, fmt_str);
    _fprintf(0, buffer, fmt_str, ap);
}
