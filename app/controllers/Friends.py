from system.core.controller import *
from datetime import datetime, timedelta

class Friends(Controller):
    def __init__(self, action):
        super(Friends, self).__init__(action)
        self.load_model('Friend')
        self.db = self._app.db

    def index(self):

        return self.load_view('index.html')

    def login(self):
        login_info = self.models['Friend'].login_user(request.form)
        print login_info
        if 'logged_info' in login_info:
            session['logged_info'] = login_info['logged_info']
            return redirect('/view_friends')
        else:
            flash(login_info)
            return redirect('/')

    def register(self):
        reg_info = self.models['Friend'].register_user(request.form)
        if reg_info == "registered":
            flash({'registered': "Thank you for registering, please log in."})
        else:
            flash(reg_info)
        return redirect('/')

    def view_friends(self):
        friend_info = self.models['Friend'].view_friend_list(session['logged_info']['id'])
        return self.load_view('friends_list.html', friend_info = friend_info)

    def add_friends(self, id):
        self.models['Friend'].add_friend(session['logged_info']['id'], id)
        return redirect('view_friends')

    def remove_friends(self, id):
        self.models['Friend'].remove_friend(session['logged_info']['id'], id)
        return redirect('view_friends')

    def get_users(self, id):
        user_info = self.models['Friend'].get_user(id)
        return self.load_view('user.html', user_info = user_info[0]) 

    def logout(self):
        session.clear()
        return redirect('/')