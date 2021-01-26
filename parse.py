import csv
import json

# Read CSV file to convert to JSON
with open('static/StationMap.csv') as sm:
    reader = csv.reader(sm, delimiter=",", quotechar='"')
    data_read = [row for row in reader]
# Create list for all station in respective line
NSList, EWList, CGList, CEList, NEList, CCList, DTList, TEList = [], [], [], [], [], [], [], [] 
# Create dictionary with stations and all lines at that station
res = {}
for i in range(1, len(data_read)):
    if 'NS' in data_read[i][0]:
        NSList.append(data_read[i][1])
    elif 'EW' in data_read[i][0]:
        EWList.append(data_read[i][1])
    elif 'CG' in data_read[i][0]:
        CGList.append(data_read[i][1])
    elif 'CE' in data_read[i][0]:
        CEList.append(data_read[i][1])
    elif 'NE' in data_read[i][0]:
        NEList.append(data_read[i][1])
    elif 'CC' in data_read[i][0]:
        CCList.append(data_read[i][1])
    elif 'DT' in data_read[i][0]:
        DTList.append(data_read[i][1])
    else:
        TEList.append(data_read[i][1])
    if data_read[i][1] in res:
        temp = res[data_read[i][1]] + "/" + data_read[i][0]
        res[data_read[i][1]] = temp
    else:
        res[data_read[i][1]] = data_read[i][0]
Stations = {
    'NS': NSList,
    'EW': EWList,
    'CG': CGList,
    'CE': CEList,
    'NE': NEList,
    'CC': CCList,
    'DT': DTList,
    'TE': TEList
}
# Create dictionary to find all possible next
# stations that can be visited from a given station
adj_stations = {}
for i in res.keys():
    for line in Stations.keys():
        if i in Stations[line]:
            val = Stations[line].index(i)
            # Condition for first Station in line
            if val == 0:
                if res[i] in adj_stations:
                    adj_stations[res[i]].append(res[Stations[line][val + 1]])
                else:
                    adj_stations[res[i]] = [res[Stations[line][val + 1]]]
            # Condition for last station in line
            elif val == len(Stations[line]) - 1:
                if res[i] in adj_stations:
                    adj_stations[res[i]].append(res[Stations[line][val - 1]])
                else:
                    adj_stations[res[i]] = [res[Stations[line][val - 1]]]
            # Else add previous and next stations
            else:
                if res[i] in adj_stations:
                    adj_stations[res[i]].append(res[Stations[line][val - 1]])
                    adj_stations[res[i]].append(res[Stations[line][val + 1]])
                else:
                    adj_stations[res[i]] = [res[Stations[line][val - 1]]]
                    adj_stations[res[i]].append(res[Stations[line][val + 1]])
with open('static/data.json', 'w', encoding='utf-8') as f:
    json.dump(adj_stations, f, ensure_ascii=False, indent=4)