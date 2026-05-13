import math
from config import config

def mean_std(values):
    if not values:
        return 0.0, 0.0
    m = sum(values) / len(values)
    var = sum((v - m) ** 2 for v in values) / len(values)
    return m, math.sqrt(var)


def print_results(label, result, processes):
    print(f"\n{'═'*60}")
    print(f"  {label}")
    print(f"{'═'*60}")

    print("\n  Execution Timeline:")
    print("  " + "-"*50)
    for (s, e, pid) in result['timeline']:
        bar = '█' * (e - s)
        tag = f"[{pid:4s}]"
        print(f"  t={s:>3}–{e:<3}  {tag}  {bar}")
    print()

    print(f"  {'PID':<6} {'Arrival':>7} {'Burst':>6} {'First Run':>10} "
          f"{'Finish':>7} {'Response':>9} {'Turnaround':>11}")
    print("  " + "-"*60)
    for p in result['completed']:
        rt  = p['first_run'] - p['arrivaltime']
        tat = p['finish_time'] - p['arrivaltime']
        print(f"  {p['pid']:<6} {p['arrivaltime']:>7} {p['bursttime']:>6} "
              f"{p['first_run']:>10} {p['finish_time']:>7} {rt:>9} {tat:>11}")

    rt_m,  rt_s  = mean_std(result['response_times'])
    tat_m, tat_s = mean_std(result['turnaround_times'])
    T = config['metadata']['throughputwindowT']
    print(f"\n  Avg Response Time  : {rt_m:.2f} ± {rt_s:.2f}")
    print(f"  Avg Turnaround Time: {tat_m:.2f} ± {tat_s:.2f}")
    print(f"  Throughput (T={T}): {result['throughput']} processes")


def print_analysis(all_results):
    print(f"\n{'═'*60}")
    print("  ALGORITHM ANALYSIS")
    print(f"{'═'*60}")

    print("""
  ROUND ROBIN (RR)
  ─────────────────────────────────────────────
  ✔ ADVANTAGES:
    • Fairness: Every process gets CPU time periodically.
    • Starvation-free: No process waits indefinitely.
    • Good response time for interactive/short processes when
      quantum is small.
    • Predictable: behavior is deterministic given quantum.

  ✘ DISADVANTAGES:
    • Context switch overhead: small quantum → many switches
      → high overhead (1 tick per switch in this model).
    • Large quantum → degenerates toward FCFS, poor response
      time for late-arriving short processes.
    • No priority awareness: long processes delay short ones
      when quantum is large.
    • Average turnaround can be much higher than SRTF.

  SRTF (Shortest Remaining Time First)
  ─────────────────────────────────────────────
  ✔ ADVANTAGES:
    • Optimal average turnaround time (provably minimal).
    • Short jobs finish quickly, low wait for short processes.
    • Preemption ensures newly arrived short jobs are not
      blocked by long running ones.

  ✘ DISADVANTAGES:
    • Starvation risk: long processes can be indefinitely
      delayed by a stream of short arrivals.
    • Requires knowing burst times in advance (unrealistic
      in practice without estimation).
    • Higher preemption rate → more context switches vs large
      quantum RR.
    • Complex implementation; scheduling overhead.
""")

    print("  QUANTUM IMPACT ANALYSIS (RR)")
    print("  ─────────────────────────────────────────────")
    print(f"  {'Config':<10} {'Avg RT':>8} {'±':>5} {'Avg TAT':>9} {'±':>5} "
          f"{'Throughput':>11} {'CTX switches':>13}")
    print("  " + "-"*65)
    for label, res in all_results.items():
        rt_m,  rt_s  = mean_std(res['response_times'])
        tat_m, tat_s = mean_std(res['turnaround_times'])
        ctx_count = sum(1 for (_, _, pid) in res['timeline'] if pid == 'CTX')
        print(f"  {label:<10} {rt_m:>8.2f} {rt_s:>6.2f} {tat_m:>9.2f} {tat_s:>6.2f} "
              f"{res['throughput']:>11} {ctx_count:>13}")

    print(f"\n  KEY INSIGHT:")
    rr_labels = [k for k in all_results if k.startswith('RR')]
    srtf_res  = all_results.get('SRTF')
    if srtf_res and rr_labels:
        srtf_tat, _ = mean_std(srtf_res['turnaround_times'])
        best_rr     = min(rr_labels, key=lambda k: mean_std(all_results[k]['turnaround_times'])[0])
        best_rr_tat, _ = mean_std(all_results[best_rr]['turnaround_times'])
        srtf_ctx = sum(1 for (_, _, pid) in srtf_res['timeline'] if pid == 'CTX')
        print(f"  SRTF achieves the lowest avg turnaround ({srtf_tat:.2f} ticks).")
        print(f"  Best RR ({best_rr}) achieves {best_rr_tat:.2f} ticks "
              f"— {best_rr_tat - srtf_tat:.2f} ticks worse.")
        print(f"  SRTF uses {srtf_ctx} context switches total in this workload.")
