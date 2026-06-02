# Transaction State Machine

## States

* CREATED
* ROUTE_SELECTED
* AUTH_INITIATED
* AUTHORISED
* AUTH_FAILED
* CAPTURE_INITIATED
* CAPTURED
* CAPTURE_FAILED
* REFUNDED

## State Diagram

CREATED
↓
ROUTE_SELECTED
↓
AUTH_INITIATED
├── AUTHORISED
│   ↓
│   CAPTURE_INITIATED
│   ├── CAPTURED
│   └── CAPTURE_FAILED
│
└── AUTH_FAILED

CAPTURED
↓
REFUNDED

## Purpose

The state machine ensures every transaction follows a valid lifecycle and provides a complete audit trail.
