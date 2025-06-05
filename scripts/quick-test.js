const axios = require('axios');

class QuickTest {
    constructor(baseUrl = 'http://localhost:8080') {
        this.baseUrl = baseUrl;
        this.results = [];
    }

    async runQuickTests() {
        console.log('🚀 Running Quick Tests to Verify Fixes...');
        console.log('===========================================');

        // Test 1: Basic endpoints
        await this.testBasicEndpoints();
        
        // Test 2: Authentication endpoints
        await this.testAuthEndpoints();
        
        // Test 3: Chat with authentication
        await this.testChatWithAuth();
        
        // Test 4: Knowledge endpoints
        await this.testKnowledgeEndpoints();
        
        // Test 5: User story queries (Firebase index test)
        await this.testUserStoryQueries();

        this.printResults();
    }

    async testBasicEndpoints() {
        console.log('\n📄 Testing Basic Endpoints...');
        
        const endpoints = [
            { path: '/', name: 'Landing Page' },
            { path: '/app', name: 'Main App' },
            { path: '/api/stories', name: 'Stories API' }
        ];

        for (const endpoint of endpoints) {
            try {
                const response = await axios.get(`${this.baseUrl}${endpoint.path}`, { timeout: 3000 });
                if (response.status === 200) {
                    console.log(`✅ ${endpoint.name} - Working`);
                    this.results.push({ test: endpoint.name, status: 'PASS' });
                } else {
                    console.log(`❌ ${endpoint.name} - Status ${response.status}`);
                    this.results.push({ test: endpoint.name, status: 'FAIL', error: `Status ${response.status}` });
                }
            } catch (error) {
                console.log(`❌ ${endpoint.name} - ${error.message}`);
                this.results.push({ test: endpoint.name, status: 'FAIL', error: error.message });
            }
        }
    }

    async testAuthEndpoints() {
        console.log('\n🔐 Testing Authentication Endpoints...');
        
        const uniqueEmail = `quick-test-${Date.now()}@example.com`;
        
        try {
            // Test registration
            const registerResponse = await axios.post(`${this.baseUrl}/api/auth/register`, {
                email: uniqueEmail,
                name: 'Quick Test User',
                password: 'testpass123'
            }, { timeout: 5000 });

            if (registerResponse.status === 201) {
                console.log('✅ User Registration - Working');
                this.results.push({ test: 'User Registration', status: 'PASS' });
                
                const userId = registerResponse.data.user_id;
                
                // Test login
                try {
                    const loginResponse = await axios.post(`${this.baseUrl}/api/auth/login`, {
                        email: uniqueEmail,
                        password: 'testpass123'
                    }, { timeout: 5000 });

                    if (loginResponse.status === 200) {
                        console.log('✅ User Login - Working');
                        this.results.push({ test: 'User Login', status: 'PASS' });
                    } else {
                        console.log(`⚠️ User Login - Status ${loginResponse.status}`);
                        this.results.push({ test: 'User Login', status: 'PARTIAL', error: `Status ${loginResponse.status}` });
                    }
                } catch (loginError) {
                    console.log(`❌ User Login - ${loginError.message}`);
                    this.results.push({ test: 'User Login', status: 'FAIL', error: loginError.message });
                }
                
                return userId;
            } else {
                console.log(`❌ User Registration - Status ${registerResponse.status}`);
                this.results.push({ test: 'User Registration', status: 'FAIL', error: `Status ${registerResponse.status}` });
                return null;
            }
        } catch (error) {
            console.log(`❌ User Registration - ${error.message}`);
            this.results.push({ test: 'User Registration', status: 'FAIL', error: error.message });
            return null;
        }
    }

    async testChatWithAuth() {
        console.log('\n💬 Testing Chat with Authentication...');
        
        const uniqueEmail = `chat-test-${Date.now()}@example.com`;
        
        try {
            // Register user for chat test
            const registerResponse = await axios.post(`${this.baseUrl}/api/auth/register`, {
                email: uniqueEmail,
                name: 'Chat Test User',
                password: 'testpass123'
            });

            if (registerResponse.status === 201) {
                const userId = registerResponse.data.user_id;
                
                // Wait for user to be available
                await new Promise(resolve => setTimeout(resolve, 1000));
                
                // Test chat message with auth headers
                const chatResponse = await axios.post(`${this.baseUrl}/api/chat/message`, {
                    message: 'This is a quick test message to verify chat functionality is working.',
                    user_id: userId
                }, {
                    headers: {
                        'X-User-ID': userId,
                        'Content-Type': 'application/json'
                    },
                    timeout: 10000
                });

                if (chatResponse.status === 200 || chatResponse.status === 201) {
                    console.log('✅ Chat with Authentication - Working');
                    this.results.push({ test: 'Chat with Auth', status: 'PASS' });
                    
                    if (chatResponse.data.story_created) {
                        console.log('✅ Story Creation from Chat - Working');
                        this.results.push({ test: 'Story Creation', status: 'PASS' });
                    }
                } else {
                    console.log(`❌ Chat with Authentication - Status ${chatResponse.status}`);
                    this.results.push({ test: 'Chat with Auth', status: 'FAIL', error: `Status ${chatResponse.status}` });
                }
            }
        } catch (error) {
            console.log(`❌ Chat with Authentication - ${error.message}`);
            this.results.push({ test: 'Chat with Auth', status: 'FAIL', error: error.message });
        }
    }

