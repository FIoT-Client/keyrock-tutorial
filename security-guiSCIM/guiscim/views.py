from django.shortcuts import render, redirect
from flask import Flask, session, Markup
import requests
import json
import logging
from django.http import HttpResponse

import sys
sys.path.insert(0, r'../guiscim/oauth_fiware.py')

from guiscim.oauth_fiware import OAuth2 ## You can also use '*' wildcard to import all the functions in file.py file.


try:
    import simplejson as json
except ImportError:
    import json

auth_app = OAuth2()
keystone_url = "http://10.7.52.41:5000/"
roles_id = []
paserd = None


def get_token(keystone_url):

    #logging.basicConfig(filename='script-keyrock.log', filemode='w', level=logging.DEBUG)
    logging.debug('getting token...')

    json_payload = {
        "auth": {
            "identity": {
                "methods": ["password"],
                "password": {
                    "user": {
                        "name": "idm",
                        "domain": {"id": "default"},
                        "password": "idm"
                    }
                }
            }
        }
    }

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url=keystone_url + '/v3/auth/tokens',
                             data=json.dumps(json_payload),
                             headers=headers)

    if response.status_code in (201, 200):
        token = response.headers['X-Subject-Token']
        logging.info('TOKEN --- ' + token)
        return token
    else:
        logging.error('GET TOKEN ### ' + response.text)

def auth(request, methods=['GET', 'POST']):
    error = request.GET.get('error', '')
    if error:
        return "Error: " + error

    if request.method == 'GET':
        auth_code = request.GET.get('code')
        token_dict = auth_app.get_token(auth_code)
        content_token = "s_in: {} </br> refresh_token: {}".format(
            token_dict['access_token'], token_dict['token_type'], str(token_dict['expires_in']),
            token_dict['refresh_token']
        )
        user_info = auth_app.get_user_info(token_dict['access_token'])
        response_project = json.dumps(user_info['roles'])
        resposta = response_project.split("\"")

        for key in resposta:
        	if (key == "admin") or (key == "provider"):
        		return render(request, 'guiscim/usuario.html')

        return render(request, 'guiscim/semsucesso.html')


def index(request):

	return render(request, 'guiscim/index.html')


def autentica(request):

   if request.method == "GET":
           auth_url = auth_app.authorize_url()
           token = get_token(keystone_url)
           return redirect(auth_url)

def papel(request):

	return render(request, 'guiscim/papel.html')

def usuario(request):

        return render(request, 'guiscim/usuario.html')


def projeto(request):

	return render(request, 'guiscim/projeto.html')

def index1(request):

        return redirect('http://10.7.52.41:8000')
def atualizar_usuario(request):
        token = get_token(keystone_url)
        json_payload = {
                                    "user": {
                                        "name": request.GET['nome_u'],
                                        "password": request.GET['senha_u'],
                                        "username": request.GET['nome_u']
                                    }
                                }

        headers = {'X-Auth-Token': token, 'Content-Type': 'application/json'}
        response = requests.patch(url=keystone_url +'/v3/users'+request.GET['id'],
                             data=json.dumps(json_payload),
                             headers=headers)
        if response.status_code in (201, 200):
                print(response.text)
                logging.info(response.text)
        else:
                logging.error(response.text)

        return render(request, 'guiscim/usuario.html')



