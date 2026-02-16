# Testing Documentation

## Overview

This document covers all testing performed on the Mental Health Tracker application, including automated Python tests and manual JavaScript tests.

## Test Structure

```
tracker/
├── test_models.py        # model unit tests
├── test_forms.py         # form validation tests
├── test_views.py         # view tests (auth, CRUD, permissions, pagination)
└── tests_user_flow.py    # integration test (full user journey)
```

## Running Tests

```bash
# run all tests
python manage.py test tracker

# run all tests with details
python manage.py test tracker -v 2

# run a specific test file
python manage.py test tracker.test_models
python manage.py test tracker.test_forms
python manage.py test tracker.test_views
python manage.py test tracker.tests_user_flow
```

---

## Automated Python Tests

### Model Tests (`test_models.py`)

| Test | What it checks |
|------|---------------|
| `test_create_mood_entry` | MoodEntry can be created with score and notes |
| `test_mood_entry_str` | String representation includes username and score |
| `test_mood_ordering` | Entries are ordered by date, newest first |
| `test_create_resource` | Resource can be created with all fields |
| `test_resource_str` | Resource string representation returns the title |

### Form Tests (`test_forms.py`)

| Test | What it checks |
|------|---------------|
| `test_valid_form` | RegisterForm accepts valid data |
| `test_invalid_email` | RegisterForm rejects bad email format |
| `test_passwords_do_not_match` | RegisterForm rejects mismatched passwords |
| `test_duplicate_username` | RegisterForm rejects existing username |
| `test_valid_mood_form` | MoodEntryForm accepts valid score and notes |
| `test_mood_without_notes` | MoodEntryForm allows empty notes |
| `test_invalid_mood_score` | MoodEntryForm rejects score above 10 |
| `test_notes_too_long` | MoodEntryForm rejects notes over 500 chars |

### View Tests (`test_views.py`)

| Test | What it checks |
|------|---------------|
| **Home** | |
| `test_home_page_loads` | Home page returns 200 and correct template |
| **Register** | |
| `test_register_page_loads` | Register page returns 200 |
| `test_register_valid_user` | Valid registration creates user and redirects |
| `test_register_invalid_data_stays_on_page` | Invalid data re-renders the form |
| **Logout** | |
| `test_logout_redirects_to_home` | Logout redirects to home page |
| **Mood List** | |
| `test_redirect_if_not_logged_in` | Anonymous users get redirected to login |
| `test_logged_in_user_can_view` | Logged in users can see their mood list |
| `test_user_only_sees_own_moods` | Users cannot see other users' entries |
| `test_pagination_shows_max_10` | Only 10 entries per page |
| `test_pagination_page_2` | Page 2 shows remaining entries |
| **Mood Create** | |
| `test_redirect_if_not_logged_in` | Anonymous users get redirected |
| `test_create_page_loads` | Create form renders correctly |
| `test_create_valid_mood` | Valid POST creates entry and redirects |
| `test_create_invalid_mood_stays_on_page` | Invalid score re-renders form |
| **Mood Edit** | |
| `test_redirect_if_not_logged_in` | Anonymous users get redirected |
| `test_edit_page_loads` | Edit form renders with existing data |
| `test_edit_valid_data` | Valid POST updates the entry |
| `test_cannot_edit_other_users_mood` | Returns 404 for another user's entry |
| `test_edit_nonexistent_mood_returns_404` | Returns 404 for invalid ID |
| **Mood Delete** | |
| `test_redirect_if_not_logged_in` | Anonymous users get redirected |
| `test_delete_confirmation_page_loads` | Confirmation page renders |
| `test_delete_mood_entry` | POST request deletes the entry |
| `test_cannot_delete_other_users_mood` | Returns 404 for another user's entry |
| `test_delete_nonexistent_mood_returns_404` | Returns 404 for invalid ID |
| **Mood Trends** | |
| `test_redirect_if_not_logged_in` | Anonymous users get redirected |
| `test_trends_page_loads` | Trends page renders correctly |
| `test_trends_context_has_required_data` | Context includes labels, scores, stats |
| `test_trends_with_no_data` | Works with no mood entries (defaults to 0) |
| **Resources** | |
| `test_redirect_if_not_logged_in` | Anonymous users get redirected |
| `test_resource_page_loads` | Resources page renders correctly |
| `test_resources_grouped_by_category` | Resources are grouped into 4 categories |
| **Privacy** | |
| `test_privacy_page_loads` | Privacy page returns 200 |

