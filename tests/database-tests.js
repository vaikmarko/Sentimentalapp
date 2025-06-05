const axios = require('axios');
const fs = require('fs');
const path = require('path');

class DatabaseTestSuite {
    constructor(baseUrl = 'http://localhost:8080') {
        this.baseUrl = baseUrl;
        this.testResults = [];
        this.bugTracker = require('../bugs/bug-tracker.json');
        this.testUser = null; // Store test user for authentication
    }

    async runAllDatabaseTests() {
        console.log('🗄️ Starting Database Test Suite...\n');
        
        try {
            // First register a test user for authenticated operations
            await this.setupTestUser();
            
            await this.testDatabaseConnectivity();
            await this.testCRUDOperations();
            await this.testDataRelationships();
            await this.testDataIntegrity();
            await this.testQueryPerformance();
            
            this.generateDatabaseReport();
            
        } catch (error) {
            console.error('❌ Database test suite failed:', error);
            this.logCriticalBug('Database Test Suite Failure', error.message);
        }
    }

    async setupTestUser() {
        try {
            const timestamp = Date.now();
            const testEmail = `dbtest-${timestamp}@test.com`;
            
            const response = await axios.post(`${this.baseUrl}/api/auth/register`, {
                email: testEmail,
                name: 'Database Test User',
                password: 'testpassword123'
            });
            
            if (response.status === 201) {
                this.testUser = response.data;
                console.log(`✅ Test user registered: ${this.testUser.user_id}`);
            }
        } catch (error) {
            console.log('⚠️ Could not register test user, some tests may fail');
        }
    }

    async testDatabaseConnectivity() {
        console.log('🔌 Testing Database Connectivity...');
        
        try {
            const response = await axios.get(`${this.baseUrl}/api/stories`);
            
            if (response.status === 200) {
                console.log('✅ Database connection successful');
                this.testResults.push({
                    category: 'Connectivity',
                    test: 'Basic Connection',
                    status: 'PASS',
                    details: 'Successfully connected to database'
                });
            } else {
                throw new Error(`Unexpected status code: ${response.status}`);
            }
        } catch (error) {
            console.log('❌ Database connection failed');
            this.testResults.push({
                category: 'Connectivity',
                test: 'Basic Connection',
                status: 'FAIL',
                error: error.message
            });
            this.logCriticalBug('Database Connectivity', error.message);
        }
    }

    async testCRUDOperations() {
        console.log('\n📝 Testing CRUD Operations...');
        
        // Test CREATE operations
        await this.testCreateOperations();
        
        // Test READ operations
        await this.testReadOperations();
        
        // Test UPDATE operations
        await this.testUpdateOperations();
        
        // Test DELETE operations (if implemented)
        await this.testDeleteOperations();
    }

    async testCreateOperations() {
        console.log('Testing CREATE operations...');
        
        const createTests = [
            {
                name: 'Create Story',
                endpoint: '/api/stories',
                data: {
                    title: 'Test Database Story',
                    content: 'This is a test story for database validation.'
                },
                headers: this.testUser ? { 'X-User-ID': this.testUser.user_id } : {}
            },
            {
                name: 'Create Chat Message',
                endpoint: '/api/chat/message',
                data: {
                    message: 'Test database message',
                    user_id: this.testUser ? this.testUser.user_id : 'db-test-user'
                }
            },
            {
                name: 'Register User',
                endpoint: '/api/auth/register',
                data: {
                    email: `dbtest-duplicate-${Date.now()}@example.com`,
                    password: 'testpassword123',
                    name: 'Database Test User 2'
                }
            }
        ];

        for (const test of createTests) {
            try {
                const config = {
                    headers: {
                        'Content-Type': 'application/json',
                        ...(test.headers || {})
                    }
                };
                
                const response = await axios.post(`${this.baseUrl}${test.endpoint}`, test.data, config);
                
                if (response.status >= 200 && response.status < 300) {
                    console.log(`✅ ${test.name} - CREATE successful`);
                    this.testResults.push({
                        category: 'CRUD',
                        test: `CREATE - ${test.name}`,
                        status: 'PASS',
                        details: `Status: ${response.status}`
                    });
                } else {
                    console.log(`❌ ${test.name} - CREATE failed with status ${response.status}`);
                    this.testResults.push({
                        category: 'CRUD',
                        test: `CREATE - ${test.name}`,
                        status: 'FAIL',
                        error: `HTTP ${response.status}`
                    });
                    this.logBug('Database', `CREATE ${test.name} failed: HTTP ${response.status}`, 'high');
                }
            } catch (error) {
                console.log(`💥 ${test.name} - CREATE critical failure`);
                this.testResults.push({
                    category: 'CRUD',
                    test: `CREATE - ${test.name}`,
                    status: 'FAIL',
                    error: error.message
                });
                this.logCriticalBug(`Database CREATE ${test.name}`, error.message);
            }
        }
    }

