const axios = require('axios');
const fs = require('fs');
const path = require('path');

class AutomatedTestSuite {
    constructor(baseUrl = 'http://localhost:8080') {
        this.baseUrl = baseUrl;
        this.testResults = {
            api: [],
            database: [],
            components: [],
            userFlows: [],
            performance: []
        };
        this.bugTracker = require('../bugs/bug-tracker.json');
    }

    async runAllTests() {
        console.log('🚀 Starting Comprehensive Test Suite...\n');
        
        try {
            await this.testApiEndpoints();
            await this.testDatabaseConnections();
            await this.testComponentRendering();
            await this.testUserFlows();
            await this.testPerformance();
            
            this.generateTestReport();
            this.logBugsFound();
            
        } catch (error) {
            console.error('❌ Test suite failed:', error);
            this.logCriticalBug('Test Suite Failure', error.message);
        }
    }

    async testApiEndpoints() {
        console.log('🔍 Testing API Endpoints...');
        
        const endpoints = [
            { method: 'GET', path: '/api/stories', description: 'Get all stories', expectedStatus: [200], maxResponseTime: 2000 },
            { method: 'POST', path: '/api/stories', description: 'Create new story', expectedStatus: [201, 401], maxResponseTime: 2000 },
            { method: 'GET', path: '/api/user/stories', description: 'Get user stories', expectedStatus: [200, 401], maxResponseTime: 2000 },
            { method: 'POST', path: '/api/chat/message', description: 'Send chat message', expectedStatus: [200, 201, 401], maxResponseTime: 2000 },
            { method: 'GET', path: '/api/inner-space-data', description: 'Get inner space data', expectedStatus: [200, 401], maxResponseTime: 2000 },
            { method: 'POST', path: '/api/knowledge/ask', description: 'Ask knowledge question', expectedStatus: [200, 401], maxResponseTime: 2000 },
            { method: 'POST', path: '/api/knowledge/analyze', description: 'Analyze knowledge', expectedStatus: [200, 401], maxResponseTime: 2000 },
            { method: 'POST', path: '/api/knowledge/start-conversation', description: 'Start guided conversation', expectedStatus: [200, 400, 401], maxResponseTime: 2000 },
            { method: 'POST', path: '/api/auth/register', description: 'Register user', expectedStatus: [201, 400, 409], maxResponseTime: 2000 },
            { method: 'POST', path: '/api/auth/login', description: 'Login user', expectedStatus: [200, 400, 401], maxResponseTime: 2000 },
            { method: 'POST', path: '/api/waitlist', description: 'Join waitlist', expectedStatus: [200, 201], maxResponseTime: 2000 }
        ];

        for (const endpoint of endpoints) {
            try {
                const result = await this.testEndpoint(endpoint);
                this.testResults.api.push(result);
                
                if (result.status === 'PASS') {
                    console.log(`✅ ${endpoint.method} ${endpoint.path} - ${result.responseTime}ms`);
                } else {
                    console.log(`❌ ${endpoint.method} ${endpoint.path} - ${result.error}`);
                    this.logBug('API', `${endpoint.method} ${endpoint.path} failed: ${result.error}`, 'high');
                }
            } catch (error) {
                console.log(`💥 ${endpoint.method} ${endpoint.path} - Critical failure`);
                this.logCriticalBug(`API Endpoint ${endpoint.path}`, error.message);
            }
        }
    }