def criar_usuario(request):
	token = get_token(keystone_url)
	#print(request.GET['nome'])

	json_payload_project = {

        "project": {
	        "description":request.GET['nome']+ " cloud",
	        "domain_id": "default",
	        "enabled": True,
	        "is_domain": True,
	        "name": request.GET['nome'] + "Cloud",
	        "is_cloud_project": False
    	}

    }

	headers_project = {'X-Auth-Token': token, 'Content-Type': 'application/json'}
	response_project = requests.post(url=keystone_url +'/v3/projects/',
                             data=json.dumps(json_payload_project),
                             headers=headers_project)
	if response_project.status_code in (201, 200):
		print(response_project.text)
		logging.info(response_project.text)
	else:
		logging.error(response_project.text)

	resposta = response_project.text.split("\"")

	json_payload = {
				    "user": {
				        "default_project_id": resposta[21],
				        "domain_id": "default",
				        "enabled": True,
				        "name": request.GET['nome'],
				        "password": request.GET['senha'],
				        "username": request.GET['nome']
				    }
				}


	headers = {'X-Auth-Token': token, 'Content-Type': 'application/json'}
	response = requests.post(url=keystone_url +'/v3/users',
                             data=json.dumps(json_payload),
                             headers=headers)
	if response.status_code in (201, 200):
		print(response.text)
		logging.info(response.text)
	else:
		logging.error(response.text)

	papel_usuario_keystone_criacao(request,request.GET['nome'],resposta[21])
	return render(request, 'guiscim/usuario.html')

def create_role(requests):
	#de451a346ffd4f07b5e29b5607d8c095
	token = get_token(keystone_url)
	json_payload = {

        "role": {
        	"name": "donos",
        	"application_id": "4e1e3ca1c13846f7a184cf80ef2bb425"
   		 }

    }

	headers = {'X-Auth-Token': token, 'Content-Type': 'application/json'}
	response = requests.post(url=keystone_url +'/v3/roles',
                             data=json.dumps(json_payload),
                             headers=headers)
	if response.status_code in (201, 200):
		print(response.text)
		logging.info(response.text)
	else:
		logging.error(response.text)

	return redirect('guiscim/index.html')


def deletar_usuario(request):

	token = get_token(keystone_url)
	headers = {'X-Auth-token': token}

	response = requests.delete(url=keystone_url + '/v3/users/' + request.GET['nick_del'],
                               headers=headers)

	if response.status_code in (201, 200):
		parsed = json.loads(response.text)
		logging.info(json.dumps(parsed, indent=4, sort_keys=True))
		return parsed
	else:
		logging.error('DELETE USER ### ' + response.text)

	return render(request, 'guiscim/usuario.html')

def habilitar_usuario(request):
	token = get_token(keystone_url)
	usuario = request.GET['nickh']
	headers = {'X-Auth-token': token}

	response = requests.get(url=keystone_url + '/v3/OS-REGISTRATION/users/'+ usuario +'/activate',
                               headers=headers)
	print(response.text)
	print(response.text[27]+response.text[28])

	resposta = response.text.split("\"")

	ch_ativ = resposta[5]

	print(ch_ativ)
	return redirect("http://10.7.52.41:8000/activate/?activation_key="+ ch_ativ + "&amp;user=" + usuario)

def papel_usuario_keystone(request):
	token = get_token(keystone_url)
	headers = {'X-Auth-token': token}

	response = requests.put(
        url=keystone_url + '/v3/projects/'+ request.GET['a1'] +'/users/'+ request.GET['c1'] +'/roles/'+request.GET['p1']+'/',
        headers=headers)

	if response.status_code in (201, 200):
		parsed = json.loads(response.text)
		logging.info(json.dumps(parsed, indent=4, sort_keys=True))
		return parsed
	else:
		logging.error('PUT ROLE IN USER ### ' + response.text)

	return render(request, 'guiscim/projeto.html')

def papel_usuario_keystone_criacao(request, usuario, projeto):
	token = get_token(keystone_url)
	headers = {'X-Auth-token': token}

	response = requests.put(
        url=keystone_url + '/v3/projects/'+ projeto +'/users/'+ usuario +'/roles/b2fe80ff35df41af930f8c018620093e/',
        headers=headers)

	if response.status_code in (201, 200):
		parsed = json.loads(response.text)
		logging.info(json.dumps(parsed, indent=4, sort_keys=True))
		return parsed
	else:
		logging.error('PUT ROLE IN USER ### ' + response.text)

	return render(request, 'guiscim/usuario.html')


