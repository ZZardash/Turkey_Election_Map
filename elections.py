import numpy as np
import pandas as pd
import shapefile as shp
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors

sns.set(style='whitegrid', palette='pastel', color_codes=True)
sns.mpl.rc('figure', figsize=(10,6))

#opening the vector map
shp_path = './map/TUR_adm1.shp'
#reading the shape file by using reader function of the shape lib
sf = shp.Reader(shp_path)

def read_shapefile(sf):
    #fetching the headings from the shape file 
    fields = [x[0] for x in sf.fields][1:]
    
    #fetching the records from the shape file 
    records = [list(i) for i in sf.records()]
    shps = [s.points for s in sf.shapes()]
    
    #converting shapefile data into pandas dataframe
    df = pd.DataFrame(columns=fields, data=records)
    
    #assigning the coordinates
    df = df.assign(coords=shps)
    return df

df = read_shapefile(sf)

def blend_colors(color1, color2, blend_percent):
    rgb1 = mcolors.to_rgb(color1)
    rgb2 = mcolors.to_rgb(color2)
    blended_rgb = tuple((1 - blend_percent) * c1 + blend_percent * c2 for c1, c2 in zip(rgb1, rgb2))
    return mcolors.to_hex(blended_rgb)

def plot_cities_with_blend(sf, title, city_percentages, color1, color2):
    plt.figure(figsize=(11, 9))
    fig, ax = plt.subplots(figsize=(11, 9))
    fig.suptitle(title, fontsize=16)

    for shape in sf.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        ax.plot(x, y, 'k')

    for city, percentages in city_percentages.items():
        city_id = df[df.NAME_1.str.upper() == city.upper()].index.values
        if len(city_id) > 0:
            city_id = city_id[0]
            shape_ex = sf.shape(city_id)
            x_lon = np.zeros((len(shape_ex.points), 1))
            y_lat = np.zeros((len(shape_ex.points), 1))
            for ip in range(len(shape_ex.points)):
                x_lon[ip] = shape_ex.points[ip][0]
                y_lat[ip] = shape_ex.points[ip][1]

            blend_percent = percentages['yellow']
            blended_color = blend_colors(color1, color2, blend_percent)

            ax.fill(x_lon, y_lat, color=blended_color)

            x0 = np.mean(x_lon)
            y0 = np.mean(y_lat)
            plt.text(x0, y0, city, fontsize=10, ha='center', va='center')