    async testReadOperations() {
        console.log('Testing READ operations...');
        
        const readTests = [
            {
                name: 'Read All Stories',
                endpoint: '/api/stories'
            },
            {
                name: 'Read User Stories',
                endpoint: `/api/user/stories?user_id=${this.testUser ? this.testUser.user_id : 'db-test-user'}`
            },
            {
                name: 'Read Inner Space Data',
                endpoint: `/api/inner-space-data?user_id=${this.testUser ? this.testUser.user_id : 'db-test-user'}`
            }
        ];

        for (const test of readTests) {
            try {
                const response = await axios.get(`${this.baseUrl}${test.endpoint}`);
                
                if (response.status === 200 && response.data !== undefined) {
                    console.log(`✅ ${test.name} - READ successful`);
                    this.testResults.push({
                        category: 'CRUD',
                        test: `READ - ${test.name}`,
                        status: 'PASS',
                        details: `Returned ${Array.isArray(response.data) ? response.data.length : 'object'} items`
                    });
                } else {
                    console.log(`❌ ${test.name} - READ failed`);
                    this.testResults.push({
                        category: 'CRUD',
                        test: `READ - ${test.name}`,
                        status: 'FAIL',
                        error: `Invalid response: ${response.status}`
                    });
                    this.logBug('Database', `READ ${test.name} failed`, 'medium');
                }
            } catch (error) {
                console.log(`💥 ${test.name} - READ critical failure`);
                this.testResults.push({
                    category: 'CRUD',
                    test: `READ - ${test.name}`,
                    status: 'FAIL',
                    error: error.message
                });
                this.logBug('Database', `READ ${test.name} failed: ${error.message}`, 'high');
            }
        }
    }

    async testUpdateOperations() {
        console.log('Testing UPDATE operations...');
        
        // Test story visibility update
        try {
            // First create a story to update
            let storyId = null;
            if (this.testUser) {
                const createResponse = await axios.post(`${this.baseUrl}/api/stories`, {
                    title: 'Test Story for Update',
                    content: 'This story will be updated'
                }, {
                    headers: {
                        'Content-Type': 'application/json',
                        'X-User-ID': this.testUser.user_id
                    }
                });
                
                if (createResponse.status === 201) {
                    storyId = createResponse.data.story_id || createResponse.data.id;
                }
            }
            
            if (!storyId) {
                throw new Error('No story available to update');
            }
            
            const response = await axios.put(`${this.baseUrl}/api/stories/${storyId}/visibility`, {
                public: true,
                user_id: this.testUser ? this.testUser.user_id : 'test-user'
            }, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.status >= 200 && response.status < 300) {
                console.log('✅ Story Visibility Update - UPDATE successful');
                this.testResults.push({
                    category: 'CRUD',
                    test: 'UPDATE - Story Visibility',
                    status: 'PASS',
                    details: `Status: ${response.status}`
                });
            } else {
                console.log('❌ Story Visibility Update - UPDATE failed');
                this.testResults.push({
                    category: 'CRUD',
                    test: 'UPDATE - Story Visibility',
                    status: 'FAIL',
                    error: `HTTP ${response.status}`
                });
                this.logBug('Database', 'UPDATE Story Visibility failed', 'medium');
            }
        } catch (error) {
            console.log('💥 Story Visibility Update - UPDATE critical failure');
            this.testResults.push({
                category: 'CRUD',
                test: 'UPDATE - Story Visibility',
                status: 'FAIL',
                error: error.message
            });
            this.logBug('Database', `UPDATE Story Visibility failed: ${error.message}`, 'high');
        }
    }

    async testDeleteOperations() {
        console.log('Testing DELETE operations...');
        
        // Note: DELETE operations might not be implemented yet
        // This is a placeholder for when they are added
        
        console.log('ℹ️ DELETE operations not yet implemented - skipping');
        this.testResults.push({
            category: 'CRUD',
            test: 'DELETE Operations',
            status: 'SKIP',
            details: 'DELETE operations not yet implemented'
        });
    }

