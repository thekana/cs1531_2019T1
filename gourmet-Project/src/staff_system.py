'''
StaffSystem: a system used by staff, which should be able to manage online orders and update the inventory.
'''

class StaffSystem(object):

    def __init__(self): #staff:dict):
        self._staff = []    #list of staff members
      #  self._staff_details = staff_details
        self._is_authenticated = False

    
    # Simulate login & logout (this will be different when using Flask and Flask-login)
    def login(self, username, password):
        for staff_member in self._staff:
            if staff_member.authenticate(username, password):
                self._is_authenticated = True
                return True
        return False


    def add_staff(self, username, password):
        for staff_member in self._staff:
            if username == staff_member.username:
                print('User-name already taken, please enter another username')
                return
        new_staff = Staff(username,password)
        self._staff.append(new_staff)

    def logout(self):
        self._is_authenticated = False


    @property
    def is_authenticated(self):
        return self._is_authenticated
    
    @property
    def staff_details(self):
        return self.staff_details


class Staff(object):

    def __init__(self, username, password):
        self._username = username
        self._password = password


    def authenticate(self, username, password):
        if (self._username == username and self._password == password):
            return True
        else:
            return False
    @property
    def username(self):
        return self._username
