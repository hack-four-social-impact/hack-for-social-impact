# Cloud Run Deployment Plan - 13 Phases

**Status**: In Progress - On feature branch `feature/cloud-run-deployment`
**Last Updated**: 2025-11-09

## Configuration Decisions Made

- **Python Version**: 3.13 (from backend config: `.python-version` and `pyproject.toml`)
- **Deployment Method**: Cloud Build + GitHub automation
- **Min Instances**: 0 (scale to zero for cost optimization)
- **GCS Feature**: TBD (configurable, can enable later)
- **Branch Strategy**: Feature branch → test → merge to main

---

## Phase 1: Create Feature Branch ✅ COMPLETED

1. ✅ Create branch `feature/cloud-run-deployment` from main
2. ✅ **Test**: Verify branch creation with `git branch`

**Status**: COMPLETED - Currently on feature branch

---

## Phase 2: GCP Account & Project Setup (New Setup Guide)

3. Create comprehensive GCP setup guide in `backend/GCP_SETUP.md`:
   - How to create Google Cloud account (free tier $300 credit)
   - How to create new GCP project
   - How to enable billing (required for Cloud Run)
   - How to enable required APIs (Cloud Run, Cloud Build, Secret Manager, Artifact Registry)
   - How to install gcloud CLI
   - How to authenticate gcloud CLI
   - How to set default project and region

4. **Test**: User follows GCP_SETUP.md and confirms:
   - GCP project created
   - Billing enabled
   - gcloud CLI installed and authenticated
   - Can run `gcloud projects list`

---

## Phase 3: Create Deployment Configuration Files

5. Create `backend/Dockerfile`:
   - Python 3.13-slim base image (from backend config)
   - Install uv package manager
   - Copy and install dependencies from pyproject.toml
   - Expose port from $PORT environment variable
   - Start uvicorn with proper Cloud Run configuration

6. **Test**: Build Docker image locally:
   - `cd backend && docker build -t backend-test .`
   - Verify build succeeds

7. Create `backend/.dockerignore`:
   - Exclude .venv, __pycache__, .env files, test files, service-account.json

8. Create `backend/cloudbuild.yaml`:
   - Build configuration for GitHub → Cloud Run automation
   - Use Secret Manager for GEMINI_API_KEY
   - Configure environment variables
   - Deploy to Cloud Run with proper settings

9. Create `backend/.gcloudignore`:
   - Similar to .dockerignore for Cloud Build

10. Create `backend/DEPLOYMENT.md`:
    - Step-by-step deployment instructions
    - Environment variable reference
    - Troubleshooting guide
    - How to view logs in Cloud Logging
    - How to update deployments

---

## Phase 4: Update Backend Configuration

11. Modify `backend/api/core/config.py`:
    - Change ALLOWED_ORIGINS from hardcoded ["*"] to environment variable
    - Add: `ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")`
    - Make DEBUG configurable from environment
    - Document all required environment variables

12. **Test**: Run backend locally with environment variables:
    - Set ALLOWED_ORIGINS env var: `export ALLOWED_ORIGINS="http://localhost:5173"`
    - Start backend: `uv run uvicorn main:app --reload`
    - Verify CORS configuration loads from env:
      * Quick check: `python -c "from api.core.config import config; print(config.ALLOWED_ORIGINS)"`
      * Full check: `curl -i -X OPTIONS http://localhost:8000/health -H "Origin: http://localhost:5173"`
      * Should see `access-control-allow-origin: http://localhost:5173` (not `*`)

13. Update `backend/.gitignore`:
    - Ensure service-account.json excluded
    - Ensure .env* files excluded (except .env.example)

---

## Phase 5: Local Docker Testing

14. **Test full Docker container locally**:
    - Build: `docker build -t backend-local .`
    - Run: `docker run -p 8000:8000 -e GEMINI_API_KEY=$GEMINI_API_KEY backend-local`
    - Test endpoints: `curl http://localhost:8000/health`
    - Upload test PDF via API
    - Verify all endpoints work in container

---

## Phase 6: GCP Secret Manager Setup

15. Create guide for Secret Manager in DEPLOYMENT.md:
    - How to enable Secret Manager API
    - How to create secret for GEMINI_API_KEY
    - How to grant Cloud Run service account access to secret
    - Command examples

16. **Test**: User creates GEMINI_API_KEY secret in GCP:
    - Follow Secret Manager guide
    - Verify secret created: `gcloud secrets list`

---

## Phase 7: Initial Cloud Run Deployment (Manual Test)

17. Create manual deployment guide in DEPLOYMENT.md:
    - How to deploy from local machine using gcloud
    - Command: `gcloud run deploy backend-api --source . --region us-central1`
    - How to set environment variables
    - How to configure secrets
    - How to allow unauthenticated access

18. **Test manual deployment**:
    - User runs manual deploy command
    - Deployment succeeds
    - Get Cloud Run URL
    - Test health endpoint: `curl https://backend-api-xxx.run.app/health`

19. **Test PDF processing**:
    - Upload test PDF to Cloud Run endpoint
    - Verify Gemini API integration works
    - Check Cloud Run logs for errors

---

## Phase 8: Configure CORS for Frontend

20. Update Cloud Run environment variables:
    - Set ALLOWED_ORIGINS to Vercel frontend URL
    - Redeploy with updated CORS

