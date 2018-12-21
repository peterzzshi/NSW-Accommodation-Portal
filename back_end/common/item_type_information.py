Amenities = {
    1   : 'Wireless Internet',
    2   : 'Air conditioning',
    3   : 'TV',
    4   :'Laptop friendly workspace',
    5   :'Hot water',
    6	:'Heating',
    7	:'Free parking',
    8	:'Lift',
    9	:'Kitchen',
    10:'Smoke detector'
}

def Amenities_str2int(name):
    for i in Amenities:
        if Amenities[i] == name:
            return i
    return -1

def Amenities_int2str(id):
    return Amenities[id]

bed_type = {
    1:'single',
    2:'double',
    3:'queen',
    4:'king',
    5:'sofa bed',
    6:'floor mattresses'
}

def bed_type_str2int(name):
    for i in bed_type:
        if bed_type[i] == name:
            return i
    return -1

def bed_type_int2str(id):
    return bed_type[id]


house_type = {
    1:'house',
    2:'apartment',
    3:'townhouse'
}

def house_type_str2int(name):
    for i in house_type:
        if house_type[i] == name:
            return i
    return -1

def house_type_int2str(id):
    return house_type[id]