def papel_usuario(request):

	token = get_token(keystone_url)
	headers = {'X-Auth-token': token}

	response = requests.put(
        url=keystone_url + '/v3/OS-ROLES/users/'+request.GET['nick_c']+'/applications/'+request.GET['nick_a'] +'/roles/'+request.GET['nick_p']+'/',
        headers=headers)

	if response.status_code in (201, 200):
		parsed = json.loads(response.text)
		logging.info(json.dumps(parsed, indent=4, sort_keys=True))
		return parsed
	else:
		logging.error('PUT ROLE IN USER ### ' + response.text)

	return render(request, 'guiscim/papel.html')

def deletar_permissao(request):

	token = get_token(keystone_url)

	headers = {'X-Auth-token': token}

	response = requests.delete(url=keystone_url + '/v3/OS-ROLES/permissions/' + request.GET['nick_per'],
                               headers=headers)

	if response.status_code in (201, 200):
		parsed = json.loads(response.text)
		logging.info(json.dumps(parsed, indent=4, sort_keys=True))
		return parsed
	else:
		logging.error('LIST ROLE ORGANIZATION ### ' + response.text)
		return render(request, 'guiscim/papel.html')

def listar_usuarios(request):

	return render(request, 'guiscim/usuarios_listados.html')
	#caso precise fazer a pagina nova 

	
def usuarios_listados(request):

	logging.basicConfig(filename='script-keyrock.log', filemode='w', level=logging.DEBUG)

	token = get_token(keystone_url)

	headers = {'X-Auth-token': token}

	response = requests.get(url=keystone_url + '/v3/OS-SCIM/v2/Users/',
                            headers=headers)

	if response.status_code in (201, 200):
		parsed = json.loads(response.text)
		logging.info(json.dumps(parsed, indent=4, sort_keys=True))
		data = json.dumps(parsed, indent=4, sort_keys=True)
		data_conteudo = HttpResponse(data, "application/json")
		logging.info(json.dumps(parsed, indent=4, sort_keys=True))
		return HttpResponse(data, "application/json")
	else:
		logging.error('LIST USERS ### ' + response.text)
		return render(request, 'guiscim/usuario.html')

def usuarios_listados_keystone(request):

	logging.basicConfig(filename='script-keyrock.log', filemode='w', level=logging.DEBUG)
	logging.debug('starting...')

	token = get_token(keystone_url)

	headers = {'X-Auth-token': token}

	response = requests.get(url=keystone_url + '/v3/users/',
                            headers=headers)

	if response.status_code in (201, 200):
		parsed = json.loads(response.text)
		logging.info(json.dumps(parsed, indent=4, sort_keys=True))
		data = json.dumps(parsed, indent=4, sort_keys=True)
		data_conteudo = HttpResponse(data, "application/json")
		logging.info(json.dumps(parsed, indent=4, sort_keys=True))
		return HttpResponse(data, "application/json")
	else:
		logging.error('LIST USERS ### ' + response.text)
		return render(request, 'guiscim/usuario.html')

def list_organizations(request):

	logging.basicConfig(filename='script-keyrock.log', filemode='w', level=logging.DEBUG)
	token = get_token(keystone_url)

	headers = {'X-Auth-token': token}
	response = requests.get(url=keystone_url + '/v3/OS-SCIM/v2/Organizations', headers=headers)
	
	if response.status_code in (201, 200):
		parsed = json.loads(response.text)
		logging.info(json.dumps(parsed, indent=4, sort_keys=True))
		data = json.dumps(parsed, indent=4, sort_keys=True)
		data_conteudo = HttpResponse(data, "application/json")
		logging.info(json.dumps(parsed, indent=4, sort_keys=True))
		return HttpResponse(data, "application/json")
	else:
		logging.error('LIST ORGANIZATIONS ### ' + response.text)
		return render(request, 'guiscim/projeto.html')

