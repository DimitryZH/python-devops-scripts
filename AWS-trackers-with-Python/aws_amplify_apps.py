import boto3
import json

def list_amplify_apps(region):
    client = boto3.client("amplify", region_name=region)
    apps = []
    paginator = client.get_paginator("list_apps")
    for page in paginator.paginate():
        for app in page.get("apps", []):
            apps.append({
                "Region": region,
                "AppId": app["appId"],
                "Name": app["name"],
                "ARN": app["appArn"],
                "DefaultDomain": app.get("defaultDomain"),
                "Repository": app.get("repository")
            })
    return apps

def main():
    session = boto3.session.Session()
    regions = session.get_available_regions("amplify")

    all_apps = []
    for region in regions:
        try:
            apps = list_amplify_apps(region)
            if apps:
                all_apps.extend(apps)
        except Exception as e:
            print(f"Error in {region}: {e}")

    # Print results to console
    print(json.dumps(all_apps, indent=4))

    # Save to JSON file
    with open("aws_amplify_apps.json", "w") as f:
        json.dump(all_apps, f, indent=4)

    print("\n Results saved to aws_amplify_apps.json")

if __name__ == "__main__":
    main()
