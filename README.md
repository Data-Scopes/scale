## Data Scopes and Scale

This site contains a set of Jupyter notebooks that investigate the relationship between the scale of a dataset and the resulting data scope for different research questions.

### Datasets

The notebooks use two datasets, one of correspondences of historical figures, and one of online book reviews. 

The correspondence dataset contains metadata for around 110,000 letters from the [Early Modern Letters Online (EMLO)](http://emlo.bodleian.ox.ac.uk) project. The metadata consists of sending date, sender, receiver, location of sender and location of receiver.

The online review dataset contains review text and metadata for [15 million book reviews from Goodreads](https://sites.google.com/eng.ucsd.edu/ucsdbookgraph/home) and [51 million book reviews from Amazon](https://nijianmo.github.io/amazon/index.html). The metadata consists of review author, review date, rating, reviewed book and author and the platform on which it was published (i.e. Amazon or Goodreads). 

Notebooks:

- [Transforming JSON dumps to CSV for analysis with Python and Pandas](./notebooks/Transforming-JSON-dumps-to-CSV-for-Pandas-analysis.html)
- [Filtering Goodreads reviews](./notebooks/Filtering-Goodreads-Reviews.html) ([.ipynb version](./notebooks/Filtering-Goodreads-Reviews.ipynb))
- [Merging datasets](./notebooks/Merging-datasets.html)

### Distributions

Datasets with multiple records have elements that can be analysed across all or a subset of records (dates, senders and receivers, authors, book titles, ratings). Values in certain fields or columns can occur multiple times, resulting in a distribution. Analysing these distributions and understanding their shapes can tell us a lot about the underlying processes by which the data was generated. 

- distributions and their characteristics across scales
- data generation process and characteristics of samples of different sizes

Notebooks:

- [Analysing and interpreting distributions](./notebooks/Analysing-Distributions.html)

### Getting an Overview at Different Scales

One of the biggest challenges with datasets as they become larger in scale is to get an overview of what is in the data. What are the most salient characteristics? What are data axes or dimensions along which the datasets can be split into subsets that are meaningful? 

For correspondences, one dimensions is the date of correspondence which can be sorted into periods, or the types of people sending and receiving letters which can be sorted in job types or gender.

For reviews, there dimensions such as book, author, genre, rating, review date, publication platform.

- selecting subsets and its impact on salient characteristics
- types of sampling

Notebooks:

- [EMLO correspondence - collection Analysis](./notebooks/EMLO-collection-analysis.html)
- [Goodreads reviews - content analysis](./notebooks/Goodreads-Content-Analysis.html)

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



