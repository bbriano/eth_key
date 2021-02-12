package main

import (
	"crypto/ecdsa"
	"fmt"
	"log"
	"os"
	"runtime"
	"strconv"
	"strings"
	"sync"

	"github.com/ethereum/go-ethereum/common/hexutil"
	"github.com/ethereum/go-ethereum/crypto"
)

var wants []string = []string{
	"b21A90",
	"b21A70",
	"000000",
	"999999",
	"ffffff",
}

var wg sync.WaitGroup

func main() {
	n, err := strconv.ParseInt(os.Args[1], 10, 64)
	if err != nil {
		log.Fatal(err)
	}
	coreCount := runtime.NumCPU()
	nPerCore := n / int64(coreCount)
	wg.Add(coreCount)
	for i := 0; i < coreCount; i++ {
		go checkWants(nPerCore)
	}
	wg.Wait()
}

func checkWants(n int64) {
	defer wg.Done()
	for i := int64(0); i < n; i++ {
		address, private, err := GenerateKeyPair()
		if err != nil {
			log.Fatal()
		}

		for _, w := range wants {
			n := len(w)
			if strings.ToLower(address[:n]) == strings.ToLower(w) {
				fmt.Println(i, address, private)
				continue
			}
		}
	}
}

func checkWant() {
	defer wg.Done()
	address, private, err := GenerateKeyPair()
	if err != nil {
		log.Fatal()
	}

	for _, w := range wants {
		n := len(w)
		if address[:n] == w {
			fmt.Println(address, private)
			continue
		}
	}
}

func GenerateKeyPair() (string, string, error) {
	privateKey, err := crypto.GenerateKey()
	if err != nil {
		return "", "", err
	}

	privateKeyBytes := crypto.FromECDSA(privateKey)
	private := hexutil.Encode(privateKeyBytes)[2:]

	publicKey := privateKey.Public()
	publicKeyECDSA, ok := publicKey.(*ecdsa.PublicKey)
	if !ok {
		return "", "", fmt.Errorf("Failed casting public key to ECDSA")
	}

	address := crypto.PubkeyToAddress(*publicKeyECDSA).Hex()[2:]

	return address, private, nil
}
