import os
import tqdm

wants = [
    "B21A40",
    "B21A70",
    "B21A90",
    "00000",
    "11111",
    "22222",
    "33333",
    "44444",
    "55555",
    "66666",
    "77777",
    "88888",
    "99999",
    "aaaaa",
    "bbbbb",
    "ccccc",
    "ddddd",
    "eeeee",
    "fffff",
]

# while True:
for _ in tqdm.tqdm(range(20000000)):
    # generate new key pair
    os.system("make &> /dev/null")

    # read new key pair
    with open("addr") as f:
        address = f.read().strip()
    with open("priv") as f:
        private = f.read().strip()

    for w in wants:
        n = len(w)
        if address[:n] == w:
            print("address=%s private=%s" % (address, private))
