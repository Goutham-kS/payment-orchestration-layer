# import os

# from fastapi import FastAPI

# from app.database import (
#     Base,
#     engine
# )

# # =========================================================
# # IMPORT ROUTERS
# # =========================================================

# from app.api import payments

# from app.api import mock_gateways

# import app.api.webhooks as webhooks


# # =========================================================
# # CREATE FASTAPI APP
# # =========================================================

# app = FastAPI()


# # =========================================================
# # CREATE DATABASE TABLES
# # =========================================================

# # Skip DB creation during pytest

# if os.getenv("PYTEST_RUNNING") != "1":

#     Base.metadata.create_all(
#         bind=engine
#     )


# # =========================================================
# # REGISTER ROUTERS
# # =========================================================

# # Payments API

# app.include_router(
#     payments.router
# )

# # Mock gateway APIs

# app.include_router(
#     mock_gateways.router
# )

# # Webhook APIs

# app.include_router(
#     webhooks.router
# )


# =========================================================
# IMPORT ROUTERS
# =========================================================

import os

from fastapi import FastAPI

from app.database import (
    Base,
    engine
)

# =========================================================
# IMPORT ROUTERS
# =========================================================

from app.api import payments

from app.api import mock_gateways

import app.api.webhooks as webhooks

import app.api.reconciliation as reconciliation


# =========================================================
# CREATE FASTAPI APP
# =========================================================

app = FastAPI()


# =========================================================
# CREATE DATABASE TABLES
# =========================================================

# Skip DB creation during pytest

if os.getenv("PYTEST_RUNNING") != "1":

    Base.metadata.create_all(
        bind=engine
    )


# =========================================================
# REGISTER ROUTERS
# =========================================================

# Payments API

app.include_router(
    payments.router
)

# Mock gateway APIs

app.include_router(
    mock_gateways.router
)

# Webhook APIs

app.include_router(
    webhooks.router
)

# Reconciliation APIs

app.include_router(
    reconciliation.router
)