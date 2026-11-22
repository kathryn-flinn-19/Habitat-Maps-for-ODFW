import json
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import os

"""
    the point of this file is to provide basic ruleset parsing to allow analysis of
    which data layers can be excluded from our dataset. the file has functions to 
    perform the following tasks:

    - list the attributes across all species jsons that are associated with each data 
      layer link
        * list_attrs_by_link()
    - list all attributes whose values are not None (null) or False (false), thus 
      indicating which attributes are actually factored in when generating the maps
        * extract_non_null_layers()
    - remove an indicated field from a python dict, to be used when trimming unused 
      fields from the jsons
        * remove_fld()
    - convert a python dict to a json and rewrite it back to a specified (existing) 
      file
        * rewrite_json_to_file()

    note that more analysis is needed to determine what each attribute actually refers
    to within each layer. additionally, before any data layers can be completely ruled
    out, the extract_non_null_layers() method must be applied to every supported species'
    jsons to make sure we are not accidentally removing data that we do actually need.
"""


"""
    finds the attributes associated with each data layer link.
    known limitations: 
    - intPercentCanopy is incorrectly attributed to the HUCs
      data layer in all of the species json files, even though it should be attributed
      to the percent canopy link.
    - additionally, the ascent layer is seemingly missing
    next steps: search for the metadata for what each attribute actually means 
"""
def list_attrs_by_link(data_json: dict, linked_attrs: dict[str, list]):

    # we're looking through the input layers obj in the json.
    # recall that this is structured "attr": "link"
    # so, the value in sata_json will turn into the key in
    # our dict
    for key, value in data_json.items():
        if isinstance(value, dict):
            list_attrs_by_link(value, linked_attrs)
            continue

        # if we don't have the link already
        if not value in linked_attrs.keys():
            linked_attrs.update({value: []})

        # check if we've already added that attribute to the list.
        # since we're repeating this across files, we don't want duplicates
        aa = linked_attrs[value]
        if not key in aa:
            aa.append(key)
            linked_attrs[value] = aa

"""
    helper function to check if a value is contained within a list of tuples; 
    in particular, this function checks whether the value is the SECOND entry 
    in any of the tuples. 
    
    note that the function will not check whether the value is 
    contained in the first entry of any of the tuples.
"""
def value_in_tuple_list(l: list, val: str):
    for _, v in l:
        if val == v:
            return True

    return False

"""
    takes in a model dict and updates running_list to hold the fields that are 
    actually used (i.e., those whose values are not None or False).

    note that running_list is a list of (src_file: str, attr: str) tuples, which
    necessitates the use of the specialized value_in_tuple_list() function.
"""
def extract_non_null_layers(d: dict, running_list: list, file: str):
    for key, value in d.items():
        # should confirm: are None and False both indicative that a layer / 
        # attribute isn't used?
        if (value is not None and value is not False 
            and not (value_in_tuple_list(running_list, key))):
            running_list.append((file, key))

    return running_list

"""
    removes indicated field from a dictionary representing a JSON ruleset,
    if the field is present
"""
def remove_fld(data_json: dict, fld: str):
    if fld in data_json.keys():
        data_json.pop(fld)

"""
    rewrites the file at the indicated path to contain the contents
    of the inputted dict. the dict should represent the ruleset we want
    to use.
"""
def rewrite_json_to_file(data_json: dict, file_path: str):
    converted_str = json.dumps(data_json)

    with open(file_path, "w") as file:
        file.write(converted_str)

"""
    some simple proof-of-concept runs of the above utility functions
"""
def main():
    species_info = {}

    used_layers = []

    linked_attrs: dict[str, list] = {}

    for folder in os.listdir("./starter_script/data/species"):
        for file in os.listdir("./starter_script/data/species/" + folder): 
            if file.endswith(".json"):
                with open(Path("./starter_script/data/species/" + folder + "/" + file), "r") as f:
                    species_info = json.load(f)

                for _, m in species_info["models"].items():
                    used_layers = extract_non_null_layers(m, used_layers, file)

                list_attrs_by_link(species_info["input_layers"], linked_attrs)                
    
    print("unique used layers:")
    for i in range(len(used_layers)):
        print(i+1, ": ", used_layers[i])

    print("linked attrs:")
    for key in linked_attrs:
        print(key, ": ", linked_attrs[key])

if __name__ == "__main__":
    main()