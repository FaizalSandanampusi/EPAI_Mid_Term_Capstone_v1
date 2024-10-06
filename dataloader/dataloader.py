# dataloader/dataloader.py

import os
import numpy as np
from collections import namedtuple
from contextlib import contextmanager
from functools import lru_cache
from urllib.parse import urlparse
from .preprocessors import default_preprocess
from .utils import download_file, timer

DataSample = namedtuple('DataSample', ['features', 'label'])

class DataLoader:
    def __init__(self, dataset_name='MNIST', batch_size=32, shuffle=True, url=None, **kwargs):
        self.dataset_name = dataset_name
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.url = url
        self.kwargs = kwargs
        self.data = []
        self.index = 0
        self.load_data()
    
    @timer
    def load_data(self):
        if self.url:
            self.download_from_url()
        elif not os.path.exists(f'datasets/{self.dataset_name}'):
            self.download_dataset()
        self.data = self.preprocess_data(self.read_data())
    
    @timer
    def download_dataset(self):
        print(f"Downloading {self.dataset_name} dataset...")
        url = self.get_dataset_url()
        download_file(url, f'datasets/{self.dataset_name}')
    
    @timer
    def download_from_url(self):
        print(f"Downloading dataset from {self.url}...")
        file_extension = self.get_file_extension(self.url)
        download_path = f'datasets/{self.dataset_name}{file_extension}'
        download_file(self.url, download_path)
        self.dataset_name = download_path.split('/')[-1]
    
    def get_file_extension(self, url):
        parsed_url = urlparse(url)
        path = parsed_url.path
        return os.path.splitext(path)[1]
    
    def get_dataset_url(self):
        urls = {
            'MNIST': 'http://yann.lecun.com/exdb/mnist/',
            'CIFAR-10': 'https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz',
            'CIFAR-100': 'https://www.cs.toronto.edu/~kriz/cifar-100-python.tar.gz'
        }
        return urls.get(self.dataset_name, '')
    
    def read_data(self):
        file_extension = os.path.splitext(self.dataset_name)[1]
        if file_extension in ['.jpg', '.png', '.gif']:
            return self.read_image_dataset()
        elif file_extension == '.csv':
            return self.read_csv_dataset()
        elif file_extension == '.txt':
            return self.read_text_dataset()
        elif self.dataset_name in ['MNIST', 'CIFAR-10', 'CIFAR-100']:
            return self.read_image_dataset()
        else:
            return self.read_unstructured_dataset()
    
    def read_image_dataset(self):
        # Placeholder implementation
        return [DataSample(np.random.rand(32, 32, 3), np.random.randint(10)) for _ in range(1000)]
    
    def read_csv_dataset(self):
        import csv
        data = []
        try:
            with open(f'datasets/{self.dataset_name}', 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    features = [float(x) for x in row[:-1]]
                    label = int(row[-1])
                    data.append(DataSample(features, label))
        except FileNotFoundError:
            print(f"Error: Dataset file '{self.dataset_name}' not found.")
        except csv.Error as e:
            print(f"Error reading CSV file: {e}")
        return data
    
    def read_text_dataset(self):
        data = []
        try:
            with open(f'datasets/{self.dataset_name}', 'r', encoding='utf-8') as f:
                for line in f:
                    # Assuming each line is a separate text sample
                    # and the last word is the label
                    words = line.strip().split()
                    if len(words) > 1:
                        text = ' '.join(words[:-1])
                        label = words[-1]
                        data.append(DataSample(text, label))
        except FileNotFoundError:
            print(f"Error: Dataset file '{self.dataset_name}' not found.")
        except Exception as e:
            print(f"Error reading text file: {e}")
        return data
    
    def read_unstructured_dataset(self):
        data = []
        for root, _, files in os.walk(f'datasets/{self.dataset_name}'):
            for file in files:
                with open(os.path.join(root, file), 'r') as f:
                    content = f.read()
                    data.append(DataSample(content, os.path.basename(root)))
        return data
    
    def preprocess_data(self, data):
        preprocess_func = self.kwargs.get('preprocess_func', default_preprocess)
        return [preprocess_func(sample) for sample in data]
    
    def __iter__(self):
        self.index = 0
        if self.shuffle:
            import random
            random.shuffle(self.data)
        return self
    
    def __next__(self):
        if self.index < len(self.data):
            batch = self.data[self.index:self.index + self.batch_size]
            self.index += self.batch_size
            return batch
        else:
            raise StopIteration

    @contextmanager
    def temporary_data_augmentation(self, augmentation_func):
        original_preprocess = self.kwargs.get('preprocess_func', default_preprocess)
        self.kwargs['preprocess_func'] = lambda x: augmentation_func(original_preprocess(x))
        yield
        self.kwargs['preprocess_func'] = original_preprocess

    @lru_cache(maxsize=32)
    def get_sample(self, index):
        return self.data[index]

    def apply_transformation(self, transformation_func):
        self.data = list(map(transformation_func, self.data))

    def filter_data(self, condition_func):
        self.data = list(filter(condition_func, self.data))

    def get_data_generator(self):
        for sample in self.data:
            yield sample

    @classmethod
    def from_command_line(cls):
        import argparse
        parser = argparse.ArgumentParser(description='DataLoader')
        parser.add_argument('dataset', type=str, help='Dataset name or URL')
        parser.add_argument('--batch_size', type=int, default=32, help='Batch size')
        parser.add_argument('--url', type=str, help='URL to download dataset')
        args = parser.parse_args()
        return cls(dataset_name=args.dataset, batch_size=args.batch_size, url=args.url)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

    def __repr__(self):
        return f"DataLoader(dataset={self.dataset_name}, batch_size={self.batch_size}, shuffle={self.shuffle})"

if __name__ == '__main__':
    loader = DataLoader.from_command_line()
    print(f"Loaded {len(loader)} samples from {loader.dataset_name}")