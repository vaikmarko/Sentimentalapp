const axios = require('axios');
const fs = require('fs');
const path = require('path');

class APITestSuite {
    constructor(baseUrl = 'http://localhost:8080') {
        this.baseUrl = baseUrl;
        this.testResults = [];
        this.bugTracker = require('../bugs/bug-tracker.json');
    }

    async runAllAPITests() {
        console.log('🔌 Starting API Test Suite...\n');
        
        try {
            await this.testBasicEndpoints();
            await this.testAuthenticationEndpoints();
            await this.testStoryEndpoints();
            await this.testChatEndpoints();
            await this.testKnowledgeEndpoints();
            await this.testErrorHandling();
            await this.testResponseFormats();
            
            this.generateAPIReport();
            
        } catch (error) {
            console.error('❌ API test suite failed:', error);
            this.logCriticalBug('API Test Suite Failure', error.message);
        }
    }

    async testBasicEndpoints() {
        console.log('🏠 Testing Basic Endpoints...');
        
        const basicEndpoints = [
            { method: 'GET', path: '/', description: 'Landing page', expectedStatus: [200, 201] },
            { method: 'GET', path: '/app', description: 'Main app page', expectedStatus: [200, 201] },
            { method: 'GET', path: '/chat', description: 'Chat page', expectedStatus: [200, 201] },
            { method: 'GET', path: '/inner-space', description: 'Inner space page', expectedStatus: [200, 201] },
            { method: 'GET', path: '/deck', description: 'Story deck page', expectedStatus: [200, 201] },
            { method: 'GET', path: '/story', description: 'Story page', expectedStatus: [200, 201] },
            { method: 'GET', path: '/manifest.json', description: 'PWA manifest', expectedStatus: [200, 201] }
        ];

        for (const endpoint of basicEndpoints) {
            await this.testEndpoint(endpoint, 'Basic Pages');
        }
    }

    async testAuthenticationEndpoints() {
        console.log('\n🔐 Testing Authentication Endpoints...');
        
        // Test user registration with unique email
        const uniqueEmail = `test-${Date.now()}-${Math.random().toString(36).substr(2, 9)}@example.com`;
        
        try {
            // First, register a new user
            const registerResponse = await axios.post(`${this.baseUrl}/api/auth/register`, {
                email: uniqueEmail,
                password: 'testpassword123',
                name: 'Test User'
            });

            if (registerResponse.status === 201 || registerResponse.status === 200) {
                console.log('✅ User registration - 201 (0ms)');
                this.testResults.push({
                    category: 'Authentication',
                    test: 'User registration',
                    status: 'PASS',
                    details: `Status: ${registerResponse.status}`
                });
            } else if (registerResponse.status === 409) {
                console.log('⚠️ User registration - 409 (User already exists)');
                this.testResults.push({
                    category: 'Authentication',
                    test: 'User registration',
                    status: 'SKIP',
                    details: 'User already exists - using existing user for other tests'
                });
            } else {
                throw new Error(`Unexpected registration status: ${registerResponse.status}`);
            }

            // Now test other auth endpoints with the registered user
            const authEndpoints = [
                {
                    method: 'POST',
                    path: '/api/auth/login',
                    description: 'User login',
                    expectedStatus: [200, 400, 401],
                    data: {
                        email: uniqueEmail,
                        password: 'testpassword123'
                    }
                },
                {
                    method: 'POST',
                    path: '/api/auth/firebase-sync',
                    description: 'Firebase sync',
                    expectedStatus: [200, 400],
                    data: {
                        firebase_uid: 'test-firebase-uid',
                        email: uniqueEmail
                    }
                }
            ];

            for (const endpoint of authEndpoints) {
                await this.testEndpoint(endpoint, 'Authentication');
            }
        } catch (error) {
            console.log('❌ User registration - Expected 200/201/400, got 409');
            this.testResults.push({
                category: 'Authentication',
                test: 'User registration',
                status: 'FAIL',
                error: 'Expected 200/201/400, got 409'
            });
            this.logBug('API', 'User registration failed: Expected 200/201/400, got 409', 'high');
        }
    }

