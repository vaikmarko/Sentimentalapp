const fs = require('fs');
const path = require('path');

class JavaScriptErrorFixer {
    constructor() {
        this.fixes = [];
    }

    async fixAllJavaScriptErrors() {
        console.log('🔧 Fixing JavaScript Errors in Test Files...');
        console.log('==============================================');

        // Fix 1: Fix API tests - missing results array initialization
        await this.fixApiTestsErrors();
        
        // Fix 2: Fix automated test suite - missing getTestData method
        await this.fixAutomatedTestSuiteErrors();
        
        // Fix 3: Fix user flow tests - missing results array
        await this.fixUserFlowTestsErrors();

        this.generateReport();
    }

    async fixApiTestsErrors() {
        console.log('\n📝 Fixing API Tests JavaScript Errors...');
        
        const filePath = 'tests/api-tests.js';
        if (!fs.existsSync(filePath)) return;
        
        let content = fs.readFileSync(filePath, 'utf8');
        
        // Fix missing results array initialization in constructor
        if (!content.includes('this.results = []')) {
            content = content.replace(
                /constructor\(baseUrl = 'http:\/\/localhost:8080'\) \{[\s\S]*?\}/,
                `constructor(baseUrl = 'http://localhost:8080') {
        this.baseUrl = baseUrl;
        this.results = [];
    }`
            );
        }
        
        // Fix the chat test method to properly handle results
        const fixedChatTest = `
    async testChatEndpoints() {
        console.log('\\n💬 Testing Chat Endpoints...');
        
        // First register a user for chat testing
        const uniqueEmail = \`chat-test-\${Date.now()}-\${Math.random().toString(36).substr(2, 9)}@example.com\`;
        let testUserId = 'chat-test-user';
        
        try {
            const registerResponse = await axios.post(\`\${this.baseUrl}/api/auth/register\`, {
                email: uniqueEmail,
                password: 'testpassword123',
                name: 'Chat Test User'
            });
            
            if (registerResponse.status === 201 && registerResponse.data.user_id) {
                testUserId = registerResponse.data.user_id;
                console.log(\`✅ Registered chat test user: \${testUserId}\`);
                
                // Wait for user to be available in database
                await new Promise(resolve => setTimeout(resolve, 2000));
                
                // Test chat message with registered user
                const chatResponse = await axios.post(\`\${this.baseUrl}/api/chat/message\`, {
                    message: 'Hello, this is a test message from the API test suite.',
                    user_id: testUserId
                }, { 
                    timeout: 10000,
                    validateStatus: (status) => status < 500
                });
                
                if (chatResponse.status === 200 || chatResponse.status === 201) {
                    console.log('✅ Chat message endpoint working');
                    if (this.results) {
                        this.results.push({ endpoint: 'POST /api/chat/message', status: 'PASS', response: chatResponse.status });
                    }
                } else {
                    console.log(\`❌ Chat message failed: \${chatResponse.status}\`);
                    if (this.results) {
                        this.results.push({ endpoint: 'POST /api/chat/message', status: 'FAIL', response: chatResponse.status, error: chatResponse.data });
                    }
                }
            } else {
                console.log('❌ Failed to register chat test user');
                if (this.results) {
                    this.results.push({ endpoint: 'POST /api/chat/message', status: 'FAIL', error: 'User registration failed' });
                }
            }
        } catch (error) {
            console.log(\`❌ Chat endpoint test failed: \${error.message}\`);
            if (this.results) {
                this.results.push({ endpoint: 'POST /api/chat/message', status: 'FAIL', error: error.message });
            }
        }
    }`;
        
        content = content.replace(
            /async testChatEndpoints\(\) \{[\s\S]*?\n    \}/,
            fixedChatTest.trim()
        );
        
        fs.writeFileSync(filePath, content);
        console.log('✅ Fixed API tests JavaScript errors');
        this.fixes.push('API tests - Fixed missing results array and error handling');
    }

    async fixAutomatedTestSuiteErrors() {
        console.log('\n🤖 Fixing Automated Test Suite JavaScript Errors...');
        
        const filePath = 'tests/automated-test-suite.js';
        if (!fs.existsSync(filePath)) return;
        
        let content = fs.readFileSync(filePath, 'utf8');
        
        // Add missing getTestData method
        const getTestDataMethod = `
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
    }`;
        
        // Add the method before the last closing brace of the class
        if (!content.includes('getTestData(path)')) {
            content = content.replace(
                /(\n\s*}\s*$)/,
                `\n${getTestDataMethod}\n$1`
            );
        }
        
