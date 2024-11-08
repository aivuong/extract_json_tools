"""
Must run standardfromat.py first to get stddata.json before running getAlias.py
The result in output.txt will be the list of keys that have ui:pdfMappings that contain the search string
"""

import json
import re


def findAliasWithKeyUIpdfMappingContain(data, include_strings, exclude_strings, logic_prefix_in_output=True):
    result = []

    prefix_output = ""
    if logic_prefix_in_output:
        prefix_output = "logic."

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):
                # Check if the dictionary has 'ui:pdfMappings' or 'ui:pdfMapping'
                if "ui:pdfMappings" in value:
                    pdf_mappings = value["ui:pdfMappings"]
                    # Check if any value in 'ui:pdfMappings' starts with include_strings and excludes exclude_strings
                    for item in pdf_mappings:
                        if all(include in item for include in include_strings) and not any(exclude in item for exclude in exclude_strings):
                            result.append(f"{prefix_output}{key}")

                # Recursively search within nested structures
                result.extend(findAliasWithKeyUIpdfMappingContain(value, include_strings, exclude_strings))

    return result


def write_results_to_file(results, output_file):
    with open(output_file, "w") as file:
        file.write(f"{results}\n")


def getAllAliasHavingPdfMappingOfN(maxN, data, needed_string=None, exclude_strings=None):
    result = [[]]  # first element stands for N0 and it is empty list because N0 don't have logic

    for i in range(1, maxN):  # start from 1 cause N0 don't have logic
        searchN = f"N{i}_"
        include_strings = needed_string + [searchN]
        keys_with_ui_pdf_mapping = findAliasWithKeyUIpdfMappingContain(data, include_strings, exclude_strings)
        result.append(keys_with_ui_pdf_mapping)

    return result


def getAllAliasNotMatchWithPDFAnnotation(maxN, data, needed_string=None, exclude_strings=None):
    result = []

    for i in range(maxN):  # start from 1 cause N0 don't have logic
        searchN = f"N{i}_"
        include_strings = needed_string + [searchN]
        keys_with_ui_pdf_mapping = findAliasWithKeyUIpdfMappingContain(data, include_strings, exclude_strings, False)
        for alias in keys_with_ui_pdf_mapping:
            if searchN not in alias:
                print(f"pdf annotation N{i}, current alias: {alias}")
                result.append((i, alias))

    return result


def getAllNumberOfN(data):
    result = set()
    total_mfn_fields = []

    aliases = sorted(findAliasWithKeyUIpdfMappingContain(data, [], [], False))
    for alias in aliases:
        match = re.search(r"N(\d+)_", alias)
        if match:
            num = int(match.group(1))
            result.add(num)
            total_mfn_fields.append(alias)

    return sorted(result), total_mfn_fields


try:
    input_file = "stddata.json"
    output_file = "output.txt"

    with open(input_file, "r") as file:
        json_data = json.load(file)
        # Get all number of N to find maxN value, then change it to the correct value
        allnums, total_fields = getAllNumberOfN(json_data)
        if allnums:
            print()
            # write_results_to_file(total_fields, "MFN_field_alias.py")
            # print(f"total fields that have format as N{{number}}_ in pdf aliastation: {len(total_fields)} \nallnums: {allnums}")
        else:
            print("No number found")
            exit(0)

        maxN = allnums[-1] + 1

        #TODO: uncomment below lines of code to get the result
        exclude_strings = ["_na_", "_upsilon", "_lambda", "_omega", "_gamma", "_alpha"]
        needed_string = []
        # exclude_strings = []
        # needed_string = ["_upsilon"]
        # result = getAllAliasNotMatchWithPDFAnnotation(maxN, json_data, needed_string, exclude_strings)
        result = getAllAliasHavingPdfMappingOfN(maxN, json_data, needed_string, exclude_strings)

        if result:
            print(f"total keys: {len(result)}")
            write_results_to_file(result, output_file)
        else:
            print("No value found", result)
except FileNotFoundError:
    print(f"File '{input_file}' not found")
except json.JSONDecodeError:
    print("Error decoding JSON")
