#include <stdio.h>
#include <machine.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <scan.h>
#include <print.h>
#include "enigma.h"

unsigned wait_clocks(unsigned clocks){
    clock_t start_time = clock();
    while((clock()-start_time) < clocks);
}

void hello_world(){
    puts("Hello World!");
}

void knight_rider(){
    puts("running knight rider demo...");
    int shifter = 1;
    for(int i=0; i<10; i++){
        print_udecimal(i, 0); putchar('\n');
        while(shifter < 0x80){
            shifter <<= 1;
            fputc(shifter, leds);
            wait_clocks(CLOCKS_PER_SEC/10);
        }
        while(shifter > 1){
            shifter >>= 1;
            fputc(shifter, leds);
            wait_clocks(CLOCKS_PER_SEC/10);
        }
    }
    fputc(0, leds);
}

void pwm_demo(){
    puts("running PWM demo...");
    int i, j;
    for(j=0; j<10; j++){
      print_udecimal(j, 0); putchar('\n');
      for(i=0; i<=1023; i++){
          fputc(i, pwm);
          wait_clocks(CLOCKS_PER_SEC/1000);
      }
      for(i=1023; i>=0; i--){
          fputc(i, pwm);
          wait_clocks(CLOCKS_PER_SEC/1000);
      }
    }
    fputc(0, pwm);
}

void test_multiplication(){
    volatile unsigned product = 1;
    volatile unsigned long long lproduct = 1;
    unsigned count;
    clock_t last_clock;

    last_clock=clock();
    count = 0;
    while(clock()-last_clock < CLOCKS_PER_SEC){
        product *= 0x12345678;
        product *= 0x12345678;
        product *= 0x12345678;
        product *= 0x12345678;
        count+=4;
    }
    print_udecimal(count, 0);
    puts(" 32-bit integer multiplies in 1 second");

    last_clock=clock();
    count = 0;
    while(clock()-last_clock < CLOCKS_PER_SEC){
        lproduct *= 0x12345678;
        lproduct *= 0x12345678;
        lproduct *= 0x12345678;
        lproduct *= 0x12345678;
        count+=4;
    }
    print_udecimal(count, 0);
    puts(" 64-bit integer multiplies in 1 second");

    last_clock=clock();
    count = 0;
    while(clock()-last_clock < CLOCKS_PER_SEC){
        product /= 0x12345678;
        product /= 0x12345678;
        product /= 0x12345678;
        product /= 0x12345678;
        count+=4;
    }
    print_udecimal(count, 0);
    puts(" 32-bit integer divides in 1 second");

    last_clock=clock();
    count = 0;
    while(clock()-last_clock < CLOCKS_PER_SEC){
        lproduct /= 0x12345678;
        lproduct /= 0x12345678;
        lproduct /= 0x12345678;
        lproduct /= 0x12345678;
        count+=4;
    }
    print_udecimal(count, 0);
    puts(" 64-bit integer divides in 1 second");

}

void wall_clock(){

    struct tm t;
    time_t t1;
    clock_t start_time;
    unsigned temp;

    /*set clock just before clocks go back and run*/
    puts("Year:");
    t.tm_year = scan_udecimal() - 1900;
    puts("Month:");
    t.tm_mon = scan_udecimal() - 1;
    puts("Day:");
    t.tm_mday = scan_udecimal();
    puts("Hour:");
    t.tm_hour = scan_udecimal();
    puts("Minute:");
    t.tm_min = scan_udecimal();
    t.tm_sec = 55;
    t.tm_isdst = 1;
    t1 = mktime(&t);
    set_time(t1);

    start_time = clock();
    for(int i=0; i<100; i++){
        while(difftime(clock(), start_time) < CLOCKS_PER_SEC);
        start_time += CLOCKS_PER_SEC;
        t1 = time((time_t*)NULL);
        puts(ctime(&t1));
    }
}

void main(){
    char selection;

    while(1){
        puts("\nChips-V Demo");

        puts("\na) Hello World");
        puts("b) Knight Rider");
        puts("c) Test Multiplication");
        puts("d) Wall Clock");
        puts("e) Enigma Machine");
        puts("f) PWM Demo");
        selection = getchar();
        switch(selection){
            case 'a': hello_world(); break;
            case 'b': knight_rider(); break;
            case 'c': test_multiplication(); break;
            case 'd': wall_clock(); break;
            case 'e': enigma_demo(); break;
            case 'f': pwm_demo(); break;
        }
    }
}
