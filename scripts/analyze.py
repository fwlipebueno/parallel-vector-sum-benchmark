#!/usr/bin/env python3
import argparse
import csv
import math
import os
import platform
import statistics
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt

METHOD_LABELS = {
    "sequential": "Sequencial",
    "openmp": "OpenMP",
    "tbb": "TBB",
}

METHOD_ORDER = ["sequential", "openmp", "tbb"]


def read_measurements(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        required = {"method", "run", "seconds", "sum", "vector_size", "threads"}
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"CSV sem colunas obrigatórias: {', '.join(sorted(missing))}")

        for row in reader:
            rows.append({
                "method": row["method"],
                "run": int(row["run"]),
                "seconds": float(row["seconds"]),
                "sum": int(row["sum"]),
                "vector_size": int(row["vector_size"]),
                "threads": int(row["threads"]),
            })

    if not rows:
        raise ValueError("CSV sem medições.")

    return rows


def summarize(rows):
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["method"]].append(row["seconds"])

    if "sequential" not in grouped:
        raise ValueError("Não há medições do método sequencial.")

    sequential_mean = statistics.mean(grouped["sequential"])
    summary = []

    for method in METHOD_ORDER:
        values = grouped.get(method, [])
        if not values:
            continue

        mean = statistics.mean(values)
        stdev = statistics.stdev(values) if len(values) > 1 else 0.0
        speedup = sequential_mean / mean if mean > 0 else math.nan

        summary.append({
            "method": method,
            "label": METHOD_LABELS.get(method, method),
            "runs": len(values),
            "mean": mean,
            "stdev": stdev,
            "min": min(values),
            "max": max(values),
            "speedup": speedup,
        })

    return summary


def write_summary_csv(summary, output_dir):
    path = output_dir / "summary.csv"
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["method", "runs", "mean_seconds", "stdev_seconds", "min_seconds", "max_seconds", "speedup_vs_sequential"],
        )
        writer.writeheader()
        for row in summary:
            writer.writerow({
                "method": row["label"],
                "runs": row["runs"],
                "mean_seconds": f"{row['mean']:.9f}",
                "stdev_seconds": f"{row['stdev']:.9f}",
                "min_seconds": f"{row['min']:.9f}",
                "max_seconds": f"{row['max']:.9f}",
                "speedup_vs_sequential": f"{row['speedup']:.4f}",
            })
    return path


