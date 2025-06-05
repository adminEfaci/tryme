"""
Organization service for business logic only.
Single Responsibility: Organization domain business logic.
"""

import uuid
from datetime import date
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload

from ..models.organization_models import Organization
from ..schemas.organization_schemas import (
    OrganizationCreate,
    OrganizationUpdate, 
    OrganizationResponse,
    CapacityStatusResponse
)
from ..schemas.base_schemas import PaginatedResponse
from ..enums.system_enums import OrganizationType, ComplianceStatus
from ..exceptions import (
    NotFoundError,
    BusinessRuleViolationError,
    ValidationError,
    InvalidContractorHierarchyError,
    ContractorCapacityExceededError,
    ExpiredInsuranceError
)


class OrganizationService:
    """
    Organization service for business logic.
    Single Responsibility: Organization domain operations.
    """
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_organization(
        self, 
        organization_data: OrganizationCreate
    ) -> OrganizationResponse:
        """
        Create a new organization.
        Single Responsibility: Organization creation logic.
        """
        # Validate business rules
        await self._validate_organization_creation(organization_data)
        
        # Create organization
        organization = Organization(**organization_data.dict())
        self.session.add(organization)
        await self.session.commit()
        await self.session.refresh(organization)
        
        return await self._to_response(organization)
    
    async def get_organization(self, organization_id: uuid.UUID) -> OrganizationResponse:
        """
        Get organization by ID.
        Single Responsibility: Organization retrieval.
        """
        query = select(Organization).where(Organization.id == organization_id)
        result = await self.session.execute(query)
        organization = result.scalar_one_or_none()
        
        if not organization:
            raise NotFoundError("Organization", str(organization_id))
        
        return await self._to_response(organization)
    
    async def update_organization(
        self, 
        organization_id: uuid.UUID, 
        update_data: OrganizationUpdate
    ) -> OrganizationResponse:
        """
        Update organization.
        Single Responsibility: Organization update logic.
        """
        # Get existing organization
        query = select(Organization).where(Organization.id == organization_id)
        result = await self.session.execute(query)
        organization = result.scalar_one_or_none()
        
        if not organization:
            raise NotFoundError("Organization", str(organization_id))
        
        # Update fields
        update_dict = update_data.dict(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(organization, field, value)
        
        await self.session.commit()
        await self.session.refresh(organization)
        
        return await self._to_response(organization)
    
    async def delete_organization(self, organization_id: uuid.UUID) -> None:
        """
        Delete organization.
        Single Responsibility: Organization deletion logic.
        """
        query = select(Organization).where(Organization.id == organization_id)
        result = await self.session.execute(query)
        organization = result.scalar_one_or_none()
        
        if not organization:
            raise NotFoundError("Organization", str(organization_id))
        
        await self.session.delete(organization)
        await self.session.commit()
    
    async def list_organizations(
        self, 
        page: int = 1, 
        size: int = 10
    ) -> PaginatedResponse[OrganizationResponse]:
        """
        List organizations with pagination.
        Single Responsibility: Organization listing logic.
        """
        offset = (page - 1) * size
        
        # Get total count
        count_query = select(func.count(Organization.id))
        count_result = await self.session.execute(count_query)
        total = count_result.scalar()
        
        # Get organizations
        query = (
            select(Organization)
            .offset(offset)
            .limit(size)
            .order_by(Organization.name)
        )
        result = await self.session.execute(query)
        organizations = result.scalars().all()
        
        # Convert to responses
        items = [await self._to_response(org) for org in organizations]
        
        pages = (total + size - 1) // size
        
        return PaginatedResponse(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=pages,
            has_next=page < pages,
            has_prev=page > 1
        )
    
    async def search_organizations(self, search_term: str) -> List[OrganizationResponse]:
        """
        Search organizations by name.
        Single Responsibility: Organization search logic.
        """
        query = select(Organization).where(
            Organization.name.ilike(f"%{search_term}%")
        )
        result = await self.session.execute(query)
        organizations = result.scalars().all()
        
        return [await self._to_response(org) for org in organizations]
    
    async def can_accept_additional_work(
        self, 
        organization_id: uuid.UUID, 
        additional_hours: float
    ) -> bool:
        """
        Check if organization can accept additional work.
        Single Responsibility: Capacity validation logic.
        """
        organization = await self._get_organization_by_id(organization_id)
        
        # For now, simple capacity check
        # In real implementation, would check current workload
        current_workload = 0  # TODO: Calculate from actual assignments
        available_capacity = organization.max_capacity_hours_per_day - current_workload
        
        return additional_hours <= available_capacity
    
    async def is_eligible_for_work(self, organization_id: uuid.UUID) -> bool:
        """
        Check if organization is eligible for work.
        Single Responsibility: Eligibility validation logic.
        """
        organization = await self._get_organization_by_id(organization_id)
        
        # Check insurance expiry
        if organization.insurance_expiry and organization.insurance_expiry < date.today():
            return False
        
        # Check license expiry
        if organization.license_expiry and organization.license_expiry < date.today():
            return False
        
        # Check compliance status
        if organization.status != ComplianceStatus.COMPLIANT:
            return False
        
        return True
    
    async def update_status(
        self, 
        organization_id: uuid.UUID, 
        new_status: ComplianceStatus
    ) -> OrganizationResponse:
        """
        Update organization status.
        Single Responsibility: Status update logic.
        """
        organization = await self._get_organization_by_id(organization_id)
        organization.status = new_status
        
        await self.session.commit()
        await self.session.refresh(organization)
        
        return await self._to_response(organization)
    
    async def update_performance_scores(
        self,
        organization_id: uuid.UUID,
        performance_score: Optional[float] = None,
        reliability_score: Optional[float] = None,
        safety_score: Optional[float] = None
    ) -> OrganizationResponse:
        """
        Update organization performance scores.
        Single Responsibility: Performance score update logic.
        """
        organization = await self._get_organization_by_id(organization_id)
        
        if performance_score is not None:
            organization.performance_score = performance_score
        if reliability_score is not None:
            organization.reliability_score = reliability_score
        if safety_score is not None:
            organization.safety_score = safety_score
        
        await self.session.commit()
        await self.session.refresh(organization)
        
        return await self._to_response(organization)
    
    async def get_capacity_status(
        self, 
        organization_id: uuid.UUID, 
        target_date: date
    ) -> CapacityStatusResponse:
        """
        Get organization capacity status for a specific date.
        Single Responsibility: Capacity status calculation.
        """
        organization = await self._get_organization_by_id(organization_id)
        
        # TODO: Calculate actual workload from schedules/assignments
        current_workload = 0.0  # Placeholder
        available_capacity = organization.max_capacity_hours_per_day - current_workload
        utilization_percentage = (current_workload / organization.max_capacity_hours_per_day) * 100
        
        return CapacityStatusResponse(
            organization_id=organization_id,
            date=target_date,
            max_capacity_hours_per_day=organization.max_capacity_hours_per_day,
            current_workload_hours=current_workload,
            available_capacity_hours=available_capacity,
            utilization_percentage=utilization_percentage,
            is_over_capacity=current_workload > organization.max_capacity_hours_per_day
        )
    
    async def get_subcontractors(
        self, 
        organization_id: uuid.UUID
    ) -> List[OrganizationResponse]:
        """
        Get all subcontractors for an organization.
        Single Responsibility: Subcontractor retrieval logic.
        """
        query = select(Organization).where(
            Organization.parent_organization_id == organization_id
        )
        result = await self.session.execute(query)
        subcontractors = result.scalars().all()
        
        return [await self._to_response(sub) for sub in subcontractors]
    
    async def get_parent_organization(
        self, 
        organization_id: uuid.UUID
    ) -> OrganizationResponse:
        """
        Get parent organization.
        Single Responsibility: Parent organization retrieval.
        """
        organization = await self._get_organization_by_id(organization_id)
        
        if not organization.parent_organization_id:
            raise NotFoundError("Parent Organization", "None")
        
        return await self.get_organization(organization.parent_organization_id)
    
    # Private helper methods
    
    async def _validate_organization_creation(
        self, 
        organization_data: OrganizationCreate
    ) -> None:
        """
        Validate organization creation business rules.
        Single Responsibility: Creation validation logic.
        """
        # Validate subcontractor hierarchy rule
        if organization_data.organization_type == OrganizationType.SUBCONTRACTOR:
            if not organization_data.parent_organization_id:
                raise ValidationError(
                    "parent_organization_id",
                    None,
                    "Subcontractor must have a parent organization"
                )
            
            # Check if parent is also a subcontractor (not allowed)
            parent = await self._get_organization_by_id(
                organization_data.parent_organization_id
            )
            if parent.organization_type == OrganizationType.SUBCONTRACTOR:
                raise InvalidContractorHierarchyError(
                    "Subcontractors cannot hire their own subcontractors",
                    {
                        "parent_id": str(organization_data.parent_organization_id),
                        "parent_type": parent.organization_type
                    }
                )
    
    async def _get_organization_by_id(self, organization_id: uuid.UUID) -> Organization:
        """
        Get organization by ID (internal use).
        Single Responsibility: Internal organization retrieval.
        """
        query = select(Organization).where(Organization.id == organization_id)
        result = await self.session.execute(query)
        organization = result.scalar_one_or_none()
        
        if not organization:
            raise NotFoundError("Organization", str(organization_id))
        
        return organization
    
    async def _to_response(self, organization: Organization) -> OrganizationResponse:
        """
        Convert organization model to response DTO.
        Single Responsibility: Model to DTO conversion.
        """
        # TODO: Calculate actual counts from relationships
        subcontractors_count = 0
        employees_count = 0
        active_contracts_count = 0
        
        return OrganizationResponse(
            id=organization.id,
            created_at=organization.created_at,
            updated_at=organization.updated_at,
            name=organization.name,
            legal_name=organization.legal_name,
            business_number=organization.business_number,
            tax_id=organization.tax_id,
            organization_type=organization.organization_type,
            status=organization.status,
            primary_contact_name=organization.primary_contact_name,
            primary_contact_email=organization.primary_contact_email,
            primary_contact_phone=organization.primary_contact_phone,
            address_line1=organization.address_line1,
            address_line2=organization.address_line2,
            city=organization.city,
            province_state=organization.province_state,
            postal_code=organization.postal_code,
            country=organization.country,
            max_capacity_hours_per_day=organization.max_capacity_hours_per_day,
            max_vehicles=organization.max_vehicles,
            max_employees=organization.max_employees,
            service_areas=organization.service_areas,
            insurance_policy_number=organization.insurance_policy_number,
            insurance_expiry=organization.insurance_expiry,
            license_number=organization.license_number,
            license_expiry=organization.license_expiry,
            hourly_rate=organization.hourly_rate,
            overtime_multiplier=organization.overtime_multiplier,
            holiday_multiplier=organization.holiday_multiplier,
            performance_score=organization.performance_score,
            reliability_score=organization.reliability_score,
            safety_score=organization.safety_score,
            parent_organization_id=organization.parent_organization_id,
            subcontractors_count=subcontractors_count,
            employees_count=employees_count,
            active_contracts_count=active_contracts_count,
        )