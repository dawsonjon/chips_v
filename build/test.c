/*void putc(char c){
    char* a;
    a = 0x12345678;
    *a = c;
}*/

/*void print_decimal(unsigned i){
    int mask = 1000000000;

    while(mask){
        putc(i/mask + '0');
        i %= mask;
        mask /= 10;
    }

}*/

int get_timer(){
	volatile unsigned int* p_reg = (unsigned int *) 0x80000000;
    return *p_reg;
}

#include <stdio.h>
#include <print.h>

void main(){
    putc(get_timer());
    print_decimal(12345);
    putc(get_timer());
}
