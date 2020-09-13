#ifndef __STDIO_H
#define __STDIO_H

#define FILE unsigned

#include <machine.h>

///stdio.h
///-------
///
///The globals `stdin` and `stdout` should be set to an input or output by the user.
///

///The `fgetc` returns a single character from file.
///
///.. code-block:: c
///
///        unsigned fgetc();
///

unsigned fgetc(FILE handle){
	volatile unsigned int* p_reg = (unsigned int *) handle;
        return *p_reg;
}

///The `putc` writes a single character to file.
///
///.. code-block:: c
///
///        void fputc(unsigned c, FILE handle);
///

int fputc(int c, FILE handle){
	volatile unsigned int* p_reg = (unsigned int *) handle;
	*p_reg = c;
	return c;
}


///The `fputs` function prints `string` to the output `handle`.
///
///.. code-block:: c
///
///        int fputs(const char *string, FILE handle);
///
int fputs(const char * string, FILE handle){
        unsigned i=0;
        while(string[i]){
                fputc(string[i++], handle);
        }
	return i;
}

///The `fgets` function reads a line, up to `maxlength` characters, or a line end
///from the input `handle`. The string will be null terminated. `maxlength`
///includes the null character.
///
///.. code-block:: c
///
///        char * fgets(char * string, unsigned maxlength, unsigned handle);
///

char * fgets(char * string, int maxlength, FILE handle){
        char c;
        unsigned i=0;
        while(1){
                c = fgetc(handle);
                string[i] = c;
                i++;
                if(c == '\n') break;
                if(i == maxlength-1) break;
        }
        string[i] = 0;
	return string;
}

///The `gets` function reads a line, up to `maxlength` characters, or a line end
///from stdin. The string will be null terminated. `maxlength`
///includes the null character.
///
///.. code-block:: c
///
///        char * gets(const char * string, unsigned maxlength);
///

char * gets(const char * string, unsigned maxlength){
        return fgets(string, maxlength, stdin);
}

///The `puts` function prints `string` to stdout.
///
///.. code-block:: c
///
///        int puts(unsigned string[]);
///

int puts(const char * string){
        return fputs(string, stdout);
}

///The `getc` returns a single character from stdin.
///
///.. code-block:: c
///
///        unsigned long getc();
///

unsigned getc(){
        return fgetc(stdin);
}

///The `putc` writes a single character to stdout.
///
///.. code-block:: c
///
///        void putc(unsigned c);
///

int putc(int c){
        return fputc(c, stdout);
}

#endif

