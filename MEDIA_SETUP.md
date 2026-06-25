# Media Storage Setup Guide

## The Problem
Render.com has an **ephemeral filesystem** - any files uploaded to the server are deleted when the app restarts or redeploys. This is why your images disappear.

## Solutions

### ✅ OPTION 1: Cloudinary (Recommended - Completely Free)

**Pros:**
- 100% free (25GB storage included)
- Automatic image optimization
- CDN delivery (fast loading)
- No credit card needed

**Steps:**

1. **Sign up for free:**
   - Go to https://cloudinary.com/users/register/free
   - Complete email verification

2. **Get your credentials:**
   - After login, go to https://cloudinary.com/console
   - Copy these 3 values:
     - `CLOUDINARY_CLOUD_NAME` (e.g., "dxxxxxx")
     - `CLOUDINARY_API_KEY` (e.g., "123456789")
     - `CLOUDINARY_API_SECRET` (e.g., "abcd1234...")

3. **Add to Render Dashboard:**
   - Go to your Render service
   - Click **Environment**
   - Add these variables:
     ```
     CLOUDINARY_CLOUD_NAME = your_cloud_name
     CLOUDINARY_API_KEY = your_api_key
     CLOUDINARY_API_SECRET = your_api_secret
     ```

4. **Enable in Django Settings:**
   - Uncomment the Cloudinary code in `physiotherapy_site/settings.py`
   - Install dependencies: `pip install cloudinary django-cloudinary-storage`
   - Push to GitHub and Render will auto-deploy

### ⚠️ OPTION 2: AWS S3 (Paid - ~$1/month for small usage)

- Requires AWS account
- More complex setup
- Pay per GB stored

### ❌ NOT RECOMMENDED: Local Storage
- Files are deleted on Render restart
- Only works for development

## Quick Test (Local Development)
```bash
python manage.py runserver
# Upload a file in admin panel
# Should work without any external service
```

## After Setup
1. Restart Render deployment
2. Go to admin panel
3. Upload an image
4. Image should now load permanently!

Questions? Check Cloudinary's Django integration docs:
https://cloudinary.com/documentation/django_integration
