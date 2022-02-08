
class User:
    def __init__(self, name, gmail, picture_url):
        self.name = name
        self.gmail = gmail
        self.picture_url = picture_url

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, User):
            return self.name == other.name and self.gmail == other.gmail and self.picture_url == other.picture_url    
        return False



# {u'picture': u'https://lh3.googleusercontent.com/a-/AOh14GirG6l9tljR2Bj0V1ZlJn9immSTnHStFjldw7_8pB8=s96-c', u'sub': u'102115511141434029046', u'name': u'Ken Power', u'family_name': u'Power', u'iss': u'https://accounts.google.com', u'email_verified': True, u'nbf': 1639349541, u'jti': u'4f879a7e0d893322d25ba5266ca71ebf11e9c4e8', u'given_name': u'Ken', u'exp': 1639353441, u'azp': u'633569390265-fnap71ikinh8ue861eobkurui4jk0o0s.apps.googleusercontent.com', u'iat': 1639349841, u'email': u'k3np0w3r@gmail.com', u'aud': u'633569390265-fnap71ikinh8ue861eobkurui4jk0o0s.apps.googleusercontent.com'}