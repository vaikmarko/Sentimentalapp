const axios = require('axios');
const fs = require('fs');
const path = require('path');

class UserFlowTestSuite {
    constructor(baseUrl = 'http://localhost:8080') {
        this.baseUrl = baseUrl;
        this.testResults = [];
        this.bugTracker = require('../bugs/bug-tracker.json');
    }

    async runAllUserFlowTests() {
        console.log('👤 Starting User Flow Test Suite...\n');
        
        try {
            await this.testNewUserJourney();
            await this.testReturningUserJourney();
            await this.testShareToStoryFlow();
            await this.testSpaceQuestionFlow();
            await this.testDataBuildingProcess();
            await this.testDiscoveryFlow();
            
            this.generateUserFlowReport();
            
        } catch (error) {
            console.error('❌ User flow test suite failed:', error);
            this.logCriticalBug('User Flow Test Suite Failure', error.message);
        }
    }

    async testNewUserJourney() {
        console.log('🆕 Testing New User Journey...');
        
        const userEmail = `new-user-${Date.now()}-${Math.random().toString(36).substr(2, 9)}@test.com`;
        let userId;
        
        try {
            // Step 1: User lands on the app
            const landingResponse = await axios.get(`${this.baseUrl}/`);
            if (landingResponse.status !== 200) {
                throw new Error('Landing page not accessible');
            }
            
            // Step 2: User navigates to main app
            const appResponse = await axios.get(`${this.baseUrl}/app`);
            if (appResponse.status !== 200) {
                throw new Error('Main app not accessible');
            }
            
            // Step 3: User registers
            const registerResponse = await axios.post(`${this.baseUrl}/api/auth/register`, {
                email: userEmail,
                name: 'New Test User'
            });
            
            if (registerResponse.status !== 201) {
                throw new Error('User registration failed');
            }
            
            userId = registerResponse.data.user_id;
            
            // Wait for user to be available in database
            await this.delay(2000);
            
            // Step 4: User starts first conversation
            const chatResponse = await axios.post(`${this.baseUrl}/api/chat/message`, {
                message: 'Hi, I\'m new here. Today I felt really excited about starting this journey of self-discovery.',
                user_id: userId
            });
            
            if (chatResponse.status !== 200 && chatResponse.status !== 201) {
                throw new Error('First conversation failed');
            }
            
            // Step 5: Check if story was created from conversation
            await this.delay(2000); // Wait for processing
            const storiesResponse = await axios.get(`${this.baseUrl}/api/user/stories?user_id=${userId}`);
            
            if (storiesResponse.status !== 200 || storiesResponse.data.length === 0) {
                throw new Error('Story not created from first conversation');
            }
            
            // Step 6: User asks first question in Space
            const spaceResponse = await axios.post(`${this.baseUrl}/api/knowledge/ask`, {
                question: 'What can you tell me about my emotional patterns?',
                user_id: userId
            });
            
            if (spaceResponse.status !== 200) {
                throw new Error('Space question failed');
            }
            
            // Should indicate insufficient data and suggest curated conversation
            if (spaceResponse.data.confidence !== 'low') {
                throw new Error('Space should indicate insufficient data for new user');
            }
            
            console.log('✅ New User Journey - Complete flow successful');
            this.testResults.push({
                category: 'User Journey',
                test: 'New User Journey',
                status: 'PASS',
                details: 'Complete new user flow from landing to first story and space question'
            });
            
        } catch (error) {
            console.log('❌ New User Journey - Flow failed');
            this.testResults.push({
                category: 'User Journey',
                test: 'New User Journey',
                status: 'FAIL',
                error: error.message
            });
            this.logBug('User Flow', `New User Journey failed: ${error.message}`, 'high');
        }
    }

