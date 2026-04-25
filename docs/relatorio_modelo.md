# Relatório — Soma de vetor com C++, OpenMP e TBB

## 1. Introdução
Este relatório apresenta uma comparação de desempenho entre três abordagens para somar os elementos de um vetor grande em C++: implementação sequencial, paralelização com OpenMP e paralelização com Intel TBB. O objetivo do experimento é medir o impacto da paralelização em uma operação simples, repetitiva e intensiva em acesso à memória.

## 2. Metodologia
O experimento utiliza um vetor com 100 milhões de elementos inteiros, inicializados com o valor 1. Cada abordagem é executada 30 vezes. Em todas as execuções, o resultado da soma é validado antes do registro do tempo, evitando considerar medições de uma execução incorreta.

A medição é realizada dentro do programa C++ usando `std::chrono::steady_clock`, registrando apenas o trecho da soma. Os resultados são salvos em um arquivo CSV com método, número da execução, tempo em segundos, soma calculada, tamanho do vetor e quantidade de threads reportada.

A versão sequencial utiliza um laço `for` simples. A versão OpenMP utiliza `#pragma omp parallel for reduction(+:sum)`. A versão TBB utiliza `tbb::parallel_reduce`, dividindo o intervalo do vetor em blocos processados em paralelo.

## 3. Resultados
Substituir esta seção pelos dados gerados em `results/summary.csv` após executar:

```bash
./scripts/run_linux.sh
```

Inserir também os gráficos gerados em:

- `results/comparison_times.png`
- `results/sequential_times.png`
- `results/openmp_times.png`
- `results/tbb_times.png`

## 4. Discussão
A versão sequencial serve como base de comparação. As versões paralelas tendem a reduzir o tempo de execução ao dividir o trabalho entre múltiplas threads, mas o ganho não cresce indefinidamente. Como a soma de um vetor grande depende fortemente da leitura de memória, o desempenho pode ser limitado pela largura de banda de memória e não apenas pela quantidade de núcleos disponíveis.

OpenMP costuma ser direto para paralelizar laços simples, enquanto TBB oferece uma estratégia mais flexível de divisão de trabalho. A comparação entre os dois depende da máquina utilizada, do número de threads, do escalonamento e da carga do sistema durante as medições.

## 5. Conclusão
O experimento permite observar, de forma prática, o impacto da paralelização em C++. A comparação entre média, desvio padrão e gráficos das 30 execuções oferece uma visão mais confiável do comportamento de cada abordagem do que uma única execução isolada.