    async testDataRelationships() {
        console.log('\n🔗 Testing Data Relationships...');
        
        // Test conversation to story relationship
        await this.testConversationToStoryRelationship();
        
        // Test story to insights relationship
        await this.testStoryToInsightsRelationship();
        
        // Test user to data relationship
        await this.testUserToDataRelationship();
    }

    async testConversationToStoryRelationship() {
        console.log('Testing Conversation → Story relationship...');
        
        try {
            // First register a user
            const userEmail = `relationship-test-${Date.now()}-${Math.random().toString(36).substr(2, 9)}@test.com`;
            const registerResponse = await axios.post(`${this.baseUrl}/api/auth/register`, {
                email: userEmail,
                name: 'Relationship Test User'
            });

            if (registerResponse.status !== 201) {
                throw new Error('User registration failed');
            }

            const userId = registerResponse.data.user_id;
            
            // Wait for user to be available in database
            await new Promise(resolve => setTimeout(resolve, 2000));

            // Send a chat message
            const chatResponse = await axios.post(`${this.baseUrl}/api/chat/message`, {
                message: 'This is a test message to check conversation to story relationship.',
                user_id: userId
            });

            if (chatResponse.status === 200 || chatResponse.status === 201) {
                console.log('✅ Chat message sent successfully');
                
                // Check if story was created
                const storiesResponse = await axios.get(`${this.baseUrl}/api/user/stories?user_id=${userId}`);
                
                if (storiesResponse.status === 200 && storiesResponse.data.length > 0) {
                    console.log('✅ Conversation → Story relationship working');
                    this.testResults.push({
                        category: 'Relationships',
                        test: 'Conversation → Story',
                        status: 'PASS',
                        details: 'Story created from conversation'
                    });
                } else {
                    console.log('❌ Conversation → Story relationship broken');
                    this.testResults.push({
                        category: 'Relationships',
                        test: 'Conversation → Story',
                        status: 'FAIL',
                        error: 'Story not created from conversation'
                    });
                    this.logBug('Database', 'Conversation to Story relationship broken', 'high');
                }
            }
        } catch (error) {
            console.log('💥 Conversation → Story relationship test failed');
            this.testResults.push({
                category: 'Relationships',
                test: 'Conversation → Story',
                status: 'FAIL',
                error: error.message
            });
            this.logCriticalBug('Database Relationship', error.message);
        }
    }

    async testStoryToInsightsRelationship() {
        console.log('Testing Story → Insights relationship...');
        
        try {
            // First register a user
            const userEmail = `insights-test-${Date.now()}-${Math.random().toString(36).substr(2, 9)}@test.com`;
            const registerResponse = await axios.post(`${this.baseUrl}/api/auth/register`, {
                email: userEmail,
                name: 'Insights Test User'
            });

            if (registerResponse.status !== 201) {
                throw new Error('User registration failed');
            }

            const userId = registerResponse.data.user_id;
            
            // Wait for user to be available in database
            await new Promise(resolve => setTimeout(resolve, 2000));

            const response = await axios.post(`${this.baseUrl}/api/knowledge/analyze`, {
                story_content: 'Today I felt really accomplished after completing a challenging project.',
                user_id: userId
            });

            if (response.status === 200 && (response.data.domains || response.data.priority_gaps)) {
                console.log('✅ Story → Insights relationship working');
                this.testResults.push({
                    category: 'Relationships',
                    test: 'Story → Insights',
                    status: 'PASS',
                    details: 'Insights generated from story content'
                });
            } else {
                console.log('❌ Story → Insights relationship broken');
                this.testResults.push({
                    category: 'Relationships',
                    test: 'Story → Insights',
                    status: 'FAIL',
                    error: 'Insights not generated from story'
                });
                this.logBug('Database', 'Story to Insights relationship broken', 'medium');
            }
        } catch (error) {
            console.log('💥 Story → Insights relationship test failed');
            this.testResults.push({
                category: 'Relationships',
                test: 'Story → Insights',
                status: 'FAIL',
                error: error.message
            });
            this.logBug('Database', `Story to Insights relationship failed: ${error.message}`, 'high');
        }
    }

