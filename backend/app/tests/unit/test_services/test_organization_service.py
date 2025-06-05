"""
TDD Tests for Organization Service.
Single Responsibility: Test organization business logic.

Following TDD methodology:
1. RED: Write failing tests first
2. GREEN: Implement minimal code to pass tests  
3. REFACTOR: Improve code while keeping tests green
"""

import pytest
import pytest_asyncio
import uuid
from datetime import date, timedelta
from decimal import Decimal

from app.services.organization_service import OrganizationService
from app.schemas.organization_schemas import (
    OrganizationCreate, 
    OrganizationUpdate,
    CapacityStatusResponse
)
from app.models.organization_models import Organization
from app.enums.system_enums import OrganizationType, ComplianceStatus
from app.exceptions import (
    BusinessRuleViolationError, 
    NotFoundError,
    ValidationError
)


class TestOrganizationService:
    """TDD tests for Organization service - RED phase"""
    
    @pytest_asyncio.fixture
    async def organization_service(self, test_session):
        """Create organization service instance"""
        return OrganizationService(test_session)
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_create_organization_success(
        self, 
        organization_service: OrganizationService, 
        sample_organization_data
    ):
        """RED: Test successful organization creation"""
        # Arrange
        org_data = OrganizationCreate(**sample_organization_data)
        
        # Act
        organization = await organization_service.create_organization(org_data)
        
        # Assert
        assert organization.id is not None
        assert organization.name == sample_organization_data["name"]
        assert organization.organization_type == OrganizationType.PRIME_CONTRACTOR
        assert organization.status == ComplianceStatus.COMPLIANT
        assert organization.created_at is not None
        assert organization.updated_at is not None
    
    @pytest.mark.unit
    async def test_create_organization_with_empty_name_fails(
        self, 
        organization_service: OrganizationService
    ):
        """RED: Test organization creation with empty name fails"""
        # Arrange
        invalid_data = {
            "name": "",  # Empty name should fail
            "legal_name": "Test Legal Name",
            "organization_type": "prime_contractor",
            "primary_contact_name": "John Smith",
            "primary_contact_email": "john@test.com",
            "primary_contact_phone": "+1-613-555-0123",
            "address_line1": "123 Main St",
            "city": "Ottawa",
            "province_state": "Ontario",
            "postal_code": "K1A 0A6",
        }
        
        # Act & Assert
        with pytest.raises(ValidationError) as exc:
            org_data = OrganizationCreate(**invalid_data)
            await organization_service.create_organization(org_data)
        
        assert "name" in str(exc.value).lower()
    
    @pytest.mark.unit
    async def test_get_organization_by_id_success(
        self, 
        organization_service: OrganizationService, 
        sample_organization_data
    ):
        """RED: Test retrieving organization by ID"""
        # Arrange
        org_data = OrganizationCreate(**sample_organization_data)
        created_org = await organization_service.create_organization(org_data)
        
        # Act
        retrieved_org = await organization_service.get_organization(created_org.id)
        
        # Assert
        assert retrieved_org.id == created_org.id
        assert retrieved_org.name == created_org.name
        assert retrieved_org.organization_type == created_org.organization_type
    
    @pytest.mark.unit
    async def test_get_nonexistent_organization_raises_not_found(
        self, 
        organization_service: OrganizationService
    ):
        """RED: Test retrieving non-existent organization raises NotFoundError"""
        # Arrange
        fake_id = uuid.uuid4()
        
        # Act & Assert
        with pytest.raises(NotFoundError) as exc:
            await organization_service.get_organization(fake_id)
        
        assert "Organization" in str(exc.value)
        assert str(fake_id) in str(exc.value)
    
    @pytest.mark.unit
    async def test_update_organization_success(
        self, 
        organization_service: OrganizationService, 
        sample_organization_data
    ):
        """RED: Test updating organization"""
        # Arrange
        org_data = OrganizationCreate(**sample_organization_data)
        created_org = await organization_service.create_organization(org_data)
        
        update_data = OrganizationUpdate(
            name="Updated Waste Services",
            hourly_rate=Decimal("30.00")
        )
        
        # Act
        updated_org = await organization_service.update_organization(
            created_org.id, 
            update_data
        )
        
        # Assert
        assert updated_org.name == "Updated Waste Services"
        assert updated_org.hourly_rate == Decimal("30.00")
        assert updated_org.updated_at > created_org.updated_at
        assert updated_org.id == created_org.id
    
    @pytest.mark.unit
    async def test_delete_organization_success(
        self, 
        organization_service: OrganizationService, 
        sample_organization_data
    ):
        """RED: Test deleting organization"""
        # Arrange
        org_data = OrganizationCreate(**sample_organization_data)
        created_org = await organization_service.create_organization(org_data)
        
        # Act
        await organization_service.delete_organization(created_org.id)
        
        # Assert - Should raise NotFoundError when trying to get deleted org
        with pytest.raises(NotFoundError):
            await organization_service.get_organization(created_org.id)
    
    @pytest.mark.unit
    async def test_list_organizations_with_pagination(
        self, 
        organization_service: OrganizationService, 
        sample_organization_data
    ):
        """RED: Test listing organizations with pagination"""
        # Arrange - Create multiple organizations
        for i in range(5):
            org_data = sample_organization_data.copy()
            org_data["name"] = f"Test Organization {i}"
            org_create = OrganizationCreate(**org_data)
            await organization_service.create_organization(org_create)
        
        # Act
        result = await organization_service.list_organizations(page=1, size=3)
        
        # Assert
        assert len(result.items) == 3
        assert result.total == 5
        assert result.page == 1
        assert result.pages == 2
        assert result.has_next is True
        assert result.has_prev is False
    
    @pytest.mark.unit
    async def test_search_organizations_by_name(
        self, 
        organization_service: OrganizationService, 
        sample_organization_data
    ):
        """RED: Test searching organizations by name"""
        # Arrange - Create organizations with different names
        org1_data = sample_organization_data.copy()
        org1_data["name"] = "Alpha Waste Services"
        await organization_service.create_organization(OrganizationCreate(**org1_data))
        
        org2_data = sample_organization_data.copy()
        org2_data["name"] = "Beta Recycling Inc"
        await organization_service.create_organization(OrganizationCreate(**org2_data))
        
        # Act
        result = await organization_service.search_organizations("Alpha")
        
        # Assert
        assert len(result) == 1
        assert result[0].name == "Alpha Waste Services"


