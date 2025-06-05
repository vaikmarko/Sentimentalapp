const fs = require('fs');
const path = require('path');
const axios = require('axios');

class ComprehensiveBugFixer {
    constructor(baseUrl = 'http://localhost:8080') {
        this.baseUrl = baseUrl;
        this.fixes = [];
        this.results = [];
    }

    async fixAllBugs() {
        console.log('🔧 Starting Comprehensive Bug Fix Process...');
        console.log('==============================================');

        // Fix 1: Verify server is running
        await this.verifyServerStatus();
        
        // Fix 2: Test all endpoints to verify they're working
        await this.testCriticalEndpoints();
        
        // Fix 3: Fix any remaining test file issues
        await this.fixRemainingTestIssues();
        
        // Fix 4: Verify Firebase index is working
        await this.verifyFirebaseIndex();
        
        // Fix 5: Test authentication flows
        await this.testAuthenticationFlows();

        this.generateFixReport();
    }

    async verifyServerStatus() {
        console.log('\n🔍 Verifying Server Status...');
        
        try {
            const response = await axios.get(`${this.baseUrl}/api/stories`, { timeout: 5000 });
            if (response.status === 200) {
                console.log('✅ Server is running and accessible');
                this.fixes.push({ category: 'Server', issue: 'Server accessibility', status: 'OK' });
                return true;
            }
        } catch (error) {
            console.log('❌ Server is not accessible');
            this.fixes.push({ 
                category: 'Server', 
                issue: 'Server not accessible', 
                status: 'CRITICAL', 
                error: error.message,
                solution: 'Start Flask server with: ENVIRONMENT=test python app.py'
            });
            return false;
        }
    }

    async testCriticalEndpoints() {
        console.log('\n🔌 Testing Critical Endpoints...');
        
        const endpoints = [
            { method: 'GET', path: '/api/stories', name: 'Get Stories' },
            { method: 'POST', path: '/api/auth/register', name: 'User Registration' },
            { method: 'POST', path: '/api/auth/login', name: 'User Login' },
            { method: 'POST', path: '/api/chat/message', name: 'Chat Message' },
            { method: 'GET', path: '/api/inner-space-data', name: 'Inner Space Data' },
            { method: 'POST', path: '/api/knowledge/ask', name: 'Knowledge Ask' }
        ];

        for (const endpoint of endpoints) {
            try {
                let response;
                const config = { 
                    timeout: 5000,
                    validateStatus: (status) => status < 500
                };

                if (endpoint.method === 'GET') {
                    response = await axios.get(`${this.baseUrl}${endpoint.path}`, config);
                } else if (endpoint.method === 'POST') {
                    const testData = this.getTestData(endpoint.path);
                    response = await axios.post(`${this.baseUrl}${endpoint.path}`, testData, config);
                }

                if (response.status < 400) {
                    console.log(`✅ ${endpoint.name} - Working (${response.status})`);
                    this.fixes.push({ 
                        category: 'Endpoints', 
                        issue: `${endpoint.name}`, 
                        status: 'OK',
                        details: `Status: ${response.status}`
                    });
                } else {
                    console.log(`⚠️ ${endpoint.name} - Client error (${response.status})`);
                    this.fixes.push({ 
                        category: 'Endpoints', 
                        issue: `${endpoint.name}`, 
                        status: 'WARNING',
                        details: `Status: ${response.status} - May need authentication`
                    });
                }
            } catch (error) {
                console.log(`❌ ${endpoint.name} - Failed: ${error.message}`);
                this.fixes.push({ 
                    category: 'Endpoints', 
                    issue: `${endpoint.name}`, 
                    status: 'ERROR',
                    error: error.message
                });
            }
        }
    }

