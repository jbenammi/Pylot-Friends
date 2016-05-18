from system.core.model import Model
import re
from datetime import datetime, timedelta

EMAILREGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
class Friend(Model):
    def __init__(self):
        super(Friend, self).__init__()

    def register_user(self, reginfo):
        errors = {}
        b_date = reginfo['birthdate']
        now = datetime.today()
        legal_date = now - timedelta(days=6570)         
        if b_date == '':
            errors.update({'birthdate': 'Birthdate is required' })
        else:
            b_date = datetime.strptime(reginfo['birthdate'], "%Y-%m-%d")
            if legal_date<b_date:
                errors.update({'birthdate': 'You must be at least 18 years old to register' })
        if len(reginfo['name']) < 2:
            errors.update({'name': 'The name field must be at least two characters'})
        if len(reginfo['alias']) < 2:
            errors.update({'alias': 'The alias field must be at least two characters'})
        if not EMAILREGEX.match(reginfo['email']):
            errors.update({'email': 'The E-Mail must be a valid e-mail address'})
        if len(reginfo['password']) < 8:
            errors.update({'password': 'Password must be at least 8 characters'})
        elif not any(char.isdigit() for char in str(reginfo['password'])):
            errors.update({'password': 'Password must contain at least one number'})
        elif not any(char.isupper() for char in str(reginfo['password'])):
            errors.update({'password': 'Password must contain at least one uppercase letter'})
        if reginfo['confirmpass'] != reginfo['password']:
            errors.update({'confirmpass': 'The password confirmation does not match the password'})
        if len(errors) > 0:
            return errors
        else:
            query1 = "SELECT email FROM users WHERE email = :email"
            data1 = {"email": reginfo['email']}
            if not self.db.query_db(query1, data1):
                pw_hash = self.bcrypt.generate_password_hash(reginfo['password'])
                query = "INSERT INTO users(name, alias, email, password, birthdate, created_on, updated_on) VALUES(:name, :alias, :email, :password, :birthdate, now(), now())"
                info = {
                "name": reginfo['name'],
                "alias": reginfo['alias'],
                "email": reginfo['email'],
                "password": pw_hash,
                "birthdate": reginfo['birthdate']
                }
                self.db.query_db(query, info)
                return "registered"
            else:
                errors.update({'user_registered': 'This E-Mail is already registered'})
                return errors

    def login_user(self, loginfo):
        errors = {}
        if not EMAILREGEX.match(loginfo['email']):
            errors.update({'email2': 'The E-Mail must be a valid e-mail address'})
        if len(loginfo['password']) < 8:
            errors.update({'password2': 'Password must be at least 8 characters'})
        if len(errors) > 0:
            return errors
        else:
            query = "SELECT * FROM users WHERE email = :email LIMIT 1"
            data = {'email': loginfo['email']}
            user = self.db.query_db(query, data)
            if user == []:
                errors.update({'notreg': 'E-Mail is not registered.'})
                return errors
            else:
                if self.bcrypt.check_password_hash(user[0]['password'], loginfo['password']):
                    logged_info = {'logged_info':{'id': user[0]['id'], 'name': user[0]['name'], 'alias': user[0]['alias']}}
                    return logged_info
                else:
                    errors.update({'passmatch': 'Incorrect password entered for registered E-Mail.'})
                    return errors

    def add_friend(self, fr1, fr2):
        query1 = "INSERT INTO friends(friend1_id, friend2_id, created_on, updated_on) VALUES(:id1,:id2, now(), now())"
        query2 = "INSERT INTO friends(friend1_id, friend2_id, created_on, updated_on) VALUES(:id2,:id1, now(), now())"
        data = {
                'id1': fr1,
                'id2': fr2
                }
        self.db.query_db(query1, data)
        self.db.query_db(query2, data)

    def remove_friend(self, fr1, fr2):
        query = "DELETE FROM friends WHERE friend1_id = :id1 AND friend2_id = :id2 OR friend1_id = :id2 AND friend2_id = :id1;"
        data = {
            'id1': fr1,
            'id2': fr2
            }
        self.db.query_db(query, data)

    def view_friend_list(self, id):
        query1 = "SELECT users2.id as u2_id, users2.alias as u2_alias FROM friends LEFT JOIN users on friends.friend1_id = users.id LEFT JOIN users as users2 on users2.id = friends.friend2_id WHERE friend1_id = :id"
        query2 = "SELECT DISTINCT users.id as u_id, users.alias as u_alias FROM users LEFT JOIN friends on friends.friend1_id = users.id LEFT JOIN users as users2 on users2.id = friends.friend2_id WHERE NOT users.id IN(SELECT users2.id as u2_id FROM friends LEFT JOIN users on friends.friend1_id = users.id LEFT JOIN users as users2 on users2.id = friends.friend2_id WHERE users.id = :id)"
        data = {'id': id}

        cur_friends = self.db.query_db(query1, data)
        non_friends = self.db.query_db(query2, data)
        return [cur_friends, non_friends]

    def get_user(self, id):
        query = "SELECT name, alias, email, birthdate from users WHERE id = :id"
        data = {'id': id}
        return self.db.query_db(query, data)