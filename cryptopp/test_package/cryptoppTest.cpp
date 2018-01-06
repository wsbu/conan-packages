#include <iostream>
#include <sstream>
#include <cstring>
#include <iomanip>
#include <cryptopp/sha.h>

std::string make_hex_string(const byte *bytes, const size_t size)
{
    std::ostringstream ss;
    ss << std::hex << std::setfill('0');
    ss << std::uppercase;
    for (size_t i = 0; i < size; ++i)
        ss << std::setw(2) << static_cast<int>(bytes[i]);
    return ss.str();
}

int main () {
    const std::string str = "hello";

    byte             digest[CryptoPP::SHA256::DIGESTSIZE];
    CryptoPP::SHA256 HASH;
    HASH.CalculateDigest(digest, (byte *) str.c_str(), str.size());

    digest[64] = 0;
    const std::string expected = "2CF24DBA5FB0A30E26E83B2AC5B9E29E1B161E5C1FA7425E73043362938B9824";
    const std::string actual = make_hex_string(digest, CryptoPP::SHA256::DIGESTSIZE);

    std::cout << "Actual:   " << actual << std::endl;
    std::cout << "Expected: " << expected << std::endl;

    return actual != expected;
}
