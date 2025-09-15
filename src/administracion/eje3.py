from collections import deque
import pandas as pd

# Definición de tareas: duración (días) y predecesores
tasks = {
    'A': {'dur':5, 'pred':[]},
    'B': {'dur':3, 'pred':['A']},
    'C': {'dur':10, 'pred':['A']},
    'D': {'dur':20, 'pred':['A']},
    'E': {'dur':5, 'pred':['B','C']},
    'F': {'dur':6, 'pred':['B','C']},
    'G': {'dur':7, 'pred':['B','C']},
    'H': {'dur':10, 'pred':['E','F','D']},
    'I': {'dur':9, 'pred':['G','D']},
    'J': {'dur':12, 'pred':['H','I']},
}

# Construir sucesores
successors = {k:[] for k in tasks}
for k,v in tasks.items():
    for p in v['pred']:
        successors[p].append(k)

# Topological sort (Kahn)
def topo_sort(tasks, successors):
    indeg = {k:0 for k in tasks}
    for k,v in tasks.items():
        indeg[k] = len(v['pred'])
    q = deque([n for n,d in indeg.items() if d==0])
    order = []
    while q:
        n = q.popleft()
        order.append(n)
        for s in successors[n]:
            indeg[s] -= 1
            if indeg[s] == 0:
                q.append(s)
    return order

order = topo_sort(tasks, successors)

# CPM - earliest and latest times
ES = {n:0 for n in tasks}; EF = {n:0 for n in tasks}
for n in order:
    ES[n] = max((EF[p] for p in tasks[n]['pred']), default=0)
    EF[n] = ES[n] + tasks[n]['dur']
project_duration = max(EF.values())

LF = {n:project_duration for n in tasks}; LS = {n: project_duration - tasks[n]['dur'] for n in tasks}
for n in reversed(order):
    if successors[n]:
        LF[n] = min(LS[s] for s in successors[n])
        LS[n] = LF[n] - tasks[n]['dur']

TF = {n: LS[n] - ES[n] for n in tasks}
critical_cpm = [n for n in tasks if TF[n] == 0]

# Heurística de scheduling con recursos limitados (2 personas)
# Prioridad: mayor "remaining length" (longest path to end)
def compute_remaining(tasks, successors):
    memo = {}
    def dfs(n):
        if n in memo: return memo[n]
        if not successors[n]:
            memo[n] = tasks[n]['dur']
        else:
            memo[n] = tasks[n]['dur'] + max(dfs(s) for s in successors[n])
        return memo[n]
    for n in tasks: dfs(n)
    return memo

rem_len = compute_remaining(tasks, successors)

def schedule_with_resources(tasks, successors, resources=2):
    not_started = set(tasks.keys())
    running = []   # list of tuples (task, finish_time)
    completed = set()
    start = {}
    finish = {}
    t = 0
    while not_started or running:
        # available ready tasks (predecessors finished)
        ready = [n for n in list(not_started) if all(p in completed for p in tasks[n]['pred'])]
        # start while resources free
        ready.sort(key=lambda x:(-rem_len[x], x))
        while len(running) < resources and ready:
            n = ready.pop(0)
            start[n] = t
            finish_time = t + tasks[n]['dur']
            running.append((n, finish_time))
            not_started.remove(n)
        if not running:
            # no running tasks but still tasks remaining -> deadlock (shouldn't occur if DAG is correct)
            if not not_started:
                break
            else:
                raise RuntimeError("Deadlock")
        # advance to next finish
        t_next = min(f for (_n,f) in running)
        # remove finished tasks
        finished_now = [ (n,f) for (n,f) in running if f == t_next ]
        running = [ (n,f) for (n,f) in running if f != t_next ]
        for (n,f) in finished_now:
            finish[n] = f
            completed.add(n)
        t = t_next
    makespan = max(finish.values())
    return start, finish, makespan

start_sched, finish_sched, makespan = schedule_with_resources(tasks, successors, resources=2)

# Calcular slack relativo a la programación (backward pass uso makespan)
LS_sched = {n: makespan - tasks[n]['dur'] for n in tasks}
LF_sched = {n: makespan for n in tasks}
for n in reversed(order):
    if successors[n]:
        LF_sched[n] = min(LS_sched[s] for s in successors[n])
        LS_sched[n] = LF_sched[n] - tasks[n]['dur']

slack_sched = {n: LS_sched[n] - start_sched[n] for n in tasks}
critical_sched = [n for n in tasks if abs(slack_sched[n]) < 1e-9]

# Tablas de salida
df_cpm = pd.DataFrame({
    'Task': order,
    'Dur': [tasks[n]['dur'] for n in order],
    'ES':[ES[n] for n in order],
    'EF':[EF[n] for n in order],
    'LS':[LS[n] for n in order],
    'LF':[LF[n] for n in order],
    'TF':[TF[n] for n in order]
}).set_index('Task')

df_sched = pd.DataFrame([{
    'Task': n,
    'Dur': tasks[n]['dur'],
    'Start': start_sched[n],
    'Finish': finish_sched[n],
    'Slack_in_schedule': slack_sched[n]
} for n in sorted(tasks, key=lambda x: start_sched[x])]).set_index('Task')

print("CPM (recursos infinitos)")
print("Duración total (CPM):", project_duration, "días")
print("Tareas críticas (CPM):", critical_cpm)
display(df_cpm)

print("\nScheduling con 2 recursos (heurística)")
print("Makespan con 2 recursos:", makespan, "días")
print("Tareas críticas en la programación con recursos (slack=0):", critical_sched)
display(df_sched)