import pandas as pd
import warnings
import json

warnings.filterwarnings('ignore')

def correct_data(data: pd.DataFrame) -> pd.DataFrame:
    '''
    Приводит датасет в нужный формат.
    '''
    return data.rename(dict(zip(data.columns, data.loc[0].values)), axis=1).drop(0)


def load_data(path: str) -> pd.DataFrame:
    '''
    Возвращает датасет.
    '''
    data = pd.read_csv(path)
    
    return correct_data(data)


def preprocessing_schedule(sch: pd.DataFrame) -> pd.DataFrame:
    '''
    Возвращает обработанное расписание.
    '''
    # Удаление лишних столбцов
    sch = sch.drop('id', axis=1)
    sch = sch.drop('dock.id', axis=1)
    sch = sch.drop(['timetable.startdate', 'timetable.enddate'], axis=1)
    sch = sch.drop(['timetable.starttime', 'timetable.endtime'], axis=1)
    sch = sch.drop(['Начало расписания', 'Окончание расписания'], axis=1)
    sch = sch.drop('changed_schedule.type', axis=1)
    sch = sch.drop('changed_schedule.ship_name', axis=1)
    
    # Приведение типов
    sch['timetable.duration'] = sch['timetable.duration'].astype(int)
    sch['Причаливание'] = pd.to_datetime(sch['Причаливание'])
    sch['Отход'] = pd.to_datetime(sch['Отход'])
    
    # Обработка пропусков
    sch = sch.dropna(subset='ship.name')
    sch = sch.reset_index(drop='first')
    
    return sch
    
    
def preproccesing_moorings(mr: pd.DataFrame) -> pd.DataFrame:
    '''
    Возвращает обработанный датасет с информацией о причалах.
    '''
    # Удаление лишних столбцов
    mr = mr.drop('Docs.id', axis=1)
    
    # Приведение типов
    mr['Docs.latitude'] = mr['Docs.latitude'].apply(lambda x: float(x.replace(',', '.')))
    mr['Docs.longitude'] = mr['Docs.longitude'].apply(lambda x: float(x.replace(',', '.')))
    
    return mr


def distance(p1: float, p2: float, q1: float, q2: float) -> float:
    '''
    Вычисляет манхетанское расстояние (в км).
    '''
    k = 0.95 / 0.01419299999999879 # перевод в км
    
    return (abs(p1 - q1) + abs(p2 - q2)) * k


def cord_to_dock(latitude: float, longitude: float, mr: pd.DataFrame) -> list:
    '''
    Возвращает список причалов, отсортированных по близости к текущей точке.
    '''
    dock_names = mr['Docs.name']
    res_list = []
    
    for dock_name in dock_names:
        dock_data = mr[mr['Docs.name'] == dock_name]
        dock_latitide = dock_data['Docs.latitude'].values[0] 
        dock_longitude = dock_data['Docs.longitude'].values[0]
        
        res_list.append((dock_name, distance(latitude, longitude, dock_latitide, dock_longitude)))
    
    return sorted(res_list, key=lambda x: x[1])


def dock_shedule(dock_start: str, dock_end: str, datetime_cur: str, sch: pd.DataFrame):
    '''
    Релевантное расписание для причала.
    '''
    data = pd.DataFrame(columns=sch.columns)
    nameroute_arr = sch[sch['dock.name'] == dock_start]['route.nameroute'].unique()
    
    for nameroute in nameroute_arr:
        # пункт B
        ship_list = sch[(sch['route.nameroute'] == nameroute) & (sch['dock.name'] == dock_end) & (sch['Причаливание'] > datetime_cur)]['ship.name'].unique()
        for ship_name in ship_list:
            # пункт A
            data_new = sch[(sch['ship.name'] == ship_name) & (sch['dock.name'] == dock_start) & (sch['Отход'] >= datetime_cur)]
            if not data_new.empty:
                data = pd.concat([data, data_new])

    return data.sort_values('Отход')
    

def schedule(latitude: float, longitude: float, dock_end: str, datetime_cur: str, sch: pd.DataFrame, mr: pd.DataFrame) -> pd.DataFrame:
    '''
    Создание релевантного расписания.
    
    Аргументы функции:  
    latitude - долгота точки клиента
    longitude - широта точки клиента
    dock_end - пункт назначения, название причала
    datetime_cur - текущая дата и время, в формате 'YYYY-MM-DD HH:MM:SS' (24-часовом формате времени)
    '''
    nearest_docks = cord_to_dock(latitude, longitude, mr)[:3]
    datetime_cur = pd.to_datetime(datetime_cur)
    
    res_df = pd.DataFrame(columns=sch.columns)
    for dock in nearest_docks:
        df = dock_shedule(dock[0], dock_end, datetime_cur, sch)
        if not df.empty:
            res_df = pd.concat([res_df, df])
        
    return res_df.sort_values('Отход')


def get_schedule(sch_path: str, mr_path: str, latitude: float, longitude: float, dock_end: str, datetime_cur: str) -> pd.DataFrame:
    '''
    Возвращает релевантное расписание.
    '''
    # Загрузка данных
    sch = load_data(sch_path)
    mr = load_data(mr_path)
    
    # Подготовка данных
    sch = preprocessing_schedule(sch)
    mr = preproccesing_moorings(mr)
    
    return schedule(latitude, 
                    longitude, 
                    dock_end, 
                    datetime_cur, 
                    sch,
                    mr)
    
    
def get_routes(schedule_path: str) -> None:
    '''
    Создает json файл со всеми маршрутами.
    '''
    # Загрузка данных
    sch = load_data(schedule_path)
    
    # Подготовка данных
    sch = preprocessing_schedule(schedule)
    
    routes_list = sch['route.nameroute'].unique
    routes_dict = dict()

    for route in routes_list:
        routes_dict[route] = sch[(sch['route.nameroute'] == 'Северный') & (sch['Отход'] > '2024-12-01 5:00:00')]['dock.name'].drop_duplicates().to_list()
    
    with open('routes.json', 'w') as file:
         json.dump(routes_dict, file, indent=4)
    
    
def main():
    print(get_schedule('schedule.csv',
                       'moorings.csv', 
                       37.562727, 
                       55.708950, 
                       'Красный октябрь',
                       '2024-12-01 15:30:00'))

    
# main()
