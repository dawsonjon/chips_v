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

#include <stdio.h>
#include <print.h>

void main(){
    print_decimal(12345);
}
