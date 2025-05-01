import time

import pytest

from src.financial_portfolio_manager.database.dynamodb.table_manager import (
    DynamoDBTableManager,
)


@pytest.fixture
def table_name():
    return "transaction-table"


@pytest.fixture
def table_manager(table_name):
    return DynamoDBTableManager(table_name=table_name)


def test_create_client_profile(table_manager):

    result = table_manager.create_client_profile(
        client_id="123", client_name="John Doe", phone_number="1234567890"
    )

    assert result["client_id"] == "CLIENT#123"
    assert result["secondary_key"] == "PROFILE"
    assert result["item_type"] == "Client"
    assert result["client_name"] == "John Doe"
    assert result["phone_number"] == "1234567890"
    assert "profile_added" in result
    assert "profile_updated" in result


def test_create_client_profile_with_prefix(table_manager):

    result = table_manager.create_client_profile(
        client_id="CLIENT#456", client_name="Jane Doe", phone_number="9876543210"
    )

    assert result["client_id"] == "CLIENT#456"
    assert result["client_name"] == "Jane Doe"


def test_create_transaction(table_manager):
    # No decimal type support in DynamoDB
    result = table_manager.create_transaction(
        client_id="78911",
        transaction_id="TR001",
        asset_id="IBM",
        broker_id="BR001",
        transaction_type="BUY",
        quantity=10,
        price_per_unit="150.50",
    )
    print(result)
    assert result["client_id"] == "CLIENT#78911"
    assert result["asset_id"] == "ASSET#IBM"
    assert result["broker_id"] == "BROKER#BR001"
    assert result["transaction_id"] == "TR001"
    assert result["transaction_type"] == "BUY"
    assert result["quantity"] == 10
    assert result["price_per_unit"] == "150.50"
    assert "transaction_date" in result
    assert result["secondary_key"].startswith("TRANSACTION#")


def test_get_client_profile(table_manager):

    table_manager.create_client_profile(
        client_id="999", client_name="Test User", phone_number="5551234567"
    )

    profile = table_manager.get_client_profile(client_id="999")
    assert profile is not None
    assert profile["client_name"] == "Test User"
    assert profile["phone_number"] == "5551234567"

    profile2 = table_manager.get_client_profile(client_id="CLIENT#999")
    assert profile2 is not None
    assert profile2["client_name"] == "Test User"


def test_get_client_transactions(table_manager):

    client_id = "888"
    table_manager.create_client_profile(
        client_id=client_id,
        client_name="Transaction User",
        phone_number="+1122334455",
    )

    # Add multiple transactions
    table_manager.create_transaction(
        client_id=client_id,
        transaction_id="TX1",
        asset_id="MSFT",
        broker_id="BR001",
        transaction_type="BUY",
        quantity=5,
        price_per_unit="200.00",
    )
    time.sleep(2)  # Ensure different timestamps
    table_manager.create_transaction(
        client_id=client_id,
        transaction_id="TX2",
        asset_id="GOOG",
        broker_id="BR001",
        transaction_type="BUY",
        quantity=2,
        price_per_unit="1500.00",
    )

    # Get transactions
    transactions = table_manager.get_client_transactions(client_id=client_id)

    # Verify we got both transactions
    assert len(transactions) == 2
    assert {t["transaction_id"] for t in transactions} == {"TX1", "TX2"}


def test_update_client_profile(table_manager):

    table_manager.create_client_profile(
        client_id="777", client_name="Update User", phone_number="9998887777"
    )

    update_data = {
        "client_name": "New Updated Name",
        "email": "new@example.com",
    }

    table_manager.update_client_profile(client_id="777", update_data=update_data)

    updated_profile = table_manager.get_client_profile(client_id="CLIENT#777")
    assert updated_profile is not None
    assert updated_profile["client_name"] == "New Updated Name"
    assert updated_profile["email"] == "new@example.com"
