import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

FIGDIR = 'papers/sci_affective_safety_calibration/figures'

def save_fig(fig, name):
    fig.savefig(f'{FIGDIR}/{name}.png', dpi=300, bbox_inches='tight')
    fig.savefig(f'{FIGDIR}/{name}.pdf', bbox_inches='tight')
    plt.close(fig)

def fig1_framework():
    fig, ax = plt.subplots(figsize=(4.5, 7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    boxes = [
        (5, 9.2, 'User Request + Task Context'),
        (5, 8.0, 'Action / Event Parser'),
        (5, 6.8, 'Risk Context Detector'),
        (5, 5.6, 'Affective Pressure Signal'),
        (5, 4.4, 'Experience Memory Signal'),
        (5, 3.2, 'Three-Tier SafeActionCalibrator'),
        (5, 2.0, 'Decision Output'),
        (5, 0.8, 'Outcome / Memory Update'),
    ]

    for x, y, label in boxes:
        w, h = 7.0, 0.7
        rect = mpatches.FancyBboxPatch(
            (x - w/2, y - h/2), w, h,
            boxstyle='round,pad=0.1',
            facecolor='white', edgecolor='black', linewidth=1.2
        )
        ax.add_patch(rect)
        fontsize = 8 if len(label) > 30 else 9
        ax.text(x, y, label, ha='center', va='center', fontsize=fontsize, fontweight='bold')

    for i in range(len(boxes) - 1):
        ax.annotate('', xy=(5, boxes[i+1][1] + 0.35), xytext=(5, boxes[i][1] - 0.35),
                    arrowprops=dict(arrowstyle='->', color='black', lw=1.2))

    ax.text(5, 2.0 - 0.55, 'AUTO_EXECUTE / SIMULATE_FIRST / HUMAN_REVIEW / BLOCK',
            ha='center', va='top', fontsize=6.5, style='italic')

    save_fig(fig, 'fig1_framework_architecture')

def fig2_three_tier():
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis('off')

    tiers = [
        (2, 4.5, 'Tier 1\nStrict Review', 
         ['destructive', 'sensitive', 'security-related', 'irreversible', 'production'],
         'HUMAN_REVIEW / BLOCK', 0.85),
        (2, 2.5, 'Tier 2\nSafe Auto-Execute',
         ['safe verb', 'no Tier 1 risk', 'non-destructive event'],
         'AUTO_EXECUTE', 0.95),
        (2, 0.5, 'Tier 3\nDefault Cautious',
         ['unclear intent', 'insufficient safety evidence'],
         'SIMULATE_FIRST', 0.90),
    ]

    for x, y, title, items, output, grey in tiers:
        tw, th = 4.5, 1.5
        rect = mpatches.FancyBboxPatch(
            (x - tw/2, y - th/2), tw, th,
            boxstyle='round,pad=0.1',
            facecolor=str(grey), edgecolor='black', linewidth=1.2
        )
        ax.add_patch(rect)
        ax.text(x, y + 0.45, title, ha='center', va='center', fontsize=8, fontweight='bold')
        items_text = ', '.join(items)
        ax.text(x, y - 0.05, items_text, ha='center', va='center', fontsize=6.5)
        ax.text(x, y - 0.45, output, ha='center', va='center', fontsize=7, style='italic')

    for i in range(len(tiers) - 1):
        ax.annotate('', xy=(2, tiers[i+1][1] + 0.75), xytext=(2, tiers[i][1] - 0.75),
                    arrowprops=dict(arrowstyle='->', color='black', lw=1.2))
        ax.text(2.3, (tiers[i][1] + tiers[i+1][1]) / 2, 'not matched', fontsize=6, va='center')

    ax.annotate('', xy=(2, tiers[0][1] + 0.75 + 0.3), xytext=(2, 5.8),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.2))
    ax.text(2.3, 5.6, 'input', fontsize=6, va='center')

    ax.text(8, 4.5, 'Priority\nOrder', ha='center', va='center', fontsize=9, fontweight='bold')
    ax.annotate('', xy=(8, 0.5), xytext=(8, 3.8),
                arrowprops=dict(arrowstyle='->', color='black', lw=2))
    ax.text(8.4, 2.5, 'decreasing', fontsize=7, rotation=90, va='center')

    save_fig(fig, 'fig2_three_tier_policy')

def fig3_risky_comparison():
    methods = [
        'FullCalibratorAdapter',
        'KeywordRuleBaseline',
        'SafeKeywordFirstBaseline',
        'RiskContextOracleBaseline*',
        'NoExperienceNoAffectiveBaseline',
    ]
    values = [0.036, 0.780, 0.872, 0.064, 0.043]

    fig, ax = plt.subplots(figsize=(7, 4))
    colors = ['#2c2c2c', '#888888', '#aaaaaa', '#cccccc', '#666666']
    hatches = ['', '//', '\\\\', '..', 'xx']

    bars = ax.barh(range(len(methods)), values, color=colors, edgecolor='black', linewidth=0.8, height=0.6)
    for bar, hatch in zip(bars, hatches):
        bar.set_hatch(hatch)

    ax.set_yticks(range(len(methods)))
    ax.set_yticklabels(methods, fontsize=8)
    ax.set_xlabel('Risky Auto-Execution Rate', fontsize=9)
    ax.set_xlim(0, 1.0)
    ax.invert_yaxis()

    for i, v in enumerate(values):
        ax.text(v + 0.02, i, f'{v:.3f}', va='center', fontsize=8)

    ax.axvline(x=0.05, color='red', linestyle='--', linewidth=0.8, alpha=0.7)
    ax.text(0.055, -0.3, 'target ≤ 0.05', fontsize=7, color='red')

    ax.text(0.5, 4.8, '* Oracle / upper-bound diagnostic baseline, not deployable',
            fontsize=6.5, style='italic', ha='center', transform=ax.get_xaxis_transform())

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    save_fig(fig, 'fig3_risky_auto_exec_comparison')

def fig4_longitudinal():
    groups = ['no_memory', 'single_failure\nmemory', 'accumulated_failure\nmemory']
    risky = [0.043, 0.036, 0.000]
    safe_ae = [0.757, 0.757, 0.000]
    composite = [0.830, 0.835, 0.716]

    x = np.arange(len(groups))
    width = 0.25

    fig, ax = plt.subplots(figsize=(7, 4))
    bars1 = ax.bar(x - width, risky, width, label='Risky Auto-Exec Rate',
                   color='#2c2c2c', edgecolor='black', linewidth=0.8)
    bars2 = ax.bar(x, safe_ae, width, label='Safe Auto-Exec Accuracy',
                   color='#888888', edgecolor='black', linewidth=0.8, hatch='//')
    bars3 = ax.bar(x + width, composite, width, label='Composite Score',
                   color='#cccccc', edgecolor='black', linewidth=0.8, hatch='..')

    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            h = bar.get_height()
            if h > 0:
                ax.text(bar.get_x() + bar.get_width()/2, h + 0.02,
                        f'{h:.3f}', ha='center', va='bottom', fontsize=7)

    ax.set_xticks(x)
    ax.set_xticklabels(groups, fontsize=8)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel('Score / Rate', fontsize=9)
    ax.legend(fontsize=7, loc='upper right')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.annotate('Best safety-utility\nbalance', xy=(1, 0.757), xytext=(1.6, 0.5),
                fontsize=7, ha='center',
                arrowprops=dict(arrowstyle='->', color='black', lw=0.8))

    ax.annotate('Over-caution\ncollapse', xy=(2, 0.0), xytext=(2.5, 0.3),
                fontsize=7, ha='center',
                arrowprops=dict(arrowstyle='->', color='black', lw=0.8))

    save_fig(fig, 'fig4_longitudinal_memory_tradeoff')

if __name__ == '__main__':
    fig1_framework()
    fig2_three_tier()
    fig3_risky_comparison()
    fig4_longitudinal()
    print('All 4 figures generated.')