### Integration Test (`tests_user_flow.py`)

| Test | What it checks |
|------|---------------|
| `test_complete_user_flow` | Full CRUD journey: login → create mood → view list → edit mood → delete mood → confirm deletion |

### Test Results

**46 tests passing**

```
Found 46 test(s).
..............................................
----------------------------------------------------------------------
Ran 46 tests in ~17s

OK
```

---

## Manual JavaScript Tests

The JavaScript in this project (`tracker/static/tracker/js/main.js`) handles UI interactions and the Chart.js mood trends graph. Since the JS is vanilla (no framework/bundler), it was tested manually across browsers.

### JS Validation

The JavaScript file was validated using [JSHint](https://jshint.com/) with no major errors. The `/*jslint*/` and `/*global*/` directives at the top of `main.js` declare browser globals and enable strict mode.

### Navbar Hover Effects

| # | Test | Steps | Expected | Result |
|---|------|-------|----------|--------|
| 1 | Primary nav button hover | Hover over "Get Started" button | Button lifts up and shadow appears | Pass |
| 2 | Primary nav button leave | Move mouse away from button | Button returns to original position | Pass |
| 3 | Sign in link hover | Hover over "Sign In" link | Text colour changes to purple | Pass |

### Feature Card Hover Effects

| # | Test | Steps | Expected | Result |
|---|------|-------|----------|--------|
| 4 | Card hover on homepage | Hover over a feature card | Card lifts up with shadow | Pass |
| 5 | Card mouse leave | Move mouse away from card | Card returns to original position | Pass |

### Button Hover Effects

| # | Test | Steps | Expected | Result |
|---|------|-------|----------|--------|
| 6 | Primary action button hover | Hover over green action button | Button lifts with green shadow | Pass |
| 7 | Update button hover | Hover over purple update button | Button lifts with purple shadow | Pass |
| 8 | Archive button hover | Hover over orange archive button | Button lifts with orange shadow | Pass |

### Mood Form Interactions

| # | Test | Steps | Expected | Result |
|---|------|-------|----------|--------|
| 9 | Slider colour change | Move the mood slider from 0 to 10 | Colour changes from red to green | Pass |
| 10 | Score display updates | Move the slider | Number next to slider updates in real time | Pass |
| 11 | Character counter | Type in the notes field | Counter shows current/max characters | Pass |
| 12 | Counter with maxlength | Type past 500 characters | Browser prevents further input, counter shows 500/500 | Pass |

### Mood Trends Chart

| # | Test | Steps | Expected | Result |
|---|------|-------|----------|--------|
| 13 | Chart renders with data | Navigate to Mood Trends with existing entries | Line chart displays with correct data points | Pass |
| 14 | Chart renders without data | Navigate to Mood Trends with no entries | Chart displays with all zeros, no errors | Pass |
| 15 | Chart.js loads async | Check network tab | Chart.js loads from CDN only on trends page | Pass |
| 16 | Chart.js load failure | Block CDN in dev tools, reload trends page | No console errors, page still usable | Pass |

### Responsiveness

| # | Test | Steps | Expected | Result |
|---|------|-------|----------|--------|
| 17 | Mobile navbar | Resize to 375px width | Navbar collapses, hamburger menu works | Pass |
| 18 | Tablet layout | Resize to 768px width | Cards stack correctly, chart resizes | Pass |
| 19 | Desktop layout | Full width (1200px+) | All elements positioned correctly | Pass |

### Browser Compatibility

| Browser | Version | Result |
|---------|---------|--------|
| Chrome | Latest | Pass |
| Firefox | Latest | Pass |
| Safari | Latest | Pass |

---

## Bugs Found and Fixed

| Bug | Where | Fix |
|-----|-------|-----|
| Integration test used wrong field name (`score` instead of `mood_score`) | `tests_user_flow.py` | Corrected to `mood_score` to match the MoodEntryForm field |
| Integration test used wrong URL name (`mood_update` instead of `mood_edit`) | `tests_user_flow.py` | Corrected to `mood_edit` to match urls.py |
| Views returned 500 error for non-existent or unauthorized mood entries | `views.py` | Changed `MoodEntry.objects.get()` to `get_object_or_404()` in `mood_edit` and `mood_delete` |

## Unfixed Bugs

No known unfixed bugs at this time.
