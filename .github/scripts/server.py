"""
FastMCP Server with Echo and AWS S3 Tools
"""

import boto3
from mcp.server.fastmcp import FastMCP

# Create server
mcp = FastMCP("MCP Server with AWS Tools")


@mcp.tool()
def echo(text: str) -> str:
    """Echo the input text"""
    return text


@mcp.tool()
def list_s3_buckets() -> str:
    """List all S3 buckets in the AWS account

    Returns:
        A formatted string containing the list of bucket names and their creation dates
    """
    try:
        s3_client = boto3.client('s3')
        response = s3_client.list_buckets()

        if not response.get('Buckets'):
            return "No S3 buckets found in this AWS account."

        bucket_list = []
        for bucket in response['Buckets']:
            name = bucket['Name']
            creation_date = bucket['CreationDate'].strftime('%Y-%m-%d %H:%M:%S')
            bucket_list.append(f"- {name} (Created: {creation_date})")

        result = f"Found {len(bucket_list)} S3 bucket(s):\n" + "\n".join(bucket_list)
        return result

    except Exception as e:
        return f"Error listing S3 buckets: {str(e)}"


if __name__ == "__main__":
    mcp.run(transport="sse")