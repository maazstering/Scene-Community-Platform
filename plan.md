# Scene - Production Architecture Implementation

## Overview
Building a complete, production-ready mobile-web-first social app for Pakistan with activity matching, event hosting, and venue booking. Invite-only with vouch-based trust system.

**Tech Stack:** Reflex (mobile-web UI), FastAPI backend, PostgreSQL + SQLAlchemy, Redis cache/queues, Celery workers, S3-compatible storage, WebSockets, Docker infrastructure.

**Key Features:** Invite-only onboarding, activity partner finding, event hosting/ticketing, venue discovery/booking, vouch system, payment abstraction (PayFast/JazzCash/Easypaisa), mobile-web share links, dark premium theme.

---

## Phase 1: Foundation - Data Model, Auth & Core Infrastructure ✅
**Goal:** Set up complete data model with all entities, authentication system with OTP, and development infrastructure.

### Completed:
- ✅ Complete FastAPI backend with 22 REST API endpoints
- ✅ SQLAlchemy models for all entities (User, Activity, Event, Venue, Vouch, Circle, etc.)
- ✅ Pydantic schemas for request/response validation
- ✅ JWT authentication system with token creation/verification
- ✅ OpenAPI documentation at `/docs`
- ✅ Stub implementations for all endpoints
- ✅ In-memory demo data system with 20 Pakistani users
- ✅ 6 venues (paddle courts), 12 activities, 4 events, 4 circles
- ✅ Deterministic seed (random.seed(42))
- ✅ DiceBear avatars for all users
- ✅ Vouches terminology enforced throughout

**API Endpoints Created:**
- **Auth:** Login, Logout, Get Me, Refresh Token
- **Users:** List, Get, Update, Get Vouches
- **Activities:** CRUD, Join Requests, Approve/Reject
- **Events:** CRUD, Join Requests
- **Venues:** List, Get Details, Get Slots
- **Vouches:** Create, List
- **Circles:** CRUD, Add Members

---

## Phase 2: Frontend Integration with Backend APIs ✅
**Goal:** Update Reflex frontend to consume backend APIs, replacing in-memory data with real API calls.

### Completed:
- ✅ Created HTTP client utility (`app/utils/api_client.py`)
  - GET, POST, PATCH, DELETE methods
  - JWT token management via parameter
  - Error handling with httpx exceptions
  - Response validation and JSON parsing
  
- ✅ Updated BaseState for authentication
  - Real API call to POST `/api/v1/auth/login`
  - Token storage in localStorage (not cookies)
  - Logout API call to POST `/api/v1/auth/logout`
  - Token validation with optional cookies parameter
  - Fixed cookie parameter type handling
  
- ✅ Updated SceneState for API integration
  - Prepared for API calls to GET `/api/v1/users`
  - Prepared for API calls to GET `/api/v1/activities`
  - Prepared for API calls to GET `/api/v1/events`
  - Prepared for API calls to GET `/api/v1/venues`
  - Updated create_activity_post to call POST `/api/v1/activities`
  - Updated join_activity_request to call POST `/api/v1/activities/{id}/requests`
  
- ✅ Added error handling & loading states
  - `loading: bool` state variable
  - `error_message: str` state variable
  - `success_message: str` state variable
  - Try/except blocks around API calls
  - Toast notifications for errors and success
  
- ✅ Updated WizardState for API integration
  - publish_activity calls POST `/api/v1/activities`
  - publish_event calls POST `/api/v1/events`
  - Error handling with user feedback

### What's Working:
- ✅ HTTP client with token authentication
- ✅ Login form with API integration (stub backend)
- ✅ Token storage in localStorage
- ✅ Auth check on page load
- ✅ Error handling for API failures
- ✅ All UI components render correctly

### Known Limitation:
- ⚠️ Backend API returns stub responses (501 Not Implemented)
- ⚠️ Need to implement actual database operations in Phase 3

---

## Phase 3: Backend Implementation - Database Operations (NEXT) 🎯
**Goal:** Implement actual database operations, replacing stub responses with real CRUD operations.

### Tasks:
- [ ] **Database Setup** - Docker compose with PostgreSQL
- [ ] **Run Migrations** - Alembic migrations for all tables
- [ ] **User Management** - Implement user CRUD operations
  - [ ] POST /api/v1/auth/login - Create or get user
  - [ ] GET /api/v1/users - List all users with pagination
  - [ ] GET /api/v1/users/{id} - Get user by ID
  - [ ] PATCH /api/v1/users/{id} - Update user profile
  
- [ ] **Activity Operations** - Implement activity CRUD
  - [ ] POST /api/v1/activities - Create activity with host
  - [ ] GET /api/v1/activities - List with filters (type, date, radius)
  - [ ] GET /api/v1/activities/{id} - Get activity details
  - [ ] POST /api/v1/activities/{id}/requests - Create join request
  - [ ] GET /api/v1/activities/{id}/requests - List requests (host only)
  - [ ] PATCH /api/v1/activities/{id}/requests/{req_id} - Approve/reject
  
