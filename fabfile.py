from fabric.api import run
from fabric.api import env
from fabric.api import prompt
from fabric.api import execute
from fabric.api import sudo
from fabric.api import settings
from fabric import contrib
import boto.ec2
import time
import boto

env.hosts = ['localhost', ]
env.aws_region = 'us-west-2'


def host_type():
    run('uname -s')


def get_ec2_connection():
    if 'ec2' not in env:
        conn = boto.ec2.connect_to_region(env.aws_region)
        if conn is not None:
            env.ec2 = conn
            print "Connected to EC2 region %s" % env.aws_region
        else:
            msg = "Unable to connect to EC2 region %s"
            raise IOError(msg % env.aws_region)
    return env.ec2


def provision_instance(wait_for_running=True, timeout=120, interval=2):
    wait_val = int(interval)
    timeout_val = int(timeout)
    conn = get_ec2_connection()
    instance_type = 't1.micro'
    key_name = 'pk-aws'
    security_group = 'ssh-access'
    image_id = 'ami-d0d8b8e0'

    reservations = conn.run_instances(
        image_id,
        key_name=key_name,
        instance_type=instance_type,
        security_groups=[security_group, ]
    )
    new_instances = [
        i for i in reservations.instances if i.state == u'pending'
    ]
    running_instance = []
    if wait_for_running:
        waited = 0
        while new_instances and (waited < timeout_val):
            time.sleep(wait_val)
            waited += int(wait_val)
            for instance in new_instances:
                state = instance.state
                print "Instance %s is %s" % (instance.id, state)
                if state == "running":
                    running_instance.append(
                        new_instances.pop(new_instances.index(i))
                    )
                instance.update()


def list_aws_instances(verbose=False, state='all'):
    conn = get_ec2_connection()

    reservations = conn.get_all_reservations()
    instances = []
    for res in reservations:
        for instance in res.instances:
            if state == 'all' or instance.state == state:
                print instance
                instance = {
                    'id': instance.id,
                    'type': instance.instance_type,
                    'image': instance.image_id,
                    'state': instance.state,
                    'instance': instance,
                }
                instances.append(instance)
    env.instances = instances
    if verbose:
        import pprint
        pprint.pprint(env.instances)


def select_instance(state='running'):
    if env.get('active_instance', False):
        return

    list_aws_instances(state=state)

    prompt_text = "Please select from the following instances:\n"
    instance_template = " %(ct)d: %(state)s instance %(id)s\n"
    for idx, instance in enumerate(env.instances):
        ct = idx + 1
        args = {'ct': ct}
        args.update(instance)
        prompt_text += instance_template % args
    prompt_text += "Choose an instance: "

    def validation(input):
        choice = int(input)
        if choice not in range(1, len(env.instances) + 1):
            raise ValueError("%d is not a valid instance" % choice)
        return choice

    choice = prompt(prompt_text, validate=validation)
    env.active_instance = env.instances[choice - 1]['instance']


def run_command_on_selected_server(command):
    select_instance()
    selected_hosts = [
        'ubuntu@' + env.active_instance.public_dns_name
    ]
    execute(command, hosts=selected_hosts)


# def run_psql_command_on_selected_server(command):
#     select_instance()
#     selected_hosts = [
#         'postgres@' + env.active_instance.public_dns_name
#     ]
#     execute(command, hosts=selected_hosts)


def _install_nginx():
    sudo('apt-get -y install nginx')
    print "installed nginx"
    sudo('/etc/init.d/nginx start')


def install_nginx():
    run_command_on_selected_server(_install_nginx)


def _install_supervisor():
    sudo('apt-get -y install supervisor')
    print "installed supervisor"
    sudo('mv ./tweetTrack/supervisord.conf /etc/supervisor/conf.d/tweetTrack.conf')
    sudo('/etc/init.d/supervisor stop')
    sudo('/etc/init.d/supervisor start')


def install_supervisor():
    run_command_on_selected_server(_install_supervisor)


def _move_nginx_files():
    sudo('mv /etc/nginx/sites-available/default \
        /etc/nginx/sites-available/default.orig')
    sudo('mv ./tweetTrack/simple_nginx_config /etc/nginx/sites-available/default')
    sudo('/etc/init.d/nginx restart')
    # sudo('python ./tweetTrack/tweetTrack.py')


def move_nginx_files():
    run_command_on_selected_server(_move_nginx_files)


def _psql_setup():
    sudo('psql < ~/tweetTrack/setup.sql', user='postgres')
    sudo('/usr/bin/python tweetTrack/manage.py syncdb --noinput')
    sudo('/usr/bin/python tweetTrack/manage.py loaddata tweetTrack/user.json')



def _mass_install():
    sudo('apt-get update')
    # sudo('apt-get -y install postgresql postgresql-contrib')
    # sudo('mv /etc/postgresql/9.1/main/pg_hba.conf /etc/postgresql/9.1/main/pg_hba.back')
    # sudo('mv tweetTrack/pg_hba.conf /etc/postgresql/9.1/main/pg_hba.conf')
    # sudo('service postgresql restart')
    sudo('apt-get -y install python-setuptools')
    sudo('apt-get -y install python-dev')
    sudo('apt-get -y install python-pip')
    sudo('apt-get -y install libpq-dev')
    sudo('apt-get -y install libjpeg-dev')
    with settings(warn_only=True):
        sudo('pip install -r ~/tweetTrack/requirements.txt')
    # sudo('pip install django-configurations')
    # sudo('pip install sorl-thumbnail')
    # sudo('pip install psycopg2')


def mass_install():
    run_command_on_selected_server(_mass_install)
    # run_command_on_selected_server(_psql_setup)



def stop_instance():
    conn = get_ec2_connection()
    select_instance('running')
    conn.stop_instances(env.active_instance.id)


def terminate_instance():
    conn = get_ec2_connection()
    select_instance('stopped')
    conn.terminate_instances(env.active_instance.id)


def generate_nginx_config():
    config_file = """
server {
    listen 80;
    server_name http://%s/;
    access_log  /var/log/nginx/test.log;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}""" % env.active_instance.public_dns_name
    with open("simple_nginx_config", 'w') as outfile:
        outfile.write(config_file)


def deploy():
    list_aws_instances()
    not_running = True
    while not_running:
        for instance in env.instances:
            if instance['state'] == u'running':
                not_running = False
        list_aws_instances()

    install_nginx()
    generate_nginx_config()
    run_command_on_selected_server(contrib.project.upload_project)
    mass_install()
    install_supervisor()
    move_nginx_files()

