#include "../include/ODE_Module/ODETester.hpp"
#include "../include/Utilities.hpp"

#include <iostream>
#include <vector>
#include <algorithm>

using namespace ScientificToolbox;
using namespace ScientificToolbox::ODE;

int main() {
    ODETester tester;
    bool all_passed = true;

    // Test expression parser
    all_passed &= tester.run_parser_tests();
    
    // Test Forward Euler Solver
    all_passed &= tester.run_ode_tests();

    if (all_passed) {
        std::cout << std::endl << "All tests passed!" << std::endl;
    } else {
        std::cerr << std::endl << "Some tests failed!" << std::endl;
    }

    std::cout << std::endl << "------------ Analysis Section ------------" << std::endl;

    var_expr expr = "y";                // Dummy function
    double solution = std::exp(1);      // Dummy solution
    double t0 = 0;
    double tf = 1;
    double h = 0.01;
    double y0 = 1;

    for (auto solver_type : solver_types) {
        auto solver_ptr = factories[solver_type]("y", y0, t0, tf, h);
        auto [time, sol] = measure_execution_time<ODESolution>([&solver_ptr]() {
            return solver_ptr->solve();
        });
        double error = compute_error(sol.get_result(), solution);
        double order = compute_order_of_convergence(solver_type);
        
        std::cout << "Solver: " << solver_type << std::endl;
        std::cout << "  Error: \t\t\t" << error << std::endl;
        std::cout << "  Order of Convergence: \t" << order << std::endl;
        std::cout << "  Execution Time: \t\t" << time << " seconds" << std::endl;
    }

    return 0;
}