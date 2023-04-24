import pandas as pd

file_name = 'tb_test.csv'

## load_data

df = pd.read_csv(file_name)
first_col = list(df.columns).index('Mission Waves Phase 4')+1
last_col = list(df.columns).index('Platoons Assigned Total')

waves = df[list(df.columns[first_col:last_col])]

ground_missions = [[],[],[],[]]
ship_missions = [[],[],[],[]]
max_ground = [0,0,0,0]
max_ships = [0,0,0,0]

for column in waves.columns:
    phase, type, points, num = column.split(' ')
    phase = int(phase[1])   
    points = points.split('_')
    points = [0] + list(map(int,points))
    if type == 'Ground':
        ground_missions[phase-1] = points
        max_ground[phase-1] += points[-1]
    elif type == 'Fleet':
        ship_missions[phase-1] = points
        max_ships[phase-1] += points[-1]
        
# print(ground_missions)
# print(ship_missions)
# print(max_ground)
# print(max_ships)

## needed_phases
needed_phase = 3
tb_cols = []
cm_waves_col = []
for column in df.columns:
    if column.startswith('Territory Points Phase'):
        num = int(column.split(' ')[-1])
        if num >= needed_phase:
            tb_cols.append(column)
    elif column.startswith('Mission Waves Phase'):
        num = int(column.split(' ')[-1])
        if num >= needed_phase:
            cm_waves_col.append(column)
        
print(tb_cols)
print(cm_waves_col)

# need new df with columns 'TB Points', 'CM Waves'
# no longer have GP data and therefore no 'Points Per GP'
tb_points = pd.Series([0]*len(df), index=df.index)
cm_waves = pd.Series([0]*len(df), index=df.index)
for col in tb_cols:
    tb_points += df[col]
    
for col in cm_waves_col:
    cm_waves += df[col]
    
print(tb_points)
print(cm_waves)
