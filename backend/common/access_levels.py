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
    unconfirmed = (2, 'Unconfirmed')
    participant = (3, 'Participant')
    creator = (4, 'Creator')
    admin = (5, 'Admin')
    system = (6, 'System')