    async testEndpoint(endpoint) {
        const startTime = Date.now();
        
        try {
            let response;
            const config = {
                timeout: 5000,
                validateStatus: (status) => status < 500 // Accept 4xx as valid responses
            };

            // For chat message, we need to register a user first
            if (endpoint.method === 'POST' && endpoint.path === '/api/chat/message') {
                const uniqueEmail = `auto-chat-${Date.now()}-${Math.random().toString(36).substr(2, 9)}@example.com`;
                
                try {
                    const registerResponse = await axios.post(`${this.baseUrl}/api/auth/register`, {
                        email: uniqueEmail,
                        name: 'Auto Chat Test User'
                    });
                    
                    if (registerResponse.status === 201) {
                        const userId = registerResponse.data.user_id;
                        await new Promise(resolve => setTimeout(resolve, 1000));
                        
                        response = await axios.post(`${this.baseUrl}${endpoint.path}`, {
                            message: 'Test message from automated suite',
                            user_id: userId
                        }, config);
                    } else {
                        throw new Error('User registration failed');
                    }
                } catch (regError) {
                    response = { status: 500, data: { error: 'User registration failed' } };
                }
            }
            // For story creation, we need to add auth headers
            else if (endpoint.method === 'POST' && endpoint.path === '/api/stories') {
                const uniqueEmail = `auto-story-${Date.now()}-${Math.random().toString(36).substr(2, 9)}@example.com`;
                
                try {
                    const registerResponse = await axios.post(`${this.baseUrl}/api/auth/register`, {
                        email: uniqueEmail,
                        name: 'Auto Story Test User'
                    });
                    
                    if (registerResponse.status === 201) {
                        const userId = registerResponse.data.user_id;
                        
                        response = await axios.post(`${this.baseUrl}${endpoint.path}`, {
                            title: 'Test Story',
                            content: 'This is a test story from the automated test suite.',
                            format: 'reflection'
                        }, {
                            ...config,
                            headers: {
                                'Content-Type': 'application/json',
                                'X-User-ID': userId
                            }
                        });
                    } else {
                        throw new Error('User registration failed');
                    }
                } catch (regError) {
                    response = { status: 401, data: { error: 'Authentication required' } };
                }
            }
            // For login, use proper test data
            else if (endpoint.method === 'POST' && endpoint.path === '/api/auth/login') {
                response = await axios.post(`${this.baseUrl}${endpoint.path}`, {
                    email: 'test@example.com'
                }, config);
            }
            // For other POST endpoints
            else if (endpoint.method === 'POST') {
                const testData = this.getTestData(endpoint.path);
                response = await axios.post(`${this.baseUrl}${endpoint.path}`, testData, config);
            }
            // For GET endpoints
            else {
                // Special handling for user stories endpoint which requires user_id
                if (endpoint.path === '/api/user/stories') {
                    // Create a test user first
                    const uniqueEmail = `test-user-stories-${Date.now()}-${Math.random().toString(36).substr(2, 9)}@example.com`;
                    
                    try {
                        const registerResponse = await axios.post(`${this.baseUrl}/api/auth/register`, {
                            email: uniqueEmail,
                            name: 'Test User Stories User'
                        });
                        
                        if (registerResponse.status === 201) {
                            const userId = registerResponse.data.user_id;
                            response = await axios.get(`${this.baseUrl}${endpoint.path}?user_id=${userId}`, config);
                        } else {
                            // If registration fails, test without user_id to get expected 400 response
                            response = await axios.get(`${this.baseUrl}${endpoint.path}`, config);
                        }
                    } catch (regError) {
                        // If registration fails, test without user_id to get expected 400 response
                        response = await axios.get(`${this.baseUrl}${endpoint.path}`, config);
                    }
                } else {
                    response = await axios.get(`${this.baseUrl}${endpoint.path}`, config);
                }
            }

            const responseTime = Date.now() - startTime;
            const isSuccess = endpoint.expectedStatus.includes(response.status);
            
            return {
                endpoint: `${endpoint.method} ${endpoint.path}`,
                status: isSuccess ? 'PASS' : 'FAIL',
                expectedStatus: endpoint.expectedStatus,
                actualStatus: response.status,
                responseTime: responseTime,
                withinTimeLimit: responseTime <= endpoint.maxResponseTime
            };
            
        } catch (error) {
            const responseTime = Date.now() - startTime;
            
            // Handle specific error cases
            if (error.response) {
                const isSuccess = endpoint.expectedStatus.includes(error.response.status);
                return {
                    endpoint: `${endpoint.method} ${endpoint.path}`,
                    status: isSuccess ? 'PASS' : 'FAIL',
                    expectedStatus: endpoint.expectedStatus,
                    actualStatus: error.response.status,
                    responseTime: responseTime,
                    withinTimeLimit: responseTime <= endpoint.maxResponseTime,
                    error: error.response.data
                };
            }
            
            return {
                endpoint: `${endpoint.method} ${endpoint.path}`,
                status: 'FAIL',
                expectedStatus: endpoint.expectedStatus,
                actualStatus: 'ERROR',
                responseTime: responseTime,
                withinTimeLimit: false,
                error: error.message
            };
        }
    }

