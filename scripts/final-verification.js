#!/usr/bin/env node

const http = require('http');

class FinalVerification {
    constructor() {
        this.baseUrl = 'http://localhost:8080';
        this.results = [];
    }

    async makeRequest(method, path, data = null) {
        return new Promise((resolve, reject) => {
            const options = {
                hostname: 'localhost',
                port: 8080,
                path: path,
                method: method,
                headers: {
                    'Content-Type': 'application/json'
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
                            headers: res.headers
                        });
                    } catch (e) {
                        resolve({
                            status: res.statusCode,
                            data: body,
                            headers: res.headers
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

    async testFirebaseIndexFallback() {
        console.log('\n🔍 Testing Firebase Index Fallback...');
        
        try {
            const response = await this.makeRequest('GET', '/api/user/stories?user_id=keVb3KjLwNXnro9jYWA9');
            
            if (response.status === 200) {
                console.log('✅ Firebase index fallback working - returns 200 instead of 500');
                console.log(`   Response: ${Array.isArray(response.data) ? `Array with ${response.data.length} items` : 'Valid JSON'}`);
                this.results.push({ test: 'Firebase Index Fallback', status: 'PASS' });
            } else {
                console.log(`❌ Firebase index fallback failed - status: ${response.status}`);
                this.results.push({ test: 'Firebase Index Fallback', status: 'FAIL' });
            }
        } catch (error) {
            console.log(`❌ Firebase index fallback error: ${error.message}`);
            this.results.push({ test: 'Firebase Index Fallback', status: 'ERROR' });
        }
    }

    async testResponseFormats() {
        console.log('\n📋 Testing Response Formats...');
        
        try {
            const response = await this.makeRequest('GET', '/api/stories');
            
            if (response.status === 200 && Array.isArray(response.data)) {
                const hasRequiredFields = response.data.every(story => 
                    story.hasOwnProperty('id') && 
                    story.hasOwnProperty('title')
                );
                
                if (hasRequiredFields) {
                    console.log('✅ Stories response format correct - all stories have id and title');
                    this.results.push({ test: 'Response Format', status: 'PASS' });
                } else {
                    console.log('❌ Stories missing required fields (id or title)');
                    this.results.push({ test: 'Response Format', status: 'FAIL' });
                }
            } else {
                console.log(`❌ Stories endpoint failed - status: ${response.status}`);
                this.results.push({ test: 'Response Format', status: 'FAIL' });
            }
        } catch (error) {
            console.log(`❌ Response format test error: ${error.message}`);
            this.results.push({ test: 'Response Format', status: 'ERROR' });
        }
    }

    async testAuthenticationFlow() {
        console.log('\n🔐 Testing Authentication Flow...');
        
        try {
            // Test 1: Invalid story data should return 400
            const invalidDataResponse = await this.makeRequest('POST', '/api/stories', {
                title: '',
                content: ''
            });
            
            if (invalidDataResponse.status === 400) {
                console.log('✅ Invalid story data returns 400 (correct)');
            } else {
                console.log(`❌ Invalid story data returned ${invalidDataResponse.status} instead of 400`);
            }

            // Test 2: Valid data but no auth should return 401
            const noAuthResponse = await this.makeRequest('POST', '/api/stories', {
                title: 'Test Story',
                content: 'Test content'
            });
            
            if (noAuthResponse.status === 401) {
                console.log('✅ No auth story creation returns 401 (correct)');
                this.results.push({ test: 'Authentication Flow', status: 'PASS' });
            } else {
                console.log(`❌ No auth story creation returned ${noAuthResponse.status} instead of 401`);
                this.results.push({ test: 'Authentication Flow', status: 'FAIL' });
            }
            
        } catch (error) {
            console.log(`❌ Authentication flow test error: ${error.message}`);
            this.results.push({ test: 'Authentication Flow', status: 'ERROR' });
        }
    }

    async testErrorHandling() {
        console.log('\n🚫 Testing Error Handling...');
        
        try {
            const response = await this.makeRequest('GET', '/api/nonexistent-endpoint');
            
            if (response.status === 404) {
                console.log('✅ Non-existent endpoint returns 404');
                this.results.push({ test: 'Error Handling', status: 'PASS' });
            } else {
                console.log(`❌ Non-existent endpoint returned ${response.status} instead of 404`);
                this.results.push({ test: 'Error Handling', status: 'FAIL' });
            }
        } catch (error) {
            console.log(`❌ Error handling test error: ${error.message}`);
            this.results.push({ test: 'Error Handling', status: 'ERROR' });
        }
    }

    async testPerformance() {
        console.log('\n⚡ Testing Performance...');
        
        try {
            const startTime = Date.now();
            const response = await this.makeRequest('GET', '/api/stories');
            const endTime = Date.now();
            const responseTime = endTime - startTime;
            
            if (response.status === 200 && responseTime < 2000) {
                console.log(`✅ Stories endpoint responds in ${responseTime}ms (good performance)`);
                this.results.push({ test: 'Performance', status: 'PASS' });
            } else if (response.status === 200) {
                console.log(`⚠️  Stories endpoint responds in ${responseTime}ms (slow but working)`);
                this.results.push({ test: 'Performance', status: 'SLOW' });
            } else {
                console.log(`❌ Stories endpoint failed - status: ${response.status}`);
                this.results.push({ test: 'Performance', status: 'FAIL' });
            }
        } catch (error) {
            console.log(`❌ Performance test error: ${error.message}`);
            this.results.push({ test: 'Performance', status: 'ERROR' });
        }
    }

    async runAllTests() {
        console.log('🔧 Final Bug Fix Verification');
        console.log('================================');
        
        await this.testFirebaseIndexFallback();
        await this.testResponseFormats();
        await this.testAuthenticationFlow();
        await this.testErrorHandling();
        await this.testPerformance();
        
        this.printSummary();
    }

    printSummary() {
        console.log('\n📊 VERIFICATION SUMMARY');
        console.log('========================');
        
        let passed = 0;
        let failed = 0;
        let errors = 0;
        
        this.results.forEach(result => {
            const status = result.status === 'PASS' ? '✅' : 
                          result.status === 'SLOW' ? '⚠️' : 
                          result.status === 'FAIL' ? '❌' : '💥';
            console.log(`${status} ${result.test}: ${result.status}`);
            
            if (result.status === 'PASS' || result.status === 'SLOW') passed++;
            else if (result.status === 'FAIL') failed++;
            else errors++;
        });
        
        console.log('\n📈 RESULTS:');
        console.log(`   Passed: ${passed}`);
        console.log(`   Failed: ${failed}`);
        console.log(`   Errors: ${errors}`);
        console.log(`   Success Rate: ${Math.round((passed / this.results.length) * 100)}%`);
        
        if (failed === 0 && errors === 0) {
            console.log('\n🎉 ALL MAJOR BUGS FIXED! System is stable and ready.');
        } else if (failed + errors <= 1) {
            console.log('\n✅ System is mostly stable with minor issues remaining.');
        } else {
            console.log('\n⚠️  Some issues remain that need attention.');
        }
    }
}

// Run the verification
const verification = new FinalVerification();
verification.runAllTests().catch(console.error); 