    async fixRemainingTestIssues() {
        console.log('\n🧪 Fixing Remaining Test Issues...');
        
        // Check if database tests need fixing
        const dbTestPath = 'tests/database-tests.js';
        if (fs.existsSync(dbTestPath)) {
            let content = fs.readFileSync(dbTestPath, 'utf8');
            
            // Ensure proper constructor
            if (!content.includes('this.testResults = []')) {
                content = content.replace(
                    /constructor\(baseUrl = 'http:\/\/localhost:8080'\) \{[\s\S]*?\}/,
                    `constructor(baseUrl = 'http://localhost:8080') {
        this.baseUrl = baseUrl;
        this.testResults = [];
        this.bugTracker = require('../bugs/bug-tracker.json');
    }`
                );
                fs.writeFileSync(dbTestPath, content);
                console.log('✅ Fixed database tests constructor');
                this.fixes.push({ category: 'Tests', issue: 'Database tests constructor', status: 'FIXED' });
            }
        }

        // Verify all test files have proper structure
        const testFiles = ['tests/api-tests.js', 'tests/user-flow-tests.js', 'tests/automated-test-suite.js'];
        
        testFiles.forEach(file => {
            if (fs.existsSync(file)) {
                const content = fs.readFileSync(file, 'utf8');
                
                // Check for common issues
                const issues = [];
                if (!content.includes('this.testResults')) {
                    issues.push('Missing testResults property');
                }
                if (!content.includes('this.bugTracker')) {
                    issues.push('Missing bugTracker property');
                }
                
                if (issues.length === 0) {
                    console.log(`✅ ${file} - Structure OK`);
                    this.fixes.push({ category: 'Tests', issue: `${file} structure`, status: 'OK' });
                } else {
                    console.log(`⚠️ ${file} - Issues: ${issues.join(', ')}`);
                    this.fixes.push({ 
                        category: 'Tests', 
                        issue: `${file} structure`, 
                        status: 'WARNING',
                        details: issues.join(', ')
                    });
                }
            }
        });
    }

    async verifyFirebaseIndex() {
        console.log('\n🔥 Verifying Firebase Index...');
        
        try {
            // Test user stories endpoint which requires the Firebase index
            const uniqueEmail = `index-test-${Date.now()}@example.com`;
            
            // Register a test user
            const registerResponse = await axios.post(`${this.baseUrl}/api/auth/register`, {
                email: uniqueEmail,
                name: 'Index Test User'
            });
            
            if (registerResponse.status === 201) {
                const userId = registerResponse.data.user_id;
                
                // Wait a moment
                await new Promise(resolve => setTimeout(resolve, 1000));
                
                // Test the user stories endpoint that requires the index
                const storiesResponse = await axios.get(`${this.baseUrl}/api/user/stories?user_id=${userId}`, {
                    validateStatus: (status) => status < 600
                });
                
                if (storiesResponse.status === 200) {
                    console.log('✅ Firebase index is working');
                    this.fixes.push({ category: 'Firebase', issue: 'Database index', status: 'OK' });
                } else if (storiesResponse.status === 500) {
                    console.log('❌ Firebase index still missing (500 error)');
                    this.fixes.push({ 
                        category: 'Firebase', 
                        issue: 'Database index', 
                        status: 'CRITICAL',
                        solution: 'Create composite index in Firebase console'
                    });
                } else {
                    console.log(`⚠️ Firebase index test inconclusive (${storiesResponse.status})`);
                    this.fixes.push({ 
                        category: 'Firebase', 
                        issue: 'Database index', 
                        status: 'WARNING',
                        details: `Status: ${storiesResponse.status}`
                    });
                }
            }
        } catch (error) {
            console.log(`❌ Firebase index test failed: ${error.message}`);
            this.fixes.push({ 
                category: 'Firebase', 
                issue: 'Database index test', 
                status: 'ERROR',
                error: error.message
            });
        }
    }

    async testAuthenticationFlows() {
        console.log('\n🔐 Testing Authentication Flows...');
        
        try {
            // Test complete auth flow
            const uniqueEmail = `auth-test-${Date.now()}@example.com`;
            
            // 1. Register user
            const registerResponse = await axios.post(`${this.baseUrl}/api/auth/register`, {
                email: uniqueEmail,
                name: 'Auth Test User'
            });
            
            if (registerResponse.status === 201) {
                console.log('✅ User registration working');
                const userId = registerResponse.data.user_id;
                
                // 2. Test login
                const loginResponse = await axios.post(`${this.baseUrl}/api/auth/login`, {
                    email: uniqueEmail
                }, { validateStatus: (status) => status < 500 });
                
                if (loginResponse.status === 200) {
                    console.log('✅ User login working');
                    
                    // 3. Test authenticated endpoint (chat)
                    await new Promise(resolve => setTimeout(resolve, 1000));
                    
                    const chatResponse = await axios.post(`${this.baseUrl}/api/chat/message`, {
                        message: 'Test authentication flow',
                        user_id: userId
                    });
                    
                    if (chatResponse.status === 200 || chatResponse.status === 201) {
                        console.log('✅ Authenticated endpoints working');
                        this.fixes.push({ category: 'Authentication', issue: 'Complete auth flow', status: 'OK' });
                    } else {
                        console.log('⚠️ Authenticated endpoints have issues');
                        this.fixes.push({ 
                            category: 'Authentication', 
                            issue: 'Authenticated endpoints', 
                            status: 'WARNING',
                            details: `Chat status: ${chatResponse.status}`
                        });
                    }
                } else {
                    console.log(`⚠️ Login issues (${loginResponse.status})`);
                    this.fixes.push({ 
                        category: 'Authentication', 
                        issue: 'User login', 
                        status: 'WARNING',
                        details: `Status: ${loginResponse.status}`
                    });
                }
            } else {
                console.log(`❌ Registration failed (${registerResponse.status})`);
                this.fixes.push({ 
                    category: 'Authentication', 
                    issue: 'User registration', 
                    status: 'ERROR',
                    details: `Status: ${registerResponse.status}`
                });
            }
        } catch (error) {
            console.log(`❌ Authentication flow test failed: ${error.message}`);
            this.fixes.push({ 
                category: 'Authentication', 
                issue: 'Authentication flow test', 
                status: 'ERROR',
                error: error.message
            });
        }
    }

