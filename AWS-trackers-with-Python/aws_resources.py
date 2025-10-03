"""AWS resources tracker

This small script enumerates AWS resources across all available regions using
the Resource Groups Tagging API (resourcegroupstaggingapi). It collects the
resource ARN, inferred resource type, tags, and region and prints a readable
summary to stdout. Results can be persisted to a timestamped JSON file.

Notes:
- The script uses boto3.Session(profile_name="default") by default; you can
  change the profile or rely on environment credentials.
- The Resource Groups Tagging API provides a central way to list tagged
  resources across many services, but not every AWS resource is taggable or
  returned by this API. For service-specific details (Amplify, etc.) consider
  adding dedicated trackers in this package.
"""

import boto3
import json
from datetime import datetime


def list_all_resources():
    """Return a list of resource dictionaries found across regions.

    Each returned dictionary contains these keys: Region, ARN, Type, Tags.

    The function:
    - Creates a boto3 Session (uses the 'default' profile and us-east-1 by
      default). Adjust `profile_name` and `region_name` as needed for your
      environment.
    - Uses `get_available_regions('ec2')` to enumerate regions. This is a
      common trick to get the full AWS region list for multi-region scans.
    - Calls the Resource Groups Tagging API's `get_resources` paginator to
      iterate pages of tagged resources.
    - Parses the ARN to extract a crude `resource_type` (the 3rd field of the
      ARN) — this is a lightweight heuristic and may be improved for complex
      ARNs or service-specific needs.
    """

    # Create a session tied to an AWS profile and a default region. If you
    # rely on environment variables or instance role credentials, remove the
    # profile_name argument.
    session = boto3.Session(profile_name="default", region_name="us-east-1")

    # Use EC2's regions list as a canonical set of AWS regions to iterate.
    regions = session.get_available_regions("ec2")
    all_resources = []

    for region in regions:
        # Informational print so the user knows scan progress.
        print(f"\n Scanning region: {region}")

        # The Resource Groups Tagging API is region-aware; create a regional
        # client so results are scoped to the current region.
        client = session.client("resourcegroupstaggingapi", region_name=region)

        try:
            # Use the paginator to handle potentially large result sets.
            paginator = client.get_paginator("get_resources")
            for page in paginator.paginate(ResourcesPerPage=50):
                # Each page contains a ResourceTagMappingList we can iterate.
                for resource in page.get("ResourceTagMappingList", []):
                    arn = resource.get("ResourceARN")

                    # Best-effort resource type extraction from ARN. Example
                    # ARN: arn:aws:ec2:us-east-1:123456789012:instance/i-0123
                    # The service portion (ec2) is at index 2 when splitting by
                    # ':' (arn:partition:service:region:account:resource).
                    resource_type = arn.split(":")[2] if arn and ":" in arn else "unknown"

                    # Tags are returned as a list of {Key,Value} dicts; convert
                    # to a simple mapping for easier consumption and JSON output.
                    tags = {t["Key"]: t["Value"] for t in resource.get("Tags", [])}

                    res_data = {
                        "Region": region,
                        "ARN": arn,
                        "Type": resource_type,
                        "Tags": tags,
                    }
                    all_resources.append(res_data)

                    # Print a friendly, English-style line for quick review.
                    print(f"➡ {arn}")
                    print(f"    Type: {resource_type}")
                    if tags:
                        print(f"    Tags: {tags}")
        except client.exceptions.ClientError as e:
            # If the call fails for a region (permission, throttling, etc.),
            # skip and continue with others. The error is printed to help
            # debugging.
            print(f" Skipping region {region} due to error: {e}")

    return all_resources


def save_to_json(data):
    """Persist `data` to a JSON file with a timestamp in the filename.

    This helper creates filenames like `aws_resources_2025-10-03_14-30-59.json`.
    """

    # Create filename with timestamp to avoid collisions and keep history.
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"aws_resources_{timestamp}.json"

    # Write indented JSON for readability.
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"\n Resources saved to {filename}")


if __name__ == "__main__":
    # When run as a script, perform a full scan and save results.
    resources = list_all_resources()
    print("\n Total resources found:", len(resources))

    # Save results to JSON with timestamp
    save_to_json(resources)
