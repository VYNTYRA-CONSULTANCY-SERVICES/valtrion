# Valtrion - Car Service Booking Platform

A full-stack web application for managing car services, bookings, and customer interactions.

## Features

- **User Management**: Customer registration, login, and profile management
- **Service Catalog**: Browse and book various car services
- **Booking System**: Schedule service appointments with date/time selection
- **Payment Integration**: Razorpay payment gateway integration
- **Admin Dashboard**: Manage services, bookings, mechanics, and customers
- **Real-time Chat**: WebSocket-based communication between admins and customers
- **Email Notifications**: Automated booking confirmations and updates via Gmail
- **SMS Notifications**: Optional Twilio SMS alerts
- **Service Packages**: Premium packages for regular maintenance
- **Review System**: Customers can leave reviews for services

## Tech Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: SQLAlchemy ORM with SQLite/PostgreSQL support
- **Authentication**: Flask-Login with Bcrypt
- **Email**: Flask-Mail (Gmail SMTP)
- **Real-time**: Flask-SocketIO for WebSocket support
- **Payment**: Razorpay API integration
- **SMS**: Twilio API integration (optional)

### Frontend
- **Templating**: Jinja2 (Flask Templates)
- **Styling**: Bootstrap CSS
- **JavaScript**: jQuery, vanilla JS
- **Real-time**: Socket.IO client

## Project Structure

```
valtrion/
├── app/                      # Main application package
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # SQLAlchemy models (User, Service, Booking, etc.)
│   ├── sockets.py           # WebSocket event handlers
│   ├── gmail_email.py       # Gmail email utilities
│   ├── resend_email.py      # Email resend utilities
│   ├── routes/              # Blueprint modules
│   │   ├── main.py          # Main/home routes
│   │   ├── auth.py          # Authentication routes (login/register)
│   │   ├── booking.py       # Booking management routes
│   │   ├── profile.py       # User profile routes
│   │   └── admin.py         # Admin dashboard routes
│   ├── static/              # Static assets
│   │   ├── logos/           # Logo images
│   │   └── offers/          # Promotional offers
│   └── templates/           # HTML templates
│       ├── base.html        # Base template
│       ├── index.html       # Home page
│       ├── login.html       # Login page
│       ├── register.html    # Registration page
│       ├── dashboard.html   # User dashboard
│       ├── booking.html     # Booking form
│       ├── payment.html     # Payment page
│       └── admin/           # Admin templates
├── config.py                # Configuration management
├── run.py                   # Development server entry point
├── wsgi.py                  # Production WSGI entry point
├── seed.py                  # Database initialization script
├── requirements.txt         # Python dependencies
├── Procfile                 # Heroku/deployment configuration
├── vercel.json              # Vercel deployment configuration
├── runtime.txt              # Python version specification
└── DEPLOYMENT.md            # Deployment guide
```

## Quick Start

### Prerequisites
- Python 3.11+
- pip
- Virtual environment (recommended)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/NivedithaDevang/valtrion.git
   cd valtrion
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize database**
   ```bash
   python seed.py
   ```

6. **Run development server**
   ```bash
   python run.py
   ```

   Access the application at: `http://localhost:5000`

### Default Admin Credentials
- **Email**: `valtrionbookings@gmail.com`
- **Password**: `valtrion@123`

⚠️ **Change these credentials immediately in production!**

## Configuration

### Environment Variables

Key environment variables (see `.env.example` for all):

```
FLASK_ENV=development|production
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///valtrion.db  # or PostgreSQL URL
MAIL_USERNAME=your-gmail@gmail.com
MAIL_PASSWORD=your-16-char-app-password
RAZORPAY_KEY_ID=your-key-id
RAZORPAY_KEY_SECRET=your-key-secret
```

