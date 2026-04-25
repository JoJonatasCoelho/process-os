from pathlib import Path
from config import config, processes, ctx_cost, T, quantums
from schedulers import simulate_rr, simulate_srtf
from metrics import print_results, print_analysis
from plots import plot_gantt, plot_metrics

OUTPUT_DIR = Path(__file__).parent / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
print("\n" + "═"*60)
print("  QUANTUM SCHEDULING SIMULATOR")
print("  RR vs SRTF with Context Switch Cost")
print("═"*60)
print(f"\n  Processes : {[p['pid'] for p in processes]}")
print(f"  Arrivals  : {[p['arrivaltime'] for p in processes]}")
print(f"  Bursts    : {[p['bursttime'] for p in processes]}")
print(f"  CTX Cost  : {ctx_cost} tick(s)")
print(f"  Throughput window T: {T}")

# ─────────────────────────────────────────────
# RUN SIMULATIONS
# ─────────────────────────────────────────────
all_results = {}

for q in quantums:
    label = f"RR Q={q}"
    all_results[label] = simulate_rr(processes, q, ctx_cost, T)
    print_results(label, all_results[label], processes)

all_results['SRTF'] = simulate_srtf(processes, ctx_cost, T)
print_results('SRTF', all_results['SRTF'], processes)

# ─────────────────────────────────────────────
# ANALYSIS & PLOTS
# ─────────────────────────────────────────────
print_analysis(all_results)

plot_gantt(all_results, processes, OUTPUT_DIR / "gantt_chart.png")
plot_metrics(all_results, T, OUTPUT_DIR / "metrics_chart.png")

print("\n  Done.\n")