city_percentages = {
    "Adana": {"red": 0.43, "yellow": 0.50},
    "Ankara": {"red": 0.46, "yellow": 0.47},
    "Adiyaman": {"red": 0.66, "yellow": 0.31},
    "Afyon": {"red": 0.63, "yellow": 0.28},
    "Agri": {"red": 0.31, "yellow": 0.65},
    "Amasya": {"red": 0.56, "yellow": 0.38},
    "Antalya": {"red": 0.39, "yellow": 0.53},
    "Artvin": {"red": 0.47, "yellow": 0.46},
    "Aydin": {"red": 0.38, "yellow": 0.56},
    "Balikesir": {"red": 0.45, "yellow": 0.48},
    "Bilecik": {"red": 0.49, "yellow": 0.41},
    "Bingol": {"red": 0.65, "yellow": 0.32},
    "Bitlis": {"red": 0.46, "yellow": 0.50},
    "Bolu": {"red": 0.60, "yellow": 0.31},
    "Burdur": {"red": 0.51, "yellow": 0.40},
    "Bursa": {"red": 0.51, "yellow": 0.40},
    "Canakkale": {"red": 0.39, "yellow": 0.54},
    "Cankiri": {"red": 0.72, "yellow": 0.20},
    "Corum": {"red": 0.61, "yellow": 0.33},
    "Denizli": {"red": 0.43, "yellow": 0.48},
    "Diyarbakir": {"red": 0.26, "yellow": 0.72},
    "Edirne": {"red": 0.32, "yellow": 0.63},
    "Elazig": {"red": 0.67, "yellow": 0.28},
    "Erzincan": {"red": 0.59, "yellow": 0.35},
    "Erzurum": {"red": 0.6859, "yellow": 0.2456},
    "Eskisehir": {"red": 0.4181, "yellow": 0.5039},
    "Gaziantep": {"red": 0.5976, "yellow": 0.3465},
    "Giresun": {"red": 0.6105, "yellow": 0.3292},
    "Gumushane": {"red": 0.7442, "yellow": 0.1992},
    "Hakkari": {"red": 0.2464, "yellow": 0.7232},
    "Hatay": {"red": 0.4803, "yellow": 0.4808},
    "Isparta": {"red": 0.5365, "yellow": 0.3823},
    "Mersin": {"red": 0.3757, "yellow": 0.5718},
    "Istanbul": {"red": 0.4668, "yellow": 0.4856},
    "Izmir": {"red": 0.3148, "yellow": 0.6331},
    "Kars": {"red": 0.3939, "yellow": 0.5457},
    "Kastamonu": {"red": 0.6545, "yellow": 0.2664},
    "Kayseri": {"red": 0.6333, "yellow": 0.2748},
    "Kirklareli": {"red": 0.3047, "yellow": 0.6502},
    "Kirsehir": {"red": 0.5411, "yellow": 0.388},
    "Kocaeli": {"red": 0.5427, "yellow": 0.3873},
    "Konya": {"red": 0.68, "yellow": 0.23},
    "Kutahya": {"red": 0.6631, "yellow": 0.2638},
    "Malatya": {"red": 0.6939, "yellow": 0.2711},
    "Manisa": {"red": 0.4715, "yellow": 0.4608},
    "KMaras": {"red": 0.7188, "yellow": 0.222},
    "Mardin": {"red": 0.3229, "yellow": 0.6611},
    "Mugla": {"red": 0.3166, "yellow": 0.629},
    "Mus": {"red": 0.3912, "yellow": 0.5888},
    "Nevsehir": {"red": 0.6288, "yellow": 0.3064},
    "Nigde": {"red": 0.5849, "yellow": 0.3492},
    "Ordu": {"red": 0.6216, "yellow": 0.3245},
    "Rize": {"red": 0.7279, "yellow": 0.2203},
    "Sakarya": {"red": 0.6475, "yellow": 0.2787},
    "Samsun": {"red": 0.6202, "yellow": 0.3147},
    "Siirt": {"red": 0.4155, "yellow": 0.5626},
    "Sinop": {"red": 0.5852, "yellow": 0.3546},
    "Sivas": {"red": 0.694, "yellow": 0.2425},
    "Tekirdag": {"red": 0.3902, "yellow": 0.5544},
    "Tokat": {"red": 0.6319, "yellow": 0.3137},
    "Trabzon": {"red": 0.6532, "yellow": 0.2833},
    "Tunceli": {"red": 0.162, "yellow": 0.8026},
    "Sanliurfa": {"red": 0.62, "yellow": 0.3608},
    "Usak": {"red": 0.476, "yellow": 0.4513},
    "Van": {"red": 0.3561, "yellow": 0.6226},
    "Yozgat": {"red": 0.727, "yellow": 0.2134},
    "Zonguldak": {"red": 0.5189, "yellow": 0.4159},
    "Aksaray": {"red": 0.7153, "yellow": 0.224},
    "Bayburt": {"red": 0.7886, "yellow": 0.1538},
    "Karaman": {"red": 0.6128, "yellow": 0.3017},
    "Kirikkale": {"red": 0.5966, "yellow": 0.3309},
    "Batman": {"red": 0.3095, "yellow": 0.6757},
    "Sirnak": {"red": 0.2143, "yellow": 0.7585},
    "Bartin": {"red": 0.561, "yellow": 0.3649},
    "Ardahan": {"red": 0.3916, "yellow": 0.5615},
    "Igdir": {"red": 0.2529, "yellow": 0.6249},
    "Yalova": {"red": 0.4774, "yellow": 0.4542},
    "Karabuk": {"red": 0.594, "yellow": 0.3205},
    "Kilis": {"red": 0.6555, "yellow": 0.2702},
    "Osmaniye": {"red": 0.6232, "yellow": 0.3074},
    "Duzce": {"red": 0.686, "yellow": 0.2491}
}
plot_cities_with_blend(sf, 'City Blending', city_percentages, "white", "blue")
plt.show()



