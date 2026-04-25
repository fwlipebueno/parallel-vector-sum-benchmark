#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <memory>
#include <numeric>
#include <stdexcept>
#include <string>
#include <thread>
#include <vector>

#ifdef _OPENMP
#include <omp.h>
#endif

#include <tbb/blocked_range.h>
#include <tbb/global_control.h>
#include <tbb/parallel_reduce.h>

namespace {

using Sum = std::int64_t;
using Clock = std::chrono::steady_clock;

struct Config {
    std::size_t size = 100000000;
    int runs = 30;
    int threads = 0;
    bool warmup = true;
    std::string output = "results/raw_times.csv";
};

enum class Method {
    Sequential,
    OpenMP,
    TBB
};

struct Measurement {
    double seconds;
    Sum sum;
};

std::string methodName(Method method) {
    switch (method) {
        case Method::Sequential: return "sequential";
        case Method::OpenMP: return "openmp";
        case Method::TBB: return "tbb";
    }
    throw std::logic_error("Invalid method");
}

std::size_t parseSize(const std::string& value) {
    std::size_t parsed = 0;
    std::size_t read = 0;
    parsed = std::stoull(value, &read);
    if (read != value.size() || parsed == 0) {
        throw std::invalid_argument("Invalid positive integer: " + value);
    }
    return parsed;
}

int parseInt(const std::string& value, const std::string& name) {
    std::size_t read = 0;
    int parsed = std::stoi(value, &read);
    if (read != value.size() || parsed <= 0) {
        throw std::invalid_argument(name + " must be a positive integer: " + value);
    }
    return parsed;
}

void printUsage(const char* program) {
    std::cout
        << "Usage: " << program << " [options]\n\n"
        << "Options:\n"
        << "  --size N          Vector size. Default: 100000000\n"
        << "  --runs N          Number of measured runs per method. Default: 30\n"
        << "  --threads N       Max worker threads for OpenMP and TBB. Default: runtime default\n"
        << "  --output FILE     CSV output path. Default: results/raw_times.csv\n"
        << "  --no-warmup       Disable the initial unmeasured warm-up pass\n"
        << "  --help            Show this message\n";
}

Config parseArgs(int argc, char** argv) {
    Config config;

    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];

        auto nextValue = [&](const std::string& option) -> std::string {
            if (i + 1 >= argc) {
                throw std::invalid_argument("Missing value for " + option);
            }
            return argv[++i];
        };

        if (arg == "--size") {
            config.size = parseSize(nextValue(arg));
        } else if (arg == "--runs") {
            config.runs = parseInt(nextValue(arg), "runs");
        } else if (arg == "--threads") {
            config.threads = parseInt(nextValue(arg), "threads");
        } else if (arg == "--output") {
            config.output = nextValue(arg);
        } else if (arg == "--no-warmup") {
            config.warmup = false;
        } else if (arg == "--help") {
            printUsage(argv[0]);
            std::exit(EXIT_SUCCESS);
        } else {
            throw std::invalid_argument("Unknown option: " + arg);
        }
    }

    return config;
}

std::vector<int> makeVector(std::size_t size) {
    return std::vector<int>(size, 1);
}

Sum sequentialSum(const std::vector<int>& values) {
    Sum sum = 0;
    for (std::size_t i = 0; i < values.size(); ++i) {
        sum += values[i];
    }
    return sum;
}

Sum openmpSum(const std::vector<int>& values) {
#ifndef _OPENMP
    throw std::runtime_error("OpenMP is not available. Rebuild with -fopenmp.");
#else
    Sum sum = 0;
    const auto size = static_cast<std::int64_t>(values.size());

#pragma omp parallel for reduction(+:sum) schedule(static)
    for (std::int64_t i = 0; i < size; ++i) {
        sum += values[static_cast<std::size_t>(i)];
    }

    return sum;
#endif
}

Sum tbbSum(const std::vector<int>& values) {
    return tbb::parallel_reduce(
        tbb::blocked_range<std::size_t>(0, values.size()),
        Sum{0},
        [&](const tbb::blocked_range<std::size_t>& range, Sum partial) {
            for (std::size_t i = range.begin(); i != range.end(); ++i) {
                partial += values[i];
            }
            return partial;
        },
        std::plus<Sum>{}
    );
}

Sum run(Method method, const std::vector<int>& values) {
    switch (method) {
        case Method::Sequential: return sequentialSum(values);
        case Method::OpenMP: return openmpSum(values);
        case Method::TBB: return tbbSum(values);
    }
    throw std::logic_error("Invalid method");
}

Measurement measure(Method method, const std::vector<int>& values) {
    const auto start = Clock::now();
    const Sum sum = run(method, values);
    const auto finish = Clock::now();
    const std::chrono::duration<double> elapsed = finish - start;
    return {elapsed.count(), sum};
}

void ensureParentDirectory(const std::string& filePath) {
    const std::filesystem::path path(filePath);
    const std::filesystem::path parent = path.parent_path();
    if (!parent.empty()) {
        std::filesystem::create_directories(parent);
    }
}

int reportedThreads(const Config& config) {
    if (config.threads > 0) {
        return config.threads;
    }

    const unsigned int detected = std::thread::hardware_concurrency();
    return detected == 0 ? -1 : static_cast<int>(detected);
}

}  // namespace

int main(int argc, char** argv) {
    try {
        const Config config = parseArgs(argc, argv);

#ifdef _OPENMP
        if (config.threads > 0) {
            omp_set_num_threads(config.threads);
        }
#endif

        std::unique_ptr<tbb::global_control> tbbThreads;
        if (config.threads > 0) {
            tbbThreads = std::make_unique<tbb::global_control>(
                tbb::global_control::max_allowed_parallelism,
                static_cast<std::size_t>(config.threads)
            );
        }

        const std::array<Method, 3> methods = {
            Method::Sequential,
            Method::OpenMP,
            Method::TBB
        };

        std::cout << "Allocating vector with " << config.size << " elements...\n";
        const std::vector<int> values = makeVector(config.size);
        const Sum expected = static_cast<Sum>(config.size);

        if (config.warmup) {
            std::cout << "Running warm-up pass...\n";
            for (const Method method : methods) {
                const Sum sum = run(method, values);
                if (sum != expected) {
                    throw std::runtime_error("Invalid warm-up sum for " + methodName(method));
                }
            }
        }

        ensureParentDirectory(config.output);
        std::ofstream csv(config.output);
        if (!csv) {
            throw std::runtime_error("Could not open output file: " + config.output);
        }

        csv << "method,run,seconds,sum,vector_size,threads\n";
        csv << std::fixed << std::setprecision(9);

        std::cout << "Writing measurements to " << config.output << "\n";
        std::cout << std::fixed << std::setprecision(6);

        for (int runNumber = 1; runNumber <= config.runs; ++runNumber) {
            for (const Method method : methods) {
                const Measurement measurement = measure(method, values);

                if (measurement.sum != expected) {
                    throw std::runtime_error("Invalid sum for " + methodName(method));
                }

                csv << methodName(method) << ','
                    << runNumber << ','
                    << measurement.seconds << ','
                    << measurement.sum << ','
                    << config.size << ','
                    << reportedThreads(config) << '\n';

                std::cout << "run=" << std::setw(2) << runNumber
                          << " method=" << std::setw(10) << methodName(method)
                          << " seconds=" << measurement.seconds << '\n';
            }
        }

        std::cout << "Done.\n";
        return EXIT_SUCCESS;
    } catch (const std::exception& error) {
        std::cerr << "Error: " << error.what() << '\n';
        return EXIT_FAILURE;
    }
}