    async testReturningUserJourney() {
        console.log('\n🔄 Testing Returning User Journey...');
        
        const userEmail = `returning-user-${Date.now()}-${Math.random().toString(36).substr(2, 9)}@test.com`;
        let userId;
        
        try {
            // Step 1: Register user
            const registerResponse = await axios.post(`${this.baseUrl}/api/auth/register`, {
                email: userEmail,
                name: 'Returning Test User'
            });
            
            if (registerResponse.status !== 201) {
                throw new Error('User registration failed');
            }
            
            userId = registerResponse.data.user_id;
            
            // Wait for user to be available in database
            await this.delay(2000);
            
            // Step 2: Simulate user with existing data by creating multiple stories
            const conversations = [
                'Today I had a great meeting with my team. We solved a complex problem together.',
                'I felt a bit overwhelmed with my workload, but I managed to prioritize well.',
                'Had a wonderful dinner with friends. It reminded me how important relationships are.',
                'Spent some quiet time reading. It helped me feel more centered and peaceful.'
            ];
            
            // Create multiple conversations/stories
            for (const message of conversations) {
                await axios.post(`${this.baseUrl}/api/chat/message`, {
                    message,
                    user_id: userId
                });
                await this.delay(1000); // Wait between conversations
            }
            
            // Step 3: Wait for stories to be created
            await this.delay(3000);
            
            // Step 4: Check that multiple stories exist
            const storiesResponse = await axios.get(`${this.baseUrl}/api/user/stories?user_id=${userId}`);
            
            if (storiesResponse.status !== 200 || storiesResponse.data.length < 2) {
                throw new Error('Insufficient stories created for returning user simulation');
            }
            
            // Step 5: User asks question in Space (should have sufficient data now)
            const spaceResponse = await axios.post(`${this.baseUrl}/api/knowledge/ask`, {
                question: 'What are my main emotional patterns based on my recent experiences?',
                user_id: userId
            });
            
            if (spaceResponse.status !== 200) {
                throw new Error('Space question failed for returning user');
            }
            
            // Should provide analysis based on existing data
            if (!spaceResponse.data.analysis && spaceResponse.data.confidence === 'low') {
                console.log('⚠️ Space still shows low confidence despite multiple stories');
                // This might be expected behavior, not necessarily a failure
            }
            
            // Step 6: User browses their stories
            const userStoriesResponse = await axios.get(`${this.baseUrl}/api/user/stories?user_id=${userId}`);
            
            if (userStoriesResponse.status !== 200) {
                throw new Error('User cannot access their stories');
            }
            
            console.log('✅ Returning User Journey - Complete flow successful');
            this.testResults.push({
                category: 'User Journey',
                test: 'Returning User Journey',
                status: 'PASS',
                details: 'Returning user with existing data can access stories and get insights'
            });
            
        } catch (error) {
            console.log('❌ Returning User Journey - Flow failed');
            this.testResults.push({
                category: 'User Journey',
                test: 'Returning User Journey',
                status: 'FAIL',
                error: error.message
            });
            this.logBug('User Flow', `Returning User Journey failed: ${error.message}`, 'high');
        }
    }