class TestOrganizationBusinessRules:
    """TDD tests for organization business rules - RED phase"""
    
    @pytest.fixture
    def organization_service(self, test_session):
        return OrganizationService(test_session)
    
    @pytest.mark.unit
    async def test_subcontractor_hierarchy_rule_violation(
        self, 
        organization_service: OrganizationService, 
        sample_organization_data
    ):
        """RED: Test CONTRACTOR_HIERARCHY_001 business rule"""
        # Arrange - Create prime contractor
        prime_data = sample_organization_data.copy()
        prime_data["organization_type"] = "prime_contractor"
        prime = await organization_service.create_organization(
            OrganizationCreate(**prime_data)
        )
        
        # Create subcontractor
        sub_data = sample_organization_data.copy()
        sub_data["name"] = "Sub Contractor Inc."
        sub_data["organization_type"] = "subcontractor"
        sub_data["parent_organization_id"] = prime.id
        sub = await organization_service.create_organization(
            OrganizationCreate(**sub_data)
        )
        
        # Act & Assert - Attempt to create sub-subcontractor (should fail)
        sub_sub_data = sample_organization_data.copy()
        sub_sub_data["name"] = "Sub-Sub Contractor"
        sub_sub_data["organization_type"] = "subcontractor"
        sub_sub_data["parent_organization_id"] = sub.id
        
        with pytest.raises(BusinessRuleViolationError) as exc:
            await organization_service.create_organization(
                OrganizationCreate(**sub_sub_data)
            )
        
        assert "CONTRACTOR_HIERARCHY_001" in str(exc.value)
    
    @pytest.mark.unit
    async def test_contractor_capacity_validation(
        self, 
        organization_service: OrganizationService, 
        sample_organization_data
    ):
        """RED: Test CONTRACTOR_CAPACITY_001 business rule"""
        # Arrange
        org_data = sample_organization_data.copy()
        org_data["max_capacity_hours_per_day"] = 480  # 8 hours
        organization = await organization_service.create_organization(
            OrganizationCreate(**org_data)
        )
        
        # Act & Assert - Test capacity check
        can_accept_600_hours = await organization_service.can_accept_additional_work(
            organization.id, 
            600  # 10 hours - exceeds capacity
        )
        assert can_accept_600_hours is False
        
        can_accept_400_hours = await organization_service.can_accept_additional_work(
            organization.id, 
            400  # 6.67 hours - within capacity
        )
        assert can_accept_400_hours is True
    
    @pytest.mark.unit
    async def test_contractor_insurance_validation(
        self, 
        organization_service: OrganizationService, 
        sample_organization_data
    ):
        """RED: Test CONTRACTOR_INSURANCE_001 business rule"""
        # Arrange - Create contractor with expired insurance
        org_data = sample_organization_data.copy()
        org_data["insurance_expiry"] = date.today() - timedelta(days=1)
        organization = await organization_service.create_organization(
            OrganizationCreate(**org_data)
        )
        
        # Act & Assert - Test insurance validation
        is_eligible = await organization_service.is_eligible_for_work(organization.id)
        assert is_eligible is False
        
        # Update insurance to valid date
        update_data = OrganizationUpdate(
            insurance_expiry=date.today() + timedelta(days=365)
        )
        await organization_service.update_organization(organization.id, update_data)
        
        is_eligible_after_update = await organization_service.is_eligible_for_work(
            organization.id
        )
        assert is_eligible_after_update is True
    
    @pytest.mark.unit
    async def test_organization_status_transitions(
        self, 
        organization_service: OrganizationService, 
        sample_organization_data
    ):
        """RED: Test valid organization status transitions"""
        # Arrange
        organization = await organization_service.create_organization(
            OrganizationCreate(**sample_organization_data)
        )
        
        # Act & Assert - Test valid transition: COMPLIANT -> NON_COMPLIANT
        await organization_service.update_status(
            organization.id, 
            ComplianceStatus.NON_COMPLIANT
        )
        updated_org = await organization_service.get_organization(organization.id)
        assert updated_org.status == ComplianceStatus.NON_COMPLIANT
        
        # Test valid transition: NON_COMPLIANT -> COMPLIANT
        await organization_service.update_status(
            organization.id, 
            ComplianceStatus.COMPLIANT
        )
        updated_org = await organization_service.get_organization(organization.id)
        assert updated_org.status == ComplianceStatus.COMPLIANT


