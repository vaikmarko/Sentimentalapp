const fs = require('fs');
const path = require('path');

// Import all test suites
const AutomatedTestSuite = require('../tests/automated-test-suite');
const DatabaseTestSuite = require('../tests/database-tests');
const APITestSuite = require('../tests/api-tests');
const UserFlowTestSuite = require('../tests/user-flow-tests');
const PriorityBugFixer = require('./fix-priority-bugs');

class MasterTestRunner {
    constructor(baseUrl = 'http://localhost:8080') {
        this.baseUrl = baseUrl;
        this.results = {
            startTime: new Date().toISOString(),
            endTime: null,
            duration: null,
            testSuites: {},
            overallStatus: 'UNKNOWN',
            summary: {
                totalTests: 0,
                passed: 0,
                failed: 0,
                skipped: 0
            },
            bugsFound: 0,
            criticalIssues: [],
            recommendations: []
        };
    }

    async runAllTests() {
        console.log('🚀 Starting Comprehensive Sentimental App Testing Suite');
        console.log('========================================================\n');
        
        try {
            // Create necessary directories
            this.ensureDirectories();
            
            // Run all test suites in order
            await this.runDatabaseTests();
            await this.runAPITests();
            await this.runAutomatedTests();
            await this.runUserFlowTests();
            
            // Analyze results and run bug fixing
            await this.analyzeResults();
            await this.runBugFixing();
            
            // Generate final report
            this.generateMasterReport();
            
        } catch (error) {
            console.error('❌ Master test runner failed:', error);
            this.results.overallStatus = 'FAILED';
            this.results.criticalIssues.push(`Master test runner failure: ${error.message}`);
        } finally {
            this.results.endTime = new Date().toISOString();
            this.results.duration = this.calculateDuration();
            this.displayFinalSummary();
        }
    }

    ensureDirectories() {
        const dirs = ['reports', 'bugs', 'tests', 'scripts'];
        dirs.forEach(dir => {
            if (!fs.existsSync(dir)) {
                fs.mkdirSync(dir, { recursive: true });
            }
        });
    }

    async runDatabaseTests() {
        console.log('🗄️ Running Database Tests...');
        console.log('============================');
        
        try {
            const dbTestSuite = new DatabaseTestSuite(this.baseUrl);
            await dbTestSuite.runAllDatabaseTests();
            
            // Read the generated report
            const reportPath = path.join(__dirname, '../reports/database-test-report.json');
            if (fs.existsSync(reportPath)) {
                const report = JSON.parse(fs.readFileSync(reportPath, 'utf8'));
                this.results.testSuites.database = {
                    status: 'COMPLETED',
                    summary: report.summary,
                    details: report.details
                };
                this.updateOverallSummary(report.summary);
            }
            
            console.log('✅ Database tests completed\n');
            
        } catch (error) {
            console.log('❌ Database tests failed\n');
            this.results.testSuites.database = {
                status: 'FAILED',
                error: error.message
            };
            this.results.criticalIssues.push(`Database tests failed: ${error.message}`);
        }
    }

    async runAPITests() {
        console.log('🔌 Running API Tests...');
        console.log('=======================');
        
        try {
            const apiTestSuite = new APITestSuite(this.baseUrl);
            await apiTestSuite.runAllAPITests();
            
            // Read the generated report
            const reportPath = path.join(__dirname, '../reports/api-test-report.json');
            if (fs.existsSync(reportPath)) {
                const report = JSON.parse(fs.readFileSync(reportPath, 'utf8'));
                this.results.testSuites.api = {
                    status: 'COMPLETED',
                    summary: report.summary,
                    details: report.details
                };
                this.updateOverallSummaryFromAPI(report.summary);
            }
            
            console.log('✅ API tests completed\n');
            
        } catch (error) {
            console.log('❌ API tests failed\n');
            this.results.testSuites.api = {
                status: 'FAILED',
                error: error.message
            };
            this.results.criticalIssues.push(`API tests failed: ${error.message}`);
        }
    }

    async runAutomatedTests() {
        console.log('🤖 Running Automated Test Suite...');
        console.log('===================================');
        
        try {
            const automatedTestSuite = new AutomatedTestSuite(this.baseUrl);
            await automatedTestSuite.runAllTests();
            
            // Read the generated report
            const reportPath = path.join(__dirname, '../reports/test-report.json');
            if (fs.existsSync(reportPath)) {
                const report = JSON.parse(fs.readFileSync(reportPath, 'utf8'));
                this.results.testSuites.automated = {
                    status: 'COMPLETED',
                    summary: report.summary,
                    details: report.details
                };
                this.updateOverallSummaryFromAutomated(report.summary);
            }
            
            console.log('✅ Automated tests completed\n');
            
        } catch (error) {
            console.log('❌ Automated tests failed\n');
            this.results.testSuites.automated = {
                status: 'FAILED',
                error: error.message
            };
            this.results.criticalIssues.push(`Automated tests failed: ${error.message}`);
        }
    }

