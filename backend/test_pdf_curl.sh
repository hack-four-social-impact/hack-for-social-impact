#!/bin/bash
# Test PDF to Markdown API with curl

API_URL="http://localhost:8000"
PDF_FILE="$1"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 PDF to Markdown API Test${NC}"
echo "=================================="

# Check if PDF file is provided
if [ -z "$PDF_FILE" ]; then
    echo -e "${RED}❌ Usage: $0 <path_to_pdf_file>${NC}"
    echo "Example: $0 /path/to/document.pdf"
    exit 1
fi

# Check if file exists
if [ ! -f "$PDF_FILE" ]; then
    echo -e "${RED}❌ PDF file not found: $PDF_FILE${NC}"
    exit 1
fi

echo -e "${YELLOW}📄 Testing with PDF: $PDF_FILE${NC}"

# Test 1: Health Check
echo -e "\n${BLUE}🔍 Testing API health...${NC}"
health_response=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL/health")

if [ "$health_response" = "200" ]; then
    echo -e "${GREEN}✅ API is healthy!${NC}"
    curl -s "$API_URL/health" | jq '.'
else
    echo -e "${RED}❌ API health check failed (HTTP $health_response)${NC}"
    echo "Make sure the FastAPI server is running:"
    echo "cd /path/to/backend && uvicorn main:app --reload"
    exit 1
fi

# Test 2: PDF Processing with Markdown Conversion
echo -e "\n${BLUE}🤖 Processing PDF for markdown conversion...${NC}"

MARKDOWN_PROMPT="Please convert this document content into well-formatted markdown. Include:
- Proper headings with # ## ###
- Bullet points where appropriate  
- Bold and italic text for emphasis
- Code blocks if there are any technical sections
- Tables if the document contains tabular data

Make the markdown clean, readable, and well-structured."

# Make the API call
response=$(curl -s -X POST "$API_URL/pdf/process" \
    -H "accept: application/json" \
    -H "Content-Type: multipart/form-data" \
    -F "file=@$PDF_FILE" \
    -F "prompt=$MARKDOWN_PROMPT" \
    -F "max_tokens=2000")

# Check if the response is valid JSON
if echo "$response" | jq empty 2>/dev/null; then
    success=$(echo "$response" | jq -r '.success // false')
    
    if [ "$success" = "true" ]; then
        echo -e "${GREEN}✅ PDF processed successfully!${NC}"
        
        # Extract information
        filename=$(echo "$response" | jq -r '.filename // "unknown"')
        file_size=$(echo "$response" | jq -r '.file_size // 0')
        text_length=$(echo "$response" | jq -r '.extracted_text_length // 0')
        
        echo -e "   📁 Filename: $filename"
        echo -e "   📊 File size: $file_size bytes"
        echo -e "   📝 Extracted text length: $text_length characters"
        
        # Get the markdown content
        markdown_content=$(echo "$response" | jq -r '.gemini_analysis // "No markdown generated"')
        
        # Save to file
        output_file="${PDF_FILE%.*}_converted.md"
        echo "# Converted from: $(basename "$PDF_FILE")" > "$output_file"
        echo "" >> "$output_file"
        echo "$markdown_content" >> "$output_file"
        
        echo -e "${GREEN}📝 Markdown saved to: $output_file${NC}"
        
        # Show preview
        echo -e "\n${YELLOW}📖 Markdown Preview (first 500 chars):${NC}"
        echo "=================================================="
        echo "$markdown_content" | head -c 500
        if [ ${#markdown_content} -gt 500 ]; then
            echo "..."
        fi
        echo ""
        echo "=================================================="
        
    else
        echo -e "${RED}❌ PDF processing failed${NC}"
        echo "$response" | jq '.'
    fi
else
    echo -e "${RED}❌ Invalid JSON response or API error${NC}"
    echo "Response: $response"
fi