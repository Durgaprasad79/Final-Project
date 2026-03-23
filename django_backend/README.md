# Smart Civic Complaint Management System

A comprehensive Django-based web application for citizens to report civic issues in Vijayawada, Andhra Pradesh, India. Features photo capture with automatic location detection, AI-powered complaint validation, and real-time ticket tracking.

## 🌟 Features

### User Portal

- **📸 Photo Capture with Location**
  - Real-time camera access (supports mobile & desktop)
  - Mandatory GPS location capture
  - Automatic reverse geocoding (coordinates → address)
  - 5MB image size limit with validation
  - Session-based storage for draft submissions

- **🎯 Ticket Tracking**
  - Search tickets by exact number (format: `CMP-YYYYMMDD-NNN`)
  - Real-time status updates (Submitted → Assigned → In Progress → Resolved)
  - Status-specific information display:
    - **Assigned**: Contractor name & phone
    - **In Progress**: Ward admin name & phone
    - **Resolved**: Rating option (1-5 stars)
  - Photo thumbnail preview
  - Mobile-responsive design

- **⭐ Work Rating System**
  - Rate resolved tickets (1-5 stars)
  - One-time rating (prevents duplicate ratings)
  - Automatic contractor average rating calculation

### Admin Portal

- **Ward Management**: Configure ward boundaries and administrators
- **Contractor Management**: Track contractor performance and ratings
- **Ticket Assignment**: Assign contractors and wards to tickets
- **Status Management**: Update ticket statuses through lifecycle

### AI Integration (Mock Ready)

- Base64 image submission to FastAPI
- Location data transmission
- Multi-issue detection (creates separate tickets per issue)
- Validation result processing (is_valid flag)
- Automatic complaint cleanup for invalid submissions

### Automated Maintenance

- **Daily Cleanup Cron Job** (11:55 PM IST)
  - Deletes unsubmitted photos (is_submit=False)
  - Frees up storage space
  - Timezone: Asia/Kolkata
  - Dry-run mode available

## 🛠️ Technology Stack

- **Backend**: Django 5.0.1
- **REST API**: Django REST Framework 3.14.0
- **Database**: SQLite3 (production-ready PostgreSQL migration possible)
- **Image Processing**: Pillow 10.2.0
- **Geocoding**: geopy 2.4.1 (Nominatim/OpenStreetMap)
- **Frontend**: Bootstrap 5.3.2 + Vanilla JavaScript
- **Icons**: Bootstrap Icons 1.11.3

## 📁 Project Structure

```
django_backend/
├── civic_complaint_system/      # Project settings
│   ├── settings.py              # Django configuration
│   ├── urls.py                  # Main URL routing
│   └── wsgi.py
├── user_portal/                 # Citizen-facing app
│   ├── models.py                # CivicComplaint, Ticket models
│   ├── views.py                 # API endpoints + template views
│   ├── serializers.py           # REST API serializers
│   ├── urls.py                  # User portal routing
│   ├── admin.py                 # Django admin configuration
│   ├── utils/
│   │   ├── geocoding.py         # Reverse geocoding service
│   │   ├── ticket_generator.py  # Daily-reset ticket numbering
│   │   └── image_validator.py   # Base64 image validation
│   ├── templates/user_portal/
│   │   ├── base.html            # Base template
│   │   ├── capture.html         # Photo capture page
│   │   └── track.html           # Ticket tracking page
│   └── management/commands/
│       └── cleanup_unsubmitted_complaints.py  # Cron job
├── admin_portal/                # Administrative app
│   ├── models.py                # Ward, Contractor models
│   └── admin.py                 # Django admin configuration
├── manage.py
├── requirements.txt
└── db.sqlite3
```

## 🚀 Installation & Setup

### Prerequisites

- Python 3.10+ (tested on Python 3.10)
- pip (Python package manager)
- Git

### 1. Clone Repository

```bash
cd autonomous_hacks_finale/django_backend
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Migrations

```bash
python3 manage.py migrate
```

### 4. Create Superuser (for Django Admin)

```bash
python3 manage.py createsuperuser
```

### 5. Run Development Server

```bash
python3 manage.py runserver 0.0.0.0:8000
```

Access the application:

- **Photo Capture**: <http://localhost:8000/capture/>
- **Ticket Tracking**: <http://localhost:8000/track/>
- **Django Admin**: <http://localhost:8000/admin/>

## 📡 API Endpoints

### Photo Capture

```http
POST /api/user/capture-photo/
Content-Type: application/json

{
  "image_base64": "data:image/jpeg;base64,...",
  "latitude": 23.0225,
  "longitude": 72.5714
}

Response:
{
  "success": true,
  "session_id": "uuid-string",
  "complaint_id": 123,
  "location": {
    "street": "132 Feet Ring Road",
    "area": "Satellite",
    "postal_code": "380015"
  },
  "message": "Photo captured successfully..."
}
```

### Submit Complaint

```http
POST /api/user/submit-complaint/
Content-Type: application/json

{
  "session_id": "uuid-string"
}