class TestOrganizationPerformanceTracking:
    """TDD tests for organization performance tracking - RED phase"""
    
    @pytest.fixture
    def organization_service(self, test_session):
        return OrganizationService(test_session)
    
    @pytest.mark.unit
    async def test_update_performance_scores(
        self, 
        organization_service: OrganizationService, 
        sample_organization_data
    ):
        """RED: Test updating organization performance scores"""
        # Arrange
        organization = await organization_service.create_organization(
            OrganizationCreate(**sample_organization_data)
        )
        
        # Act
        await organization_service.update_performance_scores(
            organization.id,
            performance_score=85.5,
            reliability_score=90.0,
            safety_score=95.0
        )
        
        # Assert
        updated_org = await organization_service.get_organization(organization.id)
        assert updated_org.performance_score == 85.5
        assert updated_org.reliability_score == 90.0
        assert updated_org.safety_score == 95.0
    
    @pytest.mark.unit
    async def test_get_organization_capacity_status(
        self, 
        organization_service: OrganizationService, 
        sample_organization_data
    ):
        """RED: Test getting organization capacity status"""
        # Arrange
        org_data = sample_organization_data.copy()
        org_data["max_capacity_hours_per_day"] = 480
        organization = await organization_service.create_organization(
            OrganizationCreate(**org_data)
        )
        
        # Act
        capacity_status = await organization_service.get_capacity_status(
            organization.id, 
            date.today()
        )
        
        # Assert
        assert isinstance(capacity_status, CapacityStatusResponse)
        assert capacity_status.organization_id == organization.id
        assert capacity_status.max_capacity_hours_per_day == 480
        assert capacity_status.current_workload_hours >= 0
        assert capacity_status.available_capacity_hours >= 0
        assert capacity_status.utilization_percentage >= 0


class TestOrganizationRelationships:
    """TDD tests for organization relationships - RED phase"""
    
    @pytest.fixture
    def organization_service(self, test_session):
        return OrganizationService(test_session)
    
    @pytest.mark.unit
    async def test_get_subcontractors(
        self, 
        organization_service: OrganizationService, 
        sample_organization_data
    ):
        """RED: Test getting organization subcontractors"""
        # Arrange - Create prime contractor
        prime_data = sample_organization_data.copy()
        prime_data["organization_type"] = "prime_contractor"
        prime = await organization_service.create_organization(
            OrganizationCreate(**prime_data)
        )
        
        # Create subcontractors
        subcontractor_ids = []
        for i in range(3):
            sub_data = sample_organization_data.copy()
            sub_data["name"] = f"Subcontractor {i}"
            sub_data["organization_type"] = "subcontractor"
            sub_data["parent_organization_id"] = prime.id
            sub = await organization_service.create_organization(
                OrganizationCreate(**sub_data)
            )
            subcontractor_ids.append(sub.id)
        
        # Act
        subcontractors = await organization_service.get_subcontractors(prime.id)
        
        # Assert
        assert len(subcontractors) == 3
        for sub in subcontractors:
            assert sub.parent_organization_id == prime.id
            assert sub.organization_type == OrganizationType.SUBCONTRACTOR
            assert sub.id in subcontractor_ids
    
    @pytest.mark.unit
    async def test_get_parent_organization(
        self, 
        organization_service: OrganizationService, 
        sample_organization_data
    ):
        """RED: Test getting parent organization"""
        # Arrange - Create prime contractor
        prime_data = sample_organization_data.copy()
        prime_data["organization_type"] = "prime_contractor"
        prime = await organization_service.create_organization(
            OrganizationCreate(**prime_data)
        )
        
        # Create subcontractor
        sub_data = sample_organization_data.copy()
        sub_data["name"] = "Subcontractor Inc."
        sub_data["organization_type"] = "subcontractor"
        sub_data["parent_organization_id"] = prime.id
        sub = await organization_service.create_organization(
            OrganizationCreate(**sub_data)
        )
        
        # Act
        parent = await organization_service.get_parent_organization(sub.id)
        
        # Assert
        assert parent.id == prime.id
        assert parent.organization_type == OrganizationType.PRIME_CONTRACTOR