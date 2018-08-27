# NbMeta
As of August 2018, there are over [2.5 Million jupyter notebooks on GitHub](http://nbviewer.jupyter.org/github/parente/nbestimate/blob/master/estimate.ipynb).
The code and text in these notebooks form an important body of knowledge of
research, practice, and pedagogy. Unfortunately, it is very difficult to find
notebooks that might meet a particular need due to a complete lack of metadata
associated with these resources.

There has been  significant work done on representing software as searchable,
citable resources. We believe that it is to create automated metadata
extraction tools for Jupyter notebooks that would allow us to imply useful
metadata simply by looking at files that are exposed in notebooks' GitHub
repos.

At the ESIP Summer 2018 meeting, collaborators in this repo proposed a project
to pilot work on populating a  database with metadata automatically extracted
from Jupyter notebooks on GitHub. This project was awarded a
[FUNding Friday](http://wiki.esipfed.org/index.php/FUNding_Friday_Projects)
grant.

## Deliverables
By the Winter 2019 ESIP meeting we propose to demonstrate the following outcomes
from this project:
1. A metadata repository based on existing software or a simple solution built
on top of Mongo DB
2. A workflow for querying the GitHub API to find Jupyter Notebooks
3. Initial code to transform GitRepo account info into DataCite metadata
4. Initial code to transform a Jupyter notebook into CodeMeta metadata
5. Some initial code to extract more meaning from the Jupyter Notebook, the
repo's README, `requirements.txt`, `environment.yml`, `apt.txt`, etc
6. A blog posting on our experience and suggestions for next steps.

## Follow Along
Please visit our project
[site and blog](https://esipfed.github.io/NbMeta/posts/).

## How to Contribute
We believe this project is the start of a useful resource for the notebook-using
community and intend for it to continue past the deliverables at the ESIP Winter
meeting. We'd love to work with you if you agree. We are managing tasks via
a [GitHub Project](https://github.com/ESIPFed/NbMeta/projects/1). Please comment
on the issues and feel free to propose your own.
