#include <stdio.h>
#include <machine.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

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

void wall_clock(){
    tm *t;
    time_t t1;
    t->tm_year = 1985 - 1900;
    t->tm_mon = 10 - 1;
    t->tm_mday = 25;
    t->tm_hour = 1;
    t->tm_min = 21;
    t->tm_sec = 0;
    t->tm_isdst = -1; /*negative value uatomatically determines dst*/
    set_time(mktime(t));
    while(1){
        t1 = time((time_t*)NULL);
        t = localtime(&t1);
        puts(asctime(t));
        wait_clocks(CLOCKS_PER_SEC);
    }
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

void mem_test(){
    char from[100];
    char to[100];

    //fill from memory
    for(int i=0; i<100; i++){
        from[i] = i;
    }

    //test memcpy
    for(int j=0; j<4; j++){
        printf("alignment %u...", j);
        memcpy(to+j, from, 100-j);
        for(int i=j; i<100; i++){
            if(from[i] != to[i]+j){
                printf("fail\n");
                return;
            }
        }
        printf("pass\n");
    }

    void *a, *b, *c;

    a = malloc(16);
    b = malloc(32);
    c = malloc(64);
    for(int i=0; i<100; i++){
        free(a);
        a = malloc(64);
        free(b);
        b = malloc(32);
        free(c);
        c = malloc(16);
        printf("Allocated %08x %08x %08x\n", (int)a, (int)b, (int)c);
    }
    free(a);
    free(b);
    free(c);


}


void main(){
    char selection;

    while(1){
        printf("\nChips-V Demo\n");
        printf("\na) Hello World\n");
        printf("b) Knight Rider\n");
        printf("c) Stop Watch\n");
        printf("d) Test Multiplication\n");
        printf("e) Test Memory\n");
        selection = getchar();
        switch(selection){
            case 'a': hello_world(); break;
            case 'b': knight_rider(); break;
            case 'c': wall_clock(); break;
            case 'd': test_multiplication(); break;
            case 'e': mem_test(); break;
        }
    }
}
