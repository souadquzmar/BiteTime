# Architecture

## 1. Layer Breakdown & Responsibilities

```text
HTTP Request
     |
     v
Views / ViewSets
     |
     v
Serializers
     |
     v
Components
     |
     v
Services
     |
     v
External Systems
```

Not every request needs to pass through every layer. Simple CRUD operations may only require Views and Serializers, while more complex business operations may also use Components and Services.

### Views / ViewSets

**Location:** `apps/<app>/views.py`

Views and ViewSets are responsible strictly for HTTP-related concerns.

Responsibilities include:

* Handling incoming HTTP requests.
* Routing requests to the appropriate operation.
* Performing authentication and permission checks.
* Passing request data to serializers for validation.
* Returning the appropriate HTTP response and status code.

Views should not contain business rules or application-specific processing.

For example, a ViewSet should not contain logic for calculating discounts, changing an order's state, or communicating directly with an external API. Such logic belongs in the appropriate lower layer.

---

### Serializers

**Location:** `apps/<app>/serializers.py`

Serializers are responsible for input validation, payload transformation, and standard database interaction.

Responsibilities include:

* Validating incoming request data.
* Performing field-level and object-level validation.
* Transforming request payloads into Python and model data.
* Transforming model instances into response representations.
* Handling standard database persistence through `.create()` and `.update()`.

Serializers can contain straightforward ORM persistence logic.

When an operation requires reusable business logic or complex processing, the serializer should delegate that work to a Component rather than implementing the business rule itself.

Serializers should not communicate directly with external third-party services.

---

### Components

**Location:** `apps/<app>/components/` or a shared `components/` package

Components contain internal, reusable business logic.

They are used when logic goes beyond basic validation and standard database persistence, especially when the same business operation may be used from multiple parts of the application.

Examples include:

* Calculating a discount.
* Recalculating an order total.
* Applying business rules to an operation.
* Performing a state transition.
* Coordinating operations involving multiple models.
* Managing a database transaction containing several related operations.

Components are responsible for deciding **when and why** an external service is required.

When an operation needs an external integration, a Component may call the appropriate Service.

---

### Services

**Location:** `services/`

Services are responsible for communication with external systems and third-party integrations outside Django's core.

Examples include:

* AWS S3 for file storage.
* Stripe for payment processing.
* SendGrid for email delivery.
* Other third-party APIs or SDKs.

Services should hide the implementation details of external integrations from the rest of the application.

For example, application code should not need to directly import an external SDK such as `boto3`, `stripe`, or `sendgrid`. Instead, it should interact with a Service that provides the required functionality.

The Component decides **when and why** an external integration is needed, while the Service handles **how** to communicate with that external system.

---

## 2. Helpers vs. Utils

Helpers and Utils both contain reusable functions, but they differ in their dependency on application context.

|                            | `utils/`         | `helpers/`        |
| -------------------------- | ---------------- | ----------------- |
| Django-dependent           | No               | Usually yes       |
| Database/context-dependent | No               | Maybe             |
| Domain-specific            | No               | Maybe             |
| Reusable outside Django    | Yes              | Usually no        |
| Example                    | String sanitizer | Extract client IP |

### Utils

**Location:** `core/utils/`

Utils contain pure, domain-agnostic, standalone utility functions.

A utility function should not depend on Django, HTTP requests, database state, or model instances.

Examples include:

* String sanitization.
* Slug generation.
* String truncation.
* Timestamp formatting.
* General data transformation.

For example:

```python
def sanitize_string(value):
    return " ".join(value.strip().split())
```

This function does not need Django or any database state and could be reused in a normal Python application.

---

### Helpers

**Location:** `core/helpers/`

Helpers contain context-aware functions that are specifically related to Django or the application's domain.

They may work with:

* Django request objects.
* Django model instances.
* Database-related information.
* Application-specific parameters.

Examples include:

* Extracting a client's IP address from `request.META`.
* Extracting a bearer token from a Django request.

For example:

```python
def get_client_ip(request):
    return request.META.get("REMOTE_ADDR")
```

Unlike a general utility, this function depends on Django's request context.
