#!/usr/bin/env node

const http = require('http');

class ComprehensiveTestSuite {
    constructor() {
        this.baseUrl = 'http://localhost:8080';
        this.results = [];
        this.testUser = null;
        this.testStoryId = null;
    }

    async makeRequest(method, path, data = null, headers = {}) {
        return new Promise((resolve, reject) => {
            const options = {
                hostname: 'localhost',
                port: 8080,
                path: path,
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    ...headers
                }
            };

            const req = http.request(options, (res) => {
                let body = '';
                res.on('data', (chunk) => body += chunk);
                res.on('end', () => {
                    try {
                        const responseData = body ? JSON.parse(body) : {};
                        resolve({
                            status: res.statusCode,
                            data: responseData,
                            headers: res.headers,
                            rawBody: body
                        });
                    } catch (e) {
                        resolve({
                            status: res.statusCode,
                            data: body,
                            headers: res.headers,
                            rawBody: body
                        });
                    }
                });
            });

            req.on('error', reject);
            
            if (data) {
                req.write(JSON.stringify(data));
            }
            req.end();
        });
    }

    logTest(category, testName, status, details = '') {
        const emoji = status === 'PASS' ? '✅' : status === 'FAIL' ? '❌' : '⚠️';
        console.log(`${emoji} [${category}] ${testName}: ${status}${details ? ' - ' + details : ''}`);
        this.results.push({ category, testName, status, details });
    }

    async testBasicEndpoints() {
        console.log('\n🌐 Testing Basic Endpoints...');
        
        try {
            // Test homepage
            const homeResponse = await this.makeRequest('GET', '/');
            this.logTest('Basic', 'Homepage', homeResponse.status === 200 ? 'PASS' : 'FAIL', `Status: ${homeResponse.status}`);

            // Test app page
            const appResponse = await this.makeRequest('GET', '/app');
            this.logTest('Basic', 'App Page', appResponse.status === 200 ? 'PASS' : 'FAIL', `Status: ${appResponse.status}`);

            // Test chat page
            const chatResponse = await this.makeRequest('GET', '/chat');
            this.logTest('Basic', 'Chat Page', chatResponse.status === 200 ? 'PASS' : 'FAIL', `Status: ${chatResponse.status}`);

            // Test inner-space page
            const spaceResponse = await this.makeRequest('GET', '/inner-space');
            this.logTest('Basic', 'Inner Space Page', spaceResponse.status === 200 ? 'PASS' : 'FAIL', `Status: ${spaceResponse.status}`);

            // Test deck page
            const deckResponse = await this.makeRequest('GET', '/deck');
            this.logTest('Basic', 'Deck Page', deckResponse.status === 200 ? 'PASS' : 'FAIL', `Status: ${deckResponse.status}`);

            // Test story page
            const storyResponse = await this.makeRequest('GET', '/story');
            this.logTest('Basic', 'Story Page', storyResponse.status === 200 ? 'PASS' : 'FAIL', `Status: ${storyResponse.status}`);

        } catch (error) {
            this.logTest('Basic', 'Endpoint Tests', 'FAIL', `Error: ${error.message}`);
        }
    }

    async testAuthenticationSystem() {
        console.log('\n🔐 Testing Authentication System...');
        
        try {
            // Test user registration
            const timestamp = Date.now();
            const testEmail = `test-user-${timestamp}@test.com`;
            
            const registerResponse = await this.makeRequest('POST', '/api/auth/register', {
                email: testEmail,
                name: 'Test User',
                password: 'testpassword123'
            });

            if (registerResponse.status === 201) {
                this.testUser = registerResponse.data;
                this.logTest('Auth', 'User Registration', 'PASS', `User ID: ${this.testUser.user_id}`);
            } else {
                this.logTest('Auth', 'User Registration', 'FAIL', `Status: ${registerResponse.status}, Error: ${JSON.stringify(registerResponse.data)}`);
            }

            // Test invalid registration
            const invalidRegResponse = await this.makeRequest('POST', '/api/auth/register', {
                email: '',
                name: ''
            });
            this.logTest('Auth', 'Invalid Registration', invalidRegResponse.status === 400 ? 'PASS' : 'FAIL', `Status: ${invalidRegResponse.status}`);

        } catch (error) {
            this.logTest('Auth', 'Authentication Tests', 'FAIL', `Error: ${error.message}`);
        }
    }

    async testStoriesAPI() {
        console.log('\n📚 Testing Stories API...');
        
        try {
            // Test get all stories
            const storiesResponse = await this.makeRequest('GET', '/api/stories');
            if (storiesResponse.status === 200 && Array.isArray(storiesResponse.data)) {
                const hasRequiredFields = storiesResponse.data.every(story => 
                    story.hasOwnProperty('id') && story.hasOwnProperty('title')
                );
                this.logTest('Stories', 'Get All Stories', hasRequiredFields ? 'PASS' : 'FAIL', 
                    `Count: ${storiesResponse.data.length}, Fields: ${hasRequiredFields ? 'Complete' : 'Missing'}`);
            } else {
                this.logTest('Stories', 'Get All Stories', 'FAIL', `Status: ${storiesResponse.status}`);
            }

            // Test story creation with valid data and auth
            if (this.testUser) {
                const createStoryResponse = await this.makeRequest('POST', '/api/stories', {
                    title: 'Test Story',
                    content: 'This is a test story content for comprehensive testing.'
                }, {
                    'X-User-ID': this.testUser.user_id
                });

                if (createStoryResponse.status === 201) {
                    this.testStoryId = createStoryResponse.data.story_id || createStoryResponse.data.id;
                    this.logTest('Stories', 'Create Story (Valid)', 'PASS', `Story ID: ${this.testStoryId}`);
                } else {
                    this.logTest('Stories', 'Create Story (Valid)', 'FAIL', `Status: ${createStoryResponse.status}, Error: ${JSON.stringify(createStoryResponse.data)}`);
                }
            }

            // Test story creation with invalid data
            const invalidStoryResponse = await this.makeRequest('POST', '/api/stories', {
                title: '',
                content: ''
            });
            this.logTest('Stories', 'Create Story (Invalid Data)', invalidStoryResponse.status === 400 ? 'PASS' : 'FAIL', 
                `Status: ${invalidStoryResponse.status}`);

            // Test story creation without auth
            const noAuthStoryResponse = await this.makeRequest('POST', '/api/stories', {
                title: 'Test Story',
                content: 'Test content'
            });
            this.logTest('Stories', 'Create Story (No Auth)', noAuthStoryResponse.status === 401 ? 'PASS' : 'FAIL', 
                `Status: ${noAuthStoryResponse.status}`);

        } catch (error) {
            this.logTest('Stories', 'Stories API Tests', 'FAIL', `Error: ${error.message}`);
        }
    }

    async testUserStoriesAPI() {
        console.log('\n👤 Testing User Stories API...');
        
        try {
            if (this.testUser) {
                // Test get user stories (this was the main bug we fixed)
                const userStoriesResponse = await this.makeRequest('GET', `/api/user/stories?user_id=${this.testUser.user_id}`);
                
                if (userStoriesResponse.status === 200) {
                    this.logTest('User Stories', 'Get User Stories', 'PASS', 
                        `Status: 200, Count: ${Array.isArray(userStoriesResponse.data) ? userStoriesResponse.data.length : 'N/A'}`);
                } else {
                    this.logTest('User Stories', 'Get User Stories', 'FAIL', `Status: ${userStoriesResponse.status}`);
                }

                // Test user stories without user_id
                const noUserIdResponse = await this.makeRequest('GET', '/api/user/stories');
                this.logTest('User Stories', 'Get User Stories (No User ID)', noUserIdResponse.status === 400 ? 'PASS' : 'FAIL', 
                    `Status: ${noUserIdResponse.status}`);
            } else {
                this.logTest('User Stories', 'Get User Stories', 'SKIP', 'No test user available');
            }

        } catch (error) {
            this.logTest('User Stories', 'User Stories API Tests', 'FAIL', `Error: ${error.message}`);
        }
    }

    async testChatAPI() {
        console.log('\n💬 Testing Chat API...');
        
        try {
            if (this.testUser) {
                // Test chat message
                const chatResponse = await this.makeRequest('POST', '/api/chat/message', {
                    message: 'This is a test chat message for comprehensive testing.',
                    user_id: this.testUser.user_id
                });

                if (chatResponse.status === 201 || chatResponse.status === 200) {
                    this.logTest('Chat', 'Send Chat Message', 'PASS', `Status: ${chatResponse.status}`);
                } else {
                    this.logTest('Chat', 'Send Chat Message', 'FAIL', `Status: ${chatResponse.status}`);
                }

                // Test chat without message
                const noChatResponse = await this.makeRequest('POST', '/api/chat/message', {
                    user_id: this.testUser.user_id
                });
                this.logTest('Chat', 'Send Empty Message', noChatResponse.status === 400 ? 'PASS' : 'FAIL', 
                    `Status: ${noChatResponse.status}`);
            } else {
                this.logTest('Chat', 'Chat API Tests', 'SKIP', 'No test user available');
            }

        } catch (error) {
            this.logTest('Chat', 'Chat API Tests', 'FAIL', `Error: ${error.message}`);
        }
    }

    async testKnowledgeAPI() {
        console.log('\n🧠 Testing Knowledge API...');
        
        try {
            // Test knowledge ask
            const askResponse = await this.makeRequest('POST', '/api/knowledge/ask', {
                question: 'What can you tell me about my personal growth?',
                user_id: this.testUser?.user_id || 'test-user'
            });

            if (askResponse.status === 200) {
                this.logTest('Knowledge', 'Ask Question', 'PASS', `Status: ${askResponse.status}`);
            } else {
                this.logTest('Knowledge', 'Ask Question', 'FAIL', `Status: ${askResponse.status}`);
            }

            // Test knowledge analyze
            if (this.testUser) {
                const analyzeResponse = await this.makeRequest('POST', '/api/knowledge/analyze', {
                    story_content: 'This is test content for knowledge analysis.',
                    user_id: this.testUser.user_id
                });

                if (analyzeResponse.status === 200) {
                    this.logTest('Knowledge', 'Analyze Content', 'PASS', `Status: ${analyzeResponse.status}`);
                } else {
                    this.logTest('Knowledge', 'Analyze Content', 'FAIL', `Status: ${analyzeResponse.status}`);
                }
            }

        } catch (error) {
            this.logTest('Knowledge', 'Knowledge API Tests', 'FAIL', `Error: ${error.message}`);
        }
    }

    async testInnerSpaceAPI() {
        console.log('\n🌌 Testing Inner Space API...');
        
        try {
            if (this.testUser) {
                const innerSpaceResponse = await this.makeRequest('GET', `/api/inner-space-data?user_id=${this.testUser.user_id}`);
                
                if (innerSpaceResponse.status === 200) {
                    this.logTest('Inner Space', 'Get Inner Space Data', 'PASS', `Status: ${innerSpaceResponse.status}`);
                } else {
                    this.logTest('Inner Space', 'Get Inner Space Data', 'FAIL', `Status: ${innerSpaceResponse.status}`);
                }
            } else {
                this.logTest('Inner Space', 'Inner Space API Tests', 'SKIP', 'No test user available');
            }

        } catch (error) {
            this.logTest('Inner Space', 'Inner Space API Tests', 'FAIL', `Error: ${error.message}`);
        }
    }

    async testErrorHandling() {
        console.log('\n🚫 Testing Error Handling...');
        
        try {
            // Test 404 for non-existent endpoint
            const notFoundResponse = await this.makeRequest('GET', '/api/nonexistent-endpoint');
            this.logTest('Error Handling', '404 Not Found', notFoundResponse.status === 404 ? 'PASS' : 'FAIL', 
                `Status: ${notFoundResponse.status}`);

            // Test 404 for non-existent API endpoint
            const apiNotFoundResponse = await this.makeRequest('GET', '/api/fake/endpoint');
            this.logTest('Error Handling', 'API 404 Not Found', apiNotFoundResponse.status === 404 ? 'PASS' : 'FAIL', 
                `Status: ${apiNotFoundResponse.status}`);

        } catch (error) {
            this.logTest('Error Handling', 'Error Handling Tests', 'FAIL', `Error: ${error.message}`);
        }
    }

    async testPerformance() {
        console.log('\n⚡ Testing Performance...');
        
        try {
            const startTime = Date.now();
            const response = await this.makeRequest('GET', '/api/stories');
            const endTime = Date.now();
            const responseTime = endTime - startTime;
            
            if (response.status === 200) {
                if (responseTime < 1000) {
                    this.logTest('Performance', 'Stories Response Time', 'PASS', `${responseTime}ms (excellent)`);
                } else if (responseTime < 2000) {
                    this.logTest('Performance', 'Stories Response Time', 'PASS', `${responseTime}ms (good)`);
                } else {
                    this.logTest('Performance', 'Stories Response Time', 'SLOW', `${responseTime}ms (needs optimization)`);
                }
            } else {
                this.logTest('Performance', 'Stories Response Time', 'FAIL', `Status: ${response.status}`);
            }

        } catch (error) {
            this.logTest('Performance', 'Performance Tests', 'FAIL', `Error: ${error.message}`);
        }
    }

    async runAllTests() {
        console.log('🧪 COMPREHENSIVE TEST SUITE');
        console.log('============================');
        console.log('Testing all major functionality of the Sentimental app...\n');
        
        await this.testBasicEndpoints();
        await this.testAuthenticationSystem();
        await this.testStoriesAPI();
        await this.testUserStoriesAPI();
        await this.testChatAPI();
        await this.testKnowledgeAPI();
        await this.testInnerSpaceAPI();
        await this.testErrorHandling();
        await this.testPerformance();
        
        this.printSummary();
    }

    printSummary() {
        console.log('\n📊 COMPREHENSIVE TEST RESULTS');
        console.log('===============================');
        
        const categories = {};
        let totalPassed = 0;
        let totalFailed = 0;
        let totalSkipped = 0;
        let totalSlow = 0;
        
        this.results.forEach(result => {
            if (!categories[result.category]) {
                categories[result.category] = { pass: 0, fail: 0, skip: 0, slow: 0 };
            }
            
            if (result.status === 'PASS') {
                categories[result.category].pass++;
                totalPassed++;
            } else if (result.status === 'FAIL') {
                categories[result.category].fail++;
                totalFailed++;
            } else if (result.status === 'SKIP') {
                categories[result.category].skip++;
                totalSkipped++;
            } else if (result.status === 'SLOW') {
                categories[result.category].slow++;
                totalSlow++;
            }
        });
        
        // Print category breakdown
        Object.keys(categories).forEach(category => {
            const cat = categories[category];
            const total = cat.pass + cat.fail + cat.skip + cat.slow;
            console.log(`\n📂 ${category}:`);
            console.log(`   ✅ Passed: ${cat.pass}/${total}`);
            if (cat.fail > 0) console.log(`   ❌ Failed: ${cat.fail}/${total}`);
            if (cat.skip > 0) console.log(`   ⏭️  Skipped: ${cat.skip}/${total}`);
            if (cat.slow > 0) console.log(`   ⚠️  Slow: ${cat.slow}/${total}`);
        });
        
        // Print overall summary
        const totalTests = this.results.length;
        const successRate = Math.round(((totalPassed + totalSlow) / totalTests) * 100);
        
        console.log('\n🎯 OVERALL RESULTS:');
        console.log(`   Total Tests: ${totalTests}`);
        console.log(`   ✅ Passed: ${totalPassed}`);
        console.log(`   ⚠️  Slow: ${totalSlow}`);
        console.log(`   ❌ Failed: ${totalFailed}`);
        console.log(`   ⏭️  Skipped: ${totalSkipped}`);
        console.log(`   📈 Success Rate: ${successRate}%`);
        
        // Final assessment
        if (totalFailed === 0 && totalSlow <= 1) {
            console.log('\n🎉 EXCELLENT! All systems are functioning perfectly!');
        } else if (totalFailed <= 2) {
            console.log('\n✅ GOOD! System is mostly stable with minor issues.');
        } else if (totalFailed <= 5) {
            console.log('\n⚠️  FAIR! Some issues need attention but core functionality works.');
        } else {
            console.log('\n❌ NEEDS WORK! Multiple critical issues detected.');
        }
        
        if (this.testUser) {
            console.log(`\n👤 Test User Created: ${this.testUser.user_id}`);
        }
        if (this.testStoryId) {
            console.log(`📖 Test Story Created: ${this.testStoryId}`);
        }
    }
}

// Run the comprehensive test suite
const testSuite = new ComprehensiveTestSuite();
testSuite.runAllTests().catch(console.error); 