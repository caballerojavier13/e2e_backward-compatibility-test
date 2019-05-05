from portainer.portainer import Portainer

import getpass
import jenkins
import time

chrome_data = {
    'name': 'Chrome',
    'min_version': 48,
    'max_version': 73,
    'docker_image': 'jctesting/selenium_chrome',
    'jenkins_job_path': ''
}

firefox_data = {
    'name': 'Firefox',
    'min_version': 45,
    'max_version': 67,
    'docker_image': 'jctesting/selenium_firefox',
    'jenkins_job_path': ''
}

platforms = [chrome_data, firefox_data]

def deploy_container(docker_image):
    p = Portainer(
        base_url=portainer_url, 
        username=portainer_username, 
        password=portainer_password
    )

    p.deploy_container('selenium', docker_image, ['4444:4444'])


def get_jenkins_server():
    return jenkins.Jenkins(
        url=jenkins_url, 
        username=jenkins_username, 
        password=jenkins_password
    )


def run_tests(jenkins_job):
    server = get_jenkins_server()
    run_number = server.build_job(jenkins_job)

    while 'executable' not in server.get_queue_item(run_number):
        time.sleep(10)

    build_number = server.get_queue_item(run_number)['executable']['number']

    while server.get_build_info(jenkins_job, build_number)['building']:
        time.sleep(10)


def perform_cross_browsing_test(data):

    print()
    print('Running test over %s:' % data['name'])

    for v in range(data['min_version'], data['max_version'] + 1):
        print('     - testing in %s version %s' % (data['name'], v))
        deploy_container(data['docker_image'] + ':' + str(v))
        run_tests(data['jenkins_job_path'])


print('Please enter your portainer credentials:')
portainer_url = input('URL: ')
portainer_username = input('Username: ')
portainer_password = getpass.getpass()

print('Please enter your Jenkins credentials:')
jenkins_url = input('URL: ')
jenkins_username = input('Username: ')
jenkins_password = getpass.getpass()

for p in platforms:
    perform_cross_browsing_test(p)