    async runUserFlowTests() {
        console.log('👤 Running User Flow Tests...');
        console.log('==============================');
        
        try {
            const userFlowTestSuite = new UserFlowTestSuite(this.baseUrl);
            await userFlowTestSuite.runAllUserFlowTests();
            
            // Read the generated report
            const reportPath = path.join(__dirname, '../reports/user-flow-test-report.json');
            if (fs.existsSync(reportPath)) {
                const report = JSON.parse(fs.readFileSync(reportPath, 'utf8'));
                this.results.testSuites.userFlow = {
                    status: 'COMPLETED',
                    summary: report.summary,
                    details: report.details
                };
                this.updateOverallSummaryFromUserFlow(report.summary);
            }
            
            console.log('✅ User flow tests completed\n');
            
        } catch (error) {
            console.log('❌ User flow tests failed\n');
            this.results.testSuites.userFlow = {
                status: 'FAILED',
                error: error.message
            };
            this.results.criticalIssues.push(`User flow tests failed: ${error.message}`);
        }
    }

    async analyzeResults() {
        console.log('📊 Analyzing Test Results...');
        console.log('============================');
        
        // Count total bugs found
        const bugTrackerPath = path.join(__dirname, '../bugs/bug-tracker.json');
        if (fs.existsSync(bugTrackerPath)) {
            const bugTracker = JSON.parse(fs.readFileSync(bugTrackerPath, 'utf8'));
            this.results.bugsFound = bugTracker.bugs ? bugTracker.bugs.length : 0;
            
            // Count critical bugs
            const criticalBugs = bugTracker.bugs ? bugTracker.bugs.filter(bug => bug.severity === 'critical') : [];
            if (criticalBugs.length > 0) {
                this.results.criticalIssues.push(`${criticalBugs.length} critical bugs found`);
            }
        }
        
        // Determine overall status
        if (this.results.criticalIssues.length > 0) {
            this.results.overallStatus = 'CRITICAL_ISSUES';
        } else if (this.results.summary.failed > 0) {
            this.results.overallStatus = 'ISSUES_FOUND';
        } else if (this.results.summary.passed > 0) {
            this.results.overallStatus = 'HEALTHY';
        } else {
            this.results.overallStatus = 'NO_TESTS_RUN';
        }
        
        // Generate recommendations
        this.generateRecommendations();
        
        console.log('✅ Analysis completed\n');
    }

    async runBugFixing() {
        console.log('🔧 Running Priority Bug Fixing...');
        console.log('==================================');
        
        try {
            const bugFixer = new PriorityBugFixer();
            await bugFixer.runPriorityBugFix();
            
            console.log('✅ Bug fixing completed\n');
            
        } catch (error) {
            console.log('❌ Bug fixing failed\n');
            this.results.criticalIssues.push(`Bug fixing failed: ${error.message}`);
        }
    }

    updateOverallSummary(summary) {
        Object.keys(summary).forEach(category => {
            if (summary[category].passed) {
                this.results.summary.passed += summary[category].passed;
            }
            if (summary[category].total) {
                this.results.summary.totalTests += summary[category].total;
                this.results.summary.failed += (summary[category].total - (summary[category].passed || 0));
            }
        });
    }

    updateOverallSummaryFromAPI(summary) {
        this.results.summary.totalTests += summary.totalTests || 0;
        this.results.summary.passed += summary.passed || 0;
        this.results.summary.failed += summary.failed || 0;
    }

    updateOverallSummaryFromAutomated(summary) {
        Object.keys(summary).forEach(category => {
            if (summary[category].passed) {
                this.results.summary.passed += summary[category].passed;
            }
            if (summary[category].total) {
                this.results.summary.totalTests += summary[category].total;
                this.results.summary.failed += (summary[category].total - (summary[category].passed || 0));
            }
        });
    }

    updateOverallSummaryFromUserFlow(summary) {
        this.results.summary.totalTests += summary.totalTests || 0;
        this.results.summary.passed += summary.passed || 0;
        this.results.summary.failed += summary.failed || 0;
        this.results.summary.skipped += summary.skipped || 0;
    }

    generateRecommendations() {
        const recommendations = [];
        
        // Based on overall status
        if (this.results.overallStatus === 'CRITICAL_ISSUES') {
            recommendations.push('🚨 URGENT: Address critical issues immediately before deployment');
        }
        
        // Based on test results
        const failureRate = this.results.summary.failed / this.results.summary.totalTests;
        if (failureRate > 0.3) {
            recommendations.push('⚠️ High failure rate detected - review core functionality');
        } else if (failureRate > 0.1) {
            recommendations.push('📝 Moderate issues found - prioritize fixes based on severity');
        }
        
        // Based on bugs found
        if (this.results.bugsFound > 10) {
            recommendations.push('🐛 High number of bugs detected - consider code review and refactoring');
        } else if (this.results.bugsFound > 5) {
            recommendations.push('🔍 Several bugs found - implement regular testing schedule');
        }
        
        // Component-specific recommendations
        if (this.results.testSuites.database && this.results.testSuites.database.status === 'FAILED') {
            recommendations.push('🗄️ Database issues detected - check connectivity and permissions');
        }
        
        if (this.results.testSuites.api && this.results.testSuites.api.status === 'FAILED') {
            recommendations.push('🔌 API issues detected - review endpoint implementations');
        }
        
        if (this.results.testSuites.userFlow && this.results.testSuites.userFlow.status === 'FAILED') {
            recommendations.push('👤 User flow issues detected - test core user journeys manually');
        }
        
        // General recommendations
        if (this.results.summary.totalTests < 20) {
            recommendations.push('📈 Consider adding more comprehensive test coverage');
        }
        
        if (recommendations.length === 0) {
            recommendations.push('✨ System appears healthy - maintain regular testing schedule');
        }
        
        this.results.recommendations = recommendations;
    }

