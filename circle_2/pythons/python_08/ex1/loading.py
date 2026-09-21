import importlib
import sys


def check_dependency(name):
    try:
        module = importlib.import_module(name)
        version = getattr(module, "__version__", "unknown")

        if name == 'pandas':
            description = "Data manipulation ready"
        elif name == 'numpy':
            description = "Numerical computation ready"
        elif name == 'matplotlib':
            description = "Visualization ready"
        else:
            description = "Ready"

        print(f"[OK] {name} ({version}) - {description}")
        return True
    except ImportError:
        print(f"[MISSING] {name}")
        return False


def check_dependencies():

    print("LOADING STATUS: Loading programs...\n")
    print("Checking dependencies:")

    packages = ["pandas", "numpy", "matplotlib"]
    missing = []

    for pkg in packages:
        if not check_dependency(pkg):
            missing.append(pkg)

    return missing


def analyze_data():
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    print("\nAnalyzing Matrix data...")

    # create sample data
    data = np.random.randint(1, 10, 100)

    df = pd.DataFrame({"threat_level": data})

    print("Processing 1000 data points...")
    print("Generating visualization...\n")
    # create simple visualization
    plt.hist(df["threat_level"], bins=10)
    plt.title("Matrix Threat Level Distribution")
    plt.xlabel("Threat Level")
    plt.ylabel("Frequency")

    plt.savefig("matrix_analysis.png")
    plt.close()

    print("Analysis complete!")
    print("Visualization saved to: matrix_analysis.png")


def main():
    missing = check_dependencies()

    if missing:
        print("\nMissing dependencies.")
        print("Install them with:")
        print("pip install -r requirements.txt")
        print("or")
        print("poetry install")
        sys.exit(1)

    analyze_data()


if __name__ == "__main__":
    main()
