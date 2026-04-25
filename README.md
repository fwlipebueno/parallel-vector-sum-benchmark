<a id="english"></a>

<p align="right">
  <kbd><a href="#english">English</a></kbd>
  <kbd><a href="#portuguese">Português</a></kbd>
</p>

# Parallel Vector Sum Benchmark
C++ benchmark comparing sequential execution, OpenMP, and Intel TBB for summing a vector with 100 million elements.

The project was built as a reproducible performance experiment: it runs multiple measurements, validates the computed result, stores raw execution times, calculates statistical metrics, generates charts and produces a technical report.

## Purpose
The goal is to compare three vector summation strategies under the same conditions:

- sequential execution with a simple `for` loop;
- parallel execution with OpenMP;
- parallel execution with Intel TBB.

Rather than measuring only a single execution, the benchmark performs 30 runs for each approach and analyzes the results using mean time, standard deviation, minimum, maximum and speedup.

## Results
The official execution used a vector with `100,000,000` elements and 30 runs per approach.

| Method | Runs | Mean time (s) | Standard deviation (s) | Min (s) | Max (s) | Speedup |
|---|---:|---:|---:|---:|---:|---:|
| Sequential | 30 | 0.042079 | 0.005446 | 0.029392 | 0.054537 | 1.00x |
| OpenMP | 30 | 0.020261 | 0.006075 | 0.015218 | 0.034884 | 2.08x |
| Intel TBB | 30 | 0.022501 | 0.006314 | 0.015401 | 0.037220 | 1.87x |

In the tested environment, OpenMP achieved the best average execution time, followed closely by Intel TBB. Both parallel implementations reduced the average runtime compared to the sequential version.

## Performance comparison
![Execution time comparison](./results/comparison_times.png)

The benchmark was executed on a Linux virtual machine with 3 available CPUs. Since vector summation is a memory-intensive operation, the speedup is limited not only by the number of threads, but also by memory bandwidth, scheduling overhead and runtime coordination costs.

## Repository structure
    .
    ├── src/
    │   └── main.cpp
    ├── scripts/
    │   ├── analyze.py
    │   ├── build_report_docx.py
    │   └── run_linux.sh
    ├── docs/
    │   ├── relatorio_modelo.md
    │   └── relatorio_modelo.docx
    ├── results/
    │   ├── raw_times.csv
    │   ├── summary.csv
    │   ├── comparison_times.png
    │   ├── sequential_times.png
    │   ├── openmp_times.png
    │   ├── tbb_times.png
    │   ├── report.md
    │   ├── report.docx
    │   └── environment.txt
    ├── Makefile
    ├── requirements.txt
    └── README.md

## Main files
| Path | Description |
|---|---|
| `src/main.cpp` | C++ benchmark implementation with sequential, OpenMP and Intel TBB strategies. |
| `scripts/run_linux.sh` | Complete Linux/WSL execution flow. |
| `scripts/analyze.py` | Statistical analysis and chart generation. |
| `scripts/build_report_docx.py` | Word report generation from measured results. |
| `results/raw_times.csv` | Raw execution times from all runs. |
| `results/summary.csv` | Mean, standard deviation, min, max and speedup. |
| `results/environment.txt` | Execution environment metadata. |
| `results/report.docx` | Final technical report. |

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

| File | Description |
|---|---|
| `raw_times.csv` | Raw execution measurements. |
| `summary.csv` | Mean, standard deviation, min, max and speedup. |
| `comparison_times.png` | Comparison chart for all approaches. |
| `sequential_times.png` | Sequential execution chart. |
| `openmp_times.png` | OpenMP execution chart. |
| `tbb_times.png` | Intel TBB execution chart. |
| `report.md` | Technical report draft. |
| `report.docx` | Final Word report. |
| `environment.txt` | Execution environment metadata. |

## Technical report
The final report is available in:

- [`results/report.docx`](./results/report.docx)
- [`results/report.md`](./results/report.md)

The report includes the problem description, methodology, statistical results, charts, discussion and conclusion.

## Methodology notes
The program performs a warm-up pass before collecting measurements. This warm-up is not recorded in the output file and helps reduce first-run noise such as runtime initialization and initial loading effects.

Each measured execution validates the computed sum against the expected result before recording the elapsed time. This prevents invalid measurements from being included in the analysis.

The comparison should be based on mean time and standard deviation, not only on the fastest execution. Since vector summation is a simple memory-intensive operation, parallel speedup can be limited by memory bandwidth, scheduling overhead and the number of available CPU cores.

## Cleaning generated files
    make clean

---

<a id="portuguese"></a>

<p align="right">
  <kbd><a href="#english">English</a></kbd>
  <kbd><a href="#portuguese">Português</a></kbd>
</p>

# Benchmark de Soma de Vetor
Benchmark em C++ comparando execução sequencial, OpenMP e Intel TBB na soma de um vetor com 100 milhões de elementos.

