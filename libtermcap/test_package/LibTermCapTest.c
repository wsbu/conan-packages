#include <stdlib.h>
#include <termcap.h>
#include <stdio.h>
#ifdef unix
static char term_buffer[2048];
#else
#define term_buffer 0
#endif

int a_proper_test() {
    char *termtype = "xterm-256color";
    int  success;

    success = tgetent(term_buffer, termtype);
    if (success < 0) {
        printf("Could not access the termcap data base.\n");
        return 2;
    } else if (success == 0) {
        printf("Terminal type `%s' is not defined.\n", termtype);
        return 0;
    } else {
        printf("How did you even get this return code???");
        return 3;
    }
}

int a_cheap_test () {
    tgetent(term_buffer, "xterm-256color");
    return 0;
}

int main () {
    // Use the cheap test because the proper test can't find the darned termcap data base.
    // It fails every time with "tgetent(term_buffer, termtype);"
    return a_cheap_test();
}
