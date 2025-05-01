import boto3
from botocore.exceptions import ClientError


def create_financial_portfolio_table(
    table_name="transaction-table", region="us-west-2", endpoint_url=None
):
    kwargs = {"region_name": region}
    if endpoint_url:
        kwargs.update(
            {
                "endpoint_url": endpoint_url,
                "aws_access_key_id": "local",
                "aws_secret_access_key": "local",
            }
        )

    dynamodb = boto3.resource("dynamodb", **kwargs)

    # Check if table already exists
    existing_tables = [table.name for table in dynamodb.tables.all()]
    if table_name in existing_tables:
        print(f"Table {table_name} already exists.")
        return dynamodb.Table(table_name)

    # Create table with key schema matching the DynamoDBTableManager usage
    try:
        table_resource = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {"AttributeName": "client_id", "KeyType": "HASH"},  # Partition key
                {"AttributeName": "secondary_key", "KeyType": "RANGE"},  # Sort key
            ],
            AttributeDefinitions=[
                {"AttributeName": "client_id", "AttributeType": "S"},
                {"AttributeName": "secondary_key", "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
        )

        print(f"Creating table {table_name}...")
        table_resource.meta.client.get_waiter("table_exists").wait(TableName=table_name)
        print(f"Table {table_name} created successfully!")
        return table_resource

    except ClientError as e:
        print(f"Error creating table: {e}")
        raise


if __name__ == "__main__":

    # If running in Docker, use the service name as hostname
    # endpoint_url = "http://dynamodb-local:8000"
    # If running locally (outside Docker), use localhost
    # Uncomment the line below when running on local machine
    # endpoint_url = "http://localhost:8000"

    url = "http://localhost:8000"

    table = create_financial_portfolio_table(
        table_name="transaction-table", endpoint_url=url
    )

    print(f"Table status: {table.table_status}")
