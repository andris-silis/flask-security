import json
import re
from flask.ext.script import Command, Option
from flask.ext.security import (UserCreationError, UserNotFoundError, 
                                RoleNotFoundError, user_datastore) 

def pprint(obj):
    print json.dumps(obj, sort_keys=True, indent=4)

class CreateUserCommand(Command):
    """Create a user"""
    
    option_list = (
        Option('-u', '--username', dest='username', default=None),
        Option('-e', '--email',    dest='email',    default=None),
        Option('-p', '--password', dest='password', default=None),
        Option('-a', '--active',   dest='active',   default=''),
        Option('-r', '--roles',    dest='roles',    default=''),
    )

    def run(self, **kwargs):
        # sanitize active input
        ai = re.sub(r'\s', '', str(kwargs['active']))
        kwargs['active'] = ai.lower() in ['', 'y','yes', '1', 'active']
        
        # sanitize role input a bit
        ri = re.sub(r'\s', '', kwargs['roles'])
        kwargs['roles'] = [] if ri == '' else ri.split(',')
        
        user_datastore.create_user(**kwargs)
        
        print 'User created successfully.'
        kwargs['password'] = '****'
        pprint(kwargs)

        
class AddRoleCommand(Command):
    """Add a role to a user"""
    
    option_list = (
        Option('-u', '--user', dest='user_identifier'),
        Option('-r', '--role', dest='role_name'),
    )
    
    def run(self, user_identifier, role_name):
        user_datastore.add_role_to_user(user_identifier, role_name)
        print "Role '%s' added to user '%s' successfully" % (role_name, user_identifier)
        
class RemoveRoleCommand(Command):
    """Add a role to a user"""
    
    option_list = (
        Option('-u', '--user', dest='user_identifier'),
        Option('-r', '--role', dest='role_name'),
    )
    
    def run(self, user_identifier, role_name):
        user_datastore.remove_role_from_user(user_identifier, role_name)
        print "Role '%s' removed from user '%s' successfully" % (role_name, user_identifier)
        
            
class DeactiveUserCommand(Command):
    """Deactive a user"""
        
    option_list = (
        Option('-u', '--user', dest='user_identifier'),
    )
    
    def run(self, user_identifier):
        user_datastore.deactive_user(user_identifier)