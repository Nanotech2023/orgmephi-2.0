import enum


class OrgMephiAccessLevel(enum.Enum):
    visitor = (1, None)
    participant = (2, 'Participant')
    creator = (3, 'Creator')
    admin = (4, 'Admin')
    system = (5, 'System')