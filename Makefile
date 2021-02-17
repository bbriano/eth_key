# Generate ethereum private,public key and address
#
# key
# key -> priv
# key -> pub -> addr

.PHONY: default clean

default: clean priv addr

clean:
	rm -f addr pub priv key

addr: pub
	cat pub | keccak-256sum -x -l | tr -d ' -' | tail -c 41 > addr

pub: key
	cat key | grep pub -A 5 | tail -n +2 | tr -d '\n[:space:]:' | sed 's/^04//' > pub

priv: key
	cat key | grep priv -A 3 | tail -n +2 | tr -d '\n[:space:]:' | sed 's/^00//' > priv

key:
	openssl ecparam -genkey -name secp256k1 | openssl ec -text > key