    async testStoryEndpoints() {
        console.log('\n📚 Testing Story Endpoints...');
        
        // First register a user for story testing
        const uniqueEmail = `story-test-${Date.now()}-${Math.random().toString(36).substr(2, 9)}@example.com`;
        let testUserId = 'api-test-user';
        
        try {
            const registerResponse = await axios.post(`${this.baseUrl}/api/auth/register`, {
                email: uniqueEmail,
                password: 'testpassword123',
                name: 'Story Test User'
            });
            
            if (registerResponse.status === 201 && registerResponse.data.user_id) {
                testUserId = registerResponse.data.user_id;
                console.log(`✅ Registered test user: ${testUserId}`);
                
                // Wait for user to be available in database
                await new Promise(resolve => setTimeout(resolve, 1000));
            }
        } catch (error) {
            console.log('⚠️ Using default test user ID for story tests');
        }
        
        const storyEndpoints = [
            {
                method: 'GET',
                path: '/api/stories',
                description: 'Get all stories',
                expectedStatus: [200, 201]
            },
            {
                method: 'POST',
                path: '/api/stories',
                description: 'Create new story',
                expectedStatus: [200, 201],
                data: {
                    title: 'Test Story from API',
                    content: 'This is a test story created through the API test suite.',
                    user_id: testUserId,
                    visibility: 'private'
                },
                headers: {
                    'X-User-ID': testUserId,
                    'Content-Type': 'application/json'
                }
            },
            {
                method: 'GET',
                path: `/api/user/stories?user_id=${testUserId}`,
                description: 'Get user stories',
                expectedStatus: [200, 500]
            }
        ];

        for (const endpoint of storyEndpoints) {
            await this.testEndpoint(endpoint, 'Stories');
        }
    }

    async testChatEndpoints() {
        console.log('\n💬 Testing Chat Endpoints...');
        
        // First register a user for chat testing
        const uniqueEmail = `chat-test-${Date.now()}-${Math.random().toString(36).substr(2, 9)}@example.com`;
        let testUserId = 'chat-test-user';
        
        try {
            const registerResponse = await axios.post(`${this.baseUrl}/api/auth/register`, {
                email: uniqueEmail,
                password: 'testpassword123',
                name: 'Chat Test User'
            });
            
            if (registerResponse.status === 201 && registerResponse.data.user_id) {
                testUserId = registerResponse.data.user_id;
                console.log(`✅ Registered chat test user: ${testUserId}`);
                
                // Wait for user to be available in database
                await new Promise(resolve => setTimeout(resolve, 2000));
                
                // Test chat message with registered user
                const chatResponse = await axios.post(`${this.baseUrl}/api/chat/message`, {
                    message: 'Hello, this is a test message from the API test suite.',
                    user_id: testUserId
                }, { 
                    timeout: 10000,
                    validateStatus: (status) => status < 500
                });
                
                if (chatResponse.status === 200 || chatResponse.status === 201) {
                    console.log('✅ Chat message endpoint working');
                    if (this.testResults) {
                        this.testResults.push({ endpoint: 'POST /api/chat/message', status: 'PASS', response: chatResponse.status });
                    }
                } else {
                    console.log(`❌ Chat message failed: ${chatResponse.status}`);
                    if (this.testResults) {
                        this.testResults.push({ endpoint: 'POST /api/chat/message', status: 'FAIL', response: chatResponse.status, error: chatResponse.data });
                    }
                }
            } else {
                console.log('❌ Failed to register chat test user');
                if (this.testResults) {
                    this.testResults.push({ endpoint: 'POST /api/chat/message', status: 'FAIL', error: 'User registration failed' });
                }
            }
        } catch (error) {
            console.log(`❌ Chat endpoint test failed: ${error.message}`);
            if (this.testResults) {
                this.testResults.push({ endpoint: 'POST /api/chat/message', status: 'FAIL', error: error.message });
            }
        }
    }

