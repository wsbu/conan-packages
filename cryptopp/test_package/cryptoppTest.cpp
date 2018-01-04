#include <iostream>
#include <sstream>
#include <cstring>
#include <iomanip>
#include <cryptopp/sha.h>

template<typename TInputIter>
std::string make_hex_string(TInputIter first, TInputIter last)
{
    std::ostringstream ss;
    ss << std::hex << std::setfill('0');
    ss << std::uppercase;
    while (first != last)
        ss << std::setw(2) << static_cast<int>(*first++);
    return ss.str();
}

int main () {
    const std::string str = "hello";

    byte             digest[CryptoPP::SHA256::DIGESTSIZE];
    CryptoPP::SHA256 HASH;
    HASH.CalculateDigest(digest, (byte *) str.c_str(), str.size());

    digest[64] = 0;
    const std::string expected = "2CF24DBA5FB0A30E26E83B2AC5B9E29E1B161E5C1FA7425E73043362938B9824";
    const std::string actual = make_hex_string(std::begin(digest), std::end(digest));

    std::cout << "Actual:   " << actual << std::endl;
    std::cout << "Expected: " << expected << std::endl;

    return actual != expected;
}
