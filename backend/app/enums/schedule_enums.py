"""
Schedule-related enums only.
Single Responsibility: Schedule domain constants.
"""

from enum import Enum


class ScheduleStatus(str, Enum):
    """Schedule execution status"""
    PLANNED = "planned"
    SCHEDULED = "scheduled"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    PARTIALLY_COMPLETED = "partially_completed"
    CANCELLED = "cancelled"
    DELAYED = "delayed"
    FAILED = "failed"
    RESCHEDULED = "rescheduled"


class AssignmentStatus(str, Enum):
    """Real-time assignment status"""
    PLANNED = "planned"
    ASSIGNED = "assigned"
    ACKNOWLEDGED = "acknowledged"
    EN_ROUTE = "en_route"
    ON_SITE = "on_site"
    IN_PROGRESS = "in_progress"
    BREAK = "break"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REASSIGNED = "reassigned"
    NO_SHOW = "no_show"


class EventType(str, Enum):
    """Calendar event types for scheduling"""
    REGULAR_WEEK = "regular_week"
    HOLIDAY_WEEK = "holiday_week"
    LARGE_ITEM_WEEK = "large_item_week"
    LEAF_YARD_WEEK = "leaf_yard_week"
    CHRISTMAS_TREE_WEEK = "christmas_tree_week"
    SPRING_CLEANUP = "spring_cleanup"
    FALL_CLEANUP = "fall_cleanup"
    SNOW_REMOVAL = "snow_removal"
    EMERGENCY_CLEANUP = "emergency_cleanup"
    MAINTENANCE_WEEK = "maintenance_week"
    ROUTE_OPTIMIZATION = "route_optimization"


class VehicleType(str, Enum):
    """Vehicle types for assignments"""
    REAR_LOAD = "rear_load"
    FRONT_LOAD = "front_load"
    SIDE_LOAD = "side_load"
    ROLL_OFF = "roll_off"
    SPLIT_BODY = "split_body"
    LEAF_YARD_TRUCK = "leaf_yard_truck"
    SNOW_PLOW = "snow_plow"
    SWEEPER = "sweeper"
    PICKUP_TRUCK = "pickup_truck"
    SUPERVISOR_VEHICLE = "supervisor_vehicle"


class RouteStatus(str, Enum):
    """Route operational status"""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    MAINTENANCE = "maintenance"
    SEASONAL = "seasonal"
    UNDER_REVIEW = "under_review"
    DECOMMISSIONED = "decommissioned"


class WeekDay(str, Enum):
    """Days of the week"""
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"