Preparando o Ambiente:
^^^^^^^^^^^^^^^^^^^^^^

Antes de Começar
==================

Antes de colocar alguma aplicação em execução é necessário efetuar o guia sobre a infraestrutura disponível na pasta de `infraestrutura
<https://github.com/FIoT-Client/keyrock-tutorial/tree/master/security-componets>`_

Guia de Criação
================

- Para prosseguir com esse tutorial é necessário ter executado o tutorial anterior, acessar o endereço do <IP-Máquina>:8000 e acessar a interface do keyrock. Para acessar a interface de administrador acesse com usuário: idm e senha: idm.
 
- Ao entrar na conta de administrador cadastre uma nova aplicação seguindo as instruções abaixo:
 
- Para registrar uma aplicação clique no botão "register" como mostra a figura abaixo: 
.. image:: imagens/registro-app.png
- Então siga os três passos para concluir o registro, inicialmente cadastre o nome da aplicação, sua descrição, a url da aplicação e a url de redirecionamento onde o token de usuário será enviado.
.. image:: imagens/info-registro.png
- Aperte em "next" e escolha uma imagem para a aplicação, essa imagem é opcional
.. image:: imagens/exibir-aplicacao.png
- Por fim, identifique a política de acesso para a sua aplicação, você poderá criar novas permissões e papéis através dessa interface.
.. image:: imagens/developer-portal.png    
- Após o término da configuração teremos essa página:
.. image:: imagens/infos-cadastradas.png
Onde as informações de client secret serão usuadas na sua aplicação. Na mesma página gere um PEP-Proxy, e use suas credenciais na sua aplicação também, essas informações devem ser editadas no guia de configuração.

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

