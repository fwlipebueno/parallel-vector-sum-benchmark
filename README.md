# Vector Sum Benchmark — C++ / OpenMP / Intel TBB
Benchmark para comparar três abordagens de soma de um vetor grande em C++:

- sequencial, com `for` simples;
- paralela com OpenMP;
- paralela com Intel TBB.

O projeto executa 30 medições por abordagem, valida o resultado da soma, grava os tempos em CSV e gera média, desvio padrão e gráficos para o relatório técnico.

## Por que este repositório existe
A proposta não é apenas “usar threads”. O objetivo é deixar o experimento reprodutível: mesmo tamanho de entrada, mesma validação de resultado, mesma estrutura de saída e análise separada da execução. Isso torna a comparação mais honesta e facilita revisar os dados depois.

## Estrutura
```text
.
├── src/main.cpp              # benchmark em C++
├── scripts/analyze.py        # cálculo estatístico e geração dos gráficos
├── scripts/run_linux.sh      # execução completa no Linux/WSL
├── docs/relatorio_modelo.md  # modelo base do relatório técnico
├── Makefile
└── requirements.txt
```

## Requisitos
Linux ou WSL com:

```bash
sudo apt-get update
sudo apt-get install -y g++ libtbb-dev python3 python3-pip
pip3 install -r requirements.txt
```

OpenMP é habilitado pelo `g++` com a flag `-fopenmp`. A Intel TBB é fornecida pelo pacote `libtbb-dev`.

## Execução recomendada
```bash
./scripts/run_linux.sh
```

Por padrão, o script usa:

- vetor com `100000000` elementos;
- `30` execuções por abordagem;
- número de threads padrão definido pelo runtime.

Também é possível informar tamanho, número de execuções e threads:

```bash
./scripts/run_linux.sh 100000000 30 8
```

## Execução manual
```bash
make check-env
make all
./build/vector_sum_benchmark --size 100000000 --runs 30 --output results/raw_times.csv
python3 scripts/analyze.py results/raw_times.csv --out results
python3 scripts/build_report_docx.py --summary results/summary.csv --results results --out results/report.docx
```

## Saídas geradas
Após a execução, os arquivos principais ficam em `results/`:

```text
raw_times.csv          # dados brutos das execuções
summary.csv            # média, desvio padrão, mínimo, máximo e speedup
comparison_times.png   # comparação das três abordagens
sequential_times.png   # gráfico da abordagem sequencial
openmp_times.png       # gráfico da abordagem OpenMP
tbb_times.png          # gráfico da abordagem TBB
report.md              # rascunho do relatório preenchido com os dados reais
report.docx            # relatório em Word, gerado opcionalmente
```

## Observações de metodologia
O programa realiza uma passagem de aquecimento antes das medições, sem gravar esse tempo. A ideia é reduzir ruídos de primeira execução, como inicialização de runtime e efeitos de carregamento. Em todas as medições, a soma é validada contra o resultado esperado antes de registrar o tempo.

A comparação deve ser feita com base na média e no desvio padrão, não apenas no menor tempo. Como a soma de vetor é uma operação simples e fortemente dependente de leitura de memória, o ganho de paralelização pode ser limitado pela largura de banda de memória da máquina.

## Limpeza
```bash
make clean
```