- [ ] **Event Operations** - Implement event CRUD
  - [ ] POST /api/v1/events - Create event
  - [ ] GET /api/v1/events - List events
  - [ ] GET /api/v1/events/{id} - Get event details
  - [ ] POST /api/v1/events/{id}/requests - Request to join
  
- [ ] **Venue Operations** - Implement venue queries
  - [ ] GET /api/v1/venues - List venues with filters
  - [ ] GET /api/v1/venues/{id} - Get venue details
  - [ ] GET /api/v1/venues/{id}/slots - Get available slots
  
- [ ] **Vouch System** - Implement vouch CRUD
  - [ ] POST /api/v1/vouches - Create vouch (one per pair)
  - [ ] GET /api/v1/users/{id}/vouches - Get user vouches
  
- [ ] **Circle Operations** - Implement circle management
  - [ ] POST /api/v1/circles - Create circle
  - [ ] POST /api/v1/circles/{id}/members - Add member
  - [ ] GET /api/v1/circles/{id} - Get circle details
  
- [ ] **Testing** - Test all endpoints with real database
  - [ ] Seed database with demo data
  - [ ] Test authentication flow
  - [ ] Test activity creation and join requests
  - [ ] Test event creation
  - [ ] Test vouch creation with uniqueness constraint

---

## Phase 4: Activities & Events - Full CRUD with UI Integration
**Goal:** Complete activity partner matching system, event hosting with tickets, and mobile-web share links.

### Tasks:
- [ ] Activity creation wizard (6 steps) - Already built, connect to API
- [ ] Event creation wizard (6 steps) - Already built, connect to API
- [ ] Activity detail pages with join requests
- [ ] Event detail pages with ticket purchasing
- [ ] Share link generation and public pages
- [ ] Host inbox for managing requests
- [ ] Batch approve functionality
- [ ] Auto-approve settings

---

## Phase 5: Home Dashboard + Detail Pages + Join Request Flow
**Goal:** Complete home dashboard with all sections, activity/event detail pages, and request-to-join workflow.

### Tasks:
- [ ] For You — People section with API data
- [ ] Open-to-Join — People section
- [ ] Public Activities feed from API
- [ ] Featured Events section
- [ ] Places to Book section
- [ ] From Your Circles section
- [ ] Join request creation with API
- [ ] Request approval workflow
- [ ] Capacity enforcement
- [ ] Waitlist logic

---

## Phase 6: Explore & Filters + Host Inbox
**Goal:** Add discovery with filters, map toggle, and host approval interface.

### Tasks:
- [ ] Explore page with tabs (People, Activities, Places, Events)
- [ ] Filter chips (Activity type, Date & time, Radius, Circles)
- [ ] Search bar functionality
- [ ] List/Map toggle with geospatial queries
- [ ] Host inbox with pending requests
- [ ] Auto-approve settings per host
- [ ] Waitlist management
- [ ] Public share pages (/a/{slug}, /e/{slug})

---

## Phase 7: Venues & Discovery - Booking System
**Goal:** Complete venue discovery and booking with payment.

### Tasks:
- [ ] Venue discovery with filters
- [ ] Venue slot availability system
- [ ] Booking flow with provisional holds
- [ ] Payment provider integration stubs
- [ ] "Pay at venue" option
- [ ] Booking confirmation with QR codes

---

## Phase 8: Testing, Security & Production Readiness
**Goal:** Add comprehensive tests, security hardening, and production deployment.

### Tasks:
- [ ] Unit tests for all models and business logic
- [ ] API integration tests
- [ ] Rate limiting on OTP and join requests
- [ ] CSRF protection
- [ ] PII encryption
- [ ] Audit tables for moderation
- [ ] Prometheus metrics
- [ ] OpenTelemetry tracing
- [ ] Health check endpoints
- [ ] IaC templates for deployment
- [ ] CI/CD pipeline

---

## Current Status
✅ **Phase 2 COMPLETE!** Frontend now integrated with backend APIs!

🎯 **Phase 3 Next:** Implement actual database operations to replace stub responses.

**Major Accomplishments:**
- ✅ Complete FastAPI backend with 22 endpoints
- ✅ HTTP client utility with JWT token management
- ✅ Authentication flow with localStorage
- ✅ Error handling and loading states
- ✅ All API endpoints documented in OpenAPI
- ✅ Frontend ready to consume real API data

**Ready to Build:**
1. Set up PostgreSQL database with Docker
2. Run Alembic migrations
3. Implement user CRUD operations
4. Implement activity/event CRUD operations
5. Test end-to-end flows with real database
6. Connect frontend to live data