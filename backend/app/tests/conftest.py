"""
Test configuration and fixtures.
Single Responsibility: Test setup and shared fixtures.
"""

import pytest
import asyncio
from typing import AsyncGenerator, Generator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from fastapi.testclient import TestClient

from app.main import app
from app.config.database import get_session
from app.models import *  # Import all models to ensure they're registered


# Test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_waste_management.db"

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    future=True,
)

# Create test session factory
TestSessionLocal = sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def test_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Create a test database session.
    Single Responsibility: Provide isolated test database session.
    """
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    
    # Create session
    async with TestSessionLocal() as session:
        yield session
    
    # Drop tables after test
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture(scope="function")
def client(test_session: AsyncSession) -> TestClient:
    """
    Create a test client with test database session.
    Single Responsibility: Provide test HTTP client.
    """
    def get_test_session():
        return test_session
    
    app.dependency_overrides[get_session] = get_test_session
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def sample_organization_data():
    """
    Sample organization data for testing.
    Single Responsibility: Provide test data.
    """
    return {
        "name": "Test Waste Services Inc.",
        "legal_name": "Test Waste Services Incorporated",
        "business_number": "123456789",
        "tax_id": "987654321",
        "organization_type": "prime_contractor",
        "primary_contact_name": "John Smith",
        "primary_contact_email": "john@testwaste.com",
        "primary_contact_phone": "+1-613-555-0123",
        "address_line1": "123 Main Street",
        "city": "Ottawa",
        "province_state": "Ontario",
        "postal_code": "K1A 0A6",
        "max_capacity_hours_per_day": 480,
        "hourly_rate": 25.00,
        "insurance_policy_number": "INS-123456",
        "insurance_expiry": "2025-12-31",
    }


@pytest.fixture
def sample_user_data():
    """
    Sample user data for testing.
    Single Responsibility: Provide test user data.
    """
    return {
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "phone": "+1-613-555-0100",
        "password": "secure123",
    }


@pytest.fixture
def sample_employee_data():
    """
    Sample employee data for testing.
    Single Responsibility: Provide test employee data.
    """
    return {
        "employee_number": "EMP-001",
        "first_name": "John",
        "last_name": "Driver",
        "phone": "+1-613-555-0101",
        "email": "john.driver@testwaste.com",
        "hire_date": "2024-01-01",
        "job_title": "Waste Collection Driver",
        "hourly_rate": 25.00,
        "license_number": "D123456789",
        "license_class": "DZ",
        "license_expiry": "2025-12-31",
    }


@pytest.fixture
def sample_timesheet_data():
    """
    Sample timesheet data for testing.
    Single Responsibility: Provide test timesheet data.
    """
    return {
        "pay_period_start": "2024-01-01",
        "pay_period_end": "2024-01-07",
        "status": "draft",
    }


# Pytest markers for test categorization
pytest.mark.unit = pytest.mark.unit
pytest.mark.integration = pytest.mark.integration
pytest.mark.e2e = pytest.mark.e2e
pytest.mark.performance = pytest.mark.performance