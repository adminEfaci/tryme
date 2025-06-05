"""
Simple test to verify TDD setup is working.
"""

import asyncio
import pytest
from app.services.organization_service import OrganizationService
from app.schemas.organization_schemas import OrganizationCreate
from app.enums.system_enums import OrganizationType


def test_simple_import():
    """Test that imports work correctly"""
    assert OrganizationType.PRIME_CONTRACTOR == "prime_contractor"
    print("✅ Simple import test passed")


def test_organization_create_schema():
    """Test that organization create schema works"""
    data = {
        "name": "Test Organization",
        "legal_name": "Test Organization Inc.",
        "organization_type": "prime_contractor",
        "primary_contact_name": "John Doe",
        "primary_contact_email": "john@test.com",
        "primary_contact_phone": "+1-613-555-0123",
        "address_line1": "123 Main St",
        "city": "Ottawa",
        "province_state": "Ontario",
        "postal_code": "K1A 0A6",
    }
    
    org_create = OrganizationCreate(**data)
    assert org_create.name == "Test Organization"
    assert org_create.organization_type == OrganizationType.PRIME_CONTRACTOR
    print("✅ Organization schema test passed")


if __name__ == "__main__":
    test_simple_import()
    test_organization_create_schema()
    print("🎉 All simple tests passed! TDD setup is working.")