import socket
import time
import argparse


def tcping(host, port, count, timeout, interval):
    success_count = 0
    failure_count = 0
    latencies = []

    for i in range(count):
        start_time = time.time()

        try:
            with socket.create_connection((host, port), timeout=timeout):
                latency = (time.time() - start_time) * 1000
                print(f"Connecting to {host}:{port} ... "
                      f"Success ({latency:.0f} ms)")
                latencies.append(latency)
                success_count += 1
        except socket.timeout:
            print(f"Connecting to {host}:{port} ... Timeout")
            failure_count += 1
        except Exception as e:
            print(f"Connecting to {host}:{port} ... Error: {str(e)}")
            failure_count += 1

        if i < count - 1:
            time.sleep(interval)

    if latencies:
        min_latency = min(latencies)
        max_latency = max(latencies)
        avg_latency = sum(latencies) / len(latencies)
    else:
        min_latency = max_latency = avg_latency = 0

    print("\nResults:")
    print(f"Total tries: {count}")
    print(f"Successes: {success_count}")
    print(f"Failures: {failure_count}")
    if success_count > 0:
        print(f"Min: {min_latency:.0f} ms, Max: {max_latency:.0f} ms, "
              f"Avg: {avg_latency:.0f} ms")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCPing - "
                                                 "check TCP port availability")
    parser.add_argument("host", help="Host to check (IP address or domain)")
    parser.add_argument("port", type=int, help="Port to check")
    parser.add_argument("--count", type=int, default=4,
                        help="Number of attempts (default 4)")
    parser.add_argument("--timeout", type=int, default=2,
                        help="Timeout for each connection "
                             "attempt in seconds (default 2)")
    parser.add_argument("--interval", type=int, default=1,
                        help="Interval between requests "
                             "in seconds (default 1)")

    args = parser.parse_args()

    tcping(args.host, args.port, args.count, args.timeout, args.interval)
