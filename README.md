# vk_public_analyzer

Project for analyzing vk posts saved by [vk_public_saver](https://github.com/qiray/vk_public_saver)

## What it can

- Show statistics about likes, reposts, views, comments, ads and attachments;
- Show top posts - by likes, reposts, views, comments, attachments and text length;
- Show count of posts without texts, likes, reposts, comments and attachments;
- Show count of each known attachment types;
- Show polls data - polls' count, votes, average, median, mode and stdev;
- Show top polls by votes;
- Show authors info - count of posts, likes, reposts, comments, views, attachments and text length; 
- Find top words and hashtags;
- Draw plots with posts, likes, reposts, comments, views, attachments and text length data;
- Build word cloud;
- Show topics with LDA model (Latent Dirichlet allocation);
- Make output images and csv-files.

## Requirements

This tool uses Python 3 so you need to have Python 3 and pip for build and run it. To install them use instructions for your OS.

It also needs extra libraries such as nltk, pymystem3, numpy, pillow, wordcloud, matplotlib, tabulate, argparse, gensim, stop_words. This program has file [requirements.txt](requirements.txt) with list of it's requirements. For install them call pip. For example:

``` bash
pip3 install -r requirements.txt --user
```

## Usage

vk_public_analyzer uses sqlite databases saved by [vk_public_saver](https://github.com/qiray/vk_public_saver). Don't forget to get data for analysis before usage!

vk_public_analyzer is a console tool. To run it type:

```bash
python main.py
#or
python3 main.py
```

There are some extra modes:

```
usage: vk_public_analyzer [-h] [--path PATH] [--clear_output] [--about]

Tool for analyzing publics' data from vk.com.

optional arguments:
  -h, --help      show this help message and exit
  --path PATH     Database path (default = data.db)
  --clear_output  Clear output folder
  --about         Show about info
```

After processing database this tool will create 'output' folder with all data - csv-files and png images. The tool will also print all text data to standard output.

<!-- TODO: write about these files The output folder contains these files:

- common.csv
- extremum_%s.csv
- zeroes.csv
- authors.csv

- attachments.csv
- common_polls.csv, polls.csv

- top_words.csv
- allwords.png, topwords.png, hashtags.png
- topics_%Y.csv, topics.csv

- years.png, months.png, weekdays.png, quarters.png, hours.png 

So now you have a lot of interesting data to interpret it :-)
-->

## How you can help

If you like this project you can:

- Tell your friends about it;
- Star and fork this project on github - [https://github.com/qiray/vk_public_analyzer](https://github.com/qiray/vk_public_analyzer);
- Contribute;
- Write an article about this project;
- Use it in your own project;
- Donate.

## Credits

This tool uses some apps and package. I'd like to thank:

- Yandex Mystem - tool for lemmatizing Russian texts;
- nltk - toolkit for processing natural languages;
- pymystem3 - Python wrapper for Yandex Mystem;
- numpy - package for scientific computing;
- pillow - Python Imaging Library;
- wordcloud - package for making word clouds;
- matplotlib - package for making plots;
- tabulate - package for printing tables;
- argparse - package for parsing command line args;
- gensim - package for text models;
- stop_words - package with list of stop words.

## Contact

You are welcome to open [new issue](https://github.com/qiray/vk_public_analyzer/issues/new) if you have any questions, suggestions or bugs.

## License

This program uses MIT license. For more information see the LICENSE file.