O projeto foi estruturado como um experimento de desempenho reprodutível: executa múltiplas medições, valida o resultado calculado, grava os tempos brutos, calcula métricas estatísticas, gera gráficos e produz um relatório técnico.

## Objetivo
O objetivo é comparar três estratégias de soma de vetor sob as mesmas condições:

- execução sequencial com `for` simples;
- execução paralela com OpenMP;
- execução paralela com Intel TBB.

Em vez de medir apenas uma execução isolada, o benchmark realiza 30 execuções por abordagem e analisa os resultados com média, desvio padrão, mínimo, máximo e speedup.

## Resultados
A execução oficial utilizou um vetor com `100.000.000` elementos e 30 execuções por abordagem.

| Método | Execuções | Média (s) | Desvio padrão (s) | Mínimo (s) | Máximo (s) | Speedup |
|---|---:|---:|---:|---:|---:|---:|
| Sequencial | 30 | 0.042079 | 0.005446 | 0.029392 | 0.054537 | 1.00x |
| OpenMP | 30 | 0.020261 | 0.006075 | 0.015218 | 0.034884 | 2.08x |
| Intel TBB | 30 | 0.022501 | 0.006314 | 0.015401 | 0.037220 | 1.87x |

No ambiente testado, OpenMP obteve o melhor tempo médio de execução, seguido de perto pela Intel TBB. As duas implementações paralelas reduziram o tempo médio em relação à versão sequencial.

## Comparação de desempenho
![Comparação dos tempos de execução](./results/comparison_times.png)

O benchmark foi executado em uma máquina virtual Linux com 3 CPUs disponíveis. Como a soma de vetor é uma operação intensiva em acesso à memória, o ganho de paralelização é limitado não apenas pela quantidade de threads, mas também pela largura de banda de memória, pelo overhead de escalonamento e pelo custo de coordenação das bibliotecas paralelas.

## Estrutura do repositório
    .
    ├── src/
    │   └── main.cpp
    ├── scripts/
    │   ├── analyze.py
    │   ├── build_report_docx.py
    │   └── run_linux.sh
    ├── docs/
    │   ├── relatorio_modelo.md
    │   └── relatorio_modelo.docx
    ├── results/
    │   ├── raw_times.csv
    │   ├── summary.csv
    │   ├── comparison_times.png
    │   ├── sequential_times.png
    │   ├── openmp_times.png
    │   ├── tbb_times.png
    │   ├── report.md
    │   ├── report.docx
    │   └── environment.txt
    ├── Makefile
    ├── requirements.txt
    └── README.md

## Arquivos principais
| Caminho | Descrição |
|---|---|
| `src/main.cpp` | Implementação do benchmark em C++ com estratégias sequencial, OpenMP e Intel TBB. |
| `scripts/run_linux.sh` | Fluxo completo de execução no Linux/WSL. |
| `scripts/analyze.py` | Análise estatística e geração de gráficos. |
| `scripts/build_report_docx.py` | Geração do relatório em Word a partir dos resultados medidos. |
| `results/raw_times.csv` | Tempos brutos de todas as execuções. |
| `results/summary.csv` | Média, desvio padrão, mínimo, máximo e speedup. |
| `results/environment.txt` | Metadados do ambiente de execução. |
| `results/report.docx` | Relatório técnico final. |

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

| Arquivo | Descrição |
|---|---|
| `raw_times.csv` | Medições brutas das execuções. |
| `summary.csv` | Média, desvio padrão, mínimo, máximo e speedup. |
| `comparison_times.png` | Gráfico comparando todas as abordagens. |
| `sequential_times.png` | Gráfico da execução sequencial. |
| `openmp_times.png` | Gráfico da execução com OpenMP. |
| `tbb_times.png` | Gráfico da execução com Intel TBB. |
| `report.md` | Rascunho do relatório técnico. |
| `report.docx` | Relatório final em Word. |
| `environment.txt` | Metadados do ambiente de execução. |

## Relatório técnico
O relatório final está disponível em:

- [`results/report.docx`](./results/report.docx)
- [`results/report.md`](./results/report.md)

O relatório inclui a descrição do problema, metodologia, resultados estatísticos, gráficos, discussão e conclusão.

## Observações de metodologia
O programa realiza uma passagem de aquecimento antes da coleta das medições. Esse aquecimento não é registrado no arquivo de saída e ajuda a reduzir ruídos de primeira execução, como inicialização de runtime e efeitos iniciais de carregamento.

Cada execução medida valida a soma calculada contra o resultado esperado antes de registrar o tempo. Isso evita que medições inválidas entrem na análise.

A comparação deve ser feita com base na média e no desvio padrão, não apenas no menor tempo. Como a soma de vetor é uma operação simples e intensiva em leitura de memória, o ganho de paralelização pode ser limitado pela largura de banda de memória, pelo overhead de escalonamento e pela quantidade de núcleos disponíveis.

## Limpeza dos arquivos gerados
    make clean
