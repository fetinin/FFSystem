import enum


@enum.unique
class Roles(enum.Enum):
    admin = 'admin'
    lancer = 'lancer'
    employer = 'employer'


@enum.unique
class Statuses(enum.Enum):
    open = 'open'
    in_progress = 'in_progress'
    verification = 'verification'
    on_rework = 'on_rework'
    deploying = 'deploying'
    waiting_payment = 'waiting_payment'
    closed = 'closed'