#ifndef UTILS_H
#define UTILS_H

#include <string>
#include <iostream>
#include <fstream>
#include <chrono>
#include <tuple>

using namespace std;

void print_help(const char *argv[]) {
    cout << "Usage:\n"
    << argv[0] << " <string_to_hash>\n"
    << argv[0] << " f <file_to_hash>\n"
    << argv[0] << " t <string_to_hash> (gives hashing time)\n"
    << argv[0] << " tf <file_to_hash> (gives hashing time)\n";
}

void parse_flags(string flags, bool &time, bool &file) {
    if (flags.find("t") != string::npos) {
        time = true;
    }
    if (flags.find("f") != string::npos) {
        file = true;
    }
}

void manage_args(int argc, const char *argv[], bool &time, bool &file) {
    time = false;
    file = false;

    if (argc < 2 || argc > 3) {
        print_help(argv);
        exit(1);
    }

    if (argc == 3) {
        parse_flags(argv[1], time, file);
    }
}

string read_file(string filename) {
    ifstream file(filename, ios::in);
    if (!file.is_open()) {
        cout << "Error: could not open file " << filename << endl;
        exit(1);
    }

    string res;
    string line;
    while (getline(file, line)) {
        res += line + "\n";
    }

    return res;
}

string get_text_to_hash(int argc, const char *argv[], const bool file) {
    string text;
    if (file) {
        text = read_file(argv[2]);
    } else {
        text = argv[argc - 1];
    }
    return text;
}

tuple<bitset<256>, double> time_hash(string text, bitset<256> (*hash_f)(string), bool time) {
    auto start = chrono::high_resolution_clock::now();
    bitset<256> hash = hash_f(text);
    auto end = chrono::high_resolution_clock::now();
    double time_taken = chrono::duration_cast<chrono::nanoseconds>(end - start).count();
    time_taken *= 1e-6; // convert to milliseconds
    return make_tuple(hash, time_taken);
}

string convert_to_hex(bitset<256> hash) {
    string bits = hash.to_string(), hex, chr, tmp;
	for (unsigned int i=0; i<bits.length(); i+=4) {
		tmp = bits.substr(i,4);
		if (!tmp.compare("0000")) {
			hex = hex + "0";
		}
		else if (!tmp.compare("0001")) {
			hex = hex + "1";
		}
		else if (!tmp.compare("0010")) {
			hex = hex + "2";
		}
		else if (!tmp.compare("0011")) {
			hex = hex + "3";
		}
		else if (!tmp.compare("0100")) {
			hex = hex + "4";
		}
		else if (!tmp.compare("0101")) {
			hex = hex + "5";
		}
		else if (!tmp.compare("0110")) {
			hex = hex + "6";
		}
		else if (!tmp.compare("0111")) {
			hex = hex + "7";
		}
		else if (!tmp.compare("1000")) {
			hex = hex + "8";
		}
		else if (!tmp.compare("1001")) {
			hex = hex + "9";
		}
		else if (!tmp.compare("1010")) {
			hex = hex + "A";
		}
		else if (!tmp.compare("1011")) {
			hex = hex + "B";
		}
		else if (!tmp.compare("1100")) {
			hex = hex + "C";
		}
		else if (!tmp.compare("1101")) {
			hex = hex + "D";
		}
		else if (!tmp.compare("1110")) {
			hex = hex + "E";
		}
		else if (!tmp.compare("1111")) {
			hex = hex + "F";
		}
		else {
			continue;
		}
	}
	return hex;
}

#endif // UTILS_H
