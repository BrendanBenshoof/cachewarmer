CacheWarmer
=======================

CacheWarmer is a fast and hacky solution to allow people to donate ipfs gateways to cache other people's content.

It practically just wgets the requested hash on a list of addresses (and aborts to avoid getting your file gumming up my ram)

If you want to donate your public ipfs gateway, make a PR adding it to providers.txt

If you want to run your own instance of cachewarmer (you will have to manually pull to get updates), it should only require python3.

After cloning the repo, in a screen session run:

```
python3 pyhp_server.py 8001 

```
