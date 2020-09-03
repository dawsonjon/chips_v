int main(){

    int* a;
    a = 0x4;
    *a = 0x12345678;

    int i;
    for(i=0; i<10; i++){
        a = i * 0x4;
        *a = i;
    }

    return a;
}
