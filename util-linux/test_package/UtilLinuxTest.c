#include <stdio.h>
#include <uuid/uuid.h>

int main() {
    uuid_t uu;
    return 1 == uuid_is_null(uu);
}
