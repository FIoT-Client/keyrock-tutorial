Preparando o Ambiente:
^^^^^^^^^^^^^^^^^^^^^^

Antes de Começar
==================

Antes de colocar alguma aplicação em execução é necessário efetuar o guia sobre a infraestrutura disponível na pasta de `infraestrutura
<https://github.com/FIoT-Client/keyrock-tutorial/tree/master/security-componets>`_


Guia de Configuração
====================

Após efetuar os passos anteriores realize as seguintes configurações:

- Escolha a aplicação que deseja executar, veja as arquiteturas das aplicações em cada pasta das aplicações para escolher qual utilizar
- Após escolher entre na pasta.::

	APLICACAO-DESEJADA/securityapp-ui/web


- No arquivo oauth_fiware.py modifique as seguintes linhas com os valores gerados pela aplicação que você criou anteriormente no keyrock.::
	
	self.client_id = 'ID-APP-FIWARE'  
        self.client_secret = 'ID-SECRET-APP-FIWARE'

- Posteriormente é necessário mudar as seguintes linhas.::

	self.redirect_uri = 'http://IP-APP:5055/auth' ;

        self.proxy_address = "http://IP-APP:80/" ;
        self.idm_address = 'http://IP-APP:8000/' ;

- Volte para a configuração da `infraestrutura <https://github.com/FIoT-Client/keyrock-tutorial/tree/master/security-componets>`_ e siga a última parte do tutorial de configuração, que fala do arquivo config.js. Refaça também o guia de execução disponível no mesmo link.

Guia de Execução
================

- Após efetuar os passos da configuração, volte para a pasta keyrock-tutorial/security-tutorial/<APP-DESEJADA>/securityapp-ui e efetue o comando.::

	sudo docker-compose build && sudo docker-compose up

- Posteriormente ir na pasta.:: 

	APLICACAO-DESEJADA/securityapp-ui

- Efetuar o comando.::
	
	sudo docker-compose build && sudo docker-compose up

- Após esses passos repita o mesmo processo dentro da pasta.::

	APLICACAO-DESEJADA/securityapp-rest

