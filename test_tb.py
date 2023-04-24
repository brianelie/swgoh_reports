import pandas as pd

file = 'C:\\Users\\shrim\\OneDrive\\Documents\\SWGOH Data\\GSF Sigma\\tb\LSTB April 2022\\phase_all.csv'

data = pd.read_csv(file, index_col=0).drop_duplicates().replace(
            ' ?', 0).fillna(0)

# for num, col in enumerate(data.columns):
#     print(num, col)

print(data.columns[10+1:15])
# ground_missions = {1:[],2:[],3:[],4:[]}
# ship_missions = {1: [], 2: [], 3: [], 4: []}

# for col in data.columns:
#     try:
#         phase, zone, points, num = col.split(' ')
#         phase = int(phase[1])
#         zone = zone.lower()
#         # points = points.split('_')
#         points = [int(x) for x in points.split('_')]
#         points.insert(0,0)
#         num = num[1]
#         if zone == 'ground':
#             ground_missions[phase].append(points)
#         elif zone == 'fleet':
#             ship_missions[phase].append(points)
#     except:
#         pass
    
# max_ground = {1:0,2:0,3:0,4:0}
# max_ship = {1:0,2:0,3:0,4:0}

# for phase in ground_missions:
#     for cm in ground_missions[phase]:
#         max_ground[phase] += cm[-1]
        
# for phase in ship_missions:
#     for cm in ship_missions[phase]:
#         max_ship[phase] += cm[-1]
        
    
# print(ground_missions)
# print(ship_missions)
# print(max_ground)
# print(max_ship)
