# v-play

Viaplay team, thanks for to share the knowlodge! :)
More one powerful library to script our infrastructure using python.

## Getting Started

Note that both json files have the same AWS resources.

The troposphere library allows for easier creation of the AWS CloudFormation JSON by writing Python code to describe the AWS resources.


### Prerequisites

* python 2.7
* VirtualEnv

### Installing

This project was builded using virtualenv. So, first we need install them. 

[Virtualenv Installation Page](https://virtualenv.pypa.io/en/latest/installation/)

Then we need run virtual env following the commands above:

```
virtualenv ENV
source /path/to/ENV/bin/activate
```

And install the dependecies

```
pip install -r requirements.txt
```

## Running

```
# It'll print the cloudformation content to Developement Enviroment.

python app.py --env Development 

# It'll create a file at folder output.

python app.py --env Development --output ./output/template_developement.json 
```

## Authors

* **Felipe Ribeiro**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details