def list_projects(request):

	logging.basicConfig(filename='script-keyrock.log', filemode='w', level=logging.DEBUG)
	token = get_token(keystone_url)

	headers = {'X-Auth-token': token}
	response = requests.get(url=keystone_url + '/v3/projects', headers=headers)
	
	if response.status_code in (201, 200):
		parsed = json.loads(response.text)
		logging.info(json.dumps(parsed, indent=4, sort_keys=True))
		data = json.dumps(parsed, indent=4, sort_keys=True)
		data_conteudo = HttpResponse(data, "application/json")
		logging.info(json.dumps(parsed, indent=4, sort_keys=True))
		return HttpResponse(data, "application/json")
	else:
		logging.error('LIST PROJECTS ### ' + response.text)
		return render(request, 'guiscim/index.html')

def list_permissions(request):
	
	logging.basicConfig(filename='script-keyrock.log', filemode='w', level=logging.DEBUG)
	token = get_token(keystone_url)

	headers = {'X-Auth-token': token}
	response = requests.get(url=keystone_url + '/v3/OS-ROLES/permissions', headers=headers)
	
	if response.status_code in (201, 200):
		parsed = json.loads(response.text)
		logging.info(json.dumps(parsed, indent=4, sort_keys=True))
		data = json.dumps(parsed, indent=4, sort_keys=True)
		data_conteudo = HttpResponse(data, "application/json")
		logging.info(json.dumps(parsed, indent=4, sort_keys=True))
		return HttpResponse(data, "application/json")
	else:
		logging.error('LIST PERMISSIONS ### ' + response.text)
		return render(request, 'guiscim/papel.html')

def list_roles_in_organization(request):

	#Erro na API, no site nao contem a parte de headers
	logging.basicConfig(filename='script-keyrock.log', filemode='w', level=logging.DEBUG)
	token = get_token(keystone_url)
	headers = {'X-Auth-token': token}

	response = requests.get(url=keystone_url + '/v3/OS-ROLES/organizations/role_assignments', headers=headers)

	if response.status_code in (201, 200):
		parsed = json.loads(response.text)
		logging.info(json.dumps(parsed, indent=4, sort_keys=True))
		data = json.dumps(parsed, indent=4, sort_keys=True)
		data_conteudo = HttpResponse(data, "application/json")
		logging.info(json.dumps(parsed, indent=4, sort_keys=True))
		return HttpResponse(data, "application/json")
	else:
		logging.error('LIST ROLES IN ORGANIZATION ### ' + response.text)
		return render(request, 'guiscim/projeto.html')

def papeis_usuarios(request):

	token = get_token(keystone_url)
	headers = {'X-Auth-token': token}

	response = requests.get(url=keystone_url + '/v3/OS-ROLES/users/role_assignments', headers=headers)

	if response.status_code in (201, 200):
		parsed = json.loads(response.text)
		logging.info(json.dumps(parsed, indent=4, sort_keys=True))
		data = json.dumps(parsed, indent=4, sort_keys=True)
		data_conteudo = HttpResponse(data, "application/json")
		logging.info(json.dumps(parsed, indent=4, sort_keys=True))
		return HttpResponse(data, "application/json")
	else:
		logging.error('LIST ROLES AND USERS ### ' + response.text)
		return render(request, 'guiscim/usuario.html')

def papeis_listar(request):

	token = get_token(keystone_url)
	headers = {'X-Auth-token': token}

	response = requests.get(url=keystone_url + '/v3/roles', headers=headers)

	if response.status_code in (201, 200):
		parsed = json.loads(response.text)
		logging.info(json.dumps(parsed, indent=4, sort_keys=True))
		data = json.dumps(parsed, indent=4, sort_keys=True)
		data_conteudo = HttpResponse(data, "application/json")
		logging.info(json.dumps(parsed, indent=4, sort_keys=True))
		return HttpResponse(data, "application/json")
	else:
		logging.error('LIST ROLES' + response.text)
		return render(request, 'guiscim/papel.html')

