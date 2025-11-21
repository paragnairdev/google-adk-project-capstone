# VR Cricket Strategist - Test Suite

This directory contains comprehensive test coverage for the `vr_cricket_strategist` module.

## Test Structure

```
tests/
├── __init__.py                 # Test package initialization
├── conftest.py                 # Shared fixtures and pytest configuration
├── test_tools.py              # Tests for tools module
├── test_data_loader.py        # Tests for data loading
├── test_config.py             # Tests for configuration
├── test_agent.py              # Tests for agent setup
└── README.md                  # This file
```

## Running Tests

### Run all tests
```bash
pytest agents/vr_cricket_strategist/tests/
```

### Run specific test file
```bash
pytest agents/vr_cricket_strategist/tests/test_tools.py
```

### Run specific test class
```bash
pytest agents/vr_cricket_strategist/tests/test_tools.py::TestGetVenueTrends
```

### Run specific test
```bash
pytest agents/vr_cricket_strategist/tests/test_tools.py::TestGetVenueTrends::test_venue_trends_basic
```

### Run with verbose output
```bash
pytest agents/vr_cricket_strategist/tests/ -v
```

### Run with coverage report
```bash
pytest agents/vr_cricket_strategist/tests/ --cov=agents.vr_cricket_strategist --cov-report=html
```

### Run only unit tests
```bash
pytest agents/vr_cricket_strategist/tests/ -m unit
```

### Run only integration tests
```bash
pytest agents/vr_cricket_strategist/tests/ -m integration
```

### Run evaluations
```bash
bash run_evaluations.sh
```


## Test Coverage

### test_tools.py
- **TestGetCurrentIdentity**: Tests for identity management
  - Identity retrieval from session state
  - Auto-injection of test profile when missing
  - Handling of partial state

- **TestGetVenueTrends**: Tests for venue trends analysis
  - Basic venue trends calculation
  - Filtering by pitch type
  - Filtering by stadium
  - Handling of missing data
  - Accurate statistical calculations

- **TestGetHeadToHead**: Tests for head-to-head analysis
  - Basic head-to-head statistics
  - Filtering by pitch type and stadium
  - Handling of missing data
  - Accurate win/loss/average calculations

- **TestToolIntegration**: Integration tests for tools working together

### test_data_loader.py
- **TestDataLoader**: Tests for data loading functionality
  - Successful data loading
  - Error handling for missing files
  - Dataframe structure validation
  - Required columns verification

- **TestDataIntegrity**: Tests for data quality
  - Data type validation
  - Null value checks
  - Valid format values (T20, ODI, Test)
  - Valid innings numbers (1, 2)
  - Valid result values (Win, Loss, Draw, Tie)

### test_config.py
- **TestConfig**: Tests for configuration settings
  - Configuration imports
  - Model name and app name validation
  - Retry configuration
  - Dataset path definitions
  - Environment variable settings

- **TestConfigPaths**: Tests for path resolution
  - Base directory resolution
  - CSV file existence
  - File type validation

- **TestEnvironmentVariables**: Tests for environment setup
  - API key handling
  - Dotenv loading

### test_agent.py
- **TestAgentConfiguration**: Tests for agent setup
  - Model configuration
  - Agent existence and types

- **TestSubAgents**: Tests for individual agents
  - FactFinder configuration and tools
  - Tactician configuration
  - BoycottWriter persona
  - StatAnalyst configuration and tools

- **TestCompositeAgents**: Tests for sequential/parallel agents
  - GamePlanGenerator configuration
  - Root agent configuration
  - Sub-agent ordering

- **TestAgentInstructions**: Tests for agent instructions
  - Persona accuracy
  - Routing logic
  - Decision-making instructions

- **TestToolIntegration**: Tests for tool-agent integration
  - Tool callability
  - No duplicate tools

## Fixtures

Shared fixtures are defined in `conftest.py`:

- `sample_players_data`: Sample player dataframe
- `sample_matches_data`: Sample match dataframe
- `mock_tool_context`: Mock ToolContext for testing
- `mock_tool_context_with_identity`: ToolContext with identity set
- `sample_venue_trends_response`: Sample venue trends response
- `sample_head_to_head_response`: Sample head-to-head response
- `sample_empty_matches_data`: Empty dataframe with correct structure

## Writing New Tests

When adding new tests:

1. Use descriptive test names starting with `test_`
2. Organize tests into classes starting with `Test`
3. Use fixtures from `conftest.py` for common test data
4. Mock external dependencies (databases, API calls)
5. Test both success and error cases
6. Add appropriate markers (`@pytest.mark.unit`, etc.)

Example:
```python
def test_new_feature(sample_matches_data):
    """Test description"""
    # Arrange
    expected = "expected value"
    
    # Act
    result = function_to_test(sample_matches_data)
    
    # Assert
    assert result == expected
```

## Continuous Integration

These tests should be run:
- Before committing changes
- In CI/CD pipeline
- Before merging pull requests

## Dependencies

Required packages for testing:
- pytest
- pytest-cov (optional, for coverage reports)
- pandas
- unittest.mock (built-in)

Install test dependencies:
```bash
pip install pytest pytest-cov
```

## Troubleshooting

### Import Errors
If you encounter import errors, ensure:
1. You're running pytest from the project root
2. The project root is in your PYTHONPATH
3. All `__init__.py` files are present

### Mock Issues
If mocks aren't working:
1. Check that you're patching the right import path
2. Ensure patches are applied before the function is called
3. Verify mock return values match expected types

### Data Issues
If data-related tests fail:
1. Check that CSV files exist in `vr_cricket_dataset/`
2. Verify data format matches test expectations
3. Ensure required columns are present

