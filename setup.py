from setuptools import find_packages, setup


def get_requirements():
    req_lst = []
    try:
        with open('requirements.txt', 'r') as f:
            lines = f.readlines()
            for l in lines:
                requirement = l.strip()
                if requirement and requirement!= '-e .':
                    req_lst.append(requirement)
                    
    except FileNotFoundError:
        print("requirenents.txt file not found.")
        
    return req_lst

setup(
    name="Nework_Security",
    version="0.0.0.1",
    author="Hareesh kumar",
    author_email="hareeshdaxton@gmail.com",
    packages=find_packages(),  
    install_requires=get_requirements()
)