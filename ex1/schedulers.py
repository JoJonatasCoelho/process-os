import random
from config import SEED

def simulate_rr(processes, quantum, ctx_cost, throughput_T, seed=SEED):
    rng = random.Random(seed)
    procs = [dict(p) for p in processes]
    for p in procs:
        p['remaining'] = p['bursttime']
        p['first_run'] = None
        p['finish_time'] = None

    timeline = []
    t = 0
    ready_queue = []
    arrived = set()
    current = None
    current_ran = 0
    completed = []

    pending = sorted(procs, key=lambda x: x['arrivaltime'])

    def enqueue_arrivals(time):
        for p in pending:
            if p['pid'] not in arrived and p['arrivaltime'] <= time:
                arrived.add(p['pid'])
                ready_queue.append(p)

    enqueue_arrivals(t)

    while pending or ready_queue or current:
        enqueue_arrivals(t)

        if current is None:
            if not ready_queue:
                future = [p['arrivaltime'] for p in pending if p['pid'] not in arrived]
                if not future:
                    break
                next_arr = min(future)
                timeline.append((t, next_arr, 'IDLE'))
                t = next_arr
                enqueue_arrivals(t)
                continue

            current = ready_queue.pop(0)
            current_ran = 0
            if current['first_run'] is None:
                current['first_run'] = t

        run_for = min(quantum - current_ran, current['remaining'])
        start = t
        end = t + run_for
        timeline.append((start, end, current['pid']))
        t = end
        current['remaining'] -= run_for
        current_ran += run_for

        enqueue_arrivals(t)

        if current['remaining'] == 0:
            current['finish_time'] = t
            completed.append(current)
            current = None
            current_ran = 0
            if ready_queue:
                timeline.append((t, t + ctx_cost, 'CTX'))
                t += ctx_cost
                enqueue_arrivals(t)

        elif current_ran >= quantum:
            prev = current
            current = None
            current_ran = 0
            if ready_queue or any(p['arrivaltime'] <= t for p in pending if p['pid'] not in arrived):
                enqueue_arrivals(t)
                ready_queue.append(prev)
                if ready_queue:
                    timeline.append((t, t + ctx_cost, 'CTX'))
                    t += ctx_cost
                    enqueue_arrivals(t)
            else:
                ready_queue.append(prev)

    response_times = []
    turnaround_times = []
    for p in completed:
        response_times.append(p['first_run'] - p['arrivaltime'])
        turnaround_times.append(p['finish_time'] - p['arrivaltime'])

    return {
        'timeline': timeline,
        'completed': completed,
        'response_times': response_times,
        'turnaround_times': turnaround_times,
        'throughput': sum(1 for p in completed if p['finish_time'] <= throughput_T),
    }


def simulate_srtf(processes, ctx_cost, throughput_T, seed=SEED):
    rng = random.Random(seed)
    procs = [dict(p) for p in processes]
    for p in procs:
        p['remaining'] = p['bursttime']
        p['first_run'] = None
        p['finish_time'] = None

    timeline = []
    t = 0
    ready_queue = []
    arrived = set()
    current = None
    completed = []

    pending = sorted(procs, key=lambda x: x['arrivaltime'])

    def enqueue_arrivals(time):
        for p in pending:
            if p['pid'] not in arrived and p['arrivaltime'] <= time:
                arrived.add(p['pid'])
                ready_queue.append(p)

    enqueue_arrivals(t)

    while pending or ready_queue or current:
        enqueue_arrivals(t)

        if not ready_queue and current is None:
            future = [p['arrivaltime'] for p in pending if p['pid'] not in arrived]
            if not future:
                break
            next_arr = min(future)
            timeline.append((t, next_arr, 'IDLE'))
            t = next_arr
            enqueue_arrivals(t)
            continue

        candidates = list(ready_queue)
        if current:
            candidates.append(current)

        min_rem = min(p['remaining'] for p in candidates)
        shortest_candidates = [p for p in candidates if p['remaining'] == min_rem]
        rng.shuffle(shortest_candidates)
        chosen = shortest_candidates[0]

        if current and chosen['pid'] != current['pid']:
            ready_queue.append(current)
            ready_queue.remove(chosen)
            timeline.append((t, t + ctx_cost, 'CTX'))
            t += ctx_cost
            enqueue_arrivals(t)
            current = chosen
            if current['first_run'] is None:
                current['first_run'] = t
        elif current is None:
            ready_queue.remove(chosen)
            current = chosen
            if current['first_run'] is None:
                current['first_run'] = t

        future_arrivals = [p['arrivaltime'] for p in pending if p['pid'] not in arrived]
        next_event = (min(future_arrivals) - t) if future_arrivals else float('inf')

        run_for = min(current['remaining'], next_event)
        if run_for <= 0:
            run_for = 1

        timeline.append((t, t + run_for, current['pid']))
        t += run_for
        current['remaining'] -= run_for

        enqueue_arrivals(t)

        if current['remaining'] == 0:
            current['finish_time'] = t
            completed.append(current)
            current = None
            if ready_queue:
                timeline.append((t, t + ctx_cost, 'CTX'))
                t += ctx_cost
                enqueue_arrivals(t)

    response_times = []
    turnaround_times = []
    for p in completed:
        response_times.append(p['first_run'] - p['arrivaltime'])
        turnaround_times.append(p['finish_time'] - p['arrivaltime'])

    return {
        'timeline': timeline,
        'completed': completed,
        'response_times': response_times,
        'turnaround_times': turnaround_times,
        'throughput': sum(1 for p in completed if p['finish_time'] <= throughput_T),
    }
