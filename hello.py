import json
import sys
import subprocess

# Sample JSON data
json_string = '''
{
    "DoEncryptModules": false,
    "Version": "1.0.27",
    "FileType": 1,
    "ContainerName": "1.0.27-alpha",
    "Description": "1.0.27-alpha",
    "Authors": ["Mathias Seipel"],
    "Tags": ["Level:1", "SN:A", "#01:ABC"],
    "DependencyGroups": [
        {
            "targetFramework": "any",
            "dependencies": [
                {"id": "AMP", "range": "[1.0.0, 1.0.0]"},
                {"id": "ESP_GEN", "range": "[1.0.0, 1.0.0]"},
                {"id": "DM_RL", "range": "[1.0.0, 1.0.0]"}
            ]
        }
    ],
    "StateID": 2,
    "ReleaseNotes": "Published from AMP 1.0.27-alpha",
    "CurrentAuthorId": 1,
    "ID": 5,
    "Name": "AMP",
    "LatestVersion": "1.0.27",
    "IsPersonal": false,
    "PublishedState": 0
}
'''




# Build form data object
def flatten_json(obj, prefix=''):
    """Recursively flattens nested JSON into key-value pairs using dot notation and bracket indices."""
    flattened = {}

    match obj:
        case dict():
            for key, value in obj.items():
                new_prefix = f"{prefix}.{key}" if prefix else key
                flattened.update(flatten_json(value, new_prefix))
        case list():
            for index, value in enumerate(obj):
                new_prefix = f"{prefix}[{index}]"  # Use bracket notation for indices
                flattened.update(flatten_json(value, new_prefix))
        case _:  # Default case (base values like int, str, bool)
            flattened[prefix] = obj

    return flattened

# Check BaseUrl
def get_base_package_service_url(base_url):
    if "localhost" in base_url:
        return ["http://localhost:5006/", "http://host.docker.internal:9000/"]
    return [base_url]

def build_form_data(parsed_data):
    print("Building form data object")


def main(PackageMetadata, PackageContentS3Key, Email, BaseUrl, parsed_data):
    print(f"Start building ...")
    
    base_urls = get_base_package_service_url(BaseUrl)
    package_service_base_url = base_urls[0]
    minio_base_url = base_urls[1]

    # Flatten JSON
    flattened_data = flatten_json(parsed_data)

    # Generate the curl command using --form
    curl_command = 'curl -X POST "https://example.com/api" \\\n'
    for key, value in flattened_data.items():
        curl_command += f'  --form "{key}={value}" \\\n'

    # Remove trailing backslash and newline
    curl_command = curl_command.rstrip(" \\\n")

    print(curl_command)
    result = subprocess.run(curl_command, capture_output=True, text=True)

    # Print output
    print("Response:", result.stdout)
    print("Error:", result.stderr)

if __name__ == "__main__":
    PackageMetadata = sys.argv[1]
    PackageContentS3Key = sys.argv[2]
    Email = sys.argv[3]
    BaseUrl = sys.argv[4]
    # Parse JSON
    PackageMetadataAsJsonString = json.dumps(PackageMetadata)
    parsed_data = json.loads(PackageMetadataAsJsonString)
    main(PackageMetadata, PackageContentS3Key, Email, BaseUrl, parsed_data)