Response (Valid):
{
  "success": true,
  "tickets": ["CMP-20260110-001", "CMP-20260110-002"],
  "message": "2 ticket(s) created successfully",
  "details": [
    {
      "severity": "High",
      "category": "Road Damage",
      "department": "PWD"
    }
  ]
}

Response (Invalid):
{
  "success": false,
  "message": "Photo validation failed..."
}
```

### Track Ticket

```http
GET /api/user/track-ticket/?ticket_number=CMP-20260110-001

Response:
{
  "success": true,
  "ticket": {
    "ticket_number": "CMP-20260110-001",
    "status": "ASSIGNED",
    "severity": "High",
    "category": "Road Damage",
    "department": "PWD",
    "contractor_info": {
      "contractor_name": "ABC Contractors",
      "contractor_phone": "9876543210"
    },
    "ward_info": null,
    "user_rating": null,
    "can_rate": false,
    "image_url": "http://localhost:8000/media/complaints/...",
    "created_at": "2026-01-10T10:30:00Z",
    "updated_at": "2026-01-10T11:00:00Z"
  }
}
```

### Rate Ticket

```http
POST /api/user/rate-ticket/
Content-Type: application/json

{
  "ticket_number": "CMP-20260110-001",
  "rating": 4
}

Response:
{
  "success": true,
  "message": "Rating submitted successfully...",
  "contractor_rating": 4.25
}
```

## 🗄️ Database Schema

### CivicComplaint Model

```python
session_id          UUID (unique identifier)
image               ImageField (max 5MB)
street              CharField (255)
area                CharField (255) - Required
postal_code         CharField (10)
latitude            DecimalField (10, 7)
longitude           DecimalField (10, 7)
is_submit           BooleanField (default False)
is_valid            BooleanField (nullable)
created_at          DateTimeField
updated_at          DateTimeField
```

### Ticket Model

```python
ticket_number       CharField (20, unique) - CMP-YYYYMMDD-NNN
civic_complaint     ForeignKey (CivicComplaint)
severity            CharField (50) - AI-provided
category            CharField (100) - AI-provided
department          CharField (100) - AI-provided
status              CharField (20) - SUBMITTED/ASSIGNED/IN_PROGRESS/RESOLVED
contractor          ForeignKey (Contractor, nullable)
ward                ForeignKey (Ward, nullable)
user_rating         IntegerField (1-5, nullable)
created_at          DateTimeField
updated_at          DateTimeField
```

### Contractor Model (Admin Portal)

```python
contractor_name     CharField (150)
contractor_phone    CharField (15) - Indian format validation
contractor_email    EmailField
assigned_area       CharField (200)
department          CharField (100)
ratings             DecimalField (3, 2) - Average rating
created_at          DateTimeField
updated_at          DateTimeField
```

### Ward Model (Admin Portal)

```python
ward_no             CharField (10, unique)
ward_name           CharField (100)
ward_admin_name     CharField (100)
ward_admin_no       CharField (15) - Indian format validation
ward_address        TextField
created_at          DateTimeField
updated_at          DateTimeField
```

## ⚙️ Configuration

### settings.py Key Configurations

```python
# Timezone (for cron job)
TIME_ZONE = 'Asia/Kolkata'
USE_TZ = True

# Media files (complaint photos)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Apps
INSTALLED_APPS = [
    'rest_framework',
    'corsheaders',
    'user_portal',
    'admin_portal',
]

# CORS (for API access)
CORS_ALLOW_ALL_ORIGINS = True  # Development only
```

## 🔄 Ticket Lifecycle

```
1. SUBMITTED (Default)
   ↓
   [Admin assigns contractor in Django Admin]
   ↓
2. ASSIGNED
   Display: Contractor name + phone
   ↓
   [Contractor starts work - future contractor app]
   ↓
3. IN_PROGRESS
   Display: Ward name + admin name + phone
   ↓
   [Contractor marks resolved - future contractor app]
   ↓
4. RESOLVED
   Display: Rating form (1-5 stars)
   User submits rating → Updates contractor average
```

## 🕐 Cron Job Setup

### Test the Command (Dry Run)

```bash
python3 manage.py cleanup_unsubmitted_complaints --dry-run
```

### Manual Execution

```bash
python3 manage.py cleanup_unsubmitted_complaints
```

### Setup Cron (Linux/Mac)

```bash
# Edit crontab
crontab -e

# Add this line (runs daily at 11:55 PM)
55 23 * * * cd /path/to/django_backend && /path/to/python3 manage.py cleanup_unsubmitted_complaints >> /var/log/civic_cleanup.log 2>&1
```

### Verify Cron

```bash
# List all cron jobs
crontab -l