    async testUserToDataRelationship() {
        console.log('Testing User → Data relationship...');
        
        try {
            // First register a user
            const userEmail = `data-test-${Date.now()}-${Math.random().toString(36).substr(2, 9)}@test.com`;
            const registerResponse = await axios.post(`${this.baseUrl}/api/auth/register`, {
                email: userEmail,
                name: 'Data Test User'
            });

            if (registerResponse.status !== 201) {
                throw new Error('User registration failed');
            }

            const userId = registerResponse.data.user_id;
            
            // Wait for user to be available in database
            await new Promise(resolve => setTimeout(resolve, 2000));

            const response = await axios.get(`${this.baseUrl}/api/inner-space-data?user_id=${userId}`);
            
            if (response.status === 200) {
                console.log('✅ User → Data relationship working');
                this.testResults.push({
                    category: 'Relationships',
                    test: 'User → Data',
                    status: 'PASS',
                    details: 'User data retrieved successfully'
                });
            } else {
                console.log('❌ User → Data relationship broken');
                this.testResults.push({
                    category: 'Relationships',
                    test: 'User → Data',
                    status: 'FAIL',
                    error: 'User data not accessible'
                });
                this.logBug('Database', 'User to Data relationship broken', 'medium');
            }
        } catch (error) {
            console.log('💥 User → Data relationship test failed');
            this.testResults.push({
                category: 'Relationships',
                test: 'User → Data',
                status: 'FAIL',
                error: error.message
            });
            this.logBug('Database', `User to Data relationship failed: ${error.message}`, 'high');
        }
    }

    async testDataIntegrity() {
        console.log('\n🔒 Testing Data Integrity...');
        
        // Test data validation
        await this.testDataValidation();
        
        // Test data consistency
        await this.testDataConsistency();
    }

    async testDataValidation() {
        console.log('Testing data validation...');
        
        // Test invalid data rejection
        const invalidTests = [
            {
                name: 'Empty Story Content',
                endpoint: '/api/stories',
                data: {
                    title: '',
                    content: '',
                    user_id: 'validation-test-user'
                }
            },
            {
                name: 'Invalid User Registration',
                endpoint: '/api/auth/register',
                data: {
                    email: 'invalid-email',
                    password: '123', // Too short
                    name: ''
                }
            }
        ];

        for (const test of invalidTests) {
            try {
                const response = await axios.post(`${this.baseUrl}${test.endpoint}`, test.data);
                
                // We expect these to fail (4xx status codes)
                if (response.status >= 400 && response.status < 500) {
                    console.log(`✅ ${test.name} - Validation correctly rejected invalid data`);
                    this.testResults.push({
                        category: 'Data Integrity',
                        test: `Validation - ${test.name}`,
                        status: 'PASS',
                        details: 'Invalid data correctly rejected'
                    });
                } else {
                    console.log(`❌ ${test.name} - Validation failed to reject invalid data`);
                    this.testResults.push({
                        category: 'Data Integrity',
                        test: `Validation - ${test.name}`,
                        status: 'FAIL',
                        error: 'Invalid data was accepted'
                    });
                    this.logBug('Database', `Data validation failed for ${test.name}`, 'medium');
                }
            } catch (error) {
                // Axios throws on 4xx/5xx, which is expected for validation tests
                if (error.response && error.response.status >= 400 && error.response.status < 500) {
                    console.log(`✅ ${test.name} - Validation correctly rejected invalid data`);
                    this.testResults.push({
                        category: 'Data Integrity',
                        test: `Validation - ${test.name}`,
                        status: 'PASS',
                        details: 'Invalid data correctly rejected'
                    });
                } else {
                    console.log(`💥 ${test.name} - Validation test failed unexpectedly`);
                    this.testResults.push({
                        category: 'Data Integrity',
                        test: `Validation - ${test.name}`,
                        status: 'FAIL',
                        error: error.message
                    });
                    this.logBug('Database', `Data validation test failed: ${error.message}`, 'high');
                }
            }
        }
    }

