#!/bin/sh

# Define color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Run Python tests and capture output
echo "${YELLOW}Running API tests...${NC}"
echo "API tests report" > /app/test_output.txt 2>&1
python Backend/**/*tests.py > /app/test_output_1.txt 2>&1
if [ $? -eq 0 ]; then
    echo "${GREEN}API tests passed.${NC}\n"
    echo "API tests passed ✅" >> /app/test_output.txt
else
    echo "${RED}API tests failed.${NC}\n"
    cat /app/test_output_1.txt >> /app/test_output.txt
fi

# Run flake8 and append output
echo "${YELLOW}Running API code format check with flake8...${NC}"
echo "\nAPI code format check with flake8" >> /app/test_output.txt 2>&1
flake8 Backend > /app/test_output_1.txt 2>&1
if [ $? -eq 0 ]; then
    echo "${GREEN}flake8 passed.${NC}\n"
    echo "API code format check with flake8 passed ✅" >> /app/test_output.txt
else
    echo "${RED}flake8 failed.${NC}\n"
    cat /app/test_output_1.txt >> /app/test_output.txt
fi

# Run eslint and append output
echo "${YELLOW}Running frontend code format check with eslint...${NC}"
echo "\nFrontend code format check with eslint" >> /app/test_output.txt 2>&1
cd Frontend && npm run lint > /app/test_output_1.txt 2>&1
if [ $? -eq 0 ]; then
    echo "${GREEN}eslint passed.${NC}\n"
    echo "Frontend code format check with eslint passed ✅" >> /app/test_output.txt
else
    echo "${RED}eslint failed.${NC}\n"
    cat /app/test_output_1.txt >> /app/test_output.txt
fi

# Print the output file
echo "\n--------------------- collecting details ---------------------\n\n"
echo "${YELLOW}Detailed output:${NC}"
cat /app/test_output.txt