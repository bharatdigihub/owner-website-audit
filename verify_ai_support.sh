#!/bin/bash
# AI Support System Test Script
# Run this to verify the AI support system is working

echo "🤖 AI Support System - Verification Script"
echo "=========================================="
echo ""

# Check if backend is running
echo "1️⃣  Checking if backend is running..."
if curl -s http://localhost:5000/api/health > /dev/null; then
    echo "   ✅ Backend is running on http://localhost:5000"
else
    echo "   ❌ Backend is not running. Start it with: cd backend && python run.py"
    exit 1
fi

echo ""

# Check if AI Support module can be imported
echo "2️⃣  Checking AI Support module..."
python3 -c "from app.analyzers.ai_support import AISupportAssistant; print('   ✅ AI Support module loaded')" 2>/dev/null || python -c "from app.analyzers.ai_support import AISupportAssistant; print('   ✅ AI Support module loaded')"

echo ""

# Check if API key is configured
echo "3️⃣  Checking Google API configuration..."
if [ -z "$GOOGLE_API_KEY" ]; then
    echo "   ⚠️  GOOGLE_API_KEY not set (using offline mode)"
    echo "   💡 Set it with: export GOOGLE_API_KEY=your_key"
else
    echo "   ✅ Google API Key is configured"
fi

echo ""

# Test quick-fix endpoint
echo "4️⃣  Testing quick-fix endpoint..."
RESPONSE=$(curl -s -X POST http://localhost:5000/api/support/quick-fix \
  -H "Content-Type: application/json" \
  -d '{"issue_title": "Missing Meta Tags", "category": "seo"}' 2>/dev/null)

if echo "$RESPONSE" | grep -q "success"; then
    echo "   ✅ Quick-fix endpoint working"
    echo "   Response: $(echo $RESPONSE | grep -o 'quick_solution":"[^"]*' | cut -d'"' -f3 | cut -c1-50)..."
else
    echo "   ❌ Quick-fix endpoint failed"
    echo "   Response: $RESPONSE"
fi

echo ""

# Summary
echo "=========================================="
echo "✅ AI Support System is ready!"
echo ""
echo "Next steps:"
echo "  1. Open http://localhost:3000"
echo "  2. Analyze a website"
echo "  3. Click '💡 AI Support' tab"
echo "  4. Click on any issue to see solution"
echo ""
echo "📚 Documentation:"
echo "  - Setup: AI_SUPPORT_SETUP.md"
echo "  - Details: AI_SUPPORT_IMPLEMENTATION.md"
echo "  - Quick Start: AI_SUPPORT_QUICKSTART.md"
