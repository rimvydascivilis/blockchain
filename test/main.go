package main

import (
	"crypto/md5"
	"crypto/sha1"
	"crypto/sha256"
	"flag"
	"fmt"
	"os"
	"time"
)

func main() {
	hashing_algorithm := flag.String("algo", "md5", "Hashing algorithm to use")
	file_path := flag.String("file", "", "File to hash")
	text := flag.String("text", "", "Text to hash")
	flag.Parse()
	text_to_hash := get_text_to_hash(*file_path, *text)

	hashing_f := get_hashing_function(*hashing_algorithm)
	if hashing_f == nil {
		fmt.Println("Invalid hashing algorithm")
		return
	}

	start := time.Now()
	hash := hashing_f(text_to_hash)
	elapsed := time.Since(start).Milliseconds()

	fmt.Printf("%x %d\n", hash, elapsed)
}

func get_hashing_function(algorithm string) func([]byte) []byte {
	switch algorithm {
	case "sha1":
		return func(data []byte) []byte {
			hash := sha1.Sum(data)
			return hash[:]
		}
	case "sha256":
		return func(data []byte) []byte {
			hash := sha256.Sum256(data)
			return hash[:]
		}
	case "md5":
		return func(data []byte) []byte {
			hash := md5.Sum(data)
			return hash[:]
		}
	default:
		return nil
	}
}

func get_text_to_hash(fp string, text string) []byte {
	if fp == "" {
		return []byte(text)
	} else {
		return read_file(fp)
	}

}

func read_file(fp string) []byte {
	content, err := os.ReadFile(fp)
	if err != nil {
		panic(err)
	}
	return content
}
