import yaml
import os
import math

# Max single cargo item weight is 200kg
# Max single cargo item size is 2m^3 
# Max cargo trolley weight is 2000kg
max_single_cargo_weight = 200
max_single_cargo_size = 2^3
max_trolley_weight = 2000

# calculate needed trolley number 
def calculateTrolleyNumber(loaded_data):
    total_mass = 0
    for item in loaded_data:
        cargo_mass = loaded_data[item]['mass']
        cargo_volume = loaded_data[item]['volume']
        if cargo_mass > max_single_cargo_weight:
            # print(f"--The weight of cargo {item} exceeds max single cargo weight!")
            continue
        if math.prod(cargo_volume) > max_single_cargo_size:
            # print(f"--The size of cargo {item} exceeds max single cargo size!")
            continue
        total_mass += loaded_data[item]['mass']
    trolley_number = math.ceil(total_mass / max_trolley_weight)
    return trolley_number

# load data from YAML file
def loadDataFromFile(file_name):
    loaded_data = ''
    if os.path.isfile(file_name):
        with open(file_name, 'r') as file:
            loaded_data = yaml.safe_load(file)
    return loaded_data   


############################ main process ############################
#load data from Data.yaml
file_name = 'cargoData.yaml'
print("\nStart loading data from YAML file...")
loaded_data = loadDataFromFile(file_name)

if loaded_data == '':
    print("--YAML file doesn't exist!")
elif loaded_data == None: 
    print("--YAML file is empty!")
else:
    print("\nStart calculating needed number of trolley...")
    trolley_number = calculateTrolleyNumber(loaded_data)
    print(f"Needed trolley number is {trolley_number}.\n")




