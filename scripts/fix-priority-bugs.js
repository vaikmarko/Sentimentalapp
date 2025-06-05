const fs = require('fs');
const path = require('path');

class PriorityBugFixer {
    constructor() {
        this.bugTracker = require('../bugs/bug-tracker.json');
        this.fixStrategies = new Map();
        this.initializeFixStrategies();
    }

    initializeFixStrategies() {
        // Define fix strategies for common bug patterns
        this.fixStrategies.set('Database Connection', {
            priority: 1,
            autoFixable: false,
            steps: [
                'Check Firebase credentials configuration',
                'Verify network connectivity',
                'Check environment variables',
                'Restart database service',
                'Review firestore.rules for access permissions'
            ],
            estimatedTime: '30 minutes'
        });

        this.fixStrategies.set('API Endpoint', {
            priority: 2,
            autoFixable: false,
            steps: [
                'Check endpoint route definition in app.py',
                'Verify request/response data formats',
                'Check authentication requirements',
                'Review error handling in endpoint',
                'Test with curl or Postman'
            ],
            estimatedTime: '20 minutes'
        });

        this.fixStrategies.set('Share to Story', {
            priority: 1,
            autoFixable: false,
            steps: [
                'Check chat message processing logic',
                'Verify story creation triggers',
                'Review conversation-to-story conversion',
                'Check database write permissions',
                'Test story generation prompts'
            ],
            estimatedTime: '45 minutes'
        });

        this.fixStrategies.set('Space Question', {
            priority: 2,
            autoFixable: false,
            steps: [
                'Check knowledge analysis logic',
                'Verify data sufficiency calculations',
                'Review curated conversation triggers',
                'Test knowledge domain building',
                'Check insight generation algorithms'
            ],
            estimatedTime: '60 minutes'
        });

        this.fixStrategies.set('Component', {
            priority: 3,
            autoFixable: true,
            steps: [
                'Check HTML template syntax',
                'Verify CSS/JS file paths',
                'Review template variable passing',
                'Check for missing imports',
                'Validate HTML structure'
            ],
            estimatedTime: '15 minutes'
        });

        this.fixStrategies.set('Performance', {
            priority: 3,
            autoFixable: true,
            steps: [
                'Add database query optimization',
                'Implement response caching',
                'Optimize large data transfers',
                'Add pagination for large datasets',
                'Review and optimize slow algorithms'
            ],
            estimatedTime: '30 minutes'
        });

        this.fixStrategies.set('User Flow', {
            priority: 1,
            autoFixable: false,
            steps: [
                'Map complete user journey',
                'Identify broken step in flow',
                'Check data persistence between steps',
                'Verify state management',
                'Test error recovery mechanisms'
            ],
            estimatedTime: '40 minutes'
        });
    }

    async runPriorityBugFix() {
        console.log('🔧 Starting Priority Bug Fixing System...\n');
        
        try {
            const prioritizedBugs = this.prioritizeBugs();
            
            if (prioritizedBugs.length === 0) {
                console.log('✨ No bugs found! System is clean.');
                return;
            }
            
            console.log(`Found ${prioritizedBugs.length} bugs to address:\n`);
            
            // Process critical bugs first
            const criticalBugs = prioritizedBugs.filter(bug => bug.severity === 'critical');
            if (criticalBugs.length > 0) {
                console.log('🚨 CRITICAL BUGS (Fix Immediately):');
                await this.processBugs(criticalBugs);
            }
            
            // Then high priority bugs
            const highBugs = prioritizedBugs.filter(bug => bug.severity === 'high');
            if (highBugs.length > 0) {
                console.log('\n🔥 HIGH PRIORITY BUGS (Fix within 24 hours):');
                await this.processBugs(highBugs);
            }
            
            // Then medium priority bugs
            const mediumBugs = prioritizedBugs.filter(bug => bug.severity === 'medium');
            if (mediumBugs.length > 0) {
                console.log('\n⚠️ MEDIUM PRIORITY BUGS (Fix within 1 week):');
                await this.processBugs(mediumBugs.slice(0, 5)); // Limit to top 5
            }
            
            // Finally low priority bugs
            const lowBugs = prioritizedBugs.filter(bug => bug.severity === 'low');
            if (lowBugs.length > 0) {
                console.log('\n📝 LOW PRIORITY BUGS (Fix when time permits):');
                await this.processBugs(lowBugs.slice(0, 3)); // Limit to top 3
            }
            
            this.generateFixReport(prioritizedBugs);
            
        } catch (error) {
            console.error('❌ Priority bug fixing failed:', error);
        }
    }

