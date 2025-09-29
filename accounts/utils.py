def role_check(user, allowed_roles):
    """
    Utility function to check if a user has one of the allowed roles.
    """
    return getattr(user, 'role', None) in allowed_roles