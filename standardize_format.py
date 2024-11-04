'''
This script converts a JSON file containing a UI schema to a JSON file containing a flattened version of the pdfMappings.
The input JSON file is the 'form.json' file downloaded when export form
The output JSON file 'stddata.json' will have a structure of "uiSchema" with "ui:pdfMappings" instead of "ui:multipleOption" and "ui:pdfMapping" and remove other keys
Must run this script first to get stddata.json before running getAlias.py
'''
import json

def convert_ui_schema(data):
    result = {}

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):
                # If it has "multipleOption" and "options", flatten the pdfMappings
                if "ui:multipleOption" in value and "options" in value["ui:multipleOption"]:
                    options = value["ui:multipleOption"]["options"]
                    pdf_mappings = []

                    # Collect all pdfMappings from the options list
                    for option in options:
                        if isinstance(option, list) and len(option) > 1 and isinstance(option[1], dict):
                            pdf_mappings.extend(option[1].get("pdfMappings", []))

                    # Add the flattened pdfMappings under the group key
                    result[key] = {"ui:pdfMappings": pdf_mappings}

                # If there is already "ui:pdfMapping" present, retain it
                elif "ui:pdfMapping" in value:
                    result[key] = {
                        "ui:pdfMappings": value["ui:pdfMapping"]
                    }

                # Recursively process other dictionary entries
                else:
                    result[key] = convert_ui_schema(value)

    return result


def convert_json_files(input_file, output_file):
    # Read from the input JSON file
    with open(input_file, 'r') as f:
        data = json.load(f)
        # input_data is the 'uiSchema' key from the JSON file
        input_data = data['form']['namespaceFormSchemaMap']['main']['uiSchema']

    # Convert the data
    converted_data = convert_ui_schema(input_data)

    # Write the result to the output JSON file
    with open(output_file, 'w') as f:
        json.dump(converted_data, f, indent=2)


# Example usage
input_file = 'form.json'   # Specify the input JSON file path
output_file = 'stddata.json' # Specify the output JSON file path

convert_json_files(input_file, output_file)
