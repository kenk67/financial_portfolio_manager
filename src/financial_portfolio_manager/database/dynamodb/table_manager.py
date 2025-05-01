import time
from datetime import datetime
from typing import Dict, List, Optional, Any

import boto3
from botocore.exceptions import ClientError


class DynamoDBTableManager:
    """Manager class for DynamoDB table operations in financial portfolio manager."""

    def __init__(
        self,
        table_name: str,
        region: str = "us-east-1",
        endpoint_url: str = "http://localhost:8000",
    ):
        """
        Initialize DynamoDB table manager.

        Args:
            table_name: Name of the DynamoDB table
            region: AWS region name
        """
        self.dynamodb = boto3.resource(
            "dynamodb",
            region_name=region,
            endpoint_url=endpoint_url,
            aws_access_key_id="local",
            aws_secret_access_key="local",
        )
        self.table = self.dynamodb.Table(table_name)

    def create_client_profile(
        self, client_id: str, client_name: str, phone_number: str
    ) -> Dict:
        """
        Create a new client profile.

        Args:
            client_id: Client ID without prefix
            client_name: Name of the client
            phone_number: Client's phone number

        Returns:
            The created item
        """
        # Format client_id with prefix if not already formatted
        formatted_client_id = (
            client_id if client_id.startswith("CLIENT#") else f"CLIENT#{client_id}"
        )

        timestamp = int(time.time())

        item = {
            "client_id": formatted_client_id,
            "secondary_key": "PROFILE",
            "item_type": "Client",
            "client_name": client_name,
            "profile_added": timestamp,
            "profile_updated": timestamp,
            "phone_number": phone_number,
        }

        try:
            self.table.put_item(Item=item)
            return item
        except ClientError as e:
            print(f"Error creating client profile: {e}")
            raise

    def create_transaction(
        self,
        client_id: str,
        transaction_id: str,
        asset_id: str,
        broker_id: str,
        transaction_type: str,
        quantity: int,
        price_per_unit: str,
    ) -> Dict:
        """
        Create a new transaction record.

        Args:
            client_id: Client ID
            transaction_id: Transaction ID
            asset_id: Asset ID
            broker_id: Broker ID
            transaction_type: Type of transaction (BUY/SELL)
            quantity: Number of units
            price_per_unit: Price per unit

        Returns:
            The created transaction item
        """
        # Format IDs with prefixes if not already formatted
        formatted_client_id = (
            client_id if client_id.startswith("CLIENT#") else f"CLIENT#{client_id}"
        )
        formatted_asset_id = (
            asset_id if asset_id.startswith("ASSET#") else f"ASSET#{asset_id}"
        )
        formatted_broker_id = (
            broker_id if broker_id.startswith("BROKER#") else f"BROKER#{broker_id}"
        )

        # Generate timestamp for transaction
        timestamp = int(time.time())
        transaction_date_iso = datetime.utcnow().isoformat() + "Z"

        # Generate sort key with timestamp and transaction id for ordering
        sort_key = f"TRANSACTION#{transaction_date_iso}#{transaction_id}"

        item = {
            "client_id": formatted_client_id,
            "secondary_key": sort_key,
            "item_type": "Transaction",
            "transaction_id": transaction_id,
            "asset_id": formatted_asset_id,
            "broker_id": formatted_broker_id,
            "transaction_type": transaction_type,
            "quantity": quantity,
            "price_per_unit": price_per_unit,
            "transaction_date": timestamp,
        }

        try:
            self.table.put_item(Item=item)
            return item
        except ClientError as e:
            print(f"Error creating transaction: {e}")
            raise

    def get_client_profile(self, client_id: str) -> Optional[Dict]:
        """
        Get client profile by ID.

        Args:
            client_id: Client ID

        Returns:
            Client profile or None if not found
        """
        formatted_client_id = (
            client_id if client_id.startswith("CLIENT#") else f"CLIENT#{client_id}"
        )

        try:
            response = self.table.get_item(
                Key={"client_id": formatted_client_id, "secondary_key": "PROFILE"}
            )
            return response.get("Item")
        except ClientError as e:
            print(f"Error retrieving client profile: {e}")
            raise

    def get_client_transactions(self, client_id: str) -> List[Dict]:
        """
        Get all transactions for a specific client.

        Args:
            client_id: Client ID

        Returns:
            List of transaction items
        """
        formatted_client_id = (
            client_id if client_id.startswith("CLIENT#") else f"CLIENT#{client_id}"
        )

        try:
            response = self.table.query(
                KeyConditionExpression="client_id = :cid AND begins_with(#sk, :transaction)",
                ExpressionAttributeNames={"#sk": "secondary_key"},
                ExpressionAttributeValues={
                    ":cid": formatted_client_id,
                    ":transaction": "TRANSACTION#",
                },
            )
            return response.get("Items", [])
        except ClientError as e:
            print(f"Error retrieving client transactions: {e}")
            raise

    def update_client_profile(
        self, client_id: str, update_data: Dict[str, Any]
    ) -> Dict:
        """
        Update client profile with new values.

        Args:
            client_id: Client ID
            update_data: Dictionary containing fields to update

        Returns:
            Updated item
        """
        formatted_client_id = (
            client_id if client_id.startswith("CLIENT#") else f"CLIENT#{client_id}"
        )

        # Prepare update expression
        update_expression = "SET profile_updated = :updated"
        expression_values = {":updated": int(time.time())}

        # Add each field to update
        for key, value in update_data.items():
            if key not in ["client_id", "secondary_key", "item_type", "profile_added"]:
                update_expression += f", #{key} = :{key}"
                expression_values[f":{key}"] = value

        # Create attribute names dictionary
        expression_names = {
            f"#{key}": key
            for key in update_data
            if key not in ["client_id", "secondary_key", "item_type", "profile_added"]
        }

        try:
            response = self.table.update_item(
                Key={"client_id": formatted_client_id, "secondary_key": "PROFILE"},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_values,
                ExpressionAttributeNames=expression_names,
                ReturnValues="ALL_NEW",
            )
            return response.get("Attributes", {})
        except ClientError as e:
            print(f"Error updating client profile: {e}")
            raise