#OTHER USEFUL FUNCTIONS FOR MAPPING
"""
def show_dist(name):
    #to get the id of the city map to be plotted
    com_id = df[df.NAME_1 == name].index.values[0]
    plot_shape(com_id, name)
    sf.shape(com_id)
    plt.show()
    
def show_all_dists():
    for i in range(0,81):
        filteyellow_df = df.NAME_1[i]
        print(filteyellow_df)

def plot_shape(id, s=None):
    plt.figure()
    
    #plotting the graphical axes where map ploting will be done
    ax = plt.axes()
    ax.set_aspect('equal')
    
    #storing the id number to be worked upon
    shape_ex = sf.shape(id)
    
    #NP.ZERO initializes an array of rows and column with 0 in place of each elements 
    #an array will be generated where number of rows will be(len(shape_ex,point))and number of columns will be 1 and stoyellow into the variable
    x_lon = np.zeros((len(shape_ex.points),1))
    
    #an array will be generated where number of rows will be(len(shape_ex,point))and number of columns will be 1 and stoyellow into the variable
    y_lat = np.zeros((len(shape_ex.points),1))
    for ip in range(len(shape_ex.points)):
        x_lon[ip] = shape_ex.points[ip][0]
        y_lat[ip] = shape_ex.points[ip][1]
    
    #plotting using the derived coordinated stoyellow in array created by numpy
    plt.plot(x_lon,y_lat) 
    x0 = np.mean(x_lon)
    y0 = np.mean(y_lat)
    plt.text(x0, y0, s, fontsize=10)
    
    # use bbox (bounding box) to set plot limits
    plt.xlim(shape_ex.bbox[0],shape_ex.bbox[2])
    return x0, y0

def get_city_name(id):
    city_name = df.loc[id-1, 'NAME_1']
    return city_name

def plot_cities(sf, figsize=(10, 6)):
    plt.figure(figsize=figsize)
    
    for city_id in range(1,81):
        shape = sf.shapeRecords()[city_id-1]
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        plt.plot(x, y, 'k')
        
        x0 = np.mean(x)
        y0 = np.mean(y)
        #city_name = get_city_name(city_id)
        #plt.text(x0, y0, city_name, fontsize=10, ha='center', va='center')
    
    plt.axis('off')
    plt.show()
    
#ploting full map    
#plot_cities(sf)


def plot_map_fill_multiples_names(color, title, cities, sf, x_lim=None, y_lim=None, figsize=(11, 9)):
    plt.figure(figsize=figsize)
    fig, ax = plt.subplots(figsize=figsize)
    fig.suptitle(title, fontsize=16)
    
    # Draw All Shapes
    for shape in sf.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        ax.plot(x, y, 'k')
    
    # Şehirlerin isimlerine göre renklendirilmiş şekilleri doldur
    for city_name in cities:
        city_id = df[df.NAME_1.str.upper() == city_name.upper()].index.values[0]
        shape_ex = sf.shape(city_id)
        x_lon = np.zeros((len(shape_ex.points), 1))
        y_lat = np.zeros((len(shape_ex.points), 1))
        for ip in range(len(shape_ex.points)):
            x_lon[ip] = shape_ex.points[ip][0]
            y_lat[ip] = shape_ex.points[ip][1]
        ax.fill(x_lon, y_lat, color)
        
        x0 = np.mean(x_lon)
        y0 = np.mean(y_lat)
        plt.text(x0, y0, city_name, fontsize=10)
    
    if (x_lim is not None) and (y_lim is not None):     
        plt.xlim(x_lim)
        plt.ylim(y_lim)
    plt.show()
    
cities = df['NAME_1'].to_numpy()
color = '#D66F09'

"""


    


