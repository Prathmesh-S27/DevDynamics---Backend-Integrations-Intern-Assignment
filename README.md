# 🌤️ Smart Event Planner - Backend API

## DevDynamics - Backend Integrations Intern Assignment

A comprehensive weather-aware event planning system that integrates with OpenWeatherMap API to provide intelligent event recommendations and weather analysis.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [Installation & Setup](#installation--setup)
- [API Documentation](#api-documentation)
- [Frontend Interface](#frontend-interface)
- [Environment Configuration](#environment-configuration)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Weather Integration](#weather-integration)
- [Smart Features](#smart-features)
- [Deployment](#deployment)
- [Contributing](#contributing)

---

## 🎯 Overview

The Smart Event Planner is a weather-intelligent event management system that helps users create, manage, and optimize events based on real-time weather data and forecasts. The system provides smart recommendations for alternative dates and nearby locations when weather conditions are unfavorable.

### Key Objectives
- **Weather-Aware Planning**: Integrate weather data into event planning decisions
- **Smart Recommendations**: Provide alternative dates and locations for better weather
- **Real-time Analysis**: Continuous weather monitoring with alerts
- **User-Friendly Interface**: Clean, modern web interface for easy event management

---

## ✨ Features

### 🎯 Core Features (MUST HAVE)
- ✅ **Weather API Integration**: OpenWeatherMap for current weather and 5-day forecasts
- ✅ **Event Management**: Create, read, update, delete events with weather analysis
- ✅ **Weather Suitability Analysis**: Score events based on weather conditions
- ✅ **Smart Recommendations**: Alternative dates with better weather
- ✅ **RESTful API**: Comprehensive API endpoints for all functionality

### 🚀 Enhanced Features (EXTRA CREDIT)
- ✅ **Historical Weather Analysis**: Compare with past weather data
- ✅ **Hourly Weather Breakdown**: Detailed hour-by-hour forecasts
- ✅ **Weather Trends**: Analyze improving/worsening conditions
- ✅ **Nearby Location Comparison**: Weather analysis for nearby cities (50-150km radius)
- ✅ **Smart Notifications**: Weather change alerts and event reminders
- ✅ **Modern Frontend Interface**: Interactive web dashboard

---

## 🛠 Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Python 3.9+**: Core programming language
- **PostgreSQL**: Primary database for data persistence
- **SQLAlchemy**: ORM for database operations
- **Pydantic**: Data validation and serialization
- **Alembic**: Database migrations

### External APIs
- **OpenWeatherMap API**: Weather data and forecasts
- **Geocoding API**: Location coordinate resolution

### Infrastructure
- **Docker**: Containerization for easy deployment
- **Docker Compose**: Multi-container orchestration
- **CORS**: Cross-origin resource sharing support

### Frontend
- **HTML5/CSS3**: Modern responsive design
- **JavaScript ES6+**: Interactive functionality
- **CSS Grid/Flexbox**: Responsive layouts

---

## 🏗 Architecture

The architecture of the Smart Event Planner system is designed to be modular, scalable, and resilient. It follows a microservices-based approach where different functionalities are encapsulated within separate services, communicating over well-defined APIs.

### 1. **Microservices**
   - **Event Service**: Manages all event-related operations (CRUD, retrieval, weather analysis).
   - **User Service**: Handles user authentication, authorization, and management.
   - **Venue Service**: Manages venue-related information and operations.
   - **Weather Service**: Integrates with external weather APIs to fetch and analyze weather data.

### 2. **Database**
   - **PostgreSQL**: Relational database to store persistent data for events, users, and venues.
   - **Redis**: In-memory data structure store, used for caching and real-time analytics.

### 3. **API Gateway**
   - A single entry point for all client requests, routing them to the appropriate microservice.
   - Handles cross-cutting concerns like authentication, logging, and rate limiting.

### 4. **Frontend Application**
   - A separate module (to be developed) that will interact with the backend APIs to provide a seamless user interface for event planning.

### 5. **Deployment**
   - All services are containerized using Docker and orchestrated using Docker Compose for local development.
   - Production deployment will use Kubernetes for orchestration, ensuring scalability and resilience.

---

## 🚀 Installation & Setup

To get started with the Smart Event Planner backend, follow these steps:

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd smart-event-planner-backend
   ```

2. Create a `.env` file based on the `.env.example` file and configure your environment variables.

3. Build and run the application using Docker Compose:

   ```bash
   docker-compose up --build
   ```

### API Documentation

The API documentation is automatically generated by FastAPI and can be accessed at:

```
http://localhost:8000/docs
```

### Running Tests

To run the tests, you can use the following command:

```
docker-compose exec app pytest
```

---

## 🌐 Frontend Interface

The frontend interface for the Smart Event Planner is designed to be intuitive and user-friendly, providing all the necessary functionalities for event planning at your fingertips.

### Key Features
- **Dashboard**: Overview of upcoming events, weather forecasts, and smart recommendations.
- **Event Creation**: Easy-to-use form for creating new events with weather insights.
- **Event Management**: View, edit, and delete events with a focus on weather suitability.
- **Smart Recommendations**: Suggested alternative dates and venues based on weather data.

### Technology Stack
- **React**: JavaScript library for building user interfaces
- **Redux**: State management for JavaScript apps
- **Axios**: Promise-based HTTP client for the browser and Node.js
- **Bootstrap**: CSS framework for responsive design

---

## ⚙️ Environment Configuration

The Smart Event Planner backend uses environment variables for configuration, allowing for easy customization and security.

### Required Variables
- `DATABASE_URL`: Connection string for the PostgreSQL database
- `WEATHER_API_KEY`: API key for accessing the OpenWeatherMap API
- `SECRET_KEY`: Secret key for JWT authentication
- `CORS_ORIGINS`: Comma-separated list of allowed CORS origins

### Example `.env` File
```
DATABASE_URL=postgresql://user:password@localhost/smart_event_planner
WEATHER_API_KEY=your_openweathermap_api_key
SECRET_KEY=your_secret_key
CORS_ORIGINS=http://localhost:3000
```

---

## 🧪 Testing

Testing is a crucial part of the development process, ensuring that all components of the Smart Event Planner work as expected.

### Running Tests
To run the tests for the backend, use the following command:

```bash
docker-compose exec app pytest
```

### Test Coverage
We strive for high test coverage to ensure the reliability and stability of the application. Coverage reports can be generated and viewed in the browser.

---

## 📂 Project Structure

The project is organized into several key directories and files:

```
smart-event-planner-backend/
│
├── app/                    # Main application package
│   ├── api/                # API routes and endpoints
│   ├── core/               # Core functionality and business logic
│   ├── models/             # Database models and schemas
│   ├── services/           # External services integration (e.g., weather API)
│   ├── tests/              # Test cases and testing utilities
│   └── main.py             # Entry point of the application
│
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile              # Dockerfile for building the application image
├── .env.example            # Example environment configuration file
└── README.md               # Project documentation
```

---

## 📡 API Endpoints

The Smart Event Planner provides a comprehensive set of API endpoints for all its functionalities. Below are some of the key endpoints:

### Event Management
- `POST /api/events`: Create a new event
- `GET /api/events`: Retrieve a list of events
- `GET /api/events/{id}`: Retrieve detailed information about a specific event
- `PUT /api/events/{id}`: Update an existing event
- `DELETE /api/events/{id}`: Delete an event

### User Management
- `POST /api/users`: Register a new user
- `GET /api/users`: Retrieve a list of users
- `GET /api/users/{id}`: Retrieve detailed information about a specific user
- `PUT /api/users/{id}`: Update user information
- `DELETE /api/users/{id}`: Delete a user

### Weather Integration
- `GET /api/weather/current`: Get current weather data
- `GET /api/weather/forecast`: Get weather forecast data

---

## 🌦 Weather Integration

The Smart Event Planner integrates with the OpenWeatherMap API to provide real-time weather data and forecasts. This integration is crucial for the weather-aware planning feature.

### Key Features
- **Current Weather Data**: Access to real-time weather information
- **5-Day Weather Forecast**: Detailed weather forecasts for the next five days
- **Weather Alerts**: Notifications for severe weather conditions

### Configuration
To use the weather integration, you need to sign up for an API key at OpenWeatherMap and set it in your `.env` file:

```
WEATHER_API_KEY=your_openweathermap_api_key
```

---

## 🌟 Smart Features

The Smart Event Planner includes several smart features that enhance the event planning experience:

- **Smart Date Suggestions**: Alternative dates for events are suggested based on weather forecasts.
- **Location Intelligence**: Recommendations for nearby venues with better weather conditions.
- **Automated Alerts**: Notifications for users about weather changes that may impact their events.

---

## 🚢 Deployment

The deployment of the Smart Event Planner is designed to be flexible and scalable, using modern containerization and orchestration technologies.

### Local Development
For local development, Docker Compose is used to spin up the necessary services with a single command:

```bash
docker-compose up --build
```

### Production Deployment
In production, Kubernetes will be used for orchestration, providing scalability, resilience, and easy management of the microservices.

---

## 🤝 Contributing

Contributions to the Smart Event Planner are welcome! To contribute, please follow these steps:

1. Fork the repository
2. Create a new branch for your feature or bugfix
3. Make your changes and commit them with descriptive messages
4. Push your branch to your forked repository
5. Create a pull request against the main repository

Please ensure that your code adheres to the existing style and conventions used in the project.