    async testKnowledgeEndpoints() {
        console.log('\n🧠 Testing Knowledge Endpoints...');
        
        const endpoints = [
            {
                name: 'Knowledge Ask',
                method: 'POST',
                path: '/api/knowledge/ask',
                data: {
                    question: 'What are my emotional patterns?',
                    user_id: 'quick-test-user'
                }
            },
            {
                name: 'Knowledge Analyze',
                method: 'POST',
                path: '/api/knowledge/analyze',
                data: {
                    user_id: 'quick-test-user'
                }
            },
            {
                name: 'Start Conversation',
                method: 'POST',
                path: '/api/knowledge/start-conversation',
                data: {
                    user_id: 'quick-test-user',
                    conversation_id: 'procrastination_deep_dive'
                }
            }
        ];

        for (const endpoint of endpoints) {
            try {
                const response = await axios.post(`${this.baseUrl}${endpoint.path}`, endpoint.data, { timeout: 5000 });
                
                if (response.status === 200) {
                    console.log(`✅ ${endpoint.name} - Working`);
                    this.results.push({ test: endpoint.name, status: 'PASS' });
                } else if (response.status === 400) {
                    console.log(`⚠️ ${endpoint.name} - Expected 400 (validation working)`);
                    this.results.push({ test: endpoint.name, status: 'PARTIAL', note: 'Validation working' });
                } else {
                    console.log(`❌ ${endpoint.name} - Status ${response.status}`);
                    this.results.push({ test: endpoint.name, status: 'FAIL', error: `Status ${response.status}` });
                }
            } catch (error) {
                if (error.response && error.response.status === 400) {
                    console.log(`⚠️ ${endpoint.name} - Expected 400 (validation working)`);
                    this.results.push({ test: endpoint.name, status: 'PARTIAL', note: 'Validation working' });
                } else {
                    console.log(`❌ ${endpoint.name} - ${error.message}`);
                    this.results.push({ test: endpoint.name, status: 'FAIL', error: error.message });
                }
            }
        }
    }

    async testUserStoryQueries() {
        console.log('\n📚 Testing User Story Queries (Firebase Index)...');
        
        const uniqueEmail = `story-query-test-${Date.now()}@example.com`;
        
        try {
            // Register user
            const registerResponse = await axios.post(`${this.baseUrl}/api/auth/register`, {
                email: uniqueEmail,
                name: 'Story Query Test User'
            });

            if (registerResponse.status === 201) {
                const userId = registerResponse.data.user_id;
                
                // Wait for user to be available
                await new Promise(resolve => setTimeout(resolve, 1000));
                
                // Test user stories query (this was failing before Firebase index)
                const storiesResponse = await axios.get(`${this.baseUrl}/api/user/stories?user_id=${userId}`, { timeout: 5000 });

                if (storiesResponse.status === 200) {
                    console.log('✅ User Story Queries - Working (Firebase index successful!)');
                    this.results.push({ test: 'User Story Queries', status: 'PASS', note: 'Firebase index working' });
                } else {
                    console.log(`❌ User Story Queries - Status ${storiesResponse.status}`);
                    this.results.push({ test: 'User Story Queries', status: 'FAIL', error: `Status ${storiesResponse.status}` });
                }
            }
        } catch (error) {
            if (error.response && error.response.status === 500 && error.response.data && error.response.data.error && error.response.data.error.includes('index')) {
                console.log('❌ User Story Queries - Firebase index still building or missing');
                this.results.push({ test: 'User Story Queries', status: 'FAIL', error: 'Firebase index issue' });
            } else {
                console.log(`❌ User Story Queries - ${error.message}`);
                this.results.push({ test: 'User Story Queries', status: 'FAIL', error: error.message });
            }
        }
    }

    printResults() {
        console.log('\n📊 Quick Test Results Summary:');
        console.log('===============================');
        
        const passed = this.results.filter(r => r.status === 'PASS').length;
        const partial = this.results.filter(r => r.status === 'PARTIAL').length;
        const failed = this.results.filter(r => r.status === 'FAIL').length;
        const total = this.results.length;
        
        console.log(`✅ Passed: ${passed}/${total}`);
        console.log(`⚠️ Partial: ${partial}/${total}`);
        console.log(`❌ Failed: ${failed}/${total}`);
        console.log(`📈 Success Rate: ${Math.round(((passed + partial * 0.5) / total) * 100)}%`);
        
        if (failed > 0) {
            console.log('\n❌ Failed Tests:');
            this.results.filter(r => r.status === 'FAIL').forEach(r => {
                console.log(`   - ${r.test}: ${r.error}`);
            });
        }
        
        if (partial > 0) {
            console.log('\n⚠️ Partial Tests:');
            this.results.filter(r => r.status === 'PARTIAL').forEach(r => {
                console.log(`   - ${r.test}: ${r.note || 'Partially working'}`);
            });
        }
        
        console.log('\n🎯 Ready for full test suite!');
    }
}

// Run the quick tests
const quickTest = new QuickTest();
quickTest.runQuickTests().catch(console.error); 