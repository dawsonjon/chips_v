void main(){

    char* a;
    a = 0x12345678;

    const char string[] = "hello world!";
    int i;
    while(string[i]){
        *a = string[i++];
    }

}
