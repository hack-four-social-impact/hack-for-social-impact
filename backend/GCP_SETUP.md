# Google Cloud Platform (GCP) Setup Guide

This guide walks you through setting up a new Google Cloud Platform account and project for deploying the backend API to Cloud Run.

## Table of Contents

1. [Create Google Cloud Account](#1-create-google-cloud-account)
2. [Create a New GCP Project](#2-create-a-new-gcp-project)
3. [Enable Billing](#3-enable-billing)
4. [Enable Required APIs](#4-enable-required-apis)
5. [Install gcloud CLI](#5-install-gcloud-cli)
6. [Authenticate gcloud CLI](#6-authenticate-gcloud-cli)
7. [Set Default Project and Region](#7-set-default-project-and-region)
8. [Verify Setup](#8-verify-setup)

---

## 1. Create Google Cloud Account

### New Users (Free Tier)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **Get started for free** or **Try for free**
3. Sign in with your Google account (or create a new one)
4. Fill out the registration form:
   - Country
   - Terms of Service agreement
5. Complete identity verification
6. Add payment method (credit/debit card)
   - **Note**: You won't be charged unless you manually upgrade to a paid account
   - New users get **$300 in free credits** valid for 90 days
   - Cloud Run has a **generous free tier** even after credits expire

### Existing Google Cloud Users

1. Sign in to [Google Cloud Console](https://console.cloud.google.com/)
2. Skip to [Create a New GCP Project](#2-create-a-new-gcp-project)

---

## 2. Create a New GCP Project

### Via Google Cloud Console (Web UI)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click the **project dropdown** at the top of the page (next to "Google Cloud")
3. Click **NEW PROJECT** in the top right of the dialog
4. Enter project details:
   - **Project name**: `hack-for-social-impact` (or your preferred name)
   - **Organization**: Leave as "No organization" (unless you have one)
   - **Location**: Leave as default
5. Click **CREATE**
6. Wait for the project to be created (may take a few seconds)
7. **Select the new project** from the project dropdown

### Via gcloud CLI (After Installation)

```bash
# Create project
gcloud projects create hack-for-social-impact --name="Hack for Social Impact"

# List all projects to verify
gcloud projects list
```

**Save your Project ID**: You'll need this later. It's usually the project name in lowercase with numbers appended.

---

## 3. Enable Billing

Cloud Run requires a billing account to be linked to your project (even if you're using free credits).

### Via Google Cloud Console

1. Go to [Billing](https://console.cloud.google.com/billing)
2. If you have no billing account:
   - Click **ADD BILLING ACCOUNT**
   - Follow the setup wizard
   - Add payment method
3. If you already have a billing account:
   - Click **LINK A BILLING ACCOUNT**
   - Select your billing account
   - Click **SET ACCOUNT**

### Via gcloud CLI

```bash
# List billing accounts
gcloud billing accounts list

# Link billing account to project (replace BILLING_ACCOUNT_ID and PROJECT_ID)
gcloud billing projects link hack-for-social-impact \
  --billing-account=BILLING_ACCOUNT_ID
```

---

## 4. Enable Required APIs

You need to enable the following APIs for Cloud Run deployment:

- **Cloud Run API**: Deploy and run containers
- **Cloud Build API**: Build Docker images automatically
- **Secret Manager API**: Store API keys securely
- **Artifact Registry API**: Store Docker images

### Via Google Cloud Console

1. Go to [APIs & Services > Library](https://console.cloud.google.com/apis/library)
2. Search for each API and click **ENABLE**:
   - **Cloud Run API**
   - **Cloud Build API**
   - **Secret Manager API**
   - **Artifact Registry API**

### Via gcloud CLI (Recommended)

```bash
# Enable all required APIs at once
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  secretmanager.googleapis.com \
  artifactregistry.googleapis.com

# Verify APIs are enabled
gcloud services list --enabled
```

**Note**: Enabling APIs may take 1-2 minutes.

---

## 5. Install gcloud CLI

The gcloud CLI is required for deploying to Cloud Run from your local machine.

### macOS

#### Option 1: Using Homebrew (Recommended)

```bash
brew install google-cloud-sdk
```

#### Option 2: Using Installation Script

```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL  # Restart shell
```

### Linux (Ubuntu/Debian)

```bash
# Add Google Cloud SDK repository
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

# Import Google Cloud public key
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -

# Update and install
sudo apt-get update
sudo apt-get install google-cloud-cli
```

### Linux (WSL2 - Windows Subsystem for Linux)

**IMPORTANT**: Install gcloud in your home directory (NOT in your project repository).

```bash
# Navigate to home directory (outside your repo)
cd ~

# Download and extract
curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-x86_64.tar.gz
tar -xf google-cloud-cli-linux-x86_64.tar.gz

# Install (this will add gcloud to your PATH)
./google-cloud-sdk/install.sh

# Clean up the tarball (optional)
rm google-cloud-cli-linux-x86_64.tar.gz

# Restart shell to apply PATH changes
exec -l $SHELL
```

**If you accidentally installed in your repo**: Move it to your home directory and re-run the install script:

```bash
# Move the folder to home directory
mv /path/to/repo/google-cloud-sdk ~/

# Navigate to the new location
cd ~/google-cloud-sdk

# Re-run the install script (it will update your PATH)
./install.sh

# Restart your shell
exec -l $SHELL
```

### Windows

1. Download the [Google Cloud SDK installer](https://cloud.google.com/sdk/docs/install#windows)
2. Run the installer
3. Follow the installation wizard
4. Restart your terminal/command prompt

### Verify Installation

```bash
gcloud --version
```

You should see output like:

```
Google Cloud SDK 456.0.0
bq 2.0.101
core 2024.01.01
gcloud-crc32c 1.0.0
gsutil 5.27
```

---

## 6. Authenticate gcloud CLI

Authenticate your gcloud CLI with your Google Cloud account:

```bash
gcloud auth login
```

This will:
1. Open a browser window
2. Ask you to sign in with your Google account
3. Request permissions for gcloud CLI
4. Display a success message in your terminal

### For Application Default Credentials (ADC)

If you plan to test Cloud APIs locally, also run:

```bash
gcloud auth application-default login
```

---

## 7. Set Default Project and Region

Set your default project and region to avoid specifying them in every command:

```bash
# Set default project (replace with your project ID)
gcloud config set project hack-for-social-impact

# Set default region (us-central1 is recommended for Cloud Run)
gcloud config set run/region us-central1

# Verify configuration
gcloud config list
```

**Recommended Regions for Cloud Run**:
- `us-central1` (Iowa) - General purpose, lowest latency for US
- `us-east1` (South Carolina) - Alternative US region
- `europe-west1` (Belgium) - For European users
- `asia-east1` (Taiwan) - For Asian users

See all available regions:

```bash
gcloud run regions list
```

---

## 8. Verify Setup

Run these commands to verify your setup is complete:

```bash
# 1. Verify you're authenticated
gcloud auth list

# 2. Verify your project is set
gcloud config get-value project

# 3. List all projects (should see your new project)
gcloud projects list

# 4. Verify billing is enabled
gcloud billing projects describe $(gcloud config get-value project)

# 5. Verify required APIs are enabled
gcloud services list --enabled | grep -E "(run|cloudbuild|secretmanager|artifactregistry)"

# 6. Test Cloud Run access (should return empty list or existing services)
gcloud run services list
```

### Expected Output

If everything is set up correctly, you should see:

- ✅ Your email listed in `gcloud auth list` with an asterisk (*)
- ✅ Your project ID from `gcloud config get-value project`
- ✅ Your project in `gcloud projects list`
- ✅ Billing account linked in billing describe output
- ✅ All 4 APIs listed (run, cloudbuild, secretmanager, artifactregistry)
- ✅ No errors from `gcloud run services list` (list may be empty)

---

## Troubleshooting

### "Permission denied" errors

Make sure you've authenticated:

```bash
gcloud auth login
gcloud auth application-default login
```

### "Billing not enabled" errors

Link a billing account to your project:

```bash
gcloud billing projects link PROJECT_ID --billing-account=BILLING_ACCOUNT_ID
```

### "API not enabled" errors

Enable the required API:

```bash
gcloud services enable SERVICE_NAME.googleapis.com
```

### Can't find project

Make sure the project is selected:

```bash
gcloud config set project PROJECT_ID
```

---

## Next Steps

Once your GCP setup is complete, you can proceed to:

1. **Create Dockerfile** (Phase 3)
2. **Set up Secret Manager** for GEMINI_API_KEY (Phase 6)
3. **Deploy to Cloud Run** (Phase 7)

See `DEPLOYMENT.md` for full deployment instructions.

---

## Cost Estimation

### Free Tier (Always Free)

Cloud Run free tier includes:
- **2 million requests per month**
- **360,000 GB-seconds of memory**
- **180,000 vCPU-seconds of compute time**
- **1 GB network egress per month** (North America)

### Estimated Costs (If Exceeding Free Tier)

For a hackathon project with moderate usage:
- **$0-5/month** if staying within free tier
- **$5-15/month** if slightly exceeding free tier

Costs are based on:
- Request count
- Memory allocated
- CPU time
- Network egress

**Recommendation**: Set up [budget alerts](https://console.cloud.google.com/billing/budgets) to monitor spending.

---

## Security Best Practices

1. **Never commit service account keys** to git
2. **Use Secret Manager** for API keys (not environment variables in cloudbuild.yaml)
3. **Enable Cloud Armor** if you need DDoS protection (optional, costs extra)
4. **Use IAM roles** to limit permissions
5. **Enable audit logs** to track access

---

## Useful Resources

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud Build Documentation](https://cloud.google.com/build/docs)
- [Secret Manager Documentation](https://cloud.google.com/secret-manager/docs)
- [gcloud CLI Reference](https://cloud.google.com/sdk/gcloud/reference)
- [Cloud Run Pricing](https://cloud.google.com/run/pricing)
