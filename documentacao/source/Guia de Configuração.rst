Guia de Configuração
====================

Após efetuar os passos da instalação é necessário configurar o ambiente para que possamos executar a aplicação desejada.

- No arquivo config.js disponível em Example-Application-Security/security-components/fiware-pep-proxy/files mude as linhas.::

	config.app_host = 'IP-APP';
	config.username = 'ID-PEPPROXY-FIWARE';
	config.password = 'SENHA-PEPPROXY';

Lembrando que as informações do pepproxy é possível recuperar na interface do fiware lab

- Escolha a aplicação que possui as configurações que deseja utilizar
- Após escolhida a aplicação, abra o arquivo oauth_fiware.py disponível em Example-Application-Security/Python/APLICAÇÃO-ESCOLHIDA/securityapp-ui faça as seguintes modificações.::
	
	self.client_id = 'ID-APP-FIWARE'  
        self.client_secret = 'ID-SECRET-APP-FIWARE'

- Posteriormente é necessário mudar as seguintes linhas.::

	self.redirect_uri = 'http://IP-APP:5055/auth' ;

        self.proxy_address = "http://IP-APP:80/" ;
        self.idm_address = 'http://IP-APP:8000/' ;
