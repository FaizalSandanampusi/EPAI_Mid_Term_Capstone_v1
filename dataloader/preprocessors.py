import numpy as np
from collections import namedtuple
import random
import re

DataSample = namedtuple('DataSample', ['features', 'label'])

def default_preprocess(sample):
    return sample

def normalize(sample):
    if isinstance(sample, (int, float, np.number)):
        # If it's a single number, normalize it to [0, 1]
        return (sample - 0) / (255 - 0)
    elif isinstance(sample, DataSample):
        features, label = sample
        if isinstance(features, str):
            # For text data, we don't normalize
            return sample
        normalized_features = (features - np.min(features)) / (np.max(features) - np.min(features))
        return DataSample(normalized_features, label)
    else:
        raise TypeError("Input must be a number or a DataSample object")

def augment(sample):
    features, label = sample
    if isinstance(features, str):
        return augment_text(features, label)
    else:
        # Example augmentation: add random noise
        noise = np.random.normal(0, 0.1, features.shape)
        augmented_features = features + noise
    return DataSample(augmented_features, label)

def resize_image(sample, size=(32, 32)):
    from PIL import Image
    features, label = sample
    image = Image.fromarray(features.astype('uint8'))
    resized_image = image.resize(size)
    return DataSample(np.array(resized_image), label)

# Text augmentation functions
def augment_text(text, label):
    augmentation_functions = [
        synonym_replacement,
        random_insertion,
        random_deletion,
        random_swap
    ]
    augmented_text = random.choice(augmentation_functions)(text)
    return DataSample(augmented_text, label)

def synonym_replacement(text, n=1):
    # Placeholder: Replace with actual synonym replacement logic
    words = text.split()
    for _ in range(n):
        if words:
            index = random.randint(0, len(words) - 1)
            words[index] = words[index] + "_syn"
    return " ".join(words)

def random_insertion(text, n=1):
    words = text.split()
    for _ in range(n):
        if words:
            index = random.randint(0, len(words))
            words.insert(index, "NEW")
    return " ".join(words)

def random_deletion(text, p=0.1):
    words = text.split()
    return " ".join([word for word in words if random.random() > p])

def random_swap(text, n=1):
    words = text.split()
    for _ in range(n):
        if len(words) > 1:
            idx1, idx2 = random.sample(range(len(words)), 2)
            words[idx1], words[idx2] = words[idx2], words[idx1]
    return " ".join(words)