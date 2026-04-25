<p align="right">
  <a href="#english">
    <img src="https://img.shields.io/badge/lang-English-blue" alt="English">
  </a>
  <a href="#portugues">
    <img src="https://img.shields.io/badge/lang-Português-green" alt="Português">
  </a>
</p>

<a id="english"></a>

# Parallel Vector Sum Benchmark — C++ / OpenMP / Intel TBB
A reproducible C++ benchmark comparing three approaches for summing a large vector:

- sequential execution with a simple `for` loop;
- parallel execution with OpenMP;
- parallel execution with Intel TBB.

The benchmark runs 30 measurements for each approach, validates the computed sum, stores raw execution times in CSV format, calculates statistical metrics, generates charts, and produces a technical report.

## Why this repository exists
This project is not just about using threads. The goal is to make the experiment reproducible and easy to inspect: same input size, same result validation, same output structure, and a separate analysis step.

This makes the comparison more reliable and keeps the benchmark results traceable.

## Results
The official execution used a vector with `100,000,000` elements and 30 runs per approach.

| Method | Runs | Mean time (s) | Standard deviation (s) | Min (s) | Max (s) | Speedup |
|---|---:|---:|---:|---:|---:|---:|
| Sequential | 30 | 0.042079 | 0.005446 | 0.029392 | 0.054537 | 1.00x |
| OpenMP | 30 | 0.020261 | 0.006075 | 0.015218 | 0.034884 | 2.08x |
| Intel TBB | 30 | 0.022501 | 0.006314 | 0.015401 | 0.037220 | 1.87x |

In the tested environment, OpenMP achieved the best average execution time, followed closely by Intel TBB. Both parallel implementations reduced the average runtime compared to the sequential version.

The benchmark was executed on a Linux virtual machine with 3 available CPUs. Because vector summation is highly memory-bound, speedup is limited not only by thread count, but also by memory bandwidth and runtime overhead.

## Project structure
    .
    ├── src/main.cpp                    # C++ benchmark implementation
    ├── scripts/analyze.py              # statistical analysis and chart generation
    ├── scripts/build_report_docx.py    # technical report generation
    ├── scripts/run_linux.sh            # complete Linux/WSL execution flow
    ├── docs/relatorio_modelo.md        # base technical report model
    ├── results/                        # measured data, charts and final report
    ├── Makefile
    └── requirements.txt

## Requirements
Linux or WSL with:

    sudo apt-get update
    sudo apt-get install -y g++ libtbb-dev python3 python3-pip python3-venv

Python dependencies:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

OpenMP is enabled through `g++` with the `-fopenmp` flag. Intel TBB is provided by the `libtbb-dev` package.

## Recommended execution
    ./scripts/run_linux.sh

By default, the script uses:

- vector size: `100000000`;
- runs per approach: `30`;
- thread count: detected from the system.

Custom execution:

    ./scripts/run_linux.sh 100000000 30 8

## Manual execution
    make check-env
    make all

    ./build/vector_sum_benchmark \
      --size 100000000 \
      --runs 30 \
      --output results/raw_times.csv

    python3 scripts/analyze.py results/raw_times.csv --out results

    python3 scripts/build_report_docx.py \
      --summary results/summary.csv \
      --results results \
      --out results/report.docx

## Generated outputs
After execution, the main files are generated inside `results/`:

    raw_times.csv          # raw execution measurements
    summary.csv            # mean, standard deviation, min, max and speedup
    comparison_times.png   # comparison chart for all approaches
    sequential_times.png   # sequential execution chart
    openmp_times.png       # OpenMP execution chart
    tbb_times.png          # Intel TBB execution chart
    report.md              # technical report draft
    report.docx            # final Word report
    environment.txt        # execution environment metadata

## Methodology notes
The program performs a warm-up pass before collecting measurements. This warm-up is not recorded in the output file and helps reduce first-run noise such as runtime initialization and initial loading effects.

Each measured execution validates the computed sum against the expected result before recording the elapsed time. This prevents invalid measurements from being included in the analysis.

The comparison should be based on mean time and standard deviation, not only on the fastest execution. Since vector summation is a simple memory-intensive operation, parallel speedup can be limited by memory bandwidth, scheduling overhead, and the number of available CPU cores.

## Cleaning generated files
    make clean

---

<a id="portugues"></a>

# Benchmark de Soma de Vetor — C++ / OpenMP / Intel TBB
Benchmark em C++ para comparar três abordagens de soma de um vetor grande:

- execução sequencial com `for` simples;
- execução paralela com OpenMP;
- execução paralela com Intel TBB.

