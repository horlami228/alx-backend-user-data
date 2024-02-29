#!/usr/bin/env python3

"""Module for expiration session"""
from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Inherits from SessionAuth"""

    def __init__(self):
        """Initilize with expiration time"""
        duration = os.getenv("SESSION_DURATION")
        try:
            if duration is not None:
                if not isinstance(duration, int):
                    duration = int(duration)
            else:
                duration = 0
        except Exception:
            duration = 0
        self.session_duration = duration

    def create_session(self, user_id=None):
        """Create a session and return the session ID"""
        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary

        return session_id

    def user_id_for_session_id(self, session_id: str = None):
        """Return the User ID based on the Session ID"""

        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None

        if self.session_duration <= 0:
            return self.user_id_by_session_id.get(session_id).get("user_id")

        created_at = self.user_id_by_session_id.get(
            session_id).get("created_at")

        if created_at is None:
            return None

        expiration_time = created_at + timedelta(seconds=self.session_duration)
        current_time = datetime.now()

        if expiration_time < current_time:
            return None

        return self.user_id_by_session_id.get(session_id).get("user_id")