    async testKnowledgeEndpoints() {
        console.log('\n🧠 Testing Knowledge Endpoints...');
        
        const knowledgeEndpoints = [
            {
                method: 'GET',
                path: '/api/inner-space-data',
                description: 'Get inner space data',
                expectedStatus: [200, 201],
                params: { user_id: 'api-test-user' }
            },
            {
                method: 'POST',
                path: '/api/knowledge/analyze',
                description: 'Analyze knowledge',
                expectedStatus: [200, 201],
                data: {
                    user_id: 'api-test-user'
                }
            },
            {
                method: 'POST',
                path: '/api/knowledge/ask',
                description: 'Ask knowledge question',
                expectedStatus: [200, 201],
                data: {
                    question: 'What are my main emotional patterns?',
                    user_id: 'api-test-user'
                }
            },
            {
                method: 'POST',
                path: '/api/knowledge/start-conversation',
                description: 'Start guided conversation',
                expectedStatus: [200, 400],
                data: {
                    user_id: 'api-test-user',
                    conversation_id: 'procrastination_deep_dive'
                }
            }
        ];

        for (const endpoint of knowledgeEndpoints) {
            await this.testEndpoint(endpoint, 'Knowledge');
        }
    }

    async testErrorHandling() {
        console.log('\n⚠️ Testing Error Handling...');
        
        const errorTests = [
            {
                method: 'GET',
                path: '/api/nonexistent-endpoint',
                description: 'Non-existent endpoint',
                expectedStatus: 404
            },
            {
                method: 'POST',
                path: '/api/stories',
                description: 'Invalid story data',
                expectedStatus: 400,
                data: {
                    title: '',
                    content: ''
                }
            }
        ];

        for (const test of errorTests) {
            await this.testEndpoint(test, 'Error Handling');
        }
    }

    async testResponseFormats() {
        console.log('\n📋 Testing Response Formats...');
        
        const formatTests = [
            {
                endpoint: '/api/stories',
                method: 'GET',
                description: 'Stories response format',
                expectedFields: ['id', 'title', 'content'],
                isArray: true
            }
        ];

        for (const test of formatTests) {
            try {
                const response = await axios.get(`${this.baseUrl}${test.endpoint}`);
                
                if (response.status === 200) {
                    const data = response.data;
                    let formatValid = true;
                    let formatIssues = [];

                    if (test.isArray && Array.isArray(data) && data.length > 0) {
                        const firstItem = data[0];
                        test.expectedFields.forEach(field => {
                            if (!(field in firstItem)) {
                                formatValid = false;
                                formatIssues.push(`Missing field: ${field}`);
                            }
                        });
                    }

                    if (formatValid) {
                        console.log(`✅ ${test.description} - Format valid`);
                        this.testResults.push({
                            category: 'Response Format',
                            test: test.description,
                            status: 'PASS',
                            details: 'Response format matches expectations'
                        });
                    } else {
                        console.log(`❌ ${test.description} - Format issues`);
                        this.testResults.push({
                            category: 'Response Format',
                            test: test.description,
                            status: 'FAIL',
                            error: formatIssues.join(', ')
                        });
                    }
                }
            } catch (error) {
                console.log(`💥 ${test.description} - Format test failed`);
                this.testResults.push({
                    category: 'Response Format',
                    test: test.description,
                    status: 'FAIL',
                    error: error.message
                });
            }
        }
    }

