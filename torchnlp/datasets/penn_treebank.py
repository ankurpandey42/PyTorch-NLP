import os
import io

from torchnlp.text_encoders import UNKNOWN_TOKEN
from torchnlp.text_encoders import EOS_TOKEN
from torchnlp.utils import download_urls


def penn_treebank_dataset(
        directory='data/penn-treebank',
        train=False,
        dev=False,
        test=False,
        train_filename='ptb.train.txt',
        dev_filename='ptb.valid.txt',
        test_filename='ptb.test.txt',
        check_file='ptb.train.txt',
        urls=[
            'https://raw.githubusercontent.com/wojzaremba/lstm/master/data/ptb.train.txt',
            'https://raw.githubusercontent.com/wojzaremba/lstm/master/data/ptb.valid.txt',
            'https://raw.githubusercontent.com/wojzaremba/lstm/master/data/ptb.test.txt'
        ]):
    """
    Load the Penn Treebank dataset.

    This is the Penn Treebank Project: Release 2 CDROM, featuring a million words of 1989 Wall
    Street Journal material.

    More details:
    https://catalog.ldc.upenn.edu/ldc99t42

    Citation:
    Marcus, Mitchell P., Marcinkiewicz, Mary Ann & Santorini, Beatrice (1993).
    Building a Large Annotated Corpus of English: The Penn Treebank

    Args:
        directory (str, optional): Directory to cache the dataset.
        train (bool, optional): If to load the training split of the dataset.
        dev (bool, optional): If to load the development split of the dataset.
        test (bool, optional): If to load the test split of the dataset.
        train_filename (str, optional): The filename of the training split.
        dev_filename (str, optional): The filename of the development split.
        test_filename (str, optional): The filename of the test split.
        name (str, optional): Name of the dataset directory.
        check_file (str, optional): Check this file exists if download was successful.
        urls (str, optional): URLs to download.

    Returns:
        :class:`tuple` of :class:`torchnlp.datasets.Dataset`: Tuple with the training tokens, dev tokens
        and test tokens in order if their respective boolean argument is true.

    Example:
        >>> from torchnlp.datasets import penn_treebank_dataset
        >>> train = penn_treebank_dataset(train=True)
        >>> train[:10]
        ['aer', 'banknote', 'berlitz', 'calloway', 'centrust', 'cluett', 'fromstein', 'gitano',
        'guterman', 'hydro-quebec']
    """
    download_urls(directory=directory, file_urls=urls, check_file=check_file)

    ret = []
    splits = [(train, train_filename), (dev, dev_filename), (test, test_filename)]
    split_filenames = [dir_ for (requested, dir_) in splits if requested]
    for filename in split_filenames:
        full_path = os.path.join(directory, filename)
        text = []
        with io.open(full_path, encoding='utf-8') as f:
            for line in f:
                text.extend(line.replace('<unk>', UNKNOWN_TOKEN).split())
                text.append(EOS_TOKEN)
        ret.append(text)

    if len(ret) == 1:
        return ret[0]
    else:
        return tuple(ret)
