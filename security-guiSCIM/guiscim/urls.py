from django.conf.urls import url

from . import views

app_name = 'guiscim'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^atualizar_usuario$', views.atualizar_usuario, name='atualizar_usuario'),
    url(r'^criar_usuario$', views.criar_usuario, name='criar_usuario'),
    url(r'^deletar_usuario$', views.deletar_usuario, name='deletar_usuario'),
    url(r'^habilitar_usuario$', views.habilitar_usuario, name='habilitar_usuario'),
    url(r'^papel_usuario$', views.papel_usuario, name='papel_usuario'),
    url(r'^deletar_permissao$', views.deletar_permissao, name='deletar_permissao'),
    url(r'^index1$', views.index1, name='index1'),
    url(r'^listar_usuarios$', views.listar_usuarios, name='listar_usuarios'),
    url('papel.html', views.papel, name='papel'),
    url('projeto.html', views.projeto, name='projeto'),
    url('usuario.html', views.usuario, name='usuario'),
    url(r'^autentica$', views.autentica, name='autentica'),
    url(r'^usuarios_listados$', views.usuarios_listados, name='usuarios_listados'),
    url(r'^usuarios_listados_keystone$', views.usuarios_listados_keystone, name='usuarios_listados_keystone'),
    url(r'^list_organizations$', views.list_organizations, name='list_organizations'),
    url(r'^list_permissions$', views.list_permissions, name='list_permissions'),
    url(r'^list_projects$', views.list_projects, name='list_projects'),
    url(r'^list_roles_in_organization$', views.list_roles_in_organization, name='list_roles_in_organization'),
    url(r'^papel_usuario_keystone$', views.papel_usuario_keystone, name='papel_usuario_keystone'),
    url(r'^papeis_usuarios$', views.papeis_usuarios, name='papeis_usuarios'),
    url(r'^papeis_listar$', views.papeis_listar, name='papeis_listar'),
    url(r'^auth$', views.auth, name='auth'),


]
