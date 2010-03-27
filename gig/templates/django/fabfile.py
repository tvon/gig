from fabric.api import env, run, sudo, prompt

env.hosts = ['user@remotehost']

remote_path = '/u/apps/{{ GIG_PROJECT_NAME }}'

def deploy():
    svn('update')
    apache('reload')

def svn(command):
    run("cd %s && svn %s" % (remotepath, command))

def apache(command):
    sudo("/etc/init.d/apache2 %s" % command, shell=False)

def memcached(command):
    sudo("/etc/init.d/memcached %s" % command, shell=False)

def django(command):
    run("%s/script/manage.py %s" % (remote_path, command))

def uptime():
    run("uptime")
