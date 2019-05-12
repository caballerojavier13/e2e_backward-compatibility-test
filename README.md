# Backwards Compatibility Test
> Check the website in old browsers with Docker

## Overview

This repository contains how to create the docker images for old version of 
Chrome and Firefox, and how to use those to fire automated tests in Jenkins.

> **Note:** The managing of the docker containers is made through [Portainer](https://portainer.io).

## Clone

```bash
git clone https://github.com/caballerojavier13/e2e_backward-compatibility-test.git
git remote rm origin
git remote add origin <your-git-path>
```

## Requirements

* **Python:** 3.6.5 or above
* **Docker:** 18.0.0 or above
* **Portainer:** 1.10.0 or above

## Installation

The installation is recommended made by python virtual environments (Linux and Mac users). For that reason, the following instruction includes the installation of virtualenv.

1. ### Pyhton 3

    - Debian / Ubuntu
    
        - Ubuntu 16.04
        
        ```Bash
        sudo add-apt-repository ppa:jonathonf/python-3.6
        sudo apt update
        sudo apt install python3.6
        ```
            
        - Ubuntu 16.10 or above
    
        ```bash
        sudo apt update
        sudo apt install python3.6
        ```
    
    - MacOS
    
        - Installer
        
        Install Python 3.6.x from [https://www.python.org/downloads/](https://www.python.org/downloads/).
        
        - Brew
        ```bash
        brew install python3
        ```
    
    - Windows
    
        - Installer
        
        Install Python 3.6.x from [https://www.python.org/downloads/](https://www.python.org/downloads/).

2. ### Virtual environments - pyenv (Linux/MacOS) 

    - Debian / Ubuntu
    
    ```bash
    curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
    ```
    
    - MacOS
    
        - Bash
        
        ```bash
        curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
        ```
        
        - Brew
        ```bash
        brew install pyenv
        ```
    
3. ### Creation of virtualenv (Linux/Mac)
    
    Creation of virtualenv:
    
    ```bash
    virtualenv -p python3 <desired-path>
    ```
    Activate the virtualenv:
    
    ```bash
    source <desired-path>/bin/activate
    ```
    
    Deactivate the virtualenv:
    
    ```bash
    deactivate
    ```

4. ### Dependencies (All)

    This will install all dependencies from requirements.txt
    
    ```bash
    pip install -r requirements.txt
    ```
    
5. ### Docker

    - Debian / Ubuntu
    
        - Documentation
        
        Install Docker from https://docs.docker.com/install/linux/docker-ce/ubuntu/.
    
    - MacOS
    
        - Documentation
        
        Install Docker from https://docs.docker.com/docker-for-mac/install/.
    
    - Windows
    
        - Documentation
        
        Install Docker from https://docs.docker.com/docker-for-windows/install/.

6. ### Portainer

    - Debian / Ubuntu & MacOS
    
    ```bash
    docker volume create portainer_data
    docker run -d -p 9000:9000  --restart always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer
    ```
    
    - Windows
    
    ```bash
    docker volume create portainer_data
    docker run -d -p 9000:9000 --name portainer --restart always -v \\.\pipe\docker_engine:\\.\pipe\docker_engine -v portainer_data:C:\data portainer/portainer
    ```
    

## Environment

 - `GITHUB_TOKEN`: [How to create a github access token](https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line)

## Build Docker Images`

Each Chrome and Firefox version is saved as a docker image version to make a easy reference.

Is very important that you change the repository where the docker images will be stored. 
That information for Chrome and Firefox is stored in each script (`generate_chrome_docker.sh` & `generate_firefox_docker.sh`)


Chanege `caballerojavier13` for your own account.

```bash
docker build -t caballerojavier13/${name[0]}_${name[1]}:${name[2]} .
docker push caballerojavier13/${name[0]}_${name[1]}:${name[2]}
```


> In windows execute the `sh` script with [Powershell](https://es.wikipedia.org/wiki/Windows_PowerShell).

> Before start make sure that you login into docker: `$ docker login`

> [Docker Hub](https://hub.docker.com/) is a public and free docker image repository when you can store the images 

### Chrome

#### 1. Create a Dockerfile for each image 
```bash
source venv/bin/activate
python pre_build_chrome.py
```

#### 2. Build and upload the docker images
```bash
./generate_chrome_dockers.sh
```

### Firefox

#### 1. Create a Dockerfile for each image 
```bash
source venv/bin/activate
python pre_build_firefox.py
```

#### 2. Build and upload the docker images
```bash
./generate_firefox_dockers.sh
```

## Running the Magic

With all the docker images create, now is necessary understand that the script will start a docker container with the required
browser version, then it'll fire the Jenkins job that run the tests. 

> Is very important that the tests listen the same Selenium address that the exposed in the docker

To prevent keep the credentials in the console history, are used user input instead parameter to send the username and 
password.

### Configuration

```python
data = {
    'name': 'Chrome',
    'min_version': 48,
    'max_version': 73,
    'docker_image': 'caballerojavier/selenium_chrome',
    'jenkins_job_path': 'test_in_chrome'
}
```

 - **name:** Browser name, for information purposes only;
 - **min_version:** Number that represent the first browser version to test;
 - **max_version:** Number that represent the last browser version to test;
 - **docker:** String with the docker image, the browser version is managed by a version of the same image;
 - **jenkins_job_path:** Path for the Jenkins job that will executed. Also known as `JOB_NAME`

### Execution

```bash
source venv/bin/activate
python main.py
```

## Test

Without test for the moment :(

## Contributing

Contributions welcome! See the  [Contributing Guide](https://github.com/caballerojavier13/e2e_backward-compatibility-test/blob/master/CONTRIBUTING.md).

## Author

Created and maintained by [Javier Hernán Caballero García](https://javiercaballero.info).

## License

Apache License v2.0

See  [LICENSE](https://github.com/caballerojavier13/e2e_backward-compatibility-test/blob/master/LICENSE)