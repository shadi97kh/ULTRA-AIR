import os
import matplotlib.pyplot as plt

def read_all_uncertainty_files(directory):
    confidences = []
    uncertainties = []
    class_names = []
    files_found = False  

    for filename in os.listdir(directory):
        if filename.endswith("_uncertainties.txt"):
            files_found = True
            file_path = os.path.join(directory, filename)
            print(f"Processing file: {file_path}") 
            with open(file_path, 'r') as f:
                for line in f:
                    try:
                        # Expected format: <Class Name>: Confidence <Value>, Uncertainty <Value>
                        class_part, values_part = line.strip().split(':')
                        class_name = class_part.strip()

                        # Split by ',' to separate confidence and uncertainty
                        confidence_part, uncertainty_part = values_part.split(',')

                        # Extract numeric values
                        confidence = float(confidence_part.split()[1])
                        uncertainty = float(uncertainty_part.split()[1])

                        class_names.append(class_name)
                        confidences.append(confidence)
                        uncertainties.append(uncertainty)
                    except Exception as e:
                        print(f"Error parsing line: {line}")
                        print(e)
                        continue

    if not files_found:
        print("No _uncertainties.txt files found in the directory.")

    return class_names, confidences, uncertainties

def plot_confidence_and_uncertainty(confidences, uncertainties, save_path, threshold=None):
    plt.figure(figsize=(10, 5))
    plt.scatter(confidences, uncertainties, c='blue', label='Uncertainty')
    plt.xlabel('Confidence')
    plt.ylabel('Uncertainty')
    plt.title('Confidence vs Uncertainty')
    plt.grid(True)

    if threshold is not None:
        plt.axhline(y=threshold, color='red', linestyle='--', label=f'Threshold {threshold}')
        plt.legend()

    plt.savefig(save_path)
    plt.close()

def save_uncertainties(class_names, confidences, uncertainties, save_path):
    with open(save_path, 'w') as f:
        for class_name, confidence, uncertainty in zip(class_names, confidences, uncertainties):
            f.write(f"{class_name}: Confidence {confidence:.2f}, Uncertainty {uncertainty:.2f}\n")
    print(f"Uncertainty data saved to {save_path}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Plot Confidence vs Uncertainty')
    parser.add_argument('--dir', type=str, required=True, help='Directory containing uncertainty files')
    parser.add_argument('--threshold', type=float, default=None, help='Uncertainty threshold to highlight in plot')
    args = parser.parse_args()

    class_names, confidences, uncertainties = read_all_uncertainty_files(args.dir)
    if not confidences or not uncertainties:
        print("No valid uncertainty data found.")
    else:
        plot_confidence_and_uncertainty(confidences, uncertainties, os.path.join(args.dir, "confidence_uncertainty.png"), args.threshold)
        save_uncertainties(class_names, confidences, uncertainties, os.path.join(args.dir, "combined_uncertainties.txt"))
        print(f"Plot saved to {os.path.join(args.dir, 'confidence_uncertainty.png')}")
