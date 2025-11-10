import re
from collections import defaultdict

# Path to the Locust log file to analyze. Change this if your logs are named differently.
logfile = "locust_logs_highload.txt"


# Captures named groups:
#  - method: HTTP method (GET/POST)
#  - path: endpoint path starting with '/'
#  - fails: failure count and percentage like "0(0.00%)"
#  - avg/min/max/med: response time metrics in milliseconds
pattern = re.compile(
    r"(?P<method>GET|POST)\s+(?P<path>/[^\s]*)\s+(\d+)\s+(?P<fails>\d+\(\d+\.\d+%\))\s+\|\s+"
    r"(?P<avg>\d+)\s+(?P<min>\d+)\s+(?P<max>\d+)\s+(?P<med>\d+)\s+\|"
)

# Aggregation structure: for each "METHOD /path" we keep counters and lists of
# observed statistics so we can compute means and find maxima later.
summary = defaultdict(lambda: {
    "count": 0,
    "fails": 0,
    "avg_list": [],
    "min_list": [],
    "max_list": [],
    "med_list": []
})

with open(logfile, "r") as f:
    # Read the log file line-by-line and try to match the regex on each line.
    for line in f:
        match = pattern.search(line)
        # If a stats line matches, extract fields and accumulate them.
        if match:
            method = match.group("method")
            path = match.group("path")
            fails_str = match.group("fails")
            # Convert captured timing strings to integers (milliseconds).
            avg = int(match.group("avg"))
            min_ = int(match.group("min"))
            max_ = int(match.group("max"))
            med = int(match.group("med"))
            # "fails" field has format like "0(0.00%)"; take the leading number.
            fails = int(fails_str.split("(")[0])

            key = f"{method} {path}"
            # Update aggregation
            summary[key]["count"] += 1
            summary[key]["fails"] += fails
            summary[key]["avg_list"].append(avg)
            summary[key]["min_list"].append(min_)
            summary[key]["max_list"].append(max_)
            summary[key]["med_list"].append(med)

# --- Reporting: summarize aggregated results and print useful diagnostics ---
# Total counts across all endpoints
total_requests = sum(v["count"] for v in summary.values())
total_fails = sum(v["fails"] for v in summary.values())
print(f"Total endpoints: {len(summary)}")
print(f"Total requests: {total_requests}")
print(f"Total failures: {total_fails} ({(total_fails/total_requests*100):.2f}%)\n")

# Top 3 slowest endpoints by average response time.
# We compute the mean of the recorded avg values for each endpoint and sort descending.
slowest = sorted(summary.items(), key=lambda x: sum(x[1]["avg_list"]) / len(x[1]["avg_list"]), reverse=True)[:3]
print("Top 3 slowest endpoints (avg response time):")
for k, v in slowest:
    avg_time = sum(v["avg_list"]) / len(v["avg_list"])
    print(f"{k}: avg={avg_time:.2f}ms, max={max(v['max_list'])}ms, fails={v['fails']}")

# Top 3 endpoints by request count (most frequently exercised endpoints).
most_requests = sorted(summary.items(), key=lambda x: x[1]["count"], reverse=True)[:3]
print("\nTop 3 endpoints by request count:")
for k, v in most_requests:
    print(f"{k}: requests={v['count']}, avg={sum(v['avg_list'])/len(v['avg_list']):.2f}ms, fails={v['fails']}")

 