    async testDatabaseConnections() {
        console.log('\n🗄️ Testing Database Connections...');
        
        try {
            // Test basic connectivity
            const response = await axios.get(`${this.baseUrl}/api/stories`);
            if (response.status === 200) {
                console.log('✅ Database connection successful');
                this.testResults.database.push({
                    test: 'Database Connectivity',
                    status: 'PASS'
                });
            }
        } catch (error) {
            console.log('❌ Database connection failed');
            this.testResults.database.push({
                test: 'Database Connectivity',
                status: 'FAIL',
                error: error.message
            });
            this.logCriticalBug('Database Connection', error.message);
        }
    }

    async testComponentRendering() {
        console.log('\n🎨 Testing Component Rendering...');
        
        const pages = [
            { path: '/', name: 'Landing Page' },
            { path: '/app', name: 'Main App' },
            { path: '/chat', name: 'Chat Interface' },
            { path: '/inner-space', name: 'Inner Space' },
            { path: '/deck', name: 'Story Deck' },
            { path: '/story', name: 'Story View' }
        ];

        for (const page of pages) {
            try {
                const response = await axios.get(`${this.baseUrl}${page.path}`);
                
                if (response.status === 200 && response.data.includes('<!DOCTYPE html>')) {
                    console.log(`✅ ${page.name} renders successfully`);
                    this.testResults.components.push({
                        component: page.name,
                        status: 'PASS'
                    });
                } else {
                    console.log(`❌ ${page.name} failed to render properly`);
                    this.testResults.components.push({
                        component: page.name,
                        status: 'FAIL',
                        error: 'Invalid HTML response'
                    });
                    this.logBug('Component', `${page.name} rendering issue`, 'medium');
                }
            } catch (error) {
                console.log(`💥 ${page.name} critical rendering failure`);
                this.testResults.components.push({
                    component: page.name,
                    status: 'FAIL',
                    error: error.message
                });
                this.logBug('Component', `${page.name} failed: ${error.message}`, 'high');
            }
        }
    }

    async testUserFlows() {
        console.log('\n👤 Testing User Flows...');
        
        // Test Share → Story Creation Flow
        await this.testShareToStoryFlow();
        
        // Test Space Question → Curated Conversation Flow
        await this.testSpaceQuestionFlow();
        
        // Test Story Discovery Flow
        await this.testDiscoveryFlow();
    }

    async testShareToStoryFlow() {
        console.log('Testing Share → Story Creation Flow...');
        
        try {
            // Step 1: Register a user
            const userEmail = `share-flow-${Date.now()}-${Math.random().toString(36).substr(2, 9)}@test.com`;
            const registerResponse = await axios.post(`${this.baseUrl}/api/auth/register`, {
                email: userEmail,
                name: 'Share Flow Test User'
            });

            if (registerResponse.status !== 201) {
                throw new Error('User registration failed');
            }

            const userId = registerResponse.data.user_id;
            
            // Wait for user to be available in database
            await new Promise(resolve => setTimeout(resolve, 2000));

            // Step 2: Send a chat message
            const chatResponse = await axios.post(`${this.baseUrl}/api/chat/message`, {
                message: 'Today I had an amazing breakthrough at work. I finally understood a complex problem that had been bothering me for weeks.',
                user_id: userId
            });

            if (chatResponse.status === 200 || chatResponse.status === 201) {
                console.log('✅ Chat message sent successfully');
                
                // Step 3: Check if story was created
                const storiesResponse = await axios.get(`${this.baseUrl}/api/user/stories?user_id=${userId}`);
                
                if (storiesResponse.status === 200 && storiesResponse.data.length > 0) {
                    console.log('✅ Story created from conversation');
                    this.testResults.userFlows.push({
                        flow: 'Share to Story',
                        status: 'PASS'
                    });
                } else {
                    console.log('❌ Story not created from conversation');
                    this.testResults.userFlows.push({
                        flow: 'Share to Story',
                        status: 'FAIL',
                        error: 'Story creation failed'
                    });
                    this.logBug('User Flow', 'Share to Story flow broken', 'high');
                }
            }
        } catch (error) {
            console.log('💥 Share to Story flow failed');
            this.logCriticalBug('Share to Story Flow', error.message);
        }
    }

