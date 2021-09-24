
# Restaurant Rating Prediction

A Machine Learning webapp.

## Description

- This is a webapp to predict the ratings of restaurants in bangalore.
- This uses Random Forest Classifier

## Aim / Goal

- This is said to be a intermediate level project in ineuron's internship portal and i wanted to get started with some projects and interships so, i thought of starting with this project.


## Skillset

- EDA
- Data Preprocessing
- Feature Engineering
- Model Building and Tuning
- Python Programming (backend)
- Web Development
- AWS Cloud skills (ec2 instances, s3 bucket)
- Cassandra Database
- Version control (git, github, dvc)

## Dataset

- Download the dataset for custom training.
    - https://www.kaggle.com/himanshupoddar/zomato-bangalore-restaurants
- Download a modified version with a primary key added by me.
    - https://drive.google.com/file/d/1rA3AZcptVCr54B84oW0gtO1igEttmK6r/view?usp=sharing

## Demo

[YouTube Video link](https://youtu.be/cpAEbemEo2U)

## Tech Stack

<code><img height="80" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/python/python.png"></code>
<code><img height="80" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/html/html.png"></code>
<code><img height="80" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/css/css.png"></code>
<code><img height="80" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/javascript/javascript.png"></code>
<code><img height="80" src="https://github.com/tomchen/stack-icons/raw/master/logos/bootstrap.svg"></code>
<code><img height="80" src="https://symbols.getvecta.com/stencil_80/56_flask.3a79b5a056.jpg"></code>
<code><img height="80" src="https://raw.githubusercontent.com/github/explore/fbceb94436312b6dacde68d122a5b9c7d11f9524/topics/aws/aws.png"></code>
<code><img height="80" src="https://raw.githubusercontent.com/github/explore/d8574c7bce27faa27fb879bca56dfe351ee66efd/topics/pycharm/pycharm.png"></code>
<code><img height="80" src="https://raw.githubusercontent.com/github/explore/8b79365c693905ff9adad384ab1534b5ab041cb9/topics/cassandra/cassandra.png"></code>
<code><img height="80" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/git/git.png"></code>
<code><img height="80" src="https://raw.githubusercontent.com/github/explore/d530d6a3a171a53f7b8eb4e9e005136e7ebd898f/topics/numpy/numpy.png"></code>
<code><img height="80" src="https://raw.githubusercontent.com/pandas-dev/pandas/761bceb77d44aa63b71dda43ca46e8fd4b9d7422/web/pandas/static/img/pandas.svg"></code>
<code><img height="80" src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Scikit_learn_logo_small.svg/1280px-Scikit_learn_logo_small.svg.png"></code>
- Seaborn
- Matplotlib
- dtale
- DVC

  
## Installation

Requirements

- Python 3.8
- Cassandra 3.11
- Windows or ubuntu 20.04 (preferbly, setup Cassandra on dockers if working on windows)


## Deployment

The Deployment was done on aws ec2 instances.

What you need to do:
- setup cassandra database and push data onto it.
- create a s3 bucket and use it as intermediate in file sharing.
- setup the webapp and run it. 

### Setting up the database
(Note: use 4GB of memory for a every instance you create to act as a node or cassnadra will stop right after it starts.)


- First install java

```bash
sudo apt update
sudo apt install openjdk-8-jdk -y
java -version
sudo update-alternatives --config java
```
- Make Java accessible, edit the .bashrc file by:

```bash
sudo nano ~/.bashrc
```
- Paste this line on the last line in the file and save it:
```bash
JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
```

- then run below line to apply the changes:
```bash
source ~/.bashrc
```

- Now, install and setup cassandra
```bash
sudo apt install apt-transport-https
wget -q -O - https://www.apache.org/dist/cassandra/KEYS | sudo apt-key add -
sudo sh -c 'echo "deb http://www.apache.org/dist/cassandra/debian 311x main" > /etc/apt/sources.list.d/cassandra.list'
sudo apt-get update
sudo apt-get install cassandra -y
```

- wait for half a minute or so for cassandra to start, then run to see if its running:
```bash
nodetool status
```

- Now, download and unzip the dataset:
( I have modified the original dataset to have a primary key column and changed the delimiter to '|')
```bash
sudo apt-get install unzip
wget --no-check-certificate -r 'https://docs.google.com/uc?export=download&id=1rA3AZcptVCr54B84oW0gtO1igEttmK6r' -O zomato.zip
unzip zomato.zip
```

- We will be using a python script to upload the csv file onto the cassandra database (Copy command and dsbulk come across 2 issues that is, firstly they have a field size limit and they tend to read more if not less columns, which i think is a delimiter issue so i just used python. The field size limit is easy to solve, you only have to change the .cqlshrc file but i couldn't solve the latter problem)
```bash
sudo apt install python3-pip
pip install cassandra-driver pandas
```

- Enter cqlsh shell by running:
```bash
cqlsh
```

- Now, we create a keyspace and table:
(Note: i am using a single node in this case but you can use multiple nodes and link them easily. You may find this video helpful: [YouTube video link](https://www.youtube.com/watch?v=3zhJyAwZkYo&t=876s))

```bash
create keyspace if not exists Data with replication = {'class' : 'SimpleStrategy', 'replication_factor':1};

Use Data;

CREATE TABLE if not exists Data.zomato (url text,address text,name text,online_order text,book_table text,rate text,votes int,phone text,location text,rest_type text,dish_liked text,cuisines text,approx_cost text, reviews_list text, menu_item text, listed_in_type text,listed_in_city text,id_no Bigint, primary key(id_no));
```
- Now, exit cqlsh shell and enter python shell by doing CRLT+Z or CRLT+X and running:
```bash
python3
```

- Run the below script to upload the data into cassandra deb
```bash
from cassandra.cluster import Cluster
import csv
import pandas as pd

cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect()
session.execute("create keyspace if not exists Data with replication = {'class' : 'SimpleStrategy', 'replication_factor':1};")
session.execute('Use Data;')
with open('zomato.csv', 'r') as file:
    csv.field_size_limit(10000000)
    csv_reader = csv.reader(file, delimiter='|')
    next(csv_reader)
    for row in csv_reader:
        (url, address, name, online_order, book_table, rate, votes, phone, location, rest_type, dish_liked,cuisines,approx_cost,reviews_list, menu_item,listed_in_type,listed_in_city, id_no) = row
        session.execute("""INSERT INTO zomato ( url ,address, name, online_order, book_table, rate, votes, phone, location, rest_type, dish_liked,cuisines,approx_cost,reviews_list,menu_item, listed_in_type , listed_in_city, id_no) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s,%s, %s, %s);""", [url ,address, name, online_order, book_table, rate, int(votes), phone, location, rest_type, dish_liked,cuisines,approx_cost,reviews_list,menu_item, listed_in_type , listed_in_city, int(id_no)])
```

- after the process stops (about 3-5 minutes), run:
```bash
select count(*) from data.zomato;
```
It prints the number of rows in the zomato table.

- Now, when you want to export the table, just run this in the cqlsh shell
```bash
COPY data.zomato ( id_no , address , approx_cost , book_table , cuisines  , dish_liked ,  listed_in_city, listed_in_type, location, menu_item, name, online_order, phone, rate, rest_type, reviews_list, url, votes) TO 'export.csv' WITH HEADER = TRUE AND DELIMITER='|';
```

- then zip the file:
```bash
sudo apt-get install zip
zip export export.csv
```

- Now to upload the file to s3 bucket, install awscli

(Note: You will have to create a IAM role with access to s3 bucket and give that role the instances you are using. )

```bash
sudo apt-get install awscli
```

- Then you need your unique bucket name to upload the data:

```bash
aws s3 cp export.zip s3://UniqueBucketName
```


### Setting up the webapp
first upload your files to the instance.
Then, fullfill the requirements.

(Note: Use t2 small (2GB) memory if you intend to train it remotely)

- Do the installations:
```bash
sudo apt-get update
sudo apt install awscli
sudo apt-get install unzip
sudo apt install python3-pip -y
pip3 install -r requirements
```
- Go to the data_given directory and run the below to get the data from s3 bucket and unzip it.
You can just keep the file name as zomato instead of export from the start. i just didn't think of it at the time.
```bash
aws s3 cp s3://UniqueBucketName/export.zip .
unzip export.zip
mv "export.csv" "zomato.csv"
```

- Now, go to the main directory of our project and run our app:
```bash
python app.py
```

You can do the training either on the cloud or on your local system.
you have to run the files in the src folder one by one, i usually did it on the local system and used dvc to do so.


## Documentation

- [High Level Documents](https://drive.google.com/file/d/1EAOnpQhf3ap8X5ZOHQGU3NjqJa8umhp7/view?usp=sharing)
- [Low Level Documents](https://drive.google.com/file/d/1oNYMINswUHTthdt66PbtEtuaT4rJnlwj/view?usp=sharing)
- [Wireframe](https://drive.google.com/file/d/1gLoHLRzVcfGwWxG5kmx0x4f_U5lHpy_8/view?usp=sharing)
- [Report](https://docs.google.com/presentation/d/14Pmn4SR93L7fRnGJvNQfJuKAf8PURd94/edit?usp=sharing&ouid=105403021575418724386&rtpof=true&sd=true)

 
## Challenges

- Setting up cassandra and successfully using it was a big challenge and i spent about 10 days dealing with the problems i faced... some of the problems were because i developed it on windows at first i didn't know which version to use and how to install and run some of the versions without problems, with running it on remote system and with insertion of bulk data into cassandra.
- 'Depression', the thing is i spent a lot of time on features engineering and kept trying to come up with as many good features and new-new ideas but while i was doing feature selection and model training, i found out that one of the feature 'votes' was able to give 95% score on its own. Although the other features i made weren't useless on their own, they failed to improve the accuracy beyound 95% and it was very depression as i had put so much time and effort into getting those features. so, initially after i made my model i didn't want to finish the project.

## What i Learnt

- Usage of cassandra DB
- AWS ec2, s3 bucket (uploading and download data), IAM roles.
- Usage of DVC, git, github.
- End to End development.
- Dockers (to setup cassnadra locally)


## Support

For support, email jackneutron786@gmail.com or contact me on linkedin.

  
## Usage
- You can use this project for further developing it and adding your work in it. If you use this project, kindly mention the original source of the project and mention the link of this repo in your report.
- I have provided the steps for deployment hoping it might help someone.
  
## 🚀 About Me
- I am a data science enthusiast.
- Currently studying 4th year in CSE
- I have some helpful content on kaggle as well so, check it out if interested
  

## 🔗 Links
[![kaggle](https://img.shields.io/badge/Kaggle-000?style=for-the-badge&logo=kaggle&logoColor=white)](https://www.kaggle.com/jackfroster)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/syed-rahim-saqib-2505221b5/)

  
## License

[MIT](https://choosealicense.com/licenses/mit/)

  
## Author

- [Syed Rahim Saqib](https://www.github.com/Jack8861)

  