O benchmark executa 30 medições por abordagem, valida o resultado da soma, grava os tempos brutos em CSV, calcula métricas estatísticas, gera gráficos e produz um relatório técnico.

## Por que este repositório existe
Este projeto não é apenas sobre usar threads. O objetivo é tornar o experimento reprodutível e fácil de revisar: mesmo tamanho de entrada, mesma validação de resultado, mesma estrutura de saída e análise separada da execução.

Isso torna a comparação mais confiável e mantém os resultados rastreáveis.

## Resultados
A execução oficial utilizou um vetor com `100.000.000` elementos e 30 execuções por abordagem.

| Método | Execuções | Média (s) | Desvio padrão (s) | Mínimo (s) | Máximo (s) | Speedup |
|---|---:|---:|---:|---:|---:|---:|
| Sequencial | 30 | 0.042079 | 0.005446 | 0.029392 | 0.054537 | 1.00x |
| OpenMP | 30 | 0.020261 | 0.006075 | 0.015218 | 0.034884 | 2.08x |
| Intel TBB | 30 | 0.022501 | 0.006314 | 0.015401 | 0.037220 | 1.87x |

No ambiente testado, OpenMP obteve o melhor tempo médio de execução, seguido de perto pela Intel TBB. As duas implementações paralelas reduziram o tempo médio em relação à versão sequencial.

O benchmark foi executado em uma máquina virtual Linux com 3 CPUs disponíveis. Como a soma de vetor é uma operação fortemente dependente de acesso à memória, o ganho de paralelização é limitado não apenas pela quantidade de threads, mas também pela largura de banda de memória e pelo overhead do runtime.

## Estrutura do projeto
    .
    ├── src/main.cpp                    # implementação do benchmark em C++
    ├── scripts/analyze.py              # análise estatística e geração de gráficos
    ├── scripts/build_report_docx.py    # geração do relatório técnico
    ├── scripts/run_linux.sh            # fluxo completo de execução no Linux/WSL
    ├── docs/relatorio_modelo.md        # modelo base do relatório técnico
    ├── results/                        # dados medidos, gráficos e relatório final
    ├── Makefile
    └── requirements.txt

## Requisitos
Linux ou WSL com:

    sudo apt-get update
    sudo apt-get install -y g++ libtbb-dev python3 python3-pip python3-venv

Dependências Python:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

OpenMP é habilitado pelo `g++` com a flag `-fopenmp`. A Intel TBB é fornecida pelo pacote `libtbb-dev`.

## Execução recomendada
    ./scripts/run_linux.sh

Por padrão, o script usa:

- tamanho do vetor: `100000000`;
- execuções por abordagem: `30`;
- quantidade de threads: detectada pelo sistema.

Execução personalizada:

    ./scripts/run_linux.sh 100000000 30 8

## Execução manual
    make check-env
    make all

    ./build/vector_sum_benchmark \
      --size 100000000 \
      --runs 30 \
      --output results/raw_times.csv

    python3 scripts/analyze.py results/raw_times.csv --out results

    python3 scripts/build_report_docx.py \
      --summary results/summary.csv \
      --results results \
      --out results/report.docx

## Saídas geradas
Após a execução, os principais arquivos são gerados em `results/`:

    raw_times.csv          # medições brutas das execuções
    summary.csv            # média, desvio padrão, mínimo, máximo e speedup
    comparison_times.png   # gráfico comparando todas as abordagens
    sequential_times.png   # gráfico da execução sequencial
    openmp_times.png       # gráfico da execução com OpenMP
    tbb_times.png          # gráfico da execução com Intel TBB
    report.md              # rascunho do relatório técnico
    report.docx            # relatório final em Word
    environment.txt        # metadados do ambiente de execução

## Observações de metodologia
O programa realiza uma passagem de aquecimento antes da coleta das medições. Esse aquecimento não é registrado no arquivo de saída e ajuda a reduzir ruídos de primeira execução, como inicialização de runtime e efeitos iniciais de carregamento.

Cada execução medida valida a soma calculada contra o resultado esperado antes de registrar o tempo. Isso evita que medições inválidas entrem na análise.

A comparação deve ser feita com base na média e no desvio padrão, não apenas no menor tempo. Como a soma de vetor é uma operação simples e intensiva em leitura de memória, o ganho de paralelização pode ser limitado pela largura de banda de memória, pelo overhead de escalonamento e pela quantidade de núcleos disponíveis.

## Limpeza dos arquivos gerados
    make clean
