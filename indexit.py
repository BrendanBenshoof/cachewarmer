import pymultihash as pmh
import re
from bs4 import BeautifulSoup
import myrequests as requests
import base64

IPFSGateway = "http://blamestross.com/ipfs/"

INDEX_PATH = "index.json"


def onecount(bloomint):
    count = 0
    while bloomint>0:
        count += bloomint % 2
        bloomint //= 2
    return count


def generateBloomFilter(wordlist):
    f = 0
    j = 0
    for w in wordlist:
        hashInt = 0
        hashVal = pmh.genHash(w, 0x12)
        for i in range(0, 10):
            try:
                tmpInt = 2**256-1
                for j in range(0,10):
                    tmpInt &= pmh.parseHash(hashVal)
                    hashVal = pmh.genHash(hashVal, 0x12)
                hashInt = (hashInt << 256) | tmpInt

            except Exception as e:
                print("error ",e)
                print(hashVal, w, i, j, len(wordlist))
            hashVal = pmh.genHash(hashVal, 0x12)
        f |= hashInt

        j += 1
    return f


def wordInFilter(bloomInt, testWord):
    hashVal = pmh.genHash(testWord, 0x12)
    hashInt = pmh.parseHash(hashVal)
    return (bloomInt & hashInt) == hashInt


def filterInFilter(bloomInt, testInt):
    return (bloomInt & testInt) == testInt


def tokenizeHTML(html):
    raw = BeautifulSoup(html, 'html.parser').get_text()
    wordlist = map(lambda x: x.strip().lower(), re.split(r'[ \n\t]', raw))
    longlist = filter(lambda x: len(x) > 1, wordlist)
    return list(set(longlist))


def indexFile(IPFSHash):
    path = IPFSGateway+IPFSHash
    req = requests.get(path)
    print("got request")
    rawText = req.text
    bloom = generateBloomFilter(tokenizeHTML(rawText))
    return bloom
