# hr/ldap_auth.py

from ldap3 import Server, Connection, ALL
from ldap3.core.exceptions import LDAPBindError, LDAPSocketOpenError  # Specific exceptions
from django.contrib.auth.backends import BaseBackend


class LDAPBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Your LDAP authentication logic here
        try:
            server = Server('your_ldap_server', get_info=ALL)
            conn = Connection(server, f"uid={username},ou=users,dc=example,dc=com", password=password, auto_bind=True)
            if conn.bind():
                return self.get_user(username)
        except Exception as e:
            print(f"LDAP authentication failed: {e}")
        return None

    def get_user(self, username):
        # Get or create a user from the database
        from django.contrib.auth.models import User
        user, created = User.objects.get_or_create(username=username)
        return user


def ldap_connect():
    try:
        # Initialize server and connection objects
        server = Server('your_ldap_server', get_info=ALL)
        conn = Connection(server, 'your_ldap_user_dn', 'your_ldap_password', auto_bind=True)
        return conn
    except LDAPBindError as e:
        print(f"LDAP bind error: {e}")
    except LDAPSocketOpenError as e:
        print(f"Error opening LDAP socket: {e}")
    except Exception as e:  # General exception handling
        print(f"Failed to connect to LDAP server: {e}")
    return None
