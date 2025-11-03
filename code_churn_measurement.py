#!/usr/bin/env python3
"""
code_churn_measurement.py

A from-scratch measurement instrument for **Code Churn** in a Git repository.

Features:
- Computes lines added, removed, and total churn per file.
- Aggregates churn per module (folder).
- Outputs JSON results.
- Produces bar charts for top files and module-level churn.

Usage:
    python3 code_churn_measurement.py --repo /path/to/git/repo --out churn_results.json

Dependencies:
    pip install matplotlib
"""

import argparse
import subprocess
import json
from collections import defaultdict
from pathlib import Path
import matplotlib.pyplot as plt

# -------------------------
# Helper functions
# -------------------------

def run_git_log(repo_path):
    """
    Runs git log to get numstat (lines added/removed per commit per file)
    """
    cmd = ['git', '-C', str(repo_path), 'log', '--numstat', '--pretty=format:commit %H']
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Git command failed: {result.stderr}")
    return result.stdout.splitlines()

def parse_git_numstat(lines):
    """
    Parses git log --numstat output and returns a list of (added, removed, file_path)
    """
    file_churn = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith('commit'):
            continue
        parts = line.split('\t')
        if len(parts) != 3:
            continue
        added, removed, file_path = parts
        # Sometimes added/removed is '-' for binary files
        try:
            added = int(added)
            removed = int(removed)
            file_churn.append((added, removed, file_path))
        except ValueError:
            continue
    return file_churn

def aggregate_churn(file_churn):
    """
    Aggregates churn per file and per module
    """
    file_metrics = defaultdict(lambda: {'added': 0, 'removed': 0})
    module_metrics = defaultdict(lambda: {'added': 0, 'removed': 0})
    
    for added, removed, path in file_churn:
        file_metrics[path]['added'] += added
        file_metrics[path]['removed'] += removed
        module = Path(path).parent.as_posix() if Path(path).parent != Path('.') else '.'
        module_metrics[module]['added'] += added
        module_metrics[module]['removed'] += removed
    
    # Compute total churn
    for metrics in file_metrics.values():
        metrics['total_churn'] = metrics['added'] + metrics['removed']
    for metrics in module_metrics.values():
        metrics['total_churn'] = metrics['added'] + metrics['removed']
    
    return file_metrics, module_metrics

def save_json(file_metrics, module_metrics, out_path):
    results = {
        'files': file_metrics,
        'modules': module_metrics
    }
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)

def plot_top_files(file_metrics, top_n=10, save_path=None):
    sorted_files = sorted(file_metrics.items(), key=lambda x: x[1]['total_churn'], reverse=True)[:top_n]
    files = [f[0] for f in sorted_files]
    churn_values = [f[1]['total_churn'] for f in sorted_files]

    plt.figure(figsize=(10,6))
    plt.barh(files[::-1], churn_values[::-1], color='skyblue')
    plt.xlabel('Total Churn (lines added + removed)')
    plt.title(f'Top {top_n} Files by Code Churn')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    plt.show()

def plot_modules(module_metrics, save_path=None):
    sorted_modules = sorted(module_metrics.items(), key=lambda x: x[1]['total_churn'], reverse=True)
    modules = [m[0] for m in sorted_modules]
    churn_values = [m[1]['total_churn'] for m in sorted_modules]

    plt.figure(figsize=(12,6))
    plt.bar(modules, churn_values, color='salmon')
    plt.xticks(rotation=90)
    plt.ylabel('Total Churn (lines added + removed)')
    plt.title('Code Churn per Module')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    plt.show()

# -------------------------
# Main
# -------------------------
def main():
    parser = argparse.ArgumentParser(description="Code Churn Measurement Instrument")
    parser.add_argument("--repo", required=True, help="Path to local Git repository")
    parser.add_argument("--out", required=True, help="Output JSON file path")
    args = parser.parse_args()

    print(f"Running git log on {args.repo} ...")
    lines = run_git_log(args.repo)
    print(f"Parsing {len(lines)} lines of git log ...")
    file_churn_list = parse_git_numstat(lines)
    print(f"Found {len(file_churn_list)} file entries with churn ...")
    file_metrics, module_metrics = aggregate_churn(file_churn_list)
    save_json(file_metrics, module_metrics, args.out)
    print(f"Results saved to {args.out}")

    print("Plotting top files by churn ...")
    plot_top_files(file_metrics, top_n=10, save_path="top_files_churn.png")

    print("Plotting churn per module ...")
    plot_modules(module_metrics, save_path="module_churn.png")

if __name__ == "__main__":
    main()
