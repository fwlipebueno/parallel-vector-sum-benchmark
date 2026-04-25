CXX ?= g++
CXXFLAGS ?= -O3 -std=c++17 -march=native -Wall -Wextra -Wpedantic
OPENMP_FLAG ?= -fopenmp
LDFLAGS ?= -fopenmp -ltbb -pthread

TARGET := build/vector_sum_benchmark
SOURCE := src/main.cpp

.PHONY: all run analyze clean check-env

all: $(TARGET)

$(TARGET): $(SOURCE)
	mkdir -p build
	$(CXX) $(CXXFLAGS) $(OPENMP_FLAG) $(SOURCE) -o $(TARGET) $(LDFLAGS)

run: all
	mkdir -p results
	./$(TARGET) --size 100000000 --runs 30 --threads $$(nproc) --output results/raw_times.csv

analyze:
	python3 scripts/analyze.py results/raw_times.csv --out results

check-env:
	@$(CXX) --version | head -n 1
	@echo "Checking OpenMP..."
	@printf '#include <omp.h>\nint main(){return 0;}\n' | $(CXX) -x c++ - $(OPENMP_FLAG) -o /tmp/openmp_check >/dev/null 2>&1 && echo "OpenMP: ok" || echo "OpenMP: missing"
	@echo "Checking TBB..."
	@printf '#include <tbb/parallel_reduce.h>\nint main(){return 0;}\n' | $(CXX) -x c++ - -ltbb -o /tmp/tbb_check >/dev/null 2>&1 && echo "TBB: ok" || echo "TBB: missing"

clean:
	rm -rf build results/*.csv results/*.png results/*.md results/*.docx
