#include <stdio.h>
#include <machine.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <scan.h>

unsigned wait_clocks(unsigned clocks){
    clock_t start_time = clock();
    while((clock()-start_time) < clocks);
}

void hello_world(){
    printf("Hello World!\n");
}

void knight_rider(){
    printf("running knight rider demo...\n");
    int shifter = 1;
    for(int i=0; i<10; i++){
        printf("%u\n", i);
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
    printf("%u 32-bit integer multiplies in 1 second\n", count);

    last_clock=clock();
    count = 0;
    while(clock()-last_clock < CLOCKS_PER_SEC){
        lproduct *= 0x12345678;
        lproduct *= 0x12345678;
        lproduct *= 0x12345678;
        lproduct *= 0x12345678;
        count+=4;
    }
    printf("%u 64-bit integer multiplies in 1 second\n", count);

    last_clock=clock();
    count = 0;
    while(clock()-last_clock < CLOCKS_PER_SEC){
        product /= 0x12345678;
        product /= 0x12345678;
        product /= 0x12345678;
        product /= 0x12345678;
        count+=4;
    }
    printf("%u 32-bit integer divides in 1 second\n", count);

    last_clock=clock();
    count = 0;
    while(clock()-last_clock < CLOCKS_PER_SEC){
        lproduct /= 0x12345678;
        lproduct /= 0x12345678;
        lproduct /= 0x12345678;
        lproduct /= 0x12345678;
        count+=4;
    }
    printf("%u 64-bit integer divides in 1 second\n", count);

}

void wall_clock(){

    struct tm t;
    time_t t1;
    clock_t start_time;
    unsigned temp;

    /*set clock just before clocks go back and run*/
    printf("Year:\n");
    t.tm_year = scan_udecimal() - 1900;
    printf("Month:\n");
    t.tm_mon = scan_udecimal() - 1;
    printf("Day:\n");
    t.tm_mday = scan_udecimal();
    printf("Hour:\n");
    t.tm_hour = scan_udecimal();
    printf("Minute:\n");
    t.tm_min = scan_udecimal();
    t.tm_sec = 55;
    t.tm_isdst = 1;
    t1 = mktime(&t);
    puts(asctime(&t));
    puts(ctime(&t1));
    set_time(t1);
    t1 = time((time_t*)NULL);
    puts(ctime(&t1));

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
        printf("\nChips-V Demo\n");

        printf("\na) Hello World\n");
        printf("b) Knight Rider\n");
        printf("c) Test Multiplication\n");
        printf("d) Wall Clock\n");
        selection = getchar();
        switch(selection){
            case 'a': hello_world(); break;
            case 'b': knight_rider(); break;
            case 'c': test_multiplication(); break;
            case 'd': wall_clock(); break;
        }
    }
}
