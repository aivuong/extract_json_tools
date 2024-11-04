'''
Must run standardfromat.py first to get stddata.json before running getAlias.py
The result in output.txt will be the list of keys that have ui:pdfMappings that contain the search string
'''
import json


def findAliasWithKeyUIpdfMappingContain(data, include_strings, exclude_strings):
    result = []

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):
                # Check if the dictionary has 'ui:pdfMappings' or 'ui:pdfMapping'
                if "ui:pdfMappings" in value:
                    pdf_mappings = value["ui:pdfMappings"]
                    # Check if any value in 'ui:pdfMappings' starts with include_strings and excludes exclude_strings
                    for item in pdf_mappings:
                        if all(include in item for include in include_strings) and not any(exclude in item for exclude in exclude_strings):
                            result.append(f"logic.{key}")

                # Recursively search within nested structures
                result.extend(findAliasWithKeyUIpdfMappingContain(value, include_strings, exclude_strings))

    return result


def write_results_to_file(results, output_file):
    with open(output_file, "w") as file:
        file.write(f"{results}\n")


# Example usage
file_path = "stddata.json"
output_file = "output.txt"
numberOfN = 32  # max number of N is 31


def getAllAliasHavingPdfMappingOfN(data, needed_string=None, exclude_strings=None):
    result = [[]]  # first element stands for N0 and it is empty list because N0 don't have logic

    for i in range(1, numberOfN):  # start from 1 cause N0 don't have logic
        searchN = f"N{i}_"
        include_strings = needed_string + [searchN]
        keys_with_ui_pdf_mapping = findAliasWithKeyUIpdfMappingContain(data, include_strings, exclude_strings)
        result.append(keys_with_ui_pdf_mapping)

    return result

def getAllAliasNotMatchWithPDFAnnotation(data, needed_string=None, exclude_strings=None):
    result = []

    for i in range(numberOfN):  # start from 1 cause N0 don't have logic
        searchN = f"N{i}_"
        include_strings = needed_string + [searchN]
        keys_with_ui_pdf_mapping = findAliasWithKeyUIpdfMappingContain(data, include_strings, exclude_strings)
        for alias in keys_with_ui_pdf_mapping:
            if searchN not in alias:
              print(i, "alias: ", alias)
              result.append((i, alias))

    return result


try:
    # exclude_strings = ["_na_", "_upsilon", "_lambda", "_omega", "_gamma", "_alpha"]
    needed_string = []

    exclude_strings = []
    # needed_string = ["_na_"]
    with open(file_path, "r") as file:
        json_data = json.load(file)
        # result = getAllAliasHavingPdfMappingOfN(json_data, needed_string, exclude_strings)
        result = getAllAliasNotMatchWithPDFAnnotation(json_data, needed_string, exclude_strings)

        if result:
            print(f"total keys: {len(result)}")
            write_results_to_file(result, output_file)
        else:
            print("No value found", result)
except FileNotFoundError:
    print(f"File '{file_path}' not found")
except json.JSONDecodeError:
    print("Error decoding JSON")
