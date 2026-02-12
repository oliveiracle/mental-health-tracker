# Testing Documentation

## Overview

This document outlines the testing strategy and test cases for the Mental Health Tracker application.

## Test Structure

Tests are organized in the `tracker/tests/` directory:

```
tracker/tests/
├── __init__.py
├── test_models.py
├── test_forms.py
└── test_views.py
```

## Running Tests

### Run All Tests
```bash
python manage.py test tracker.tests
```

### Run Specific Test Module
```bash
python manage.py test tracker.tests.test_models
python manage.py test tracker.tests.test_forms
python manage.py test tracker.tests.test_views
```

### Run with Verbosity
```bash
python manage.py test tracker.tests -v 2
```

## Test Coverage

### Model Tests (`test_models.py`)

#### MoodEntry Model
- **test_mood_entry_creation**: Validates mood entry creation with all required fields
- **test_mood_entry_str**: Tests string representation format
- **test_mood_entry_ordering**: Ensures entries are ordered by date (newest first)
- **test_mood_choices**: Verifies mood score choices and display values

### Form Tests (`test_forms.py`)

#### RegisterForm
- **test_register_form_valid**: Tests valid user registration data
- **test_register_form_invalid_password**: Validates password mismatch handling

#### MoodEntryForm
- **test_mood_entry_form_valid**: Tests valid mood entry data
- **test_mood_entry_form_invalid_score**: Validates mood score range (0-10)
- **test_mood_entry_form_optional_notes**: Confirms notes field is optional

### View Tests (`test_views.py`)

#### HomeViewTest
- **test_home_page_loads**: Verifies home page accessibility (200 status)

#### MoodListViewTest
- **test_redirect_if_not_logged_in**: Ensures login requirement (302 redirect)
- **test_logged_in_user_can_view**: Validates authenticated access (200 status)

#### MoodCreateViewTest
- **test_can_create_mood**: Tests mood entry creation through POST request

## Test Results

Current test suite status: **11 tests passing**

```
Found 11 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
...........
----------------------------------------------------------------------
Ran 11 tests in ~3.8s

OK
Destroying test database for alias 'default'...
```

## Best Practices

1. **Isolation**: Each test uses a fresh test database
2. **Authentication**: Tests use `Client` for simulating logged-in users
3. **Coverage**: Tests cover models, forms, and views
4. **Assertions**: Clear, specific assertions for expected behavior
5. **Setup**: Common test data created in `setUp()` methods

## Future Testing Considerations

- Add integration tests for complete user workflows
- Implement tests for mood trends visualization
- Add tests for resource listing functionality
- Consider adding performance tests for pagination
- Add tests for edge cases and error handling
