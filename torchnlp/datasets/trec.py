import os

from torchnlp.utils import download_urls
from torchnlp.datasets.dataset import Dataset


def trec_dataset(directory='data/trec/',
                 train=False,
                 test=False,
                 train_filename='train_5500.label',
                 test_filename='TREC_10.label',
                 check_file='train_5500.label',
                 urls=[
                     'http://cogcomp.org/Data/QA/QC/train_5500.label',
                     'http://cogcomp.org/Data/QA/QC/TREC_10.label'
                 ]):
    """
    Load the Text REtrieval Conference (TREC) Question Classification dataset.

    TREC dataset contains 5500 labeled questions in training set and another 500 for test set. The
    dataset has 6 labels, 50 level-2 labels. Average length of each sentence is 10, vocabulary size
    of 8700.

    More details:
    https://nlp.stanford.edu/courses/cs224n/2004/may-steinberg-project.pdf
    http://cogcomp.org/Data/QA/QC/
    http://www.aclweb.org/anthology/C02-1150 

    Citation:
    Xin Li, Dan Roth, Learning Question Classifiers. COLING'02, Aug., 2002.

    Args:
        directory (str, optional): Directory to cache the dataset.
        train (bool, optional): If to load the training split of the dataset.
        test (bool, optional): If to load the test split of the dataset.
        train_filename (str, optional): The filename of the training split.
        test_filename (str, optional): The filename of the test split.
        check_file (str, optional): Check this file exists if download was successful.
        urls (str, optional): URLs to download.

    Returns:
        :class:`tuple` of :class:`torchnlp.datasets.Dataset`: Tuple with the training tokens, dev
        tokens and test tokens in order if their respective boolean argument is true.

    Example:
        >>> from torchnlp.datasets import trec_dataset
        >>> train = trec_dataset(train=True)
        >>> train[:2] # Sentence at index 17 is shortish
        [{
          'label_fine': 'manner',
          'label': 'DESC',
          'text': 'How did serfdom develop in and then leave Russia ?'
        }, {
          'label_fine': 'cremat',
          'label': 'ENTY',
          'text': 'What films featured the character Popeye Doyle ?'
        }]
    """
    download_urls(directory=directory, file_urls=urls, check_file=check_file)

    ret = []
    splits = [(train, train_filename), (test, test_filename)]
    split_filenames = [dir_ for (requested, dir_) in splits if requested]
    for filename in split_filenames:
        full_path = os.path.join(directory, filename)
        examples = []
        for line in open(full_path, 'rb'):
            # there is one non-ASCII byte: sisterBADBYTEcity; replaced with space
            label, _, text = line.replace(b'\xf0', b' ').strip().decode().partition(' ')
            label, _, label_fine = label.partition(':')
            examples.append({'label_fine': label_fine, 'label': label, 'text': text})
        ret.append(Dataset(examples))

    if len(ret) == 1:
        return ret[0]
    else:
        return tuple(ret)
