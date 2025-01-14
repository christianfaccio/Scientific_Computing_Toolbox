import os
import csv
import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import scientific_toolbox.stats as stats

class StatisticsAnalyzer:
    def __init__(self, data_dir=f'{ROOT_DIR}/data/', output_dir=f'{ROOT_DIR}/output/'):
        self.data_dir = data_dir
        self.output_dir = output_dir
        self.dataset = None
        self.analyzer = None
        self.numeric_columns = []
        self.output_file = None
        
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        timestamp = datetime.datetime.now().strftime("%Y%m%d")
        self.output_file = os.path.join(output_dir, f'statistics_report_{timestamp}.txt')

    def write_to_file(self, text):
        with open(self.output_file, 'a') as f:
            f.write(text + '\n')
        print(text)


    def _read_csv_to_dataset(self, file_path):
        dataset = stats.Dataset()
        with open(file_path, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                parsed_row = {k: float(v) if v.replace('.','',1).isdigit() else v 
                            for k, v in row.items()}
                dataset.addRow(parsed_row)
        return dataset


    def _identify_numeric_columns(self):
        self.numeric_columns = [col for col in self.dataset.getColumnNames() 
                              if self.dataset.isNumeric(col)]
        self.write_to_file(f"\nNumeric columns found: {self.numeric_columns}")

    def get_data(self):
        data_file = input("Enter the name of the csv data file: ")
        data_path = os.path.join(self.data_dir, data_file) if data_file else os.path.join(self.data_dir, 'Food_and_Nutrition__.csv')
        
        if not data_file:
            self.write_to_file("No path entered, using default Food_and_Nutrition__.csv")
        
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"File '{data_path}' not found.")
            
        self.dataset = self._read_csv_to_dataset(data_path)
        self.analyzer = stats.StatisticalAnalyzer(self.dataset)
        self._identify_numeric_columns()

    

    




    def choose_analysis(self):
        self.write_to_file("\nAvailable analyses:")
        self.write_to_file("1. Basic statistics (mean, median, variance, std dev)")
        self.write_to_file("2. Frequency count")
        self.write_to_file("3. Correlation analysis")
        self.write_to_file("4. All of the above")
        
        choice = input("Choose analysis type (1-4): ")
        if not choice:
            choice = "4"
            self.write_to_file("No choice entered, performing all analyses")
        
        return int(choice)

    def basic_statistics(self, columns=None):
        columns = columns or self.numeric_columns
        self.write_to_file("\nBasic statistics:")
        for col in columns:
            self.write_to_file(f"\nColumn: {col}")
            self.write_to_file(f"  Mean: {self.analyzer.mean(col):.4f}")
            self.write_to_file(f"  Median: {self.analyzer.median(col):.4f}")
            self.write_to_file(f"  Variance: {self.analyzer.variance(col):.4f}")
            self.write_to_file(f"  Std Dev: {self.analyzer.standardDeviation(col):.4f}")

    def frequency_analysis(self, columns=None):
        columns = columns or self.dataset.getColumnNames()
        self.write_to_file("\nFrequency analysis:")
        for col in columns:
            self.write_to_file(f"\nColumn: {col}")
            if self.dataset.isNumeric(col):
                self.write_to_file(f"  Frequency count: {self.analyzer.frequencyCount(col)}")
            else:
                self.write_to_file(f"  Frequency count: {self.analyzer.frequencyCountStr(col)}")

    def correlation_analysis(self):
        if len(self.numeric_columns) > 1:
            self.write_to_file("\nCorrelation matrix:")
            corr_matrix = self.analyzer.correlationMatrix(self.numeric_columns)
            self.write_to_file(str(corr_matrix))
            
            threshold = 0.7
            self.write_to_file(f"\nStrong correlations (|corr| > {threshold}):")
            strong_corrs = self.analyzer.reportStrongCorrelations(self.numeric_columns, threshold)
            self.write_to_file(strong_corrs)
        else:
            self.write_to_file("\nInsufficient numeric columns for correlation analysis.")

    def run(self):
        self.write_to_file("Starting statistical analysis...")
        self.get_data()
        choice = self.choose_analysis()
        
        if choice in [1, 4]:
            self.basic_statistics()
        if choice in [2, 4]:
            self.frequency_analysis()
        if choice in [3, 4]:
            self.correlation_analysis()
            
        

if __name__ == "__main__":
    analyzer = StatisticsAnalyzer()
    analyzer.run()