"""
Domain Enums for Test Case Generator Agent.
"""

from enum import Enum


class TestCaseType(str, Enum):
    __test__ = False
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"
    VALIDATION = "VALIDATION"
    BOUNDARY = "BOUNDARY"



class Category(str, Enum):
    FUNCTIONAL = "FUNCTIONAL"
    BUSINESS_RULE = "BUSINESS_RULE"
    VALIDATION = "VALIDATION"
    ERROR_HANDLING = "ERROR_HANDLING"
    BOUNDARY = "BOUNDARY"


class Priority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Status(str, Enum):
    NEW = "NEW"
    READY = "READY"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"


class Confidence(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