### Gmail Setup
1. Enable 2-Step Verification on your Gmail account
2. Go to [App Passwords](https://myaccount.google.com/apppasswords)
3. Generate an app password for Mail
4. Use this 16-character password in `.env`

### Razorpay Setup
1. Create account at [Razorpay](https://razorpay.com)
2. Get API keys from dashboard
3. Use test keys for development, live keys for production

## Deployment

Comprehensive deployment guides are available in [DEPLOYMENT.md](DEPLOYMENT.md)

### Supported Platforms
- **Vercel** (recommended for serverless)
- **Heroku** (traditional platform-as-a-service)
- **Docker** (for containerized deployment)
- **Self-hosted** (any server with Python support)

## Key Features Implementation

### Authentication
- Secure password hashing with bcrypt
- Session-based authentication with Flask-Login
- Admin role-based access control

### Database Models
- **User**: Customer and admin profiles
- **Service**: Car services with pricing and duration
- **Booking**: Service appointments with status tracking
- **Mechanic**: Mechanic profiles and assignments
- **Review**: Customer feedback and ratings
- **ChatMessage**: Real-time messaging between admin and customers

### Real-time Features
- WebSocket support via Flask-SocketIO
- Live chat between admin and customers
- Real-time booking status updates

### Payment Processing
- Razorpay integration for secure payments
- Order creation and verification
- Payment status tracking

## API Endpoints

### Authentication
- `POST /register` - User registration
- `POST /login` - User login
- `GET /logout` - User logout

### Booking
- `GET /booking` - Booking form page
- `POST /book-service` - Create new booking
- `GET /bookings` - View user bookings
- `GET /booking/<id>` - Booking details

### Services
- `GET /services` - Browse services
- `GET /packages` - View service packages
- `GET /estimator` - Service cost estimator

### Admin
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/bookings` - Manage bookings
- `GET /admin/customers` - Customer list
- `GET /admin/services` - Service management
- `GET /admin/mechanics` - Mechanic management

## Troubleshooting

### Common Issues

**Issue**: "SECRET_KEY environment variable is not set"
- **Solution**: Set `SECRET_KEY` in `.env` file

**Issue**: Email not sending
- **Solution**: Verify Gmail App Password and 2FA is enabled

**Issue**: Payment fails
- **Solution**: Check Razorpay API keys and test mode settings

**Issue**: Database connection error
- **Solution**: Verify `DATABASE_URL` format and database server is running

For more troubleshooting, see [DEPLOYMENT.md](DEPLOYMENT.md#troubleshooting)

## Development Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions and classes

### Database Migrations
For schema changes, use Alembic:
```bash
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

### Testing
```bash
# Run tests
python -m pytest

# With coverage
python -m pytest --cov=app
```

## Security Notes

⚠️ **Important Security Considerations:**

1. **Never commit `.env` file** - Use `.gitignore` to exclude it
2. **Use strong SECRET_KEY** - Generate with: `openssl rand -hex 32`
3. **Enable HTTPS** in production
4. **Validate all user inputs**
5. **Keep dependencies updated**
6. **Use environment-specific configurations**
7. **Enable CSRF protection**
8. **Implement rate limiting** for APIs

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the ISC License - see the LICENSE file for details.

## Support

For support, issues, or questions:
- Open an issue on [GitHub Issues](https://github.com/NivedithaDevang/valtrion/issues)
- Check [Deployment Guide](DEPLOYMENT.md) for common issues
- Review Flask documentation: https://flask.palletsprojects.com

## Additional Resources

- [Flask Official Documentation](https://flask.palletsprojects.com)
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org)
- [Flask-Login Documentation](https://flask-login.readthedocs.io)
- [Razorpay API Docs](https://razorpay.com/docs/api/)
- [Vercel Python Support](https://vercel.com/docs/concepts/functions/serverless-functions/python)

## Changelog

### Version 1.0.0 (Current)
- Initial release
- Core booking system
- Admin dashboard
- Payment integration
- Real-time chat

## Authors

- Developed by the Valtrion Team
- Special thanks to all contributors

---

**Last Updated**: May 2026
**Status**: Production Ready ✅
