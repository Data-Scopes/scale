## Data Scopes and Scale

This site contains a set of Jupyter notebooks that investigate the relationship between the scale of a dataset and the resulting data scope for different research questions.

### Datasets

The notebooks use two datasets, one of correspondences of historical figures, and one of online book reviews. 

The correspondence dataset contains metadata for around 110,000 letters from the [Early Modern Letters Online (EMLO)](http://emlo.bodleian.ox.ac.uk) project. The metadata consists of sending date, sender, receiver, location of sender and location of receiver.

The online review dataset contains review text and metadata for [15 million book reviews from Goodreads](https://sites.google.com/eng.ucsd.edu/ucsdbookgraph/home) and [51 million book reviews from Amazon](https://nijianmo.github.io/amazon/index.html). The metadata consists of review author, review date, rating, reviewed book and author and the platform on which it was published (i.e. Amazon or Goodreads). 

Notebooks:

- [Transforming JSON dumps to CSV for analysis with Python and Pandas](./notebooks/Transforming-JSON-dumps-to-CSV-for-Pandas-analysis.html) ([.ipynb version](./notebooks/Transforming-JSON-dumps-to-CSV-for-Pandas-analysis.ipynb))
- [Transforming revewis to spacy docs](./notebooks/Transforming-reviews-to-spacy-docs.html) ([.ipynb version](./notebooks/Transforming-reviews-to-spacy-docs.ipynb))
- [Filtering Goodreads reviews](./notebooks/Filtering-Goodreads-Reviews.html) ([.ipynb version](./notebooks/Filtering-Goodreads-Reviews.ipynb))
- [Merging datasets](./notebooks/Merging-datasets.html) ([.ipynb version](./notebooks/Merging-datasets.ipynb))

### Distributions

Datasets with multiple records have elements that can be analysed across all or a subset of records (dates, senders and receivers, authors, book titles, ratings). Values in certain fields or columns can occur multiple times, resulting in a distribution. Analysing these distributions and understanding their shapes can tell us a lot about the underlying processes by which the data was generated. 

- distributions and their characteristics across scales
- data generation process and characteristics of samples of different sizes

Notebooks:

- [Analysing and interpreting distributions](./notebooks/Analysing-Distributions.html) ([.ipynb version](./notebooks/Analysing-Distributions.ipynb))

### Getting an Overview at Different Scales

One of the biggest challenges with datasets as they become larger in scale is to get an overview of what is in the data. What are the most salient characteristics? What are data axes or dimensions along which the datasets can be split into subsets that are meaningful? 

For correspondences, one dimensions is the date of correspondence which can be sorted into periods, or the types of people sending and receiving letters which can be sorted in job types or gender.

For reviews, there dimensions such as book, author, genre, rating, review date, publication platform.

- selecting subsets and its impact on salient characteristics
- types of sampling

Notebooks:

- [EMLO correspondence - collection Analysis](./notebooks/EMLO-collection-analysis.html) ([.ipynb version](./notebooks/EMLO-collection-analysis.ipynb))
- [Goodreads reviews - content analysis - popular books](./notebooks/Goodreads-Content-Analysis-Popular-Books.html) ([.ipynb version](./notebooks/Goodreads-Content-Analysis-Popular-Books.ipynb))
- [Goodreads reviews - content analysis - random sample](./notebooks/Goodreads-Content-Analysis-Random-Sample.html) ([.ipynb version](./notebooks/Goodreads-Content-Analysis-Random-Sample.ipynb))
- [Goodreads reviews - content analysis - comparing genres](./notebooks/Goodreads-Content-Analysis-Comparing-Genres.html) ([.ipynb version](./notebooks/Goodreads-Content-Analysis-Comparing-Genres.ipynb))

### Extracting and Structuring Information at different Scales

Extracting information such as topics and social networks is affected by the amount of available data.

- Co-occurrence and networks across different samples sizes

### References

The Amazon review data was originally used in:

-  Jianmo Ni, Jiacheng Li, Julian McAuley (2019). *Justifying recommendations using distantly-labeled reviews and fined-grained aspects*. Empirical Methods in Natural Language Processing (EMNLP), 2019

The Goodreads review data was originally used in :

- Mengting Wan, Julian McAuley (2018). *Item Recommendation on Monotonic Behavior Chains*. RecSys'18.  
- Mengting Wan, Rishabh Misra, Ndapa Nakashole, Julian McAuley. (2019). *Fine-Grained Spoiler Detection from Large-Scale Review Corpora*. ACL'19. 

The EMLO dataset is described in:

- Howard Hotson, Thomas Wallnig (2019). Reassembling the Republic of Letters in the Digital Age - Standards, Systems, Scholarship. Göttingen University Press. ISBN: 978-3-86395-403-1. Available at: [https://univerlag.uni-goettingen.de/bitstream/handle/3/isbn-978-3-86395-403-1/cost_hotson.pdf?sequence=6&](https://univerlag.uni-goettingen.de/bitstream/handle/3/isbn-978-3-86395-403-1/cost_hotson.pdf?sequence=6&)


### Tool Criticism Workshops

An [overview of related Tool Criticism workshops and materials](./Workshops/index.md).

### About Data Scopes

Data Scopes is a project by [Marijn Koolen](https://marijnkoolen.com) and [Rik Hoekstra](https://www.researchgate.net/profile/Rik_Hoekstra), both at the [Humanities Cluster](https://huc.knaw.nl) of the [Royal Netherlands Academy of Arts and Sciences](https://knaw.nl/nl).

Data Scopes workshop websites:

- [Data Scopes 2019 workshop](https://data-scopes.github.io/Data-Scopes-2019/)
- [Data Scopes for Developers 2018 workshop](https://data-scopes.github.io/Data-Scopes-Developers-2018/)
- [Data Scopes 2018 workshop](https://data-scopes.github.io/Data-Scopes-2018/)
