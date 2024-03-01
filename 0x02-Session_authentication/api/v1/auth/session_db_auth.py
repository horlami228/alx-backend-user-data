#!/usr/bin/env python3

"""Session DB Auth module"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import timedelta, datetime
from flask import request


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth Class"""

    def create_session(self, user_id=None):
        """Create a session in the database"""
        if user_id is None:
            return None

        session_id = super().create_session(user_id)
        print(session_id)
        session = UserSession(user_id=user_id, session_id=session_id)
        print(session.session_id)
        session.save()
        UserSession.save_to_file()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns a User ID based on a Session ID"""

        if session_id is None:
            return None
        UserSession.load_from_file()
        user_session = UserSession.search({"session_id": session_id})

        if user_session and user_session != []:

            if self.session_duration <= 0:
                return user_session[0].id

            created_at = user_session[0].created_at

            if created_at is None:
                return None

            expiration_time = created_at + \
                timedelta(seconds=self.session_duration)
            current_time = datetime.now()

            if expiration_time < current_time:
                self.destroy_session(request)
                return None

            return user_session[0].user_id

        return None

    def destroy_session(self, request=None):
        """Deletes the user session / log out"""
        if request is None:
            return False

        session_id = self.session_cookie(request)

        if session_id:
            user_session = UserSession.search({"session_id": session_id})

            if user_session and user_session != []:
                user_session[0].remove()
                UserSession.save_to_file()
                return True
            return False

        return False
