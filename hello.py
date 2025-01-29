import json

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

# Parse JSON
parsed_data = json.loads(json_string)

def flatten_json(obj, prefix=''):
    """Recursively flattens nested JSON into key-value pairs with bracket notation."""
    flattened = {}
    
    if isinstance(obj, dict):
        for key, value in obj.items():
            new_prefix = f"{prefix}[{key}]" if prefix else key
            flattened.update(flatten_json(value, new_prefix))
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            new_prefix = f"{prefix}[{index}]"  # Use bracket notation for arrays
            flattened.update(flatten_json(value, new_prefix))
    else:
        flattened[prefix] = obj
    
    return flattened

# Flatten JSON
flattened_data = flatten_json(parsed_data)

# Generate the curl command using bracket notation
curl_command = 'curl -X POST "https://example.com/api" \\\n'
for key, value in flattened_data.items():
    # Replace dot notation with bracket notation
    key = key.replace('.', '][').replace('[', '[', 1)  # Keep the first '[' after the root
    curl_command += f'  -F "{key}={value}" \\\n'

# Remove trailing backslash and newline
curl_command = curl_command.rstrip(" \\\n")

print(curl_command)