    async testDataConsistency() {
        console.log('Testing data consistency...');
        
        try {
            // Get stories and check consistency
            const storiesResponse = await axios.get(`${this.baseUrl}/api/stories`);
            
            if (storiesResponse.status === 200 && Array.isArray(storiesResponse.data)) {
                const stories = storiesResponse.data;
                let consistencyIssues = 0;
                
                stories.forEach(story => {
                    // Check required fields
                    if (!story.id || !story.title || !story.content) {
                        consistencyIssues++;
                    }
                    
                    // Check data types
                    if (typeof story.title !== 'string' || typeof story.content !== 'string') {
                        consistencyIssues++;
                    }
                });
                
                if (consistencyIssues === 0) {
                    console.log('✅ Data consistency check passed');
                    this.testResults.push({
                        category: 'Data Integrity',
                        test: 'Data Consistency',
                        status: 'PASS',
                        details: `Checked ${stories.length} stories`
                    });
                } else {
                    console.log(`❌ Data consistency issues found: ${consistencyIssues}`);
                    this.testResults.push({
                        category: 'Data Integrity',
                        test: 'Data Consistency',
                        status: 'FAIL',
                        error: `${consistencyIssues} consistency issues found`
                    });
                    this.logBug('Database', `Data consistency issues: ${consistencyIssues} problems found`, 'medium');
                }
            }
        } catch (error) {
            console.log('💥 Data consistency test failed');
            this.testResults.push({
                category: 'Data Integrity',
                test: 'Data Consistency',
                status: 'FAIL',
                error: error.message
            });
            this.logBug('Database', `Data consistency test failed: ${error.message}`, 'high');
        }
    }

    async testQueryPerformance() {
        console.log('\n⚡ Testing Query Performance...');
        
        const performanceTests = [
            { endpoint: '/api/stories', maxTime: 500, description: 'Stories query' },
            { endpoint: '/api/inner-space-data?user_id=perf-test-user', maxTime: 1000, description: 'Inner space data query' }
        ];

        for (const test of performanceTests) {
            const startTime = Date.now();
            
            try {
                await axios.get(`${this.baseUrl}${test.endpoint}`);
                const queryTime = Date.now() - startTime;
                
                if (queryTime <= test.maxTime) {
                    console.log(`✅ ${test.description}: ${queryTime}ms (target: ${test.maxTime}ms)`);
                    this.testResults.push({
                        category: 'Performance',
                        test: test.description,
                        status: 'PASS',
                        details: `${queryTime}ms (target: ${test.maxTime}ms)`
                    });
                } else {
                    console.log(`⚠️ ${test.description}: ${queryTime}ms (exceeds target: ${test.maxTime}ms)`);
                    this.testResults.push({
                        category: 'Performance',
                        test: test.description,
                        status: 'SLOW',
                        details: `${queryTime}ms (target: ${test.maxTime}ms)`
                    });
                    this.logBug('Performance', `${test.description} slow: ${queryTime}ms`, 'medium');
                }
            } catch (error) {
                console.log(`❌ ${test.description}: Failed`);
                this.testResults.push({
                    category: 'Performance',
                    test: test.description,
                    status: 'FAIL',
                    error: error.message
                });
                this.logBug('Database', `Query performance test failed: ${error.message}`, 'high');
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
            source: 'database-tests'
        };

        this.bugTracker.bugs = this.bugTracker.bugs || [];
        this.bugTracker.bugs.push(bug);
    }

    logCriticalBug(component, error) {
        this.logBug('Critical', `${component}: ${error}`, 'critical');
    }

    generateDatabaseReport() {
        console.log('\n📊 Database Test Results Summary:');
        console.log('==================================');
        
        const categories = ['Connectivity', 'CRUD', 'Relationships', 'Data Integrity', 'Performance'];
        
        categories.forEach(category => {
            const categoryTests = this.testResults.filter(t => t.category === category);
            const passed = categoryTests.filter(t => t.status === 'PASS').length;
            const total = categoryTests.length;
            
            if (total > 0) {
                console.log(`${category}: ${passed}/${total} passed`);
            }
        });
        
        // Save detailed results
        const reportPath = path.join(__dirname, '../reports/database-test-report.json');
        fs.writeFileSync(reportPath, JSON.stringify({
            timestamp: new Date().toISOString(),
            summary: this.testResults.reduce((acc, test) => {
                acc[test.category] = acc[test.category] || { passed: 0, total: 0 };
                acc[test.category].total++;
                if (test.status === 'PASS') acc[test.category].passed++;
                return acc;
            }, {}),
            details: this.testResults
        }, null, 2));
        
        console.log(`\n📄 Detailed database report saved to: ${reportPath}`);
        
        // Save updated bug tracker
        const bugTrackerPath = path.join(__dirname, '../bugs/bug-tracker.json');
        fs.writeFileSync(bugTrackerPath, JSON.stringify(this.bugTracker, null, 2));
    }
}

// Export for use in other scripts
module.exports = DatabaseTestSuite;

// Run if called directly
if (require.main === module) {
    const testSuite = new DatabaseTestSuite();
    testSuite.runAllDatabaseTests().catch(console.error);
} 