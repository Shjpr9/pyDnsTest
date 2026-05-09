from utils import *
import dns.resolver
import time
import requests
import json

TIMEOUT = 300


def main():
    target = input("Enter the domain: ")
    result_ip = "na"
    target_ips = []
    ips = extract_ips()
    for ip in ips:
        try:
            resolver = dns.resolver.Resolver()
            resolver.nameservers = [ip]
            resolver.timeout = TIMEOUT / 1000
            resolver.lifetime = TIMEOUT / 1000

            start = time.perf_counter()
            result = resolver.resolve(target)
            end = time.perf_counter()

            latency = (end - start) * 1000

            if len(result) and str(result[0]) != "10.10.34.36":
                print(f"Resolver: {ip} | {latency:.2f}ms")
                print("Answer(s): ")
                for answer in result:
                    target_ips.append(str(answer))
                    print(answer)
                
                result_ip = result[0]
                break
        except Exception:
            pass

    if result_ip == "na":
        print("No answer returned by DNSs! exiting...")
        exit(0)

    print("--------------")
    print("Getting ip info....")
    while True:
    # Try until we get the result
        try:
            ip_info_raw = requests.get(f"https://api.lookip.ir/ip/info/{result_ip}")
            ip_info = json.loads(ip_info_raw.text)
            
            # Check if this is a rate limit response (has 'code' field)
            if "code" in ip_info and ip_info["code"] == 429:
                print("Rate limit exceeded! waiting 10s...")
                time.sleep(10)
                continue
            
            # Success case - these fields should exist
            print("Query IP: ", ip_info.get("query_ip", "N/A"))
            print("Country: ", ip_info.get("country", "N/A"))
            print("ASN Name: ", ip_info.get("asn_name", "N/A"))
            break
            
        except Exception:
            pass
    
        time.sleep(3)

    print("Saving the result...")
    add_result_to_json(target, target_ips, ip_info.get("asn_name", "N/A"))


if __name__ == "__main__":
    main()
    input("Press Enter to exit.")