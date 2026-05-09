---

```markdown
# Coffee Store Project

## Project Overview
An e-commerce website specialized in selling coffee and coffee equipment.
Supports Arabic and English languages (i18n).

## Tech Stack
- Python 3.12+
- Django 5.x
- PostgreSQL (production) / SQLite (development)
- Bootstrap 5 (RTL support for Arabic)
- Django REST Framework (if API needed)
- django-environ for environment variables

## Project Structure
```
coffee_store/
│
├── config/           ← Main project settings
├── apps/
│   ├── accounts/     ← Users, authentication, addresses
│   ├── products/     ← Products, categories, images
│   ├── cart/         ← Shopping cart and cart items
│   ├── orders/       ← Orders, order items, payments
│   └── reviews/      ← Product reviews and ratings
│
├── templates/        ← HTML templates
├── static/           ← CSS, JS, images
├── media/            ← Uploaded product images
└── requirements.txt
```

## Apps & Relationships
- **accounts** → base app, all other apps depend on it
- **products** → depends on nothing
- **cart** → depends on accounts + products
- **orders** → depends on accounts + products + cart
- **reviews** → depends on accounts + products

## Database Relationships
- User → Cart: One-to-One
- Cart → CartItem: One-to-Many
- User → Orders: One-to-Many
- Order → OrderItem: One-to-Many
- Product → Category: Many-to-One
- User → Review: One-to-Many
- Product → Review: One-to-Many

## Coding Conventions
- Use Class-Based Views (CBV) always
- Follow PEP8 strictly
- English variable names and comments
- Use django-environ for all sensitive data (.env file)
- Never hardcode passwords, keys, or secrets

## Security Rules
- Validate all inputs via Django Forms or DRF Serializers
- Use @login_required and permissions on protected views
- Never expose sensitive data in responses

## Error Handling
- Use Django logging framework for all errors
- Return clear user-friendly error messages

## Performance
- Use select_related() and prefetch_related() to avoid N+1 queries
- Apply Django caching where needed

## Testing
- Write Django TestCase for every model and view
- Cover both normal and edge cases

## Instructions for Claude
- Build ONE app at a time
- Start with Models only, wait for confirmation before proceeding
- Never mix logic and templates in the same step
- Always mention new dependencies to add to requirements.txt
- Ask before making any structural changes
## How We Work Together
- We discuss and plan here in Arabic
- Claude Code in VS Code handles all code execution
- I give prompts to Claude Code in English
- You give me the prompt first, I send it to Claude Code, then report back

## Workflow for Each Feature
1. You give me the English prompt to send to Claude Code
2. I send it and report the result back to you
3. We review together before moving to next step

## Current Progress
- All 5 apps models are complete and migrated
- All models registered in admin panel
- Next step: Views, URLs, Templates

## What's Done
- accounts: CustomUser, Address ✅
- products: Category, Product, ProductImage ✅
- cart: Cart, CartItem ✅
- orders: Order, OrderItem ✅
- reviews: Review ✅