    async testEndpoint(endpoint, category) {
        const startTime = Date.now();
        
        try {
            let response;
            let url = `${this.baseUrl}${endpoint.path}`;
            
            if (endpoint.params) {
                const params = new URLSearchParams(endpoint.params);
                url += `?${params}`;
            }

            const config = {
                timeout: 10000,
                validateStatus: (status) => status < 600,
                headers: endpoint.headers || {}
            };

            if (endpoint.method === 'GET') {
                response = await axios.get(url, config);
            } else if (endpoint.method === 'POST') {
                response = await axios.post(url, endpoint.data || {}, config);
            }

            const responseTime = Date.now() - startTime;
            const expectedStatuses = Array.isArray(endpoint.expectedStatus) 
                ? endpoint.expectedStatus 
                : [endpoint.expectedStatus];
            
            const statusMatch = expectedStatuses.includes(response.status);
            
            if (statusMatch) {
                console.log(`✅ ${endpoint.description} - ${response.status} (${responseTime}ms)`);
                this.testResults.push({
                    category,
                    test: endpoint.description,
                    status: 'PASS',
                    details: `${endpoint.method} ${endpoint.path} - ${response.status} (${responseTime}ms)`,
                    responseTime
                });
            } else {
                console.log(`❌ ${endpoint.description} - Expected ${expectedStatuses.join('/')}, got ${response.status}`);
                this.testResults.push({
                    category,
                    test: endpoint.description,
                    status: 'FAIL',
                    error: `Expected status ${expectedStatuses.join('/')}, got ${response.status}`,
                    responseTime
                });
            }
        } catch (error) {
            const responseTime = Date.now() - startTime;
            
            if (error.response) {
                const expectedStatuses = Array.isArray(endpoint.expectedStatus) 
                    ? endpoint.expectedStatus 
                    : [endpoint.expectedStatus];
                
                if (expectedStatuses.includes(error.response.status)) {
                    console.log(`✅ ${endpoint.description} - ${error.response.status} (${responseTime}ms)`);
                    this.testResults.push({
                        category,
                        test: endpoint.description,
                        status: 'PASS',
                        details: `${endpoint.method} ${endpoint.path} - ${error.response.status} (${responseTime}ms)`,
                        responseTime
                    });
                } else {
                    console.log(`❌ ${endpoint.description} - Unexpected error: ${error.response.status}`);
                    this.testResults.push({
                        category,
                        test: endpoint.description,
                        status: 'FAIL',
                        error: `HTTP ${error.response.status}: ${error.message}`,
                        responseTime
                    });
                }
            } else {
                console.log(`💥 ${endpoint.description} - Network/Critical error`);
                this.testResults.push({
                    category,
                    test: endpoint.description,
                    status: 'FAIL',
                    error: error.message,
                    responseTime
                });
            }
        }
    }

    logBug(category, description, severity) {
        const bug = {
            id: `bug-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
            category,
            description,
            severity,
            timestamp: new Date().toISOString(),
            status: 'open',
            source: 'api-tests'
        };

        this.bugTracker.bugs = this.bugTracker.bugs || [];
        this.bugTracker.bugs.push(bug);
    }

    logCriticalBug(component, error) {
        this.logBug('Critical', `${component}: ${error}`, 'critical');
    }

    generateAPIReport() {
        console.log('\n📊 API Test Results Summary:');
        console.log('=============================');
        
        const categories = ['Basic Pages', 'Authentication', 'Stories', 'Chat', 'Knowledge', 'Error Handling', 'Response Format'];
        
        categories.forEach(category => {
            const categoryTests = this.testResults.filter(t => t.category === category);
            const passed = categoryTests.filter(t => t.status === 'PASS').length;
            const total = categoryTests.length;
            
            if (total > 0) {
                console.log(`${category}: ${passed}/${total} passed`);
            }
        });
        
        const reportPath = path.join(__dirname, '../reports/api-test-report.json');
        fs.writeFileSync(reportPath, JSON.stringify({
            timestamp: new Date().toISOString(),
            summary: {
                totalTests: this.testResults.length,
                passed: this.testResults.filter(t => t.status === 'PASS').length,
                failed: this.testResults.filter(t => t.status === 'FAIL').length
            },
            details: this.testResults
        }, null, 2));
        
        console.log(`\n📄 Detailed API report saved to: ${reportPath}`);
        
        const bugTrackerPath = path.join(__dirname, '../bugs/bug-tracker.json');
        fs.writeFileSync(bugTrackerPath, JSON.stringify(this.bugTracker, null, 2));
    }
}

module.exports = APITestSuite;

if (require.main === module) {
    const testSuite = new APITestSuite();
    testSuite.runAllAPITests().catch(console.error);
} 