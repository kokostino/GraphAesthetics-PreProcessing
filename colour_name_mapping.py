# ------- IMPORT --------------

from scipy.spatial import KDTree
import csv
import ast

    
# ------- FUNCTIONS --------------

def get_name_of_nearest_colour(dictionary, rgb):
    names = []
    rgb_values = []
    for color_name, color_rgb in dictionary.items():
        names.append(color_name)
        rgb_values.append(ast.literal_eval(color_rgb))
    lst = [0] * len(names)
    kdt_db = KDTree(rgb_values)
    distance, index = kdt_db.query(tuple(rgb), k=5)
    for d in range(len(distance)):
        lst[index[d]]+=round(distance[0]/distance[d],2)

    return lst

def get_dict(filename) :       
    with open(filename, mode='r') as infile:
        reader = csv.reader(infile)
        return {rows[0]:rows[1] for rows in reader}

def read_rgb_csv(path):
    with open(path, newline='') as csvfile:
        rgb=[]
        csv.register_dialect("custom", delimiter=",", skipinitialspace=True)
        reader = csv.reader(csvfile, dialect='custom')
        next(reader)
        for row in reader:
            if row!=[]:
                rgb.append(row)  
        return rgb   

def get_colour_names_of_all_images(path, folder, dict_file, n_clstrs):
    dictionary=get_dict(path + dict_file)
    aa = read_rgb_csv(path + folder + "_metadata/colour_rgb.csv")
    clr=[]
    
    for rgb in aa:
        cl=[rgb[0].rsplit('/')[-1]]
        bu = [0] * (100)
        
        for l in range(1,n_clstrs+1):
            color = ast.literal_eval(rgb[l])
            bunew = get_name_of_nearest_colour(dictionary, color)
            bu = [round(sum(x),2) for x in zip(bu, bunew)]
        cl.extend(bu)
        clr.append(cl)
    #print(clr[0])
    names = []
    for color_name, _ in dictionary.items():
        names.append(color_name)  
    clms=names
    
    with open(path + folder + "_metadata/colours.csv", "w", newline="") as f:
        header = ['ImgName']
        header.extend(clms)        
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(clr)

        