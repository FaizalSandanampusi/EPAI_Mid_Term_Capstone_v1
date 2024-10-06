![CI/CD](https://github.com/FaizalSandanampusi/EPAI_Mid_Term_Capstone/workflows/Python%20Tests/badge.svg)


# DataLoader Package

![CI/CD](https://github.com/yourusername/dataloader-package/workflows/Python%20Tests/badge.svg)

## Overview

The **DataLoader** package is a flexible and efficient data loading solution designed for various AI and machine learning projects. It supports loading, preprocessing, and managing different types of datasets, including:

- **Image Datasets**: MNIST, CIFAR-10, CIFAR-100
- **Text Datasets**
- **Structured Data**: CSV files
- **Unstructured Data**: Folders containing multiple files of various formats

## Features

- Download datasets from online sources if not present locally
- Handle different file formats and organize data appropriately
- Provide data in batches for efficient processing
- Support data augmentation and preprocessing steps
- Extensible to accommodate new data types and sources
- Implement various Python concepts such as decorators, context managers, and generators

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/dataloader-package.git
   cd dataloader-package
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

The `DataLoader` package is designed to be easy to use with minimal setup. Here’s an example of how to load and preprocess an image dataset like CIFAR-10:

```python
from dataloader import DataLoader

# Initialize DataLoader for the CIFAR-10 dataset
data_loader = DataLoader(dataset_name='CIFAR-10', batch_size=32)

# Iterate through data in batches
for batch in data_loader:
    # Process the batch (e.g., feed it to a neural network)
    print(batch)
```

### Custom Preprocessing and Augmentation

You can pass custom preprocessing functions to the `DataLoader` to modify the data as needed:

```python
from dataloader import DataLoader
from dataloader.preprocessors import normalize

# Initialize DataLoader with a custom preprocessing function
data_loader = DataLoader(dataset_name='CIFAR-10', preprocess_func=normalize, batch_size=32)
```

This allows you to incorporate any domain-specific preprocessing logic, such as data normalization, augmentation, or even more complex transformations.

## Project Structure

```
dataloader-package/
│
├── dataloader/
│   ├── __init__.py                 # Initialization file for the dataloader module
│   ├── dataloader.py               # Core DataLoader class definition
│   ├── preprocessors.py            # Preprocessing and augmentation functions
│   └── utils.py                    # Utility functions such as file downloading and timing decorators
│
├── datasets/                       # Contains downloaded and processed datasets
│   └── (Subfolders and files specific to each dataset)
│
├── tests/
│   └── test_dataloader.py          # Unit tests for DataLoader functionality
│
├── .github/
│   └── workflows/
│       └── python-tests.yml        # GitHub Actions CI/CD workflow for running tests
│
├── main.py                         # Example script to run the DataLoader
├── README.md                       # Project documentation
└── requirements.txt                # Project dependencies
```

## Running Tests

The project uses `pytest` for running unit tests. All test cases are located in the `tests/` folder, covering core functionalities of the `DataLoader`, preprocessing logic, and utilities.

To run the test suite, simply execute:

```bash
pytest tests/test_dataloader.py
```

If you're using GitHub Actions for CI/CD, you can check the status of the tests with the badge included at the top of this README.
