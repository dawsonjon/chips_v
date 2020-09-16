#include <stdio.h>

unsigned fgetc(FILE handle){
	volatile unsigned int* p_reg = (unsigned int *) handle;
    return *p_reg;
}

int fputc(int c, FILE handle){
	volatile unsigned int* p_reg = (unsigned int *) handle;
	*p_reg = c;
	return c;
}

unsigned getc(FILE handle){
	volatile unsigned int* p_reg = (unsigned int *) handle;
    return *p_reg;
}

int putc(int c, FILE handle){
	volatile unsigned int* p_reg = (unsigned int *) handle;
	*p_reg = c;
	return c;
}


int putchar(int c){
	return fputc(c, stdout);
}

int getchar(){
	return fgetc(stdin);
}

int fputs(const char * string, FILE handle){
        unsigned i=0;
        while(string[i]){
                fputc(string[i++], handle);
        }
	return i;
}

int puts(const char * string){
        fputs(string, stdout);
        fputc('\n', stdout);
        return 0;
}

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

char * gets(const char * string, unsigned maxlength){
        return fgets(string, 100000000, stdin);
}


int _putchar(int c){
	volatile unsigned int* p_reg = (unsigned int *) stdout;
	*p_reg = c;
	return c;
}

