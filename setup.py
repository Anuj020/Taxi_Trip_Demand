from setuptools import find_packages,setup
from typing import List
import sys

def get_requirements() -> List[str]:
    """
        This function will return list of requirements.txt 
    """

    requirements_list: list[str] = []
    try:
        with open('requirements.txt','r') as file:
            lines = file.readlines()

            for line in lines:
                requirement = line.strip()
                ## ignore empty lines and -e .

                if requirement and requirement != '-e .':
                    requirements_list.append(requirement)
    except Exception as e:
        raise FileNotFoundError(e,sys)
    
    return requirements_list


setup(
    name = "TaxiDemand",
    version="0.0.1",
    author="Anuj Patel",
    author_email="2000anujpatel@gmail.com",
    packages= find_packages(),
    insall_requires = get_requirements()
)