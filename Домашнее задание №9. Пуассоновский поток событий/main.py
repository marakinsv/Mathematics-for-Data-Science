from scipy. stats import expon
import random
from datetime import datetime, timedelta

l = 10  # Интенсивность потока заявок, мин.
n = 3   # количество каналов обслуживания (число парикмахеров)
m = [random.randrange(40, 45) for i in range(n)]  # Интенсивность для каждого канала обслуживания

events = [0 for i in range(n)]                 # Текущие события (1 - парикмахер занят, 0 - свободен)
events_dtime = [None for i in range(n)]  #  Времена начала события
queue = 0                                          # Количество клиентов в очереди

U = expon.rvs(scale=l, size=1440)  # Длительность ожидания заявки

V = []
for i in range(n):
    Vi = expon.rvs(scale=m[i], size=1440)  # Длительность ожидания заявки
    V.append(Vi)

start_datetime = datetime.strptime('01.12.22 10:00:00', '%d.%m.%y %H:%M:%S')  # Время открытия парикмахерской
end_datetime = datetime.strptime('01.12.22 20:00:00', '%d.%m.%y %H:%M:%S')   # Время закрытия парикмахерской

cur_dtime = start_datetime  # Текущее время
client_id = 0

print('{}: {}/{}'.format(start_datetime, events, queue))

for _ in range(1440):
    need_print = False
    exists_client = False
    client_dtime = start_datetime
    for cm in U:
        client_dtime += timedelta(minutes=int(cm))
        #print(cur_dtime, client_dtime)
        if client_dtime == cur_dtime:
            exists_client = True
            break
    if exists_client:   # Пришел клиент        
        idxs = []
        for idx in range(n):
            if events[idx] == 0: idxs.append(idx)
        if len(idxs) > 0:   # Есть свободные парикмахеры
            idx = idxs[0]
            if len(idxs) > 1: idx = idxs[random.randrange(0, len(idxs) - 1)]  # Случайно выбираем свободного парикмахера

            events[idx] = 1
            events_dtime[idx] = cur_dtime
            need_print = True
        else:
            queue += 1   # Ставим клиента в очередь
            need_print = True
            
    # Проверяем, достригся какой-либо клиент
    for idx in range(n):     
        if events[idx] == 0: continue
        if (cur_dtime - events_dtime[idx]).total_seconds() / 60 > V[idx][client_id]:
            events_dtime[idx] = cur_dtime
            if queue > 0:            # В очереди есть клиенты
                queue -= 1           # Садим из очереди
            else: events[idx] = 0

            need_print = True
            
    if need_print: print('{}: {}/{}'.format(cur_dtime, events, queue))

    if exists_client: client_id += 1
    cur_dtime += timedelta(minutes=1)
    #print(cur_dtime)
    if cur_dtime > end_datetime: break
    
