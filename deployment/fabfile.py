from fabric.api import *

def setup_dev_virtualenv():
    local("sudo aptitude install libpq-dev python-dev libjpeg62-dev")
    local("sudo pip install virtualenv")

def setup_dev_project():
    local("mkdir ~/Dev && cd ~/Dev")
    local("git clone git@github.com:sameenjalal/mavenize-beta.git")
    local("cd mavenize-beta/")
    local("virtualenv env")
    local("source env/bin/activate")
    local("pip install -r requirements/common.txt")
    local("pip install -r requirements/dev.txt")
    local("sudo sh -c 'echo \"DEPLOYMENT_TYPE=production\" >> /etc/environment'")

def setup_git(email, name):
    local("sudo aptitude install git-core")
    local("ssh-keygen -t rsa -C '%s'", email)
    local("git config --global user.name '%s'", name)
    local("git config --global user.email '%s'", email)

def setup_node():
    local("sudo aptitude install build-essential curl libssl-dev openssl-dev")
    local("git clone git://github.com/creationix/nvm.git ~/nvm")
    local("echo . ~/nvm/nvm.sh >> ~/.bashrc")
    local("source ~/.bashrc")
    local("nvm install v0.6.18")
    local("nvm alias default v0.6.18")

def install_less():
    local("npm install less")
    local("sudo ln -s ~/node_modules/less/bin/lessc ~/mavenize-beta/env/bin/lessc")

def install_announce():
    local("npm install announce.js")

def install_postgresql():
    local("sudo aptitude install postgresql")
