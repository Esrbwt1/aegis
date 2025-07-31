# data_analyzer.py
# A simple script to simulate a scientific data analysis task.

import numpy as np

INPUT_FILE = "input_data.txt"
OUTPUT_FILE = "analysis_results.txt"

def analyze():
    try:
        # Load data from the input file
        data = np.loadtxt(INPUT_FILE)
        
        # Perform calculations
        mean = np.mean(data)
        std_dev = np.std(data)
        
        # Save results to the output file
        with open(OUTPUT_FILE, 'w') as f:
            f.write("--- Aegis Scientific Analysis Report ---\n")
            f.write(f"Source Data File: {INPUT_FILE}\n")
            f.write(f"Mean: {mean:.4f}\n")
            f.write(f"Standard Deviation: {std_dev:.4f}\n")
        
        print(f"Analysis complete. Results saved to {OUTPUT_FILE}")
        
    except Exception as e:
        print(f"An error occurred during analysis: {e}")

if __name__ == "__main__":
    analyze()