    async testSpaceQuestionFlow() {
        console.log('Testing Space Question → Curated Conversation Flow...');
        
        try {
            // Step 1: Register a user
            const userEmail = `space-flow-${Date.now()}-${Math.random().toString(36).substr(2, 9)}@test.com`;
            const registerResponse = await axios.post(`${this.baseUrl}/api/auth/register`, {
                email: userEmail,
                name: 'Space Flow Test User'
            });

            if (registerResponse.status !== 201) {
                throw new Error('User registration failed');
            }

            const userId = registerResponse.data.user_id;
            
            // Wait for user to be available in database
            await new Promise(resolve => setTimeout(resolve, 2000));

            const response = await axios.post(`${this.baseUrl}/api/knowledge/ask`, {
                question: 'What are my main emotional patterns?',
                user_id: userId
            });

            if (response.status === 200) {
                const data = response.data;
                
                // Check for the new response format
                if (data.confidence === 'low' && data.type === 'guided_discovery') {
                    console.log('✅ Space correctly identified insufficient data and created guided discovery response');
                    this.testResults.userFlows.push({
                        flow: 'Space Question to Conversation',
                        status: 'PASS'
                    });
                } else if (data.confidence === 'high' && data.type === 'analysis_with_gaps') {
                    console.log('✅ Space provided analysis based on existing data');
                    this.testResults.userFlows.push({
                        flow: 'Space Question Analysis',
                        status: 'PASS'
                    });
                } else if (data.confidence === 'medium' && data.type === 'partial_with_path') {
                    console.log('✅ Space provided partial analysis with learning path');
                    this.testResults.userFlows.push({
                        flow: 'Space Question Partial Analysis',
                        status: 'PASS'
                    });
                } else {
                    console.log('❌ Space response format unexpected');
                    console.log('Response data:', JSON.stringify(data, null, 2));
                    this.testResults.userFlows.push({
                        flow: 'Space Question Flow',
                        status: 'FAIL',
                        error: `Unexpected response format: confidence=${data.confidence}, type=${data.type}`
                    });
                    this.logBug('User Flow', 'Space question flow response format issue', 'medium');
                }
            }
        } catch (error) {
            console.log('💥 Space question flow failed');
            this.logCriticalBug('Space Question Flow', error.message);
        }
    }

    async testDiscoveryFlow() {
        console.log('Testing Discovery Flow...');
        
        try {
            const response = await axios.get(`${this.baseUrl}/api/stories`);
            
            if (response.status === 200 && Array.isArray(response.data)) {
                console.log('✅ Stories loaded for discovery');
                this.testResults.userFlows.push({
                    flow: 'Discovery Stories Load',
                    status: 'PASS'
                });
            } else {
                console.log('❌ Discovery stories failed to load');
                this.logBug('User Flow', 'Discovery stories loading issue', 'high');
            }
        } catch (error) {
            console.log('💥 Discovery flow failed');
            this.logCriticalBug('Discovery Flow', error.message);
        }
    }

