from setuptools import find_packages,setup
from typing import List

def get_requirements()-> List[str]:
    lst_requirement:List[str] = []
    try:
        with open("requirements.txt","r") as file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                # ignore empty lines and -e .
                if requirement and requirement != "-e .":
                    lst_requirement.append(requirement)
    except FileNotFoundError as e:
        print("File Not found")
    
    return lst_requirement

setup(
    name= "NetworkSecurity",
    version= "0.0.1",
    author= "Sohom Banerjee",
    author_email= "sohom.ban96@gmail.com",
    packages= find_packages(),
    install_requires= get_requirements(),
    
)