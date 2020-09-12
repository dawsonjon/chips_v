#include <stdio.h>

int get_timer(){
	volatile unsigned int* p_reg = (unsigned int *) 0x80000000;
    return *p_reg;
}

void main(){

    int kernel[128];
    int data[128];
    int i;
    volatile int sample;

    putc('x');
    for(i=0; i<64; i++){
        kernel[i] = i;
        data[i] = i;
        putc('0'+i);
    }
    
    putc('a');
    putc(get_timer());
    sample = 0;
    for(i=0; i<64; i++){
        sample += (kernel[i]*data[i]);
    }
    putc(get_timer());
    putc('b');

}