        // Fix endpoint definitions to include proper expectedStatus arrays
        const endpointFixes = [
            { 
                search: /{ path: '\/api\/stories', method: 'GET', expectedStatus: \[200\]/,
                replace: "{ path: '/api/stories', method: 'GET', expectedStatus: [200], maxResponseTime: 1000 }"
            },
            {
                search: /{ path: '\/api\/stories', method: 'POST', expectedStatus: \[201, 401\]/,
                replace: "{ path: '/api/stories', method: 'POST', expectedStatus: [201, 401], maxResponseTime: 1000 }"
            },
            {
                search: /{ path: '\/api\/user\/stories', method: 'GET', expectedStatus: \[200, 401\]/,
                replace: "{ path: '/api/user/stories', method: 'GET', expectedStatus: [200, 401], maxResponseTime: 1000 }"
            },
            {
                search: /{ path: '\/api\/chat\/message', method: 'POST', expectedStatus: \[200, 201, 401\]/,
                replace: "{ path: '/api/chat/message', method: 'POST', expectedStatus: [200, 201, 401], maxResponseTime: 1000 }"
            }
        ];
        
        endpointFixes.forEach(fix => {
            content = content.replace(fix.search, fix.replace);
        });
        
        fs.writeFileSync(filePath, content);
        console.log('✅ Fixed automated test suite JavaScript errors');
        this.fixes.push('Automated test suite - Added missing getTestData method and fixed endpoint definitions');
    }

    async fixUserFlowTestsErrors() {
        console.log('\n👤 Fixing User Flow Tests JavaScript Errors...');
        
        const filePath = 'tests/user-flow-tests.js';
        if (!fs.existsSync(filePath)) return;
        
        let content = fs.readFileSync(filePath, 'utf8');
        
        // Fix missing results array initialization in constructor
        if (!content.includes('this.results = []')) {
            content = content.replace(
                /constructor\(baseUrl = 'http:\/\/localhost:8080'\) \{[\s\S]*?\}/,
                `constructor(baseUrl = 'http://localhost:8080') {
        this.baseUrl = baseUrl;
        this.results = [];
    }`
            );
        }
        
        // Fix the share flow test method to properly handle results
        const fixedShareFlowTest = `
    async testShareToStoryFlow() {
        console.log('\\n📤 Testing Share to Story Flow...');
        
        try {
            // Step 1: Register a user
            const userEmail = \`share-flow-\${Date.now()}-\${Math.random().toString(36).substr(2, 9)}@test.com\`;
            const registerResponse = await axios.post(\`\${this.baseUrl}/api/auth/register\`, {
                email: userEmail,
                name: 'Share Flow Test User'
            });

            if (registerResponse.status !== 201) {
                throw new Error('User registration failed');
            }

            const userId = registerResponse.data.user_id;
            
            // Wait for user to be available in database
            await new Promise(resolve => setTimeout(resolve, 2000));

            // Step 2: Send a chat message (this creates a story automatically)
            const chatResponse = await axios.post(\`\${this.baseUrl}/api/chat/message\`, {
                message: 'Today I had an amazing breakthrough at work. I finally understood a complex problem that had been bothering me for weeks.',
                user_id: userId
            });

            if (chatResponse.status !== 200 && chatResponse.status !== 201) {
                throw new Error(\`Chat message failed: \${chatResponse.status}\`);
            }

            // Step 3: Verify story was created by checking user stories
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            const storiesResponse = await axios.get(\`\${this.baseUrl}/api/user/stories?user_id=\${userId}\`);
            
            if (storiesResponse.status === 200 && storiesResponse.data.length > 0) {
                console.log('✅ Share to Story flow working');
                if (this.results) {
                    this.results.push({ flow: 'Share to Story', status: 'PASS', details: 'Story created from chat message' });
                }
            } else {
                throw new Error('Story not found after chat message');
            }
            
        } catch (error) {
            console.log(\`❌ Share to Story flow failed: \${error.message}\`);
            if (this.results) {
                this.results.push({ flow: 'Share to Story', status: 'FAIL', error: error.message });
            }
        }
    }`;
        
        content = content.replace(
            /async testShareToStoryFlow\(\) \{[\s\S]*?\n    \}/,
            fixedShareFlowTest.trim()
        );
        
        fs.writeFileSync(filePath, content);
        console.log('✅ Fixed user flow tests JavaScript errors');
        this.fixes.push('User flow tests - Fixed missing results array and error handling');
    }

    generateReport() {
        console.log('\n📊 JavaScript Error Fix Summary:');
        console.log('==================================');
        
        this.fixes.forEach((fix, index) => {
            console.log(`${index + 1}. ✅ ${fix}`);
        });
        
        console.log(`\n🎯 Total JavaScript errors fixed: ${this.fixes.length}`);
        console.log('\n🚀 All JavaScript errors should now be resolved!');
        console.log('   Run the test suite again to verify fixes.');
    }
}

// Run the JavaScript error fixer
const fixer = new JavaScriptErrorFixer();
fixer.fixAllJavaScriptErrors().catch(console.error); 