    generateMasterReport() {
        console.log('📄 Generating Master Report...');
        console.log('==============================');
        
        const reportPath = path.join(__dirname, '../reports/master-test-report.json');
        fs.writeFileSync(reportPath, JSON.stringify(this.results, null, 2));
        
        // Also generate a human-readable summary
        const summaryPath = path.join(__dirname, '../reports/test-summary.md');
        const summaryContent = this.generateMarkdownSummary();
        fs.writeFileSync(summaryPath, summaryContent);
        
        console.log(`📊 Master report saved to: ${reportPath}`);
        console.log(`📝 Summary saved to: ${summaryPath}`);
    }

    generateMarkdownSummary() {
        const status = this.getStatusEmoji(this.results.overallStatus);
        
        return `# Sentimental App Test Report

## Overall Status: ${status} ${this.results.overallStatus}

**Test Run:** ${this.results.startTime}  
**Duration:** ${this.results.duration}

## Summary
- **Total Tests:** ${this.results.summary.totalTests}
- **Passed:** ${this.results.summary.passed} ✅
- **Failed:** ${this.results.summary.failed} ❌
- **Skipped:** ${this.results.summary.skipped} ⏭️
- **Bugs Found:** ${this.results.bugsFound} 🐛

## Test Suites

### Database Tests
Status: ${this.results.testSuites.database?.status || 'NOT_RUN'}

### API Tests  
Status: ${this.results.testSuites.api?.status || 'NOT_RUN'}

### Automated Tests
Status: ${this.results.testSuites.automated?.status || 'NOT_RUN'}

### User Flow Tests
Status: ${this.results.testSuites.userFlow?.status || 'NOT_RUN'}

## Critical Issues
${this.results.criticalIssues.length > 0 ? 
    this.results.criticalIssues.map(issue => `- ⚠️ ${issue}`).join('\n') : 
    '✅ No critical issues found'}

## Recommendations
${this.results.recommendations.map(rec => `- ${rec}`).join('\n')}

## Next Steps
1. Review failed tests and fix critical issues
2. Address high-priority bugs
3. Implement recommended improvements
4. Re-run tests to verify fixes
5. Schedule regular testing cycles

---
*Generated by Sentimental App Testing Suite*
`;
    }

    getStatusEmoji(status) {
        const emojis = {
            'HEALTHY': '✅',
            'ISSUES_FOUND': '⚠️',
            'CRITICAL_ISSUES': '🚨',
            'NO_TESTS_RUN': '❓',
            'FAILED': '❌'
        };
        return emojis[status] || '❓';
    }

    calculateDuration() {
        const start = new Date(this.results.startTime);
        const end = new Date(this.results.endTime);
        const diffMs = end - start;
        const diffMinutes = Math.floor(diffMs / (1000 * 60));
        const diffSeconds = Math.floor((diffMs % (1000 * 60)) / 1000);
        
        if (diffMinutes > 0) {
            return `${diffMinutes}m ${diffSeconds}s`;
        } else {
            return `${diffSeconds}s`;
        }
    }

    displayFinalSummary() {
        console.log('\n🎯 FINAL TEST SUMMARY');
        console.log('=====================');
        console.log(`Overall Status: ${this.getStatusEmoji(this.results.overallStatus)} ${this.results.overallStatus}`);
        console.log(`Duration: ${this.results.duration}`);
        console.log(`Total Tests: ${this.results.summary.totalTests}`);
        console.log(`Passed: ${this.results.summary.passed} ✅`);
        console.log(`Failed: ${this.results.summary.failed} ❌`);
        console.log(`Skipped: ${this.results.summary.skipped} ⏭️`);
        console.log(`Bugs Found: ${this.results.bugsFound} 🐛`);
        
        if (this.results.criticalIssues.length > 0) {
            console.log('\n🚨 CRITICAL ISSUES:');
            this.results.criticalIssues.forEach(issue => {
                console.log(`   - ${issue}`);
            });
        }
        
        console.log('\n💡 RECOMMENDATIONS:');
        this.results.recommendations.forEach(rec => {
            console.log(`   - ${rec}`);
        });
        
        console.log('\n📄 Reports generated in /reports/ directory');
        console.log('🔧 Run bug fixing with: node scripts/fix-priority-bugs.js');
        console.log('\n✨ Testing complete!');
    }
}

// Export for use in other scripts
module.exports = MasterTestRunner;

// Run if called directly
if (require.main === module) {
    const runner = new MasterTestRunner();
    runner.runAllTests().catch(console.error);
} 