#!/bin/bash
# Automated Test Framework - Package Creator (Bash)

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Output directory
OUTPUT_DIR="${1:-.}"

echo -e "${BLUE}========================================================${NC}"
echo -e "${BLUE}  Automated Test Framework - Package Creator${NC}"
echo -e "${BLUE}========================================================${NC}"
echo ""

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Generate timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
PACKAGE_NAME="automated-test-framework_${TIMESTAMP}"
ZIP_FILE="${OUTPUT_DIR}/${PACKAGE_NAME}.zip"
LOG_FILE="${OUTPUT_DIR}/${PACKAGE_NAME}_log.txt"
MD5_FILE="${OUTPUT_DIR}/${PACKAGE_NAME}.zip.md5"

echo -e "${GREEN}[✓]${NC} Package name: $PACKAGE_NAME"
echo -e "${GREEN}[✓]${NC} Output directory: $OUTPUT_DIR"
echo ""

echo -e "${BLUE}Creating ZIP file...${NC}"

# Create ZIP file excluding certain directories
zip -r "$ZIP_FILE" . \
    -x "venv/*" \
    "env/*" \
    ".git/*" \
    "__pycache__/*" \
    ".pytest_cache/*" \
    ".idea/*" \
    ".vscode/*" \
    "allure-results/*" \
    "htmlcov/*" \
    "logs/*" \
    "*.log" \
    ".env" \
    "dist/*" \
    "build/*" \
    "*.egg-info/*" \
    ".DS_Store" \
    "create-package.py" \
    "create-package.sh" \
    "create-package.bat" > /dev/null 2>&1

echo -e "${GREEN}[✓]${NC} ZIP file created: $ZIP_FILE"

# Calculate file size
FILE_SIZE=$(du -h "$ZIP_FILE" | cut -f1)
echo -e "${GREEN}[✓]${NC} File size: $FILE_SIZE"
echo ""

echo -e "${BLUE}Computing checksums...${NC}"

# Calculate MD5
MD5_HASH=$(md5sum "$ZIP_FILE" | awk '{print $1}')
echo "$MD5_HASH  $(basename $ZIP_FILE)" > "$MD5_FILE"
echo -e "${GREEN}[✓]${NC} MD5: $MD5_HASH"

# Calculate SHA256
SHA256_HASH=$(sha256sum "$ZIP_FILE" | awk '{print $1}')
SHA256_FILE="${OUTPUT_DIR}/${PACKAGE_NAME}.zip.sha256"
echo "$SHA256_HASH  $(basename $ZIP_FILE)" > "$SHA256_FILE"
echo -e "${GREEN}[✓]${NC} SHA256: $SHA256_HASH"
echo ""

echo -e "${BLUE}========================================================${NC}"
echo -e "${GREEN}✅ Package created successfully!${NC}"
echo -e "${BLUE}========================================================${NC}"
echo ""
echo -e "${YELLOW}Output files:${NC}"
echo "  • $(basename $ZIP_FILE)"
echo "  • $(basename $MD5_FILE)"
echo "  • $(basename $SHA256_FILE)"
echo ""
echo -e "${YELLOW}Location: $OUTPUT_DIR${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. Verify checksum: md5sum -c $(basename $MD5_FILE)"
echo "  2. Upload the ZIP file"
echo "  3. Share the checksum for verification"
echo ""
