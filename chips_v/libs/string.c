/*helpful macros*/

#define UNALIGNED(A, B) (((unsigned)A | (unsigned)B) & 3)
#define DETECTNULL(X) (((X) - 0x01010101) & ~(X) & 0x80808080)

/* Copy operations */

char *strcpy(char *to, const char *from){

    unsigned * lto = (unsigned*) to;
    unsigned * lfrom = (unsigned*) from;

    if(!UNALIGNED(lto, lfrom)){
        while(!DETECTNULL(*lfrom)){
            *lto++ = *lfrom++;
        }
    }

    char * cto = (char*) lto;
    char * cfrom = (char*) lfrom;
    while((*cto++ = *cfrom++));

    return to;

}

char *strncpy(char *to, char *from, unsigned len){

    unsigned * lto = (unsigned*) to;
    unsigned * lfrom = (unsigned*) from;

    if(!UNALIGNED(lto, lfrom)){
        while(!DETECTNULL(*lfrom) && len >= 4){
            *lto++ = *lfrom++;
            len -= 4;
        }
    }

    char * cto = (char*) lto;
    char * cfrom = (char*) lfrom;
    while(len > 0){
        --len;
        if (!(*cto++ = *cfrom++)) break;
    }

    while(len-- > 0) *cto = 0;

    return to;
}

void * memcpy(void * to, const void * from, unsigned len){

    unsigned * lto = (unsigned*) to;
    unsigned * lfrom = (unsigned*) from;

    if(!UNALIGNED(lto, lfrom)){
        while(len >= 16){
            *lto++ = *lfrom++;
            *lto++ = *lfrom++;
            *lto++ = *lfrom++;
            *lto++ = *lfrom++;
            len-=16;
        }
        while(len >= 4){
            *lto++ = *lfrom++;
            len-=4;
        }
    }

    char * cto = (char*) lto;
    char * cfrom = (char*) lfrom;
    while(len--){
        *cto++ = *cfrom++;
    }

    return to;
}

void *memmove(void * to, void * from, unsigned n){
    unsigned char tmp[n];
	memcpy(tmp, from, n);
	memcpy(to, tmp, n);
    return to;
}

/* Miscellaneous String Operations */

unsigned strlen(char s[]){
	unsigned i = 0;
	while(s[i]) i++;
	return i;
}

void *memset(void * s, unsigned value, unsigned n){
    char *cs = (char *)s;
	int i;
	for(i=0; i<n; i++){
		cs[i] = value;
	}
    return s;
}

/* String Concatenation Operations */

char *strcat(char *a, const char *b){
	unsigned i=0, j=0;
	while(a[i]) i++;
	i++;
	while(b[j]){
		a[i] = b[j];
		i++;
		j++;
	}
    return a;
}

char *strncat(char * a, const char *b, unsigned n){
	unsigned i=0, j=0;
	while(a[i]) i++;
	i++;
	while(b[j] && j < n){
		a[i] = b[j];
		i++;
		j++;
	}
    return a;
}

/* String Comparison Operations */

int strcmp(const char *a, const char *b){

    unsigned * la = (unsigned*) a;
    unsigned * lb = (unsigned*) b;

    if(!UNALIGNED(la, lb)){
        while(*la == *lb){
            if(!DETECTNULL(*lb))
                return 0;  /* equal */

            la++;
            lb++;
        }

        a = (char *)la;
        b = (char *)lb;
    }
    while (*a != '\0' && *a == *b)
    {
      a++;
      b++;
    }

    return (*(unsigned char *) a) - (*(unsigned char *) b);
}

int strncmp(const char *a, const char *b, unsigned n){
	unsigned i=0;
	while(a[i] && b[i] && i < n){
		if(a[i] > b[i]){
			return 1;
		} else if(a[i] < b[i]) {
			return -1;
		}
		i++;
	}
	return 0;
}

int memcmp(const void* str1, const void * str2, unsigned n){
    char *a = (char*) str1;
    char *b = (char*) str2;
	unsigned i=0;
	while(i < n){
		if(a[i] > b[i]){
			return 1;
		} else if(a[i] < b[i]) {
			return -1;
		}
		i++;
	}
	return 0;
}

/* String Search Operations */

/* return the position of character f in string s starting from start of s */
char *strchr(const char * s, int f){
	unsigned i;
	for(i=0; i<strlen(s); i++){
		if(s[i] == f) return &s[i];
	}
	return -1;
}

/* return the position of character f in string s starting from end of s */
char *strrchr(const char * s, char f){
	unsigned i;
	for(i=strlen(s)-1; i; i--){
		if(s[i] == f) return &s[i];
	}
	return -1;
}

/* return the number of characters at the start of string a that contain any character in string b */
unsigned strspn(const char *a, const char *b){
	unsigned i, j, match;
	for(i=0; i<strlen(a); i++){
		match = 0;
		for(j=0; j<strlen(b); j++){ 
			if(a[i] == b[j]){
				match = 1;
				break;
			}
		}
		if(!match) return i;
	}
}

/* return the number of characters at the start of string a that do not contain any character in b */
unsigned strcspn(const char *a, const char *b){
	unsigned i, j, match;
	for(i=0; i<strlen(a); i++){
		match = 0;
		for(j=0; j<strlen(b); j++){
			if(a[i] == b[j]){
				match = 1;
				break;
			}
		}
		if(match) return i;
	}
}

/* return first occurrence of the any character in string b within string a */
/* return -1 if not found */
unsigned strpbrk(const char *a, const char *b){
	unsigned i, j;
	for(i=0; i<strlen(a); i++){
		for(j=0; j<strlen(b); j++){
			if(a[i] == b[j]) return i;
		}
	}
	return -1;
}

/* return first occurrence of the whole of string b within string a */
/* return -1 if not found */
unsigned strstr(const char *a, const char *b){
	unsigned i, j, match;
	for(i=0; i<strlen(a); i++){
		match = 1;
		for(j=0; j<strlen(b); j++){
			if(a[i+j] != b[j]){
				match=0;
				break;
			}		
		}
		if(match) return match;
	}
	return -1;
}
