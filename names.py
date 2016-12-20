from random import choice
from names_static import *

class NameGeneratorException(Exception):
    pass

def parse_name(msg):
    command = msg.lower().split()
    if command[0] != '!name':
        return ['']
    
    offset = 4
    try:
        if not command[2].isdigit():
            race = synonyms[' '.join(command[1:3])]
            count = int(command[3])
        else:
            race = synonyms[command[1]]
            count = int(command[2])
            offset = 3
    except (ValueError, KeyError) as e:
        print(e)
        raise NameGeneratorException('invalid syntax, race, or count')
    else:
        if count < 1:
            raise NameGeneratorException('invalid count')
    
    name_format = [synonyms[x] for x in command[offset:] if x in synonyms]
    if len(name_format) > 10: # fuck stupidly long names
        raise NameGeneratorException('name format too long')
    
    return [generate_name(race, name_format) for name in range(count)]
    
def generate_name(race, name_format):
    return ' '.join([choice(names[race][kind]) for kind in name_format])
    