# Check logs
tail -f /var/log/civic_cleanup.log
```

## 🌐 Geocoding Service

Uses **geopy** with **Nominatim** (OpenStreetMap) for free reverse geocoding.

### Coverage

- **Region**: Vijayawada, Andhra Pradesh, India
- **Coordinates**: Lat 22.0-24.0, Long 72.0-73.0
- **Accuracy**: Street-level (when available)

### Address Components Extracted

- Street (road/neighbourhood)
- Area (locality/suburb)
- Postal Code (PIN code)
- City (Vijayawada)
- State (Andhra Pradesh)
- Country (India)

### Rate Limits

- **Nominatim**: 1 request/second
- **Retry Logic**: 3 attempts with exponential backoff
- **Timeout**: 10 seconds per request

**Production Recommendation**: Replace with Google Maps Geocoding API for higher reliability and rate limits.

## 🔐 Security Considerations

### Current Implementation (Development)

- ✅ Image size validation (5MB limit)
- ✅ Coordinate range validation (Vijayawada bounds)
- ✅ CSRF protection enabled
- ✅ SQL injection prevention (Django ORM)
- ✅ Input validation via serializers

### Production TODO

- [ ] Add rate limiting (django-ratelimit)
- [ ] Implement user authentication (optional for anonymous complaints)
- [ ] Add HTTPS enforcement
- [ ] Configure CORS_ALLOWED_ORIGINS (remove ALLOW_ALL)
- [ ] Add image content scanning (NSFW filter)
- [ ] Implement captcha for form submissions
- [ ] Set up proper logging and monitoring

## 📱 Mobile Responsiveness

The application is fully responsive and tested on:

- ✅ Desktop (1920x1080, 1366x768)
- ✅ Tablets (iPad, Android tablets)
- ✅ Mobile (iPhone, Android phones)

### Key Mobile Features

- Camera access with rear camera preference
- Touch-friendly button sizes
- Responsive grid layouts
- Optimized image sizes
- Fast loading times

## 🎨 UI/UX Design

### Design Principles

- **Color Scheme**: Purple gradient (civic/government theme)
- **Framework**: Bootstrap 5 for consistency
- **Icons**: Bootstrap Icons for scalability
- **Typography**: System fonts (Segoe UI, sans-serif)
- **Animations**: Smooth transitions and hover effects

### Accessibility

- Semantic HTML5
- ARIA labels where needed
- Color contrast compliance
- Keyboard navigation support

## 🧪 Testing

### Manual Testing Checklist

- [ ] Photo capture with location permission
- [ ] Photo capture without location (error handling)
- [ ] Image size validation (>5MB rejection)
- [ ] Geocoding success (Vijayawada coordinates)
- [ ] Geocoding failure (out of bounds)
- [ ] Ticket creation (single and multiple)
- [ ] Ticket tracking (exact match search)
- [ ] Rating submission (1-5 stars)
- [ ] Duplicate rating prevention
- [ ] Contractor average rating calculation
- [ ] Status-based info display
- [ ] Mobile responsiveness
- [ ] Cron job execution

### Future: Automated Testing

```bash
# Run Django tests
python3 manage.py test

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## 🔧 Troubleshooting

### Camera Not Working

- **Issue**: "Camera access denied"
- **Solution**: Check browser permissions (Settings → Privacy → Camera)

### Location Not Working

- **Issue**: "Location access required"
- **Solution**: Enable location services in browser and system settings

### Geocoding Fails

- **Issue**: "Failed to fetch address from coordinates"
- **Solutions**:
  1. Check internet connection
  2. Verify coordinates are in Vijayawada (Lat 22-24, Long 72-73)
  3. Check Nominatim service status

### Image Too Large

- **Issue**: "Image size exceeds 5MB"
- **Solution**: Capture photo at lower resolution or compress before upload

### Ticket Not Found

- **Issue**: "Ticket CMP-XXXXXXXX-XXX not found"
- **Solutions**:
  1. Verify ticket number format (CMP-YYYYMMDD-NNN)
  2. Check for typos
  3. Confirm ticket was created successfully

## 📝 Future Enhancements

### Phase 2: Contractor App

- [ ] Contractor login/authentication
- [ ] Accept/reject ticket assignments
- [ ] Update ticket status (In Progress, Resolved)
- [ ] Upload resolution photos
- [ ] Dashboard with assigned tickets

### Phase 3: AI Integration

- [ ] Replace mock AI with actual FastAPI endpoint
- [ ] Implement image classification model
- [ ] Multi-issue detection algorithm
- [ ] Severity assessment automation
- [ ] Department routing logic

### Phase 4: Advanced Features

- [ ] Email/SMS notifications
- [ ] Push notifications (PWA)
- [ ] Multiple photo upload per complaint
- [ ] Complaint history for users
- [ ] Analytics dashboard for admins
- [ ] Heat map visualization
- [ ] Complaint clustering by area

### Phase 5: Scalability

- [ ] Migrate to PostgreSQL
- [ ] Add Redis caching
- [ ] Implement Celery for async tasks
- [ ] CDN for media files
- [ ] Load balancing setup
- [ ] Database replication

## 👥 Contributors

- **Development**: Smart Civic Team
- **Design**: Bootstrap Community
- **Geocoding**: OpenStreetMap/Nominatim

## 📄 License

This project is proprietary software for Smart Civic Complaint Management System.

## 🆘 Support

For issues, questions, or feature requests:

- **Email**: <support@civicsystem.gov.in> (placeholder)
- **GitHub Issues**: [Create an issue](#)

---

**Made with ❤️ for a Better Vijayawada**
