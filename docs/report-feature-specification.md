# ALBOT Report Feature Specification

This document provides a comprehensive specification of the bug reporting feature implemented in the `/report/*` routes
of the ALBOT web application. This specification can be used to re-implement the same features in a different project.

## Overview

The report feature allows users to submit bug reports related to voice channel (VC) connection issues in Discord. The
feature is implemented as a web form that collects specific information about the issue and sends it to the developers
through both a database entry and a Discord webhook notification.

## Routes

### `/report/commands/<category>`

This route handles both GET and POST requests for bug reporting:

- **GET**: Renders the report form with category-specific options
- **POST**: Processes the submitted form and stores the bug report

#### URL Parameters

- `category`: The category of the bug report. Must be one of:
    - `connect`: Issues with connecting to VC
    - `disconnect`: Issues with disconnecting from VC
    - `connect-attempt`: Issues during connection attempts
    - `disconnect-attempt`: Issues during disconnection attempts

#### Query Parameters (GET)

- `guild_id`: The Discord server ID where the issue occurred (required)

## Data Model

### Bug Reports Table

The bug reports are stored in a database table named `bug_reports` with the following structure:

| Field       | Type     | Description                                    |
|-------------|----------|------------------------------------------------|
| guild_id    | String   | The Discord server ID where the issue occurred |
| category    | String   | The category of the bug report                 |
| datetime    | DateTime | The timestamp when the report was submitted    |
| description | String   | The description of the issue                   |

## User Interface

### Report Form (`report.html`)

The report form is a simple web form that includes:

1. A notice directing users to the support server for subscription inquiries or if they need a response
2. A heading displaying the category name
3. A dropdown menu with predefined descriptions specific to the selected category
4. An option to enter a custom description if the predefined options don't match the issue
5. A submit button that is disabled until a description is selected or entered
6. Hidden form fields for category and guild_id

#### Category-Specific Descriptions

Each category has specific predefined descriptions:

- **connect** / **connect-attempt**:
    - "VCに接続しない" (Cannot connect to VC)
    - "接続したが喋らない" (Connected but not speaking)

- **disconnect** / **disconnect-attempt**:
    - "VCから切断しない" (Cannot disconnect from VC)
    - "切断されるが接続中扱いのまま" (Disconnected but still treated as connected)

### Thank You Page (`thank-you-for-reporting.html`)

After submitting a report, users are redirected to a simple thank you page that confirms their report has been received
and will be sent to the developers.

## Backend Logic

### Form Processing

When a user submits the form (POST request), the server:

1. Extracts the form data (guild_id, category, description)
2. Inserts a new record into the bug_reports_table with the current timestamp
3. Calculates the shard_id based on the guild_id
4. Sends a notification to a Discord webhook with:
    - The category of the bug
    - The description of the issue
    - The server ID and shard ID
    - A timestamp
5. Renders the thank-you-for-reporting.html template

## Dependencies

The report feature depends on:

1. **Flask**: Web framework for handling routes and rendering templates
2. **Dataset**: Library for database operations
3. **Requests**: Library for sending HTTP requests to the Discord webhook
4. **Discord Webhook**: External service for receiving notifications

## Environment Variables

- `REPORT_WEBHOOK`: The URL of the Discord webhook for sending bug report notifications
- `SHARD_COUNT`: The number of shards used by the Discord bot (used to calculate the shard_id)

## Implementation Notes

1. The feature is designed to collect specific information about voice channel connection issues
2. The form is pre-populated with common issues to make reporting easier for users
3. The feature sends notifications to developers in real-time through Discord
4. The feature stores reports in a database for later analysis
5. The UI is simple and focused on collecting the necessary information with minimal user effort

## Re-implementation Guidelines

When re-implementing this feature in a different project:

1. Set up a database table with the same structure as the bug_reports table
2. Create a Discord webhook for receiving notifications
3. Implement the routes for handling GET and POST requests
4. Create templates for the report form and thank you page
5. Ensure the form collects the necessary information (guild_id, category, description)
6. Implement the logic for processing the form data and sending notifications

By following this specification, you should be able to re-implement the same bug reporting feature in a different
project with the same functionality and user experience.