# NbMeta
As of August 2018, there are over [2.5 Million jupyter notebooks on GitHub](http://nbviewer.jupyter.org/github/parente/nbestimate/blob/master/estimate.ipynb).
The code and text in these notebooks form an important body of knowledge of
research, practice, and pedagogy. Unfortunately, it is very difficult to find
notebooks that might meet a particular need due to a complete z lack of metadata
associated with these resources and with their exponential growth it is becoming
harder.

There has been significant work done on representing software and
research code as searchable, citable resources. (cite force11 and codemeta).  

We can leverage this work to inform the concept choices for notebook metadata
records. Since there is already a large corpus of publicly available notebooks,
and there is inherent difficulty in getting content creators to adopt and follow
conventions consistently, we believe that a good first step is to develop
automated metadata extraction tools for Jupyter notebooks in public GitHub
repos. This implied metadata can be leveraged for search and discovery of
relevant and useful notebooks.

At the ESIP Summer 2018 meeting, collaborators in this repo proposed a project
to pilot work on populating a  database with metadata automatically extracted
from Jupyter notebooks on GitHub. This project was awarded a
[FUNding Friday](http://wiki.esipfed.org/index.php/FUNding_Friday_Projects)
 grant.

## Deliverables
By the Winter 2019 ESIP meeting we propose to demonstrate the following outcomes
from this project:
1. A workflow for querying the GitHub API to find public repositories containing
Jupyter Notebooks
2. Initial code to transform Git Repo account info into CodeMeta Author
properties
3. Publish a JSON-LD template and example records for proof of concept  
metadata, demonstrating essential notebook metadata for citation and access and
a more complete record focused on use and understanding
4. A metadata repository based on existing software or a simple solution built
on top of Mongo DB containing an example collection of metadata records
5. Presentation/poster during the Winter ESIP Meeting.


## Follow Along
Please visit our project
[site and blog](https://esipfed.github.io/NbMeta/posts/).

## How to Contribute
We believe this project is the start of a useful resource for the notebook-using
community and intend for it to continue past the deliverables at the ESIP Winter
meeting. We'd love to work with you if you agree. We are managing tasks via
a [GitHub Project](https://github.com/ESIPFed/NbMeta/projects/1). Please comment
on the issues and feel free to propose your own.