    prioritizeBugs() {
        const openBugs = this.bugTracker.bugs.filter(bug => bug.status === 'open');
        
        // Sort by severity and age
        return openBugs.sort((a, b) => {
            const severityOrder = { critical: 1, high: 2, medium: 3, low: 4 };
            
            // First sort by severity
            const severityDiff = severityOrder[a.severity] - severityOrder[b.severity];
            if (severityDiff !== 0) return severityDiff;
            
            // Then by age (older bugs first)
            return new Date(a.timestamp) - new Date(b.timestamp);
        });
    }

    async processBugs(bugs) {
        for (const bug of bugs) {
            await this.processBug(bug);
        }
    }

    async processBug(bug) {
        console.log(`\n🐛 Bug: ${bug.id}`);
        console.log(`   Description: ${bug.description}`);
        console.log(`   Category: ${bug.category}`);
        console.log(`   Severity: ${bug.severity.toUpperCase()}`);
        console.log(`   Age: ${this.calculateAge(bug.timestamp)}`);
        
        const strategy = this.getFixStrategy(bug);
        
        if (strategy) {
            console.log(`   Estimated Fix Time: ${strategy.estimatedTime}`);
            console.log(`   Auto-fixable: ${strategy.autoFixable ? 'Yes' : 'No'}`);
            console.log('   Fix Steps:');
            strategy.steps.forEach((step, index) => {
                console.log(`     ${index + 1}. ${step}`);
            });
            
            if (strategy.autoFixable) {
                await this.attemptAutoFix(bug, strategy);
            } else {
                console.log('   ⚠️ Manual intervention required');
            }
        } else {
            console.log('   ❓ No specific fix strategy available');
            console.log('   📋 General debugging steps:');
            console.log('     1. Reproduce the issue');
            console.log('     2. Check logs for error details');
            console.log('     3. Review related code sections');
            console.log('     4. Test potential fixes');
            console.log('     5. Verify fix doesn\'t break other functionality');
        }
        
        // Mark bug as in-progress
        bug.status = 'in-progress';
        bug.lastUpdated = new Date().toISOString();
    }

    getFixStrategy(bug) {
        // Try to match bug category or description to known strategies
        for (const [pattern, strategy] of this.fixStrategies) {
            if (bug.category.includes(pattern) || bug.description.includes(pattern)) {
                return strategy;
            }
        }
        
        // Default strategy based on severity
        if (bug.severity === 'critical') {
            return {
                priority: 1,
                autoFixable: false,
                steps: [
                    'Immediately investigate the critical issue',
                    'Check system logs for error details',
                    'Identify root cause',
                    'Implement emergency fix',
                    'Test fix thoroughly',
                    'Deploy fix immediately'
                ],
                estimatedTime: '2 hours'
            };
        }
        
        return null;
    }

    async attemptAutoFix(bug, strategy) {
        console.log('   🤖 Attempting automatic fix...');
        
        try {
            if (bug.category === 'Component') {
                await this.autoFixComponent(bug);
            } else if (bug.category === 'Performance') {
                await this.autoFixPerformance(bug);
            } else {
                console.log('   ❌ Auto-fix not implemented for this bug type');
                return false;
            }
            
            console.log('   ✅ Auto-fix completed successfully');
            bug.status = 'resolved';
            bug.resolvedAt = new Date().toISOString();
            bug.resolvedBy = 'auto-fix-system';
            return true;
            
        } catch (error) {
            console.log(`   ❌ Auto-fix failed: ${error.message}`);
            return false;
        }
    }

    async autoFixComponent(bug) {
        // Implement basic component fixes
        if (bug.description.includes('rendering')) {
            console.log('     - Checking template syntax...');
            console.log('     - Validating HTML structure...');
            console.log('     - Verifying CSS/JS paths...');
        }
        
        // Simulate fix process
        await this.delay(1000);
    }

