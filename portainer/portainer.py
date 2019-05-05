import requests


class Portainer:
    
    def __init__(self, base_url, username, password, endpoint=1):
        self._base_url = base_url
        self._username = username
        self._password = password
        self._current_endpoint = str(endpoint)
        self._headers = {
            "Content-Type": 'application/json',
            "Accept": 'application/json'
        }
        self._login()
        
    def _login(self):
        data = {
            "Username": self._username,
            "Password": self._password
        }
        
        resp = requests.post(
            url=self._base_url + '/api/auth',
            json=data,
            headers=self._headers
        )
        
        if resp.status_code == 200:
            self._headers['Authorization'] = 'Bearer ' + resp.json()['jwt']
        else:
            raise Exception('Bad credentials')
        
    def pull_image(self, docker_image):
        url = self._base_url + "/api/endpoints/" + self._current_endpoint 
        url += "/docker/images/create?fromImage=" + docker_image

        resp = requests.post(
            url=url,
            json={},
            headers=self._headers
        )
        
        if resp.status_code != 200:
            raise Exception('Something gone wrong')

    def find_container_by_name(self, container_name):
        url = self._base_url
        url += '/api/endpoints/' + self._current_endpoint 
        url += '/docker/containers/json?all=true&filters={"name":["' + container_name + '"]}'
        
        resp = requests.get(
            url=url,
            headers=self._headers
        )
        
        if resp.status_code != 200:
            raise Exception('Something gone wrong')
        
        return resp.json()

    def _stop_container(self, container_id):
        url = self._base_url + "/api/endpoints/" + self._current_endpoint
        url += "/docker/containers/" + container_id + "/stop"

        resp = requests.post(
            url=url,
            json={},
            headers=self._headers
        )

        if resp.status_code != 204:
            raise Exception('Something gone wrong')

    def _start_container(self, container_id):
        url = self._base_url + "/api/endpoints/" + self._current_endpoint
        url += "/docker/containers/" + container_id + "/start"

        resp = requests.post(
            url=url,
            json={},
            headers=self._headers
        )

        if resp.status_code != 204:
            raise Exception('Something gone wrong')
    
    def _remove_container(self, container_id):

        self._stop_container(container_id)

        url = self._base_url + "/api/endpoints/" 
        url += self._current_endpoint + "/docker/containers/" + container_id
        resp = requests.delete(
            url=url,
            headers=self._headers
        )

        if resp.status_code != 204:
            raise Exception('Something gone wrong')

    def _create_container(self, container_name, docker_image, ports):
        url = self._base_url + "/api/endpoints/" + self._current_endpoint + "/docker/containers/create"

        ports_bindings = {}

        for p in ports:
            port_key = str(p).split(':')[0] + "/tcp"
            ports_bindings[port_key] = [
                {
                    'HostPort': str(p).split(':')[1]
                }
            ]

        data = {
          'Domainname': container_name,
          'Hostname': container_name,
          'Image': docker_image,
          'HostConfig': {
            'AutoRemove': False,
            'NetworkMode': 'bridge',
            'PortBindings': ports_bindings,
            'Privileged': False,
            'PublishAllPorts': False,
            'ReadonlyRootfs': False
          }
        }

        resp = requests.post(
            url=url,
            json=data,
            params= {'name': container_name},
            headers=self._headers
        )
        
        if resp.status_code != 201:
            raise Exception('Something gone wrong')

        return resp.json()['Id']

    def deploy_container(self, container_name, docker_image, ports):

        containers_list = self.find_container_by_name(container_name)

        if len(containers_list) > 0:
            self._remove_container(containers_list[0]['Id'])

        self.pull_image(docker_image)

        container_id = self._create_container(container_name, docker_image, ports)

        if container_id:
            self._start_container(container_id)

    def prune_images(self):
        url = self._base_url + "/api/endpoints/" + self._current_endpoint 
        url += '/docker/images/prune?filters={"dangling":["false"]}'
        
        resp = requests.post(
            url=url,
            headers=self._headers
        )

        if resp.status_code != 204:
            raise Exception('Something gone wrong')