    getTestData(path) {
        const testData = {
            '/api/auth/register': { 
                email: `test-${Date.now()}@example.com`, 
                name: 'Test User' 
            },
            '/api/auth/login': { 
                email: 'test@example.com' 
            },
            '/api/chat/message': { 
                message: 'test message', 
                user_id: 'test-user' 
            },
            '/api/knowledge/ask': { 
                question: 'test question', 
                user_id: 'test-user' 
            }
        };
        
        return testData[path] || {};
    }

    generateFixReport() {
        console.log('\n📊 Comprehensive Fix Results:');
        console.log('===============================');
        
        const categories = ['Server', 'Endpoints', 'Tests', 'Firebase', 'Authentication'];
        
        categories.forEach(category => {
            const categoryFixes = this.fixes.filter(f => f.category === category);
            if (categoryFixes.length > 0) {
                console.log(`\n${category}:`);
                categoryFixes.forEach(fix => {
                    const status = fix.status === 'OK' ? '✅' : 
                                  fix.status === 'CRITICAL' ? '🔴' : 
                                  fix.status === 'ERROR' ? '❌' : 
                                  fix.status === 'WARNING' ? '⚠️' : 
                                  fix.status === 'FIXED' ? '🔧' : '📝';
                    console.log(`  ${status} ${fix.issue}: ${fix.status}`);
                    if (fix.solution) {
                        console.log(`      Solution: ${fix.solution}`);
                    }
                    if (fix.details) {
                        console.log(`      Details: ${fix.details}`);
                    }
                    if (fix.error) {
                        console.log(`      Error: ${fix.error}`);
                    }
                });
            }
        });
        
        const critical = this.fixes.filter(f => f.status === 'CRITICAL').length;
        const errors = this.fixes.filter(f => f.status === 'ERROR').length;
        const warnings = this.fixes.filter(f => f.status === 'WARNING').length;
        const ok = this.fixes.filter(f => f.status === 'OK').length;
        const fixed = this.fixes.filter(f => f.status === 'FIXED').length;
        
        console.log(`\n📈 Summary: ${ok} OK, ${fixed} Fixed, ${warnings} Warnings, ${errors} Errors, ${critical} Critical`);
        
        if (critical > 0) {
            console.log('\n🔴 Critical Issues Found:');
            this.fixes.filter(f => f.status === 'CRITICAL').forEach(fix => {
                console.log(`   - ${fix.issue}: ${fix.solution || 'Needs investigation'}`);
            });
        }
        
        if (errors > 0) {
            console.log('\n❌ Errors Found:');
            this.fixes.filter(f => f.status === 'ERROR').forEach(fix => {
                console.log(`   - ${fix.issue}: ${fix.error || 'Unknown error'}`);
            });
        }
        
        // Save detailed report
        const reportPath = path.join(__dirname, '../reports/comprehensive-fix-report.json');
        fs.writeFileSync(reportPath, JSON.stringify({
            timestamp: new Date().toISOString(),
            summary: { ok, fixed, warnings, errors, critical, total: this.fixes.length },
            fixes: this.fixes
        }, null, 2));
        
        console.log(`\n📄 Detailed fix report saved to: ${reportPath}`);
        
        // Provide next steps
        console.log('\n🎯 Next Steps:');
        if (critical === 0 && errors === 0) {
            console.log('   ✅ All critical issues resolved!');
            console.log('   🚀 Run test suite to verify fixes: node scripts/run-all-tests.js');
        } else {
            console.log('   🔧 Address critical issues and errors before running tests');
            if (critical > 0) {
                console.log('   🔴 Focus on critical issues first');
            }
        }
    }
}

// Run the comprehensive fixer
const fixer = new ComprehensiveBugFixer();
fixer.fixAllBugs().catch(console.error); 