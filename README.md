# Quick Data Profiling Tool

<img src="logo.png" alt="Logo" width="200"/>

A comprehensive tool for quick data profiling and exploratory data analysis, generating interactive HTML reports.

## Features

- Generates an HTML report with:
  - Data head and data types
  - Missing values analysis and heatmap
  - Statistical summaries of numerical columns
  - Distributions of numerical and categorical variables
  - Correlation matrix

## Installation

Install directly from GitHub:

```bash
pip install git+https://github.com/mwill5/quick_data_profiling.git
```

## Usage

After installation, run the tool using the following command:

```bash
quickprof your_data_file.csv
```

Replace your_data_file.csv with the path to your dataset.

Example:

```bash
quickprof data.csv
```

An report.html file will be generated in your current directory.

## Example

To see an example of the generated report, check out [example_report.html](example_report.html).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Myles Williams
