FROM ging/fiware-idm

ADD files/local_settings.py ../horizon/openstack_dashboard/local/local_settings.py

# Arquivo criado para consertar a versão do policy_properties.xacml que está incompatível com a atual.

ADD files/rules.xacml ../horizon/openstack_dashboard/templates/access_control/policy_properties.xacml

# Arquivo para concertar outro erro no caso onde temos roles.id seria roles_id

ADD files/policy.xacml ../horizon/openstack_dashboard/templates/access_control/policy.xacml

