# 🚀 Deployment Guide - Render

This guide walks you through deploying the Smart Event Planner to Render.

## 📋 Prerequisites

1. **Render Account**: Sign up at [render.com](https://render.com)
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **OpenWeatherMap API Key**: Get one from [openweathermap.org](https://openweathermap.org/api)

## 🚀 Deployment Steps

### 1. Prepare Your Repository

Ensure these files are in your repository:
- `render.yaml` (blueprint configuration)
- `requirements.txt` (Python dependencies)
- `.env.production` (environment variables template)

### 2. Deploy to Render

#### Option A: Using Render Blueprint (Recommended)

1. **Fork/Clone** this repository to your GitHub account

2. **Connect to Render**:
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Select the repository containing this project

3. **Configure Environment Variables**:
   - Render will automatically create the services from `render.yaml`
   - Set the `OPENWEATHER_API_KEY` in the web service environment variables
   - Update `ALLOW_ORIGINS` with your actual domain

#### Option B: Manual Setup

1. **Create PostgreSQL Database**:
   - Go to Render Dashboard
   - Click "New" → "PostgreSQL"
   - Name: `smart-event-planner-db`
   - Plan: Free (for development)

2. **Create Web Service**:
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Configuration:
     - **Name**: `smart-event-planner-api`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`

3. **Set Environment Variables**:
   ```
   DATABASE_URL=<auto-filled-by-render>
   SECRET_KEY=<generate-strong-secret>
   OPENWEATHER_API_KEY=<your-api-key>
   DEBUG=False
   ALLOW_ORIGINS=["https://your-app-name.onrender.com"]
   ```

### 3. Database Migration

After deployment, run database migrations:

1. **Access Render Shell**:
   - Go to your web service dashboard
   - Click "Shell" tab
   - Run: `alembic upgrade head`

2. **Verify Database**:
   - Check if tables are created properly
   - Test API endpoints

### 4. Configure Custom Domain (Optional)

1. **Add Custom Domain**:
   - In your web service settings
   - Add your domain name
   - Update `ALLOW_ORIGINS` environment variable

2. **SSL Certificate**:
   - Render automatically provides SSL certificates
   - No additional configuration needed

## 🔧 Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Auto-set by Render |
| `SECRET_KEY` | JWT secret key | `your-secret-key-here` |
| `OPENWEATHER_API_KEY` | Weather API key | `be285f8d3bf43db17bddb0009250b485` |
| `DEBUG` | Debug mode | `False` |
| `ALLOW_ORIGINS` | CORS origins | `["https://yourapp.onrender.com"]` |

## 🌐 Access Your Application

After successful deployment:

- **API Documentation**: `https://your-app-name.onrender.com/docs`
- **Frontend Interface**: `https://your-app-name.onrender.com/static/index.html`
- **Health Check**: `https://your-app-name.onrender.com/health`

## 🐛 Troubleshooting

### Common Issues

1. **Build Failures**:
   ```bash
   # Check requirements.txt for correct versions
   # Ensure all dependencies are listed
   ```

2. **Database Connection Issues**:
   ```bash
   # Verify DATABASE_URL is set correctly
   # Check if database service is running
   ```

3. **API Key Issues**:
   ```bash
   # Ensure OPENWEATHER_API_KEY is set
   # Verify API key is valid and active
   ```

### Debug Commands

```bash
# Check logs
render logs --service smart-event-planner-api

# Run migrations
alembic upgrade head

# Test database connection
python -c "from src.core.database import engine; print(engine.execute('SELECT 1').scalar())"
```

## 📊 Monitoring

### Health Checks
- Render automatically monitors your service health
- Custom health endpoint: `/health`

### Logs
- Access logs through Render dashboard
- Monitor API usage and errors

### Performance
- Monitor response times
- Check database query performance
- Monitor OpenWeatherMap API usage

## 🔄 Updates and Maintenance

### Deploying Updates
1. Push changes to your GitHub repository
2. Render automatically redeploys from the main branch
3. Monitor deployment logs for any issues

### Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

### Backup Strategy
- Render automatically backs up PostgreSQL databases
- Consider implementing application-level backups for critical data

## 📝 Production Checklist

- [ ] Environment variables properly configured
- [ ] Database migrations applied
- [ ] API endpoints returning expected responses
- [ ] Frontend interface accessible
- [ ] Weather API integration working
- [ ] CORS configured for your domain
- [ ] SSL certificate active
- [ ] Health checks passing
- [ ] Monitoring and logging configured

## 🆘 Support

If you encounter issues:

1. **Check Render Documentation**: [render.com/docs](https://render.com/docs)
2. **Review Application Logs**: Available in Render dashboard
3. **Test Locally**: Ensure application works in local environment
4. **Check API Status**: Verify OpenWeatherMap API is accessible

---

**🎉 Congratulations!** Your Smart Event Planner is now live on Render!

Access your deployed application and start planning weather-aware events!