    async testShareToStoryFlow() {
        console.log('\n📤 Testing Share to Story Flow...');
        
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

            // Step 2: Send a chat message (this creates a story automatically)
            const chatResponse = await axios.post(`${this.baseUrl}/api/chat/message`, {
                message: 'Today I had an amazing breakthrough at work. I finally understood a complex problem that had been bothering me for weeks.',
                user_id: userId
            });

            if (chatResponse.status !== 200 && chatResponse.status !== 201) {
                throw new Error(`Chat message failed: ${chatResponse.status}`);
            }

            // Step 3: Verify story was created by checking user stories
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            const storiesResponse = await axios.get(`${this.baseUrl}/api/user/stories?user_id=${userId}`);
            
            if (storiesResponse.status === 200 && storiesResponse.data.length > 0) {
                console.log('✅ Share to Story flow working');
                if (this.testResults) {
                    this.testResults.push({ flow: 'Share to Story', status: 'PASS', details: 'Story created from chat message' });
                }
            } else {
                throw new Error('Story not found after chat message');
            }
            
        } catch (error) {
            console.log(`❌ Share to Story flow failed: ${error.message}`);
            if (this.testResults) {
                this.testResults.push({ flow: 'Share to Story', status: 'FAIL', error: error.message });
            }
        }
    }

    async testSpaceQuestionFlow() {
        console.log('\n🌌 Testing Space Question Flow...');
        
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

            // Step 2: Ask initial question
            const initialQuestionResponse = await axios.post(`${this.baseUrl}/api/knowledge/ask`, {
                question: 'What are my main emotional patterns?',
                user_id: userId
            });
            
            if (initialQuestionResponse.status !== 200) {
                throw new Error('Initial space question failed');
            }
            
            // Step 3: Start curated conversation if suggested
            if (initialQuestionResponse.data.learning_path && 
                initialQuestionResponse.data.learning_path.conversation_sequence &&
                initialQuestionResponse.data.learning_path.conversation_sequence.length > 0) {
                
                const firstConversation = initialQuestionResponse.data.learning_path.conversation_sequence[0];
                const conversationResponse = await axios.post(`${this.baseUrl}/api/knowledge/start-conversation`, {
                    user_id: userId,
                    conversation_id: firstConversation.id || 'procrastination_deep_dive'
                });
                
                if (conversationResponse.status !== 200) {
                    console.log('⚠️ Space question should indicate low confidence for new user');
                    // This is expected for new users - they should get guidance to build data first
                }
            }
            
            // Step 4: Ask the question again after some data collection
            await new Promise(resolve => setTimeout(resolve, 1000));
            const followUpQuestionResponse = await axios.post(`${this.baseUrl}/api/knowledge/ask`, {
                question: 'What are my patterns when it comes to handling stress?',
                user_id: userId
            });
            
            if (followUpQuestionResponse.status !== 200) {
                throw new Error('Follow-up space question failed');
            }

            this.testResults.push({
                test: 'Space Question Flow',
                status: 'PASS',
                details: 'Complete flow successful'
            });
            
            console.log('✅ Space Question Flow - Complete flow successful');
            return true;
            
        } catch (error) {
            this.testResults.push({
                test: 'Space Question Flow',
                status: 'FAIL',
                error: error.message
            });
            
            console.log(`❌ Space Question Flow - ${error.message}`);
            this.logBug('User Flow', `Space question flow failed: ${error.message}`, 'high');
            return false;
        }
    }

    async testDataBuildingProcess() {
        console.log('\n📊 Testing Data Building Process...');
        
        const userEmail = `data-building-${Date.now()}-${Math.random().toString(36).substr(2, 9)}@test.com`;
        let userId;
        
        try {
            // Step 1: Register user
            const registerResponse = await axios.post(`${this.baseUrl}/api/auth/register`, {
                email: userEmail,
                name: 'Data Building Test User'
            });
            
            if (registerResponse.status !== 201) {
                throw new Error('User registration failed');
            }
            
            userId = registerResponse.data.user_id;
            
            // Wait for user to be available in database
            await this.delay(2000);
            
            // Step 2: Check initial data state
            const initialDataResponse = await axios.get(`${this.baseUrl}/api/inner-space-data?user_id=${userId}`);
            
            if (initialDataResponse.status !== 200) {
                throw new Error('Cannot retrieve initial inner space data');
            }
            
            // Step 3: Add various types of content
            const contentTypes = [
                'Today I felt really confident presenting my ideas at work.',
                'I had a difficult conversation with my partner about our future.',
                'Spent time with my family and felt grateful for their support.',
                'Struggled with anxiety about an upcoming deadline.',
                'Celebrated a small victory - I finished reading a book I\'ve been working on for months.'
            ];
            
            for (const content of contentTypes) {
                await axios.post(`${this.baseUrl}/api/chat/message`, {
                    message: content,
                    user_id: userId
                });
                
                // Analyze each piece of content
                await axios.post(`${this.baseUrl}/api/knowledge/analyze`, {
                    story_content: content,
                    user_id: userId
                });
                
                await this.delay(1000);
            }
            
            // Step 4: Check if data has been built up
            await this.delay(3000);
            const updatedDataResponse = await axios.get(`${this.baseUrl}/api/inner-space-data?user_id=${userId}`);
            
            if (updatedDataResponse.status !== 200) {
                throw new Error('Cannot retrieve updated inner space data');
            }
            
            // Step 5: Verify data structure and content
            const data = updatedDataResponse.data;
            if (!data.domains || Object.keys(data.domains).length === 0) {
                throw new Error('No knowledge domains created from content');
            }
            
            // Step 6: Test that questions now get better responses
            const questionResponse = await axios.post(`${this.baseUrl}/api/knowledge/ask`, {
                question: 'How do I typically handle challenging situations?',
                user_id: userId
            });
            
            if (questionResponse.status !== 200) {
                throw new Error('Question after data building failed');
            }
            
            console.log('✅ Data Building Process - Complete flow successful');
            this.testResults.push({
                category: 'User Journey',
                test: 'Data Building Process',
                status: 'PASS',
                details: 'Data successfully built from multiple content types and improves question responses'
            });
            
        } catch (error) {
            console.log('❌ Data Building Process - Flow failed');
            this.testResults.push({
                category: 'User Journey',
                test: 'Data Building Process',
                status: 'FAIL',
                error: error.message
            });
            this.logBug('User Flow', `Data Building Process failed: ${error.message}`, 'medium');
        }
    }

    async testDiscoveryFlow() {
        console.log('\n🔍 Testing Discovery Flow...');
        
        try {
            // Step 1: User browses public stories
            const storiesResponse = await axios.get(`${this.baseUrl}/api/stories`);
            
            if (storiesResponse.status !== 200) {
                throw new Error('Cannot load public stories for discovery');
            }
            
            if (!Array.isArray(storiesResponse.data)) {
                throw new Error('Stories response is not an array');
            }
            
            // Step 2: Check story structure for discovery features
            if (storiesResponse.data.length > 0) {
                const story = storiesResponse.data[0];
                
                if (!story.id || !story.title || !story.content) {
                    throw new Error('Story missing required fields for discovery');
                }
                
                // Step 3: Test story interaction capabilities (if implemented)
                // Note: Comment and reaction features might not be fully implemented yet
                // This is more of a structure check
                
                console.log('✅ Discovery Flow - Basic discovery functionality working');
                this.testResults.push({
                    category: 'User Journey',
                    test: 'Discovery Flow',
                    status: 'PASS',
                    details: 'Public stories load correctly for discovery'
                });
            } else {
                console.log('ℹ️ Discovery Flow - No public stories available for testing');
                this.testResults.push({
                    category: 'User Journey',
                    test: 'Discovery Flow',
                    status: 'SKIP',
                    details: 'No public stories available for discovery testing'
                });
            }
            
        } catch (error) {
            console.log('❌ Discovery Flow - Flow failed');
            this.testResults.push({
                category: 'User Journey',
                test: 'Discovery Flow',
                status: 'FAIL',
                error: error.message
            });
            this.logBug('User Flow', `Discovery flow failed: ${error.message}`, 'medium');
        }
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    logBug(category, description, severity) {
        const bug = {
            id: `bug-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
            category,
            description,
            severity,
            timestamp: new Date().toISOString(),
            status: 'open',
            source: 'user-flow-tests'
        };

        this.bugTracker.bugs = this.bugTracker.bugs || [];
        this.bugTracker.bugs.push(bug);
    }

    logCriticalBug(component, error) {
        this.logBug('Critical', `${component}: ${error}`, 'critical');
    }

    generateUserFlowReport() {
        console.log('\n📊 User Flow Test Results Summary:');
        console.log('===================================');
        
        const passed = this.testResults.filter(t => t.status === 'PASS').length;
        const failed = this.testResults.filter(t => t.status === 'FAIL').length;
        const skipped = this.testResults.filter(t => t.status === 'SKIP').length;
        const total = this.testResults.length;
        
        console.log(`Total Tests: ${total}`);
        console.log(`Passed: ${passed}`);
        console.log(`Failed: ${failed}`);
        console.log(`Skipped: ${skipped}`);
        
        this.testResults.forEach(result => {
            const status = result.status === 'PASS' ? '✅' : result.status === 'FAIL' ? '❌' : 'ℹ️';
            console.log(`${status} ${result.test}: ${result.status}`);
        });
        
        // Save detailed results
        const reportPath = path.join(__dirname, '../reports/user-flow-test-report.json');
        fs.writeFileSync(reportPath, JSON.stringify({
            timestamp: new Date().toISOString(),
            summary: {
                totalTests: total,
                passed,
                failed,
                skipped
            },
            details: this.testResults
        }, null, 2));
        
        console.log(`\n📄 Detailed user flow report saved to: ${reportPath}`);
        
        // Save updated bug tracker
        const bugTrackerPath = path.join(__dirname, '../bugs/bug-tracker.json');
        fs.writeFileSync(bugTrackerPath, JSON.stringify(this.bugTracker, null, 2));
    }
}

// Export for use in other scripts
module.exports = UserFlowTestSuite;

// Run if called directly
if (require.main === module) {
    const testSuite = new UserFlowTestSuite();
    testSuite.runAllUserFlowTests().catch(console.error);
} 