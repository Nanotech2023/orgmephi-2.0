import enum


class OrgMephiAccessLevel(enum.Enum):
    """
    Access level enum

    Attributes:

    visitor: unauthenticated user

    participant: regular participant, i.e. school or university student

    creator: contest creator, supposedly university staff

    admin: administrator

    system: used for requests from other services and inner requests
    """
    visitor = (1, None)
    participant = (2, 'Participant')
    creator = (3, 'Creator')
    admin = (4, 'Admin')
    system = (5, 'System')