21. **Test CORS**:
    - Make request from Vercel frontend to Cloud Run backend
    - Verify no CORS errors in browser console

---

## Phase 9: Set Up Cloud Build Automation ✅ IN PROGRESS

22. ✅ Create guide in DEPLOYMENT.md for Cloud Build GitHub integration:
    - How to connect GitHub repository to Cloud Build
    - How to create trigger for feature branch
    - How to configure build to use cloudbuild.yaml
    - How to set substitution variables

23. **Test Cloud Build trigger** (TESTING NOW):
    - Commit and push to feature branch
    - Verify Cloud Build triggers
    - Verify automatic deployment succeeds
    - Check Cloud Build logs

---

## Phase 10: Documentation & Commit

24. Create comprehensive environment variable documentation
25. Update backend README.md with Cloud Run deployment info
26. Commit all changes to feature branch
27. **Test**: Review all changed files in git diff

---

## Phase 11: Push and Test Automated Deployment

28. Push feature branch to GitHub
29. **Test**: Verify Cloud Build triggers and deploys automatically
30. Test all endpoints on deployed Cloud Run URL
31. Monitor Cloud Run logs for any errors

---

## Phase 12: Update Frontend

32. Update Vercel environment variable VITE_API_BASE_URL to Cloud Run URL
33. Redeploy Vercel frontend
34. **Test end-to-end**:
    - Visit Vercel frontend
    - Upload PDF from frontend
    - Verify successful processing
    - Check network tab for API calls

---

## Phase 13: Create PR and Merge

35. Create Pull Request: feature/cloud-run-deployment → main
36. Review all changes
37. **Test**: Final review of all files
38. Merge to main
39. **Test**: Verify production deployment via Cloud Build
40. **Final test**: Full end-to-end test on production URLs

---

## Files to Create (7)

- [ ] `backend/GCP_SETUP.md` - Comprehensive GCP setup from scratch
- [ ] `backend/Dockerfile` - Python 3.13, uv package manager, Cloud Run config
- [ ] `backend/.dockerignore` - Exclude build artifacts and secrets
- [ ] `backend/cloudbuild.yaml` - GitHub automation config
- [ ] `backend/.gcloudignore` - Cloud Build exclusions
- [ ] `backend/DEPLOYMENT.md` - Complete deployment guide
- [ ] `backend/.env.example` - If doesn't exist, document all env vars

---

## Files to Modify (3)

- [ ] `backend/api/core/config.py` - Environment-aware CORS configuration
- [ ] `backend/.gitignore` - Ensure secrets excluded (service-account.json, .env*)
- [ ] `backend/README.md` - Add Cloud Run deployment info

---

## Testing Checkpoints (15 total)

1. ✅ Branch creation verified
2. GCP project setup verified
3. Docker build succeeds locally
4. Backend runs locally with env vars
5. Docker container runs and serves API
6. Secret Manager secrets created
7. Manual Cloud Run deployment succeeds
8. Health endpoint works on Cloud Run
9. PDF processing works on Cloud Run
10. CORS works from Vercel frontend
11. Cloud Build trigger fires on push
12. Automated deployment succeeds
13. All endpoints tested on Cloud Run
14. End-to-end frontend → backend works
15. Production deployment verified

---

## Environment Variables Reference

**Required for Cloud Run:**
- `GEMINI_API_KEY` - Google Gemini API key (Secret Manager)
- `PORT` - Auto-provided by Cloud Run (defaults to 8080)
- `ALLOWED_ORIGINS` - Comma-separated list of allowed origins (Vercel URL)
- `DEBUG` - Set to `False` for production

**Optional:**
- `GCS_BUCKET_NAME` - Google Cloud Storage bucket name (if using file upload feature)
- `GCS_SERVICE_ACCOUNT_JSON` - Not needed on Cloud Run (uses service account)

---

## Current Backend Configuration

**From analysis:**
- Python: 3.13 (`.python-version`, `pyproject.toml`)
- Package manager: uv
- Dependencies: FastAPI, Uvicorn, google-generativeai, google-cloud-storage, PyPDF2, python-multipart, python-dotenv, reportlab
- Entry point: `main.py`
- Current port: 8000 (needs to read from $PORT for Cloud Run)
- CORS: Currently `["*"]` - needs to be environment-based
- Max file size: 10MB
- Google services: Gemini AI, Cloud Storage (optional)

---

## Important Notes

- **No GCP access yet**: User needs to set up new GCP account/project
- **Service account file**: `service-account.json` should NOT be used in Cloud Run (use service account identity)
- **CORS must be updated**: From `["*"]` to specific frontend domain(s)
- **Testing between steps**: Each phase has explicit test checkpoints
- **Branch workflow**: All work on feature branch, test thoroughly, then merge to main

---

## Next Steps (Resume Here)

**Current status**: On feature branch `feature/cloud-run-deployment`
**Next task**: Create `backend/GCP_SETUP.md`

**To resume:**
1. Ensure in backend directory: `cd /home/derk/code/h4si/hack-for-social-impact/backend`
2. Verify on feature branch: `git branch` (should show `* feature/cloud-run-deployment`)
3. Start with Phase 2, Step 3: Create GCP_SETUP.md