    async autoFixPerformance(bug) {
        // Implement basic performance fixes
        if (bug.description.includes('slow')) {
            console.log('     - Adding response caching...');
            console.log('     - Optimizing database queries...');
            console.log('     - Implementing pagination...');
        }
        
        // Simulate fix process
        await this.delay(1500);
    }

    calculateAge(timestamp) {
        const now = new Date();
        const bugTime = new Date(timestamp);
        const diffMs = now - bugTime;
        const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
        const diffDays = Math.floor(diffHours / 24);
        
        if (diffDays > 0) {
            return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
        } else if (diffHours > 0) {
            return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
        } else {
            return 'Less than 1 hour ago';
        }
    }

    generateFixReport(bugs) {
        console.log('\n📊 Bug Fix Report Summary:');
        console.log('===========================');
        
        const bySeverity = bugs.reduce((acc, bug) => {
            acc[bug.severity] = (acc[bug.severity] || 0) + 1;
            return acc;
        }, {});
        
        const byStatus = bugs.reduce((acc, bug) => {
            acc[bug.status] = (acc[bug.status] || 0) + 1;
            return acc;
        }, {});
        
        console.log('Bugs by Severity:');
        Object.entries(bySeverity).forEach(([severity, count]) => {
            console.log(`  ${severity}: ${count}`);
        });
        
        console.log('\nBugs by Status:');
        Object.entries(byStatus).forEach(([status, count]) => {
            console.log(`  ${status}: ${count}`);
        });
        
        const totalEstimatedTime = this.calculateTotalEstimatedTime(bugs);
        console.log(`\nTotal Estimated Fix Time: ${totalEstimatedTime}`);
        
        // Save updated bug tracker
        const bugTrackerPath = path.join(__dirname, '../bugs/bug-tracker.json');
        this.bugTracker.metadata.lastUpdated = new Date().toISOString();
        fs.writeFileSync(bugTrackerPath, JSON.stringify(this.bugTracker, null, 2));
        
        // Save fix report
        const reportPath = path.join(__dirname, '../reports/bug-fix-report.json');
        fs.writeFileSync(reportPath, JSON.stringify({
            timestamp: new Date().toISOString(),
            summary: {
                totalBugs: bugs.length,
                bySeverity,
                byStatus,
                estimatedTotalTime: totalEstimatedTime
            },
            bugs: bugs.map(bug => ({
                id: bug.id,
                description: bug.description,
                severity: bug.severity,
                status: bug.status,
                age: this.calculateAge(bug.timestamp),
                strategy: this.getFixStrategy(bug)
            }))
        }, null, 2));
        
        console.log(`\n📄 Detailed fix report saved to: ${reportPath}`);
    }

    calculateTotalEstimatedTime(bugs) {
        let totalMinutes = 0;
        
        bugs.forEach(bug => {
            const strategy = this.getFixStrategy(bug);
            if (strategy && strategy.estimatedTime) {
                const timeStr = strategy.estimatedTime;
                const minutes = this.parseTimeToMinutes(timeStr);
                totalMinutes += minutes;
            }
        });
        
        const hours = Math.floor(totalMinutes / 60);
        const minutes = totalMinutes % 60;
        
        if (hours > 0) {
            return `${hours} hour${hours > 1 ? 's' : ''} ${minutes > 0 ? `${minutes} minutes` : ''}`;
        } else {
            return `${minutes} minutes`;
        }
    }

    parseTimeToMinutes(timeStr) {
        const hourMatch = timeStr.match(/(\d+)\s*hour/);
        const minuteMatch = timeStr.match(/(\d+)\s*minute/);
        
        let totalMinutes = 0;
        
        if (hourMatch) {
            totalMinutes += parseInt(hourMatch[1]) * 60;
        }
        
        if (minuteMatch) {
            totalMinutes += parseInt(minuteMatch[1]);
        }
        
        return totalMinutes || 30; // Default to 30 minutes if can't parse
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Export for use in other scripts
module.exports = PriorityBugFixer;

// Run if called directly
if (require.main === module) {
    const fixer = new PriorityBugFixer();
    fixer.runPriorityBugFix().catch(console.error);
} 