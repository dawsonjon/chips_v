#include <stdio.h>
#include <time.h>
#include <machine.h> /* make leds visible */

void main(){
  clock_t start_time;

  start_time = clock();
  while(1){
    while(clock()-start_time > CLOCKS_PER_SEC); /*CLOCKS_PER_SEC matches the value in spec.py*/
    start_time += CLOCKS_PER_SEC;
    fputc(1, leds);
    while(clock()-start_time > CLOCKS_PER_SEC);
    start_time += CLOCKS_PER_SEC;
    fputc(0, leds);
  }

}
