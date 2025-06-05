"""
Organization API endpoints only.
Single Responsibility: Organization HTTP API routing.
"""

import uuid
from datetime import date
from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..config.database import get_session
from ..services.organization_service import OrganizationService
from ..schemas.organization_schemas import (
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationResponse,
    CapacityStatusResponse
)
from ..schemas.base_schemas import PaginatedResponse, SuccessResponse
from ..enums.system_enums import ComplianceStatus

router = APIRouter()


def get_organization_service(
    session: AsyncSession = Depends(get_session)
) -> OrganizationService:
    """
    Dependency to get organization service.
    Single Responsibility: Service dependency injection.
    """
    return OrganizationService(session)


@router.post(
    "",
    response_model=OrganizationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Organization",
    description="Create a new organization (contractor or subcontractor)"
)
async def create_organization(
    organization: OrganizationCreate,
    service: OrganizationService = Depends(get_organization_service)
) -> OrganizationResponse:
    """
    Create new organization.
    Single Responsibility: Organization creation endpoint.
    """
    return await service.create_organization(organization)


@router.get(
    "/{organization_id}",
    response_model=OrganizationResponse,
    summary="Get Organization",
    description="Retrieve organization by ID"
)
async def get_organization(
    organization_id: uuid.UUID,
    service: OrganizationService = Depends(get_organization_service)
) -> OrganizationResponse:
    """
    Get organization by ID.
    Single Responsibility: Organization retrieval endpoint.
    """
    return await service.get_organization(organization_id)


@router.put(
    "/{organization_id}",
    response_model=OrganizationResponse,
    summary="Update Organization",
    description="Update organization information"
)
async def update_organization(
    organization_id: uuid.UUID,
    organization_update: OrganizationUpdate,
    service: OrganizationService = Depends(get_organization_service)
) -> OrganizationResponse:
    """
    Update organization.
    Single Responsibility: Organization update endpoint.
    """
    return await service.update_organization(organization_id, organization_update)


@router.delete(
    "/{organization_id}",
    response_model=SuccessResponse,
    summary="Delete Organization",
    description="Delete organization"
)
async def delete_organization(
    organization_id: uuid.UUID,
    service: OrganizationService = Depends(get_organization_service)
) -> SuccessResponse:
    """
    Delete organization.
    Single Responsibility: Organization deletion endpoint.
    """
    await service.delete_organization(organization_id)
    return SuccessResponse(message="Organization deleted successfully")


@router.get(
    "",
    response_model=PaginatedResponse[OrganizationResponse],
    summary="List Organizations",
    description="List organizations with pagination"
)
async def list_organizations(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    service: OrganizationService = Depends(get_organization_service)
) -> PaginatedResponse[OrganizationResponse]:
    """
    List organizations with pagination.
    Single Responsibility: Organization listing endpoint.
    """
    return await service.list_organizations(page=page, size=size)


@router.get(
    "/search/{search_term}",
    response_model=List[OrganizationResponse],
    summary="Search Organizations",
    description="Search organizations by name"
)
async def search_organizations(
    search_term: str,
    service: OrganizationService = Depends(get_organization_service)
) -> List[OrganizationResponse]:
    """
    Search organizations by name.
    Single Responsibility: Organization search endpoint.
    """
    return await service.search_organizations(search_term)


@router.get(
    "/{organization_id}/capacity",
    response_model=CapacityStatusResponse,
    summary="Get Capacity Status",
    description="Get organization capacity status for a specific date"
)
async def get_capacity_status(
    organization_id: uuid.UUID,
    target_date: date = Query(..., description="Target date for capacity check"),
    service: OrganizationService = Depends(get_organization_service)
) -> CapacityStatusResponse:
    """
    Get organization capacity status.
    Single Responsibility: Capacity status endpoint.
    """
    return await service.get_capacity_status(organization_id, target_date)


@router.post(
    "/{organization_id}/capacity/check",
    response_model=dict,
    summary="Check Additional Work Capacity",
    description="Check if organization can accept additional work hours"
)
async def check_additional_work_capacity(
    organization_id: uuid.UUID,
    additional_hours: float = Query(..., ge=0, description="Additional hours to check"),
    service: OrganizationService = Depends(get_organization_service)
) -> dict:
    """
    Check if organization can accept additional work.
    Single Responsibility: Capacity check endpoint.
    """
    can_accept = await service.can_accept_additional_work(organization_id, additional_hours)
    return {
        "organization_id": organization_id,
        "additional_hours": additional_hours,
        "can_accept": can_accept
    }


@router.get(
    "/{organization_id}/eligibility",
    response_model=dict,
    summary="Check Work Eligibility",
    description="Check if organization is eligible for work assignments"
)
async def check_work_eligibility(
    organization_id: uuid.UUID,
    service: OrganizationService = Depends(get_organization_service)
) -> dict:
    """
    Check organization work eligibility.
    Single Responsibility: Eligibility check endpoint.
    """
    is_eligible = await service.is_eligible_for_work(organization_id)
    return {
        "organization_id": organization_id,
        "is_eligible": is_eligible
    }


@router.put(
    "/{organization_id}/status",
    response_model=OrganizationResponse,
    summary="Update Organization Status",
    description="Update organization compliance status"
)
async def update_organization_status(
    organization_id: uuid.UUID,
    new_status: ComplianceStatus,
    service: OrganizationService = Depends(get_organization_service)
) -> OrganizationResponse:
    """
    Update organization status.
    Single Responsibility: Status update endpoint.
    """
    return await service.update_status(organization_id, new_status)


@router.get(
    "/{organization_id}/subcontractors",
    response_model=List[OrganizationResponse],
    summary="Get Subcontractors",
    description="Get all subcontractors for an organization"
)
async def get_subcontractors(
    organization_id: uuid.UUID,
    service: OrganizationService = Depends(get_organization_service)
) -> List[OrganizationResponse]:
    """
    Get organization subcontractors.
    Single Responsibility: Subcontractor listing endpoint.
    """
    return await service.get_subcontractors(organization_id)


@router.get(
    "/{organization_id}/parent",
    response_model=OrganizationResponse,
    summary="Get Parent Organization",
    description="Get parent organization for a subcontractor"
)
async def get_parent_organization(
    organization_id: uuid.UUID,
    service: OrganizationService = Depends(get_organization_service)
) -> OrganizationResponse:
    """
    Get parent organization.
    Single Responsibility: Parent organization endpoint.
    """
    return await service.get_parent_organization(organization_id)