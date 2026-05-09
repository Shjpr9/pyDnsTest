import dns.resolver
import time
import statistics
from time import sleep
from utils import *


domain_input = input("Enter domain(s) to check DNSs (Separate with comma): ")
TEST_DOMAINS = domain_input.split(",")
ATTEMPTS = 5                    # number of tries per DNS
TIMEOUT = 300                   # ms
SLEEP_DELAY = 0


def test_dns_server(ip):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [ip]
    resolver.timeout = TIMEOUT / 1000
    resolver.lifetime = TIMEOUT / 1000

    latencies = []
    ok_count = 0
    for TEST_DOMAIN in TEST_DOMAINS:
        for _ in range(ATTEMPTS):
            try:
                start = time.perf_counter()
                resolver.resolve(TEST_DOMAIN)
                end = time.perf_counter()
                latencies.append((end - start) * 1000)  # convert to ms
                ok_count += 1
            except Exception:
                pass  # skip failed attempt

            # Let's give it a delay to see if there is any rate limit
            sleep(SLEEP_DELAY / 1000)

    if len(latencies) == 0:
        return None, 0  # DNS completely failed

    avg_latency = statistics.mean(latencies)
    return avg_latency, ok_count


def main():
    ips = extract_ips()
    print(f"Found {len(ips)} IPs\n")

    output = []

    for ip in ips:
        result, count = test_dns_server(ip)
        if result is None:
            print(f"{ip}: FAIL")
        else:
            print(f"{ip}: OK  |  Avg latency: {result:.2f} ms | {count}/5")
            output.append((result, ip, count))

    print("----------------")
    if len(output):
        print("Sorted output:")
        output.sort()
        for latency, ip, count in output:
            print(f"{ip} | {latency:.2f} ms | {count}/5")
    else:
        print("No working DNS found!")

if __name__ == "__main__":
    main()
    input("Press Enter to exit.")
