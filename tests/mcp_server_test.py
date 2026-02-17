import pytest
from letta.schemas.mcp import MCPServer
from letta.functions.mcp_client.types import MCPServerType, StdioServerConfig

def test_mcp_server_execution_mode_storage():
    """Test that execution_mode is stored in metadata_ JSON column."""
    
    # Create MCP server with client execution mode
    server = MCPServer(
        server_name="test-filesystem",
        server_type=MCPServerType.STDIO,
        stdio_config=StdioServerConfig(
            server_name="test-filesystem",
            type=MCPServerType.STDIO,
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem"],
        ),
        organization_id="org-123",
    )
    
    # Set execution_mode via metadata_
    server.set_execution_mode("client")
    
    # Verify it's stored correctly
    assert server.metadata_ is not None
    assert server.metadata_["execution_mode"] == "client"
    assert server.is_client_side() == True

def test_mcp_server_default_execution_mode():
    """Test that unset execution_mode defaults to non-client-side."""
    
    server = MCPServer(
        server_name="test-server-side",
        server_type=MCPServerType.SSE,
        server_url="https://example.com/mcp",
        organization_id="org-123",
    )
    
    # Don't set execution_mode - internal model returns None
    assert server.get_execution_mode() is None
    assert server.is_client_side() is False

def test_mcp_server_is_client_side():
    """Test is_client_side() helper method."""
    
    server = MCPServer(
        server_name="test-filesystem",
        server_type=MCPServerType.STDIO,
        stdio_config=StdioServerConfig(
            server_name="test-filesystem",
            type=MCPServerType.STDIO,
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem"],
        ),
        organization_id="org-123",
    )
    
    server.set_execution_mode("client")
    assert server.is_client_side() is True
    
    server.set_execution_mode("server")
    assert server.is_client_side() is False

def test_mcp_server_get_execution_mode():
    """Test get_execution_mode() returns correct value."""
    
    server = MCPServer(
        server_name="test-filesystem",
        server_type=MCPServerType.STDIO,
        stdio_config=StdioServerConfig(
            server_name="test-filesystem",
            type=MCPServerType.STDIO,
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem"],
        ),
        organization_id="org-123",
    )
    server.set_execution_mode("client")
    
    assert server.get_execution_mode() == "client"
    server.metadata_.pop("execution_mode", None)
    assert server.get_execution_mode() is None