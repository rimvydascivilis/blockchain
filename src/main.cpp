#include "hash.h"
#include "utils.h"

#include <iostream>
#include <string>
#include <bitset>

using namespace std;

int main(int argc, const char *argv[]) {
    bool time, file; // flags
    manage_args(argc, argv, time, file);

    string text = get_text_to_hash(argc, argv, file);
    auto [hash, duration] = time_hash(text, hash_f, time);

    if (time) {
        cout << "Hashing time: " << duration << " ms" << endl;
    }
    cout << "Hash: " << convert_to_hex(hash) << endl;
}
