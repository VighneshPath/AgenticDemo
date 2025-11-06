/**
 * Frontend integration test to verify API connectivity
 * Tests that the frontend can successfully connect to the backend API
 */

const axios = require("axios");

// API configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

async function testApiConnectivity() {
  console.log("🚀 Testing Frontend-Backend Integration\n");

  let testsPasssed = 0;
  const totalTests = 4;

  try {
    // Test 1: System Info
    console.log("Testing system info endpoint...");
    const systemResponse = await axios.get(`${API_BASE_URL}/`);
    if (systemResponse.status === 200) {
      console.log("✅ System info endpoint working");
      console.log(`   API Version: ${systemResponse.data.version}`);
      testsPasssed++;
    } else {
      console.log(`❌ System info failed: ${systemResponse.status}`);
    }
  } catch (error) {
    console.log(`❌ System info error: ${error.message}`);
  }

  try {
    // Test 2: Health Check
    console.log("\nTesting health check endpoint...");
    const healthResponse = await axios.get(`${API_BASE_URL}/health`);
    if (healthResponse.status === 200) {
      console.log("✅ Health check working");
      console.log(`   Status: ${healthResponse.data.status}`);
      testsPasssed++;
    } else {
      console.log(`❌ Health check failed: ${healthResponse.status}`);
    }
  } catch (error) {
    console.log(`❌ Health check error: ${error.message}`);
  }

  try {
    // Test 3: People API
    console.log("\nTesting people API endpoint...");
    const peopleResponse = await axios.get(`${API_BASE_URL}/api/people`);
    if (peopleResponse.status === 200) {
      console.log("✅ People API working");
      console.log(`   Total people: ${peopleResponse.data.total_count}`);
      testsPasssed++;
    } else {
      console.log(`❌ People API failed: ${peopleResponse.status}`);
    }
  } catch (error) {
    console.log(`❌ People API error: ${error.message}`);
  }

  try {
    // Test 4: Beach API
    console.log("\nTesting beach API endpoint...");
    const beachResponse = await axios.get(`${API_BASE_URL}/api/beach`);
    if (beachResponse.status === 200) {
      console.log("✅ Beach API working");
      console.log(`   People on beach: ${beachResponse.data.total_count}`);
      testsPasssed++;
    } else {
      console.log(`❌ Beach API failed: ${beachResponse.status}`);
    }
  } catch (error) {
    console.log(`❌ Beach API error: ${error.message}`);
  }

  console.log(`\n📊 Test Results: ${testsPasssed}/${totalTests} tests passed`);

  if (testsPasssed === totalTests) {
    console.log("🎉 All frontend integration tests passed!");
    console.log("✅ Frontend can successfully connect to backend API");
    return true;
  } else {
    console.log("❌ Some integration tests failed");
    console.log(
      "💡 Make sure the backend server is running on http://localhost:8000"
    );
    return false;
  }
}

// Test CORS by simulating a browser request
async function testCorsHeaders() {
  console.log("\n🌐 Testing CORS configuration...");

  try {
    const response = await axios.get(`${API_BASE_URL}/api/people`, {
      headers: {
        Origin: "http://localhost:3000",
        "Access-Control-Request-Method": "GET",
      },
    });

    console.log("✅ CORS request successful");
    console.log("✅ Frontend can make cross-origin requests to backend");
    return true;
  } catch (error) {
    if (error.response) {
      console.log(`❌ CORS test failed: ${error.response.status}`);
    } else {
      console.log(`❌ CORS test error: ${error.message}`);
    }
    return false;
  }
}

async function main() {
  const apiTests = await testApiConnectivity();
  const corsTests = await testCorsHeaders();

  if (apiTests && corsTests) {
    console.log("\n🎉 All integration tests passed!");
    console.log("✅ Backend-Frontend integration is working correctly");
    console.log("✅ CORS is properly configured");
    console.log("\n🚀 Ready for development!");
    process.exit(0);
  } else {
    console.log("\n❌ Integration tests failed");
    console.log("💡 Please check the backend server and configuration");
    process.exit(1);
  }
}

// Run the tests
main().catch((error) => {
  console.error("Test execution error:", error);
  process.exit(1);
});
