# Cloud Run Service URL

## Production Service

**Service Name**: `backend-api`
**Region**: `us-central1`
**Service URL**: https://backend-api-375767705771.us-central1.run.app

## Deployment Status

✅ **Successfully Deployed** - 2025-11-09

### Verified Endpoints

- **Root**: https://backend-api-375767705771.us-central1.run.app
  - Response: `{"message":"PDF Processing API with Gemini Integration"}`

- **Health Check**: https://backend-api-375767705771.us-central1.run.app/health
  - Response: `{"status":"healthy","gemini_configured":true}`

- **API Documentation**: https://backend-api-375767705771.us-central1.run.app/docs
  - Interactive Swagger UI

## Configuration

- **Memory**: 512Mi
- **CPU**: 1
- **Min Instances**: 0 (scales to zero)
- **Max Instances**: 10
- **Timeout**: 60s
- **Authentication**: Public (unauthenticated access allowed)

## Environment Variables

- `GEMINI_API_KEY`: Configured via Secret Manager
- `ALLOWED_ORIGINS`: Set to frontend domain(s)
- `DEBUG`: False
- `PORT`: 8080 (auto-set by Cloud Run)

## Usage

### For Frontend Integration

Update your frontend's `.env` file:

```bash
VITE_API_BASE_URL=https://backend-api-375767705771.us-central1.run.app
```

### Example API Calls

```bash
# Health check
curl https://backend-api-375767705771.us-central1.run.app/health

# Process PDF
curl -X POST https://backend-api-375767705771.us-central1.run.app/api/pdf/process \
  -F "file=@document.pdf" \
  -F "custom_prompt=Summarize this document"
```

## Management Commands

```bash
# View service details
gcloud run services describe backend-api --region us-central1

# View logs
gcloud run services logs tail backend-api --region us-central1

# Update service
gcloud run services update backend-api --region us-central1

# Delete service
gcloud run services delete backend-api --region us-central1
```

## Next Steps

1. ✅ Backend deployed to Cloud Run
2. ⏳ Update frontend `VITE_API_BASE_URL` to this URL
3. ⏳ Deploy frontend to Vercel
4. ⏳ Update `ALLOWED_ORIGINS` in Cloud Run to Vercel URL
5. ⏳ Test end-to-end integration

---

**Last Updated**: 2025-11-09
