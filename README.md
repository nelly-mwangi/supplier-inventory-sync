# Supplier Inventory Sync

## Project Overview

This project demonstrates a supplier inventory synchronization system built with FastAPI and GraphQL.

The system allows a support agent to query product inventory using GraphQL while supplier inventory updates are received through a webhook.

## Original Scope: Polling Architecture

The original requirement used a polling approach.

The application periodically requested inventory information from the supplier.

The architecture was:

Supplier Inventory Source
        ↓
Polling System
        ↓
GET /poll
        ↓
Application

The polling implementation was completed and tested before the project requirements changed.

## Scope Change: Webhook Automation

The supplier integration changed from polling to webhook-based updates.

Instead of the application repeatedly requesting inventory data, the supplier now sends inventory events directly to the application.

The new architecture is:

Supplier
        ↓
POST /webhook/inventory
        ↓
Central Inventory Ledger
        ↓
GraphQL API
        ↓
Support Agent

## Idempotent Webhook Processing

Webhook events include a unique `event_id`.

The application stores processed event IDs to prevent duplicate events from being processed more than once.

When the same event is received again, the API returns:

```json
{
  "message": "Duplicate event ignored"
}