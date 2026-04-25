import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

from config import COLORS
from metrics import mean_std


def plot_gantt(all_results, processes, output_path):
    labels = list(all_results.keys())
    n = len(labels)
    fig_height = max(6, n * 1.2 + 3)
    fig, axes = plt.subplots(n, 1, figsize=(20, fig_height), facecolor='#0d1117')
    if n == 1:
        axes = [axes]

    fig.suptitle('Scheduling Algorithm Comparison – Gantt Charts',
                 fontsize=15, fontweight='bold', color='white', y=1.01)

    pid_list = [p['pid'] for p in processes]
    legend_patches = [mpatches.Patch(color=COLORS.get(pid, '#ccc'), label=pid) for pid in pid_list]
    legend_patches.append(mpatches.Patch(color=COLORS['CTX'],  label='CTX Switch'))
    legend_patches.append(mpatches.Patch(color=COLORS['IDLE'], label='IDLE'))

    all_ends = [e for res in all_results.values() for (_, e, _) in res['timeline']]
    max_t = max(all_ends) + 2 if all_ends else 20

    for ax, label in zip(axes, labels):
        ax.set_facecolor('#161b22')
        ax.set_xlim(0, max_t)
        ax.set_ylim(0, 1)
        ax.set_yticks([])
        ax.set_ylabel(label, fontsize=8.5, color='white', rotation=0,
                      labelpad=60, ha='right', va='center')
        ax.tick_params(colors='#8b949e', labelsize=7)
        ax.spines[:].set_color('#30363d')
        ax.set_xticks(range(0, max_t + 1, 5))
        ax.xaxis.set_tick_params(color='#30363d')

        for (s, e, pid) in all_results[label]['timeline']:
            color = COLORS.get(pid, '#cccccc')
            width = e - s
            rect = mpatches.FancyBboxPatch(
                (s + 0.05, 0.1), max(width - 0.1, 0.05), 0.8,
                boxstyle="round,pad=0.02",
                linewidth=0.5, edgecolor='#0d1117',
                facecolor=color, alpha=0.92,
            )
            ax.add_patch(rect)
            if width >= 1.5:
                ax.text(s + width / 2, 0.5,
                        pid if pid not in ('CTX', 'IDLE') else pid[:3],
                        ha='center', va='center', fontsize=6.5,
                        color='white', fontweight='bold')

    fig.legend(handles=legend_patches, loc='lower center',
               ncol=len(legend_patches), frameon=False,
               labelcolor='white', fontsize=9,
               bbox_to_anchor=(0.5, -0.04))
    fig.text(0.5, -0.02, 'Time (ticks)', ha='center', fontsize=10, color='#8b949e')

    plt.tight_layout(h_pad=0.6)
    plt.savefig(output_path, dpi=150, bbox_inches='tight',
                facecolor='#0d1117', edgecolor='none')
    plt.close()
    print(f"\n  [✓] Gantt chart saved → {output_path}")


def plot_metrics(all_results, throughput_T, output_path):
    labels = list(all_results.keys())

    rt_means, rt_stds, tat_means, tat_stds, throughputs = [], [], [], [], []
    for label in labels:
        res = all_results[label]
        rt_m,  rt_s  = mean_std(res['response_times'])
        tat_m, tat_s = mean_std(res['turnaround_times'])
        rt_means.append(rt_m);   rt_stds.append(rt_s)
        tat_means.append(tat_m); tat_stds.append(tat_s)
        throughputs.append(res['throughput'])

    x = np.arange(len(labels))
    bar_colors = ['#F4A460' if 'SRTF' in lbl else '#4E9AF1' for lbl in labels]

    fig, axes = plt.subplots(1, 3, figsize=(18, 5), facecolor='#0d1117')
    fig.suptitle('Metrics Summary – RR (various quantums) vs SRTF',
                 fontsize=13, fontweight='bold', color='white')

    chart_data = [
        ('Avg Response Time (ticks)',   rt_means,    rt_stds),
        ('Avg Turnaround Time (ticks)', tat_means,   tat_stds),
        (f'Throughput (T={throughput_T})', throughputs, None),
    ]

    for ax, (title, means, stds) in zip(axes, chart_data):
        ax.set_facecolor('#161b22')
        ax.spines[:].set_color('#30363d')
        ax.tick_params(colors='#8b949e', labelsize=8)
        ax.set_title(title, color='white', fontsize=10, pad=8)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=35, ha='right', fontsize=7.5)
        ax.yaxis.label.set_color('#8b949e')

        bars = ax.bar(x, means, color=bar_colors, edgecolor='#0d1117',
                      linewidth=0.5, alpha=0.9)
        if stds:
            ax.errorbar(x, means, yerr=stds, fmt='none', color='white',
                        capsize=4, linewidth=1.2, capthick=1.2)

        for bar, val in zip(bars, means):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + max(means) * 0.02,
                    f'{val:.1f}', ha='center', va='bottom',
                    fontsize=7.5, color='white', fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight',
                facecolor='#0d1117', edgecolor='none')
    plt.close()
    print(f"  [✓] Metrics chart saved → {output_path}")