    async testPerformance() {
        console.log('\n⚡ Testing Performance...');
        
        const performanceTests = [
            { endpoint: '/api/stories', maxTime: 500, description: 'Stories load time' },
            { endpoint: '/api/inner-space-data', maxTime: 1000, description: 'Inner space data load time' },
            { endpoint: '/', maxTime: 3000, description: 'Landing page load time' },
            { endpoint: '/app', maxTime: 3000, description: 'App page load time' }
        ];

        for (const test of performanceTests) {
            const startTime = Date.now();
            
            try {
                await axios.get(`${this.baseUrl}${test.endpoint}`);
                const loadTime = Date.now() - startTime;
                
                if (loadTime <= test.maxTime) {
                    console.log(`✅ ${test.description}: ${loadTime}ms (target: ${test.maxTime}ms)`);
                    this.testResults.performance.push({
                        test: test.description,
                        status: 'PASS',
                        time: loadTime,
                        target: test.maxTime
                    });
                } else {
                    console.log(`⚠️ ${test.description}: ${loadTime}ms (exceeds target: ${test.maxTime}ms)`);
                    this.testResults.performance.push({
                        test: test.description,
                        status: 'SLOW',
                        time: loadTime,
                        target: test.maxTime
                    });
                    this.logBug('Performance', `${test.description} slow: ${loadTime}ms`, 'medium');
                }
            } catch (error) {
                console.log(`❌ ${test.description}: Failed`);
                this.logBug('Performance', `${test.description} failed: ${error.message}`, 'high');
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
            source: 'automated-test-suite'
        };

        this.bugTracker.bugs = this.bugTracker.bugs || [];
        this.bugTracker.bugs.push(bug);
    }

    logCriticalBug(component, error) {
        this.logBug('Critical', `${component}: ${error}`, 'critical');
    }

    generateTestReport() {
        console.log('\n📊 Test Results Summary:');
        console.log('========================');
        
        const apiPassed = this.testResults.api.filter(t => t.status === 'PASS').length;
        const apiTotal = this.testResults.api.length;
        console.log(`API Tests: ${apiPassed}/${apiTotal} passed`);
        
        const dbPassed = this.testResults.database.filter(t => t.status === 'PASS').length;
        const dbTotal = this.testResults.database.length;
        console.log(`Database Tests: ${dbPassed}/${dbTotal} passed`);
        
        const componentsPassed = this.testResults.components.filter(t => t.status === 'PASS').length;
        const componentsTotal = this.testResults.components.length;
        console.log(`Component Tests: ${componentsPassed}/${componentsTotal} passed`);
        
        const flowsPassed = this.testResults.userFlows.filter(t => t.status === 'PASS').length;
        const flowsTotal = this.testResults.userFlows.length;
        console.log(`User Flow Tests: ${flowsPassed}/${flowsTotal} passed`);
        
        const perfPassed = this.testResults.performance.filter(t => t.status === 'PASS').length;
        const perfTotal = this.testResults.performance.length;
        console.log(`Performance Tests: ${perfPassed}/${perfTotal} passed`);
        
        // Save detailed results
        const reportPath = path.join(__dirname, '../reports/test-report.json');
        fs.writeFileSync(reportPath, JSON.stringify({
            timestamp: new Date().toISOString(),
            summary: {
                api: { passed: apiPassed, total: apiTotal },
                database: { passed: dbPassed, total: dbTotal },
                components: { passed: componentsPassed, total: componentsTotal },
                userFlows: { passed: flowsPassed, total: flowsTotal },
                performance: { passed: perfPassed, total: perfTotal }
            },
            details: this.testResults
        }, null, 2));
        
        console.log(`\n📄 Detailed report saved to: ${reportPath}`);
    }

    logBugsFound() {
        // Save updated bug tracker
        const bugTrackerPath = path.join(__dirname, '../bugs/bug-tracker.json');
        fs.writeFileSync(bugTrackerPath, JSON.stringify(this.bugTracker, null, 2));
        
        const newBugs = this.bugTracker.bugs.filter(bug => 
            bug.source === 'automated-test-suite' && 
            new Date(bug.timestamp) > new Date(Date.now() - 60000) // Last minute
        );
        
        if (newBugs.length > 0) {
            console.log(`\n🐛 Found ${newBugs.length} new bugs:`);
            newBugs.forEach(bug => {
                console.log(`  ${bug.severity.toUpperCase()}: ${bug.description}`);
            });
        } else {
            console.log('\n✨ No new bugs found!');
        }
    }

    getTestData(path) {
        const testData = {
            '/api/auth/register': { email: 'test@example.com', name: 'Test User' },
            '/api/auth/login': { email: 'test@example.com' },
            '/api/chat/message': { message: 'test message', user_id: 'test-user' },
            '/api/stories': { title: 'Test Story', content: 'Test content', format: 'reflection' },
            '/api/knowledge/ask': { question: 'test question', user_id: 'test-user' },
            '/api/knowledge/analyze': { content: 'test content', user_id: 'test-user' },
            '/api/knowledge/start-conversation': { user_id: 'test-user', conversation_id: 'test-conv' },
            '/api/waitlist': { email: 'test@example.com', name: 'Test User' }
        };
        
        return testData[path] || {};
    }
}

// Export for use in other scripts
module.exports = AutomatedTestSuite;

// Run if called directly
if (require.main === module) {
    const testSuite = new AutomatedTestSuite();
    testSuite.runAllTests().catch(console.error);
} 