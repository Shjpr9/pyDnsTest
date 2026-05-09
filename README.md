# PyDnsTest
### A small tool to fetch dns information of domains

- `main.py` takes a list of domains in input and tries to resolve those domains via list.txt resolvers. Then it returns the fastest dns reslovers for your network
- `getIp.py` takes only one domain and resolve its ips, then it tries to get its ASN and save it in domain_ips.json for further analysis.
