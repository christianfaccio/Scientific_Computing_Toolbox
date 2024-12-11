#ifndef ANALYSISINTERPOLATION_HPP
#define ANALYSISINTERPOLATION_HPP

#include "utilities_interpolation.hpp"

#include <vector>
#include <functional>
#include <set>

namespace ScientificToolbox::Interpolation {
    class AnalysisInterpolation {
    public:
        AnalysisInterpolation(std::set<point<double>> points, std::function<double(double)> generator_function, std::vector<double> random_x);
        ~AnalysisInterpolation();

        void AccuracyAnalysis();
        void EfficiencyAnalysis();
        void OrderConvergenceAnalysis();

    private:
        std::set<point<double>> points;
        std::function<double(double)> generator_function;
        std::vector<double> random_x;

        double mae(std::vector<double> y_true, std::vector<double> y_pred);
    };
}

#endif
