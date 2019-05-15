#include <string>
#include <iostream>
#include <atca_basic.h>

using namespace std;

static const string EXPECTED_VERSION = "20190304";

int main () {
    char actualVersion[32];
    const auto status = atcab_version(actualVersion);

    if (status) {
        return status;
    }

    const string actualVersionStr = actualVersion;
    if (EXPECTED_VERSION != actualVersionStr) {
        cerr << "Expected " << EXPECTED_VERSION << " but got " << actualVersionStr << " instead." << endl;
        return -1;
    } else {
        return 0;
    }
}
