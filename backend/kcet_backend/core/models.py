# This file is the "bridge" between Django and your modular model layout

from core.infrastructure.django_models.colleges import College
from core.infrastructure.django_models.Branch import Branch
from core.infrastructure.django_models.category import Category
from core.infrastructure.django_models.Branch_college import CollegeBranch
from core.infrastructure.django_models.Round import Round
from core.infrastructure.django_models.Year import Year
from core.infrastructure.django_models.Cutoff import Cutoff
from core.infrastructure.django_models.seat_matrix import SeatMatrix
from core.infrastructure.django_models.communication import ApprovedGmail,ChatLog, Subscriber, ApprovedGmail
from core.infrastructure.django_models.security import UserProfile
from core.infrastructure.django_models.security import UserRole
__all__ = [
    "College",
    "Branch",
    "Category",
    "CollegeBranch",
    "Round",
    "Year",
    "Cutoff",
    "SeatMatrix",
    "ApprovedGmail",
    "ChatLog",  
    "Subscriber",
]
