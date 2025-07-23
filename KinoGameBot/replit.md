# Telegram Merchandise Bot

## Overview

This is a Telegram bot for selling merchandise with a complete purchase cycle - from product selection to order tracking. The bot is built using the aiogram framework for Python and includes features like product catalog, shopping cart, order management, game integration, and admin panel.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The bot follows a modular architecture with clear separation of concerns:

### Core Components
- **Main Entry Point**: `main.py` - Initializes and starts the bot with all handlers
- **Configuration**: `config.py` - Centralized configuration including bot token, admin IDs, and product definitions
- **Database Layer**: `database.py` - SQLite database operations with async wrapper
- **Handlers**: Separate modules for different bot functions (start, catalog, cart, orders, admin, game, help)
- **Keyboards**: Inline and reply keyboard definitions
- **Utilities**: Helper functions for formatting and validation

### Database Design
- **SQLite Database**: Simple file-based storage (`bot_database.db`)
- **Key Tables**: 
  - Users (telegram_id, username, first_name, last_name)
  - Products (product_key, name, category, price, colors, sizes)
  - Orders (user_id, product_key, color, size, quantity, status, payment_status)
  - Cart (user_id, product_key, color, size, quantity)

## Key Components

### Bot Framework
- **aiogram v3**: Modern async Telegram bot framework
- **FSM (Finite State Machine)**: For handling multi-step user interactions
- **Memory Storage**: For state management during user sessions

### Product Management
- **Static Product Catalog**: Defined in `config.py` with t-shirts as main products
- **Product Variants**: Multiple colors (black, white) and sizes (S-XXL)
- **Pricing**: Fixed price of 2500 ₽ per item

### User Interface
- **Inline Keyboards**: Primary navigation method
- **Callback Queries**: For button interactions
- **Multi-language Support**: Russian language interface

### Order Processing
- **Shopping Cart**: Add/remove items with persistence
- **Order States**: pending, processing, shipped, delivered, cancelled
- **Payment Integration**: Placeholder for payment provider integration

### Admin Features
- **Admin Panel**: Order management and statistics
- **User Role Checking**: Admin ID-based authorization
- **Order Status Management**: Update order states and tracking

### Game Integration
- **External Game**: Links to "Киношлеп" (Cinema Slap) web game
- **URL Navigation**: Direct links to game website

## Data Flow

1. **User Registration**: Automatic user creation on first `/start` command
2. **Product Browsing**: Catalog → Product Details → Color/Size Selection
3. **Shopping Cart**: Add items → Review → Checkout
4. **Order Creation**: Address collection → Order confirmation → Payment
5. **Order Tracking**: Status updates → Admin management → Delivery confirmation

## External Dependencies

### Required Packages
- `aiogram`: Telegram bot framework
- `sqlite3`: Database operations (built-in Python)
- `asyncio`: Async programming support
- `logging`: Application logging

### External Services
- **Telegram Bot API**: Core bot functionality
- **Payment Provider**: For payment processing (configured via PAYMENT_TOKEN)
- **Game Website**: External game integration at configured URL

### Environment Variables
- `BOT_TOKEN`: Telegram bot token
- `ADMIN_IDS`: Comma-separated admin user IDs
- `PAYMENT_TOKEN`: Payment provider token

## Deployment Strategy

### Development Setup
- SQLite database for simple local development
- Memory-based FSM storage for user states
- File-based configuration with environment variable overrides

### Production Considerations
- Database path configurable via `DATABASE_PATH`
- Logging configured for production monitoring
- Admin notifications for new orders
- Error handling and graceful shutdowns

### Scalability Notes
- Current architecture uses SQLite (suitable for small-medium scale)
- Memory storage for FSM (not persistent across restarts)
- Single bot instance design
- Can be enhanced with Redis for distributed deployment

The application uses a simple but effective architecture suitable for a small-to-medium scale merchandise bot, with clear separation between handlers, database operations, and user interface components.

## Recent Changes

### 23.07.2025 - Critical Issues Fixed
✓ **Color Selection Logic** - Fixed broken callback routing that prevented proceeding to payment
  - Added proper `cart_color_` and `buy_color_` handlers in main.py
  - Fixed product key parsing in callback data
  - Implemented complete color selection workflow for both cart and direct purchase

✓ **Game Button Direct Linking** - Fixed "Play Kinoshlep" button to directly open game
  - Game button now uses URL button type to open https://center-kino.github.io/game_kinoshlep/
  - Removed intermediate steps and extra navigation
  - Works from both start menu and game menu

✓ **Shopping Cart Stability** - Enhanced cart functionality with proper state management
  - Added cart checkout workflow with address collection and confirmation
  - Fixed cart-to-order conversion for multiple items
  - Implemented proper cart clearing after successful order

✓ **Bot Architecture Migration** - Migrated from aiogram 2.x to 3.x
  - Updated all handlers to use async/await patterns
  - Fixed import statements and callback query handlers
  - Implemented proper FSM storage with MemoryStorage
  - Updated dispatcher initialization for aiogram 3.x

✓ **Database Integration** - Complete async database operations
  - Added all CRUD operations for users, products, orders, cart
  - Implemented proper admin functionality with order management
  - Added tracking link delivery system

### Technical Implementation
- Bot Framework: aiogram 3.x with async patterns
- Database: SQLite with async wrapper
- State Management: MemoryStorage for user sessions
- Admin Features: Order management, statistics, tracking links
- Complete end-to-end purchase workflow from selection to delivery