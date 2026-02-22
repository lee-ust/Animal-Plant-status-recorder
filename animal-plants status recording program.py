# Animal-Plant Status Recorder
# Version 1.0 

import json
import matplotlib.pyplot as plt
from pathlib import Path

# LOAD EXISTING DATA 
animal_dicts = {}
plant_dicts = {}
animals = []
plants = []

if Path('animal_list.json').exists():
    with open('animal_list.json', 'r') as f:
        animal_dicts = json.load(f)
        animals = list(animal_dicts.keys())

if Path('plant_list.json').exists():
    with open('plant_list.json', 'r') as f:
        plant_dicts = json.load(f)
        plants = list(plant_dicts.keys())

# ADD NEW ORGANISMS 
ANIMAL_CODE = 'a'
PLANT_CODE = 'p'
QUIT_CODE = 'q'
add_something = False

while True:
    user_organism = input('Please type an organism (or q to quit): ').lower().strip()
   
    # Empty input check
    if user_organism == '':
        print('Error: Input cannot be empty.')
        continue

    if user_organism == QUIT_CODE:
        if add_something or animals or plants:
            break
        else:
            confirm = input('No organisms added. Type q again to quit, anything else to continue: ').lower()
            if confirm == 'q':
                break
            else:
                continue

    organism_category = input('Type a for animal, p for plant (or q to quit): ').lower().strip()

    if organism_category == '':
        print('Error: Input cannot be empty.')
        continue

    if organism_category == ANIMAL_CODE:
        animals.append(user_organism)
        animal_dicts[user_organism] = {
            'weight': [],
            'body temperature': [],
            'blood pressure': []
        }
        print(f'{user_organism} added to animals.')
        add_something = True

    elif organism_category == PLANT_CODE:
        plants.append(user_organism)
        plant_dicts[user_organism] = {
            'plant height': [],
            'leaf count': [],
            'harvestable biomass': []
        }
        print(f'{user_organism} added to plants.')
        add_something = True

    elif organism_category == QUIT_CODE:
        if add_something or animals or plants:
            break
        else:
            confirm = input('No organisms added. Type q again to quit, anything else to continue: ').lower()
            if confirm == 'q':
                break
            else:
                continue
    else:
        print('Please enter a, p, or q only.')
        continue

#  SAVE FUNCTIONS
def store_animal():
    Path('animal_list.json').write_text(json.dumps(animal_dicts, indent=4))

def store_plant():
    Path('plant_list.json').write_text(json.dumps(plant_dicts, indent=4))
print(f'animal list is shown below:\n{animal_dicts}')
print(f'plant list is shown below:\n{plant_dicts}')
# ENTER DATA 
def enterdata():
    while True:
        print('For animals, currently support 3 categories:weight , body temperature, blood pressure')
        print('For plants, currently support 3 categories:plant height, leaf count, harvestable biomass')
        print('Please make sure for each entry, the unit of the input is consistent')
        print('\nEnter: [organism] [category] [value]')
        user_input = input('> ').split()
        if len(user_input) != 3:
            print('Please provide exactly 3 items.')
            continue
        org, cat, val = user_input[0].lower().strip(), user_input[1].lower().strip(), user_input[2].strip()
        return org, cat, val

# RECORD DATA
def reachingdata(organism_dicts, name, category, value):
    found = False
    for org_name, details in organism_dicts.items():
        if org_name == name:
            for data_key in details:
                if data_key == category:
                    details[data_key].append(value)
                    print('Value recorded.')
                    found = True
                    break
            if found:
                break
    if not found:
        print('Organism or category not found.')

#RECORDING LOOP 
print('\n--- Recording Phase ---')
while True:
    org, cat, val = enterdata()
    if org in animal_dicts:
        reachingdata(animal_dicts, org, cat, val)
        store_animal()
    elif org in plant_dicts:
        reachingdata(plant_dicts, org, cat, val)
        store_plant()
    else:
        print('Organism not found. Try again.')
        continue

    again = input('Record another? (y/n): ').lower().strip()
    if again != 'y':
        break

# CHECK DATA 
def checkingdata(organism_dicts, name, category):
    for org_name, details in organism_dicts.items():
        if org_name == name:
            for data_key, data_list in details.items():
                if data_key == category:
                    if not data_list:
                        print('No data recorded yet.')
                        return
                    print(f'\nData for {name} - {category}: {data_list}')
                    print(f'Last value: {data_list[-1]}')
                    try:
                        nums = [float(x) for x in data_list]
                        change = (nums[-1] - nums[0]) / nums[0] if nums[0] != 0 else 0
                        print(f'Overall change: {change:.2%}')
                        plt.plot(range(1, len(nums)+1), nums, marker='o')
                        plt.xlabel('Day')
                        plt.ylabel(category)
                        plt.title(f'{name} - {category}')
                        plt.show()
                    except:
                        print('Could not plot (data may not be numeric).')
                    return
    print('Organism or category not found.')

# CHECK LOOP
print('\n--- Checking Phase ---')
while True:
    check_inp = input('Enter [organism] [category] to check (or q to quit): ').lower().strip().split()
    if len(check_inp) == 1 and check_inp[0] == 'q':
        break
    if len(check_inp) != 2:
        print('Please provide organism and category.')
        continue
    org, cat = check_inp[0], check_inp[1]
    if org in animal_dicts:
        checkingdata(animal_dicts, org, cat)
    elif org in plant_dicts:
        checkingdata(plant_dicts, org, cat)
    else:
        print('Organism not found.')

print('\nProgram finished. Data saved.')
        
     
   
     
             
             
             
               
             
           
                       


    