def plot_comparison(rows, output_dir):
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["method"]].append(row)

    fig, ax = plt.subplots(figsize=(10, 5.5))
    for method in METHOD_ORDER:
        values = sorted(grouped.get(method, []), key=lambda item: item["run"])
        if not values:
            continue
        ax.plot(
            [item["run"] for item in values],
            [item["seconds"] for item in values],
            marker="o",
            label=METHOD_LABELS.get(method, method),
        )

    ax.set_title("Tempos de execução por abordagem")
    ax.set_xlabel("Execução")
    ax.set_ylabel("Tempo (s)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()

    path = output_dir / "comparison_times.png"
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path


def plot_method(rows, output_dir, method):
    values = sorted([row for row in rows if row["method"] == method], key=lambda item: item["run"])
    if not values:
        return None

    label = METHOD_LABELS.get(method, method)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(
        [item["run"] for item in values],
        [item["seconds"] for item in values],
        marker="o",
    )
    ax.set_title(f"Tempos de execução - {label}")
    ax.set_xlabel("Execução")
    ax.set_ylabel("Tempo (s)")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    path = output_dir / f"{method}_times.png"
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path


def format_table(summary):
    lines = [
        "| Abordagem | Execuções | Média (s) | Desvio padrão (s) | Mínimo (s) | Máximo (s) | Speedup |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary:
        lines.append(
            f"| {row['label']} | {row['runs']} | {row['mean']:.6f} | {row['stdev']:.6f} | "
            f"{row['min']:.6f} | {row['max']:.6f} | {row['speedup']:.2f}x |"
        )
    return "\n".join(lines)


def write_report(rows, summary, output_dir):
    vector_size = rows[0]["vector_size"]
    threads = rows[0]["threads"]
    report_path = output_dir / "report.md"

    best_parallel = min(
        [row for row in summary if row["method"] in {"openmp", "tbb"}],
        key=lambda item: item["mean"],
        default=None,
    )

    discussion = (
        "A versão paralela mais rápida, considerando a média das execuções, foi "
        f"{best_parallel['label']}, com speedup médio de {best_parallel['speedup']:.2f}x em relação à versão sequencial."
        if best_parallel else
        "Não foi possível comparar as versões paralelas porque as medições não estão completas."
    )

    content = f"""# Relatório técnico — soma de vetor com C++, OpenMP e TBB

## 1. Introdução

Este experimento compara três formas de somar os elementos de um vetor grande em C++: uma implementação sequencial, uma implementação paralela com OpenMP e uma implementação paralela com Intel TBB. O objetivo é observar o impacto da paralelização no tempo de execução e avaliar a estabilidade dos resultados por meio da média e do desvio padrão das medições.

## 2. Metodologia

O vetor utilizado possui {vector_size:,} elementos inteiros. Cada posição foi inicializada com o valor 1, permitindo validar o resultado esperado da soma antes de registrar cada medição. Foram executadas {summary[0]['runs']} medições por abordagem. O tempo foi medido dentro do programa em C++ com `std::chrono::steady_clock`, registrando apenas o trecho responsável pela soma.

As versões paralelas foram implementadas com redução: em OpenMP, por meio da diretiva `#pragma omp parallel for reduction(+:sum)`; em TBB, por meio de `tbb::parallel_reduce`. O número de threads reportado pelo programa foi {threads}. Os dados brutos foram gravados em CSV e analisados em Python.

Ambiente de análise do relatório:

- Sistema: {platform.platform()}
- Python: {platform.python_version()}

## 3. Resultados

{format_table(summary)}

### Gráficos

![Comparação dos tempos](comparison_times.png)

![Tempos da abordagem sequencial](sequential_times.png)

![Tempos da abordagem OpenMP](openmp_times.png)

![Tempos da abordagem TBB](tbb_times.png)

## 4. Discussão

{discussion} Em geral, a soma de um vetor grande tende a ser limitada pela largura de banda de memória: depois que a CPU passa a ler dados mais rapidamente do que a memória consegue entregar, adicionar mais threads nem sempre produz ganhos proporcionais. Por isso, a análise considera não apenas o menor tempo observado, mas principalmente a média e o desvio padrão ao longo das 30 execuções.

Diferenças entre OpenMP e TBB podem ocorrer por causa do escalonamento das tarefas, do custo de criação e sincronização das threads e da forma como cada biblioteca divide o trabalho. Como a operação de soma é simples, o custo de coordenação pode ter peso relevante, principalmente quando a máquina possui poucos núcleos ou quando outros processos competem por CPU e memória.

## 5. Conclusão

O experimento mostra como a paralelização pode reduzir o tempo de execução de uma tarefa simples e intensiva em leitura de memória, mas também evidencia que o ganho depende do ambiente de execução e do custo de coordenação das threads. A versão sequencial serve como base de comparação, enquanto OpenMP e TBB mostram duas estratégias práticas para explorar paralelismo em C++.
"""

    report_path.write_text(content, encoding="utf-8")
    return report_path


def main():
    parser = argparse.ArgumentParser(description="Analyze vector sum benchmark results.")
    parser.add_argument("csv", help="Path to raw_times.csv generated by the C++ benchmark.")
    parser.add_argument("--out", default="results", help="Output directory. Default: results")
    args = parser.parse_args()

    output_dir = Path(args.out)
    output_dir.mkdir(parents=True, exist_ok=True)

    rows = read_measurements(args.csv)
    summary = summarize(rows)

    summary_path = write_summary_csv(summary, output_dir)
    comparison_path = plot_comparison(rows, output_dir)
    method_paths = [plot_method(rows, output_dir, method) for method in METHOD_ORDER]
    report_path = write_report(rows, summary, output_dir)

    print(f"Summary: {summary_path}")
    print(f"Comparison chart: {comparison_path}")
    for path in method_paths:
        if path:
            print(f"Method chart: {path}")
    print(f"Report draft: {report_path}")


if __name__ == "__main__":
    main()
