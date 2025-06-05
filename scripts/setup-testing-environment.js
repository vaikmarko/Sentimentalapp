const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class TestingEnvironmentSetup {
    constructor() {
        this.requiredDirectories = [
            'tests',
            'bugs',
            'reports',
            'scripts',
            'prompts'
        ];
        
        this.requiredFiles = [
            'bugs/bug-tracker.json',
            'bugs/share-issues.json',
            'bugs/stories-issues.json',
            'bugs/space-issues.json',
            'bugs/discover-issues.json',
            'bugs/performance-issues.json'
        ];
    }

    async setup() {
        console.log('🚀 Setting up Sentimental App Testing Environment');
        console.log('================================================\n');

        try {
            await this.checkPrerequisites();
            await this.createDirectories();
            await this.validateFiles();
            await this.installDependencies();
            await this.validateSetup();
            
            console.log('\n✅ Testing environment setup complete!');
            console.log('\n🎯 Next steps:');
            console.log('1. Start your Sentimental App server: python app.py');
            console.log('2. Run the complete test suite: npm run test:all');
            console.log('3. Check the generated reports in /reports/ directory');
            
        } catch (error) {
            console.error('❌ Setup failed:', error.message);
            process.exit(1);
        }
    }

    async checkPrerequisites() {
        console.log('🔍 Checking prerequisites...');
        
        // Check Node.js version
        try {
            const nodeVersion = execSync('node --version', { encoding: 'utf8' }).trim();
            const majorVersion = parseInt(nodeVersion.slice(1).split('.')[0]);
            
            if (majorVersion < 16) {
                throw new Error(`Node.js 16+ required, found ${nodeVersion}`);
            }
            
            console.log(`✅ Node.js ${nodeVersion} found`);
        } catch (error) {
            throw new Error('Node.js not found or version too old');
        }

        // Check npm
        try {
            const npmVersion = execSync('npm --version', { encoding: 'utf8' }).trim();
            console.log(`✅ npm ${npmVersion} found`);
        } catch (error) {
            throw new Error('npm not found');
        }

        // Check Python
        try {
            const pythonVersion = execSync('python --version', { encoding: 'utf8' }).trim();
            console.log(`✅ ${pythonVersion} found`);
        } catch (error) {
            console.log('⚠️ Python not found on PATH (may be python3)');
        }

        // Check if app.py exists
        if (fs.existsSync('app.py')) {
            console.log('✅ app.py found');
        } else {
            console.log('⚠️ app.py not found - ensure you\'re in the correct directory');
        }
    }

    async createDirectories() {
        console.log('\n📁 Creating required directories...');
        
        for (const dir of this.requiredDirectories) {
            if (!fs.existsSync(dir)) {
                fs.mkdirSync(dir, { recursive: true });
                console.log(`✅ Created directory: ${dir}`);
            } else {
                console.log(`✓ Directory exists: ${dir}`);
            }
        }
    }

    async validateFiles() {
        console.log('\n📄 Validating required files...');
        
        for (const file of this.requiredFiles) {
            if (fs.existsSync(file)) {
                console.log(`✓ File exists: ${file}`);
            } else {
                console.log(`⚠️ File missing: ${file} (will be created by tests)`);
            }
        }

        // Check if package.json exists
        if (fs.existsSync('package.json')) {
            console.log('✅ package.json found');
        } else {
            console.log('⚠️ package.json not found - npm scripts may not work');
        }
    }

    async installDependencies() {
        console.log('\n📦 Installing Node.js dependencies...');
        
        try {
            // Check if package.json exists before installing
            if (fs.existsSync('package.json')) {
                console.log('Installing npm packages...');
                execSync('npm install', { stdio: 'inherit' });
                console.log('✅ Node.js dependencies installed');
            } else {
                console.log('⚠️ Skipping npm install - package.json not found');
            }
        } catch (error) {
            console.log('⚠️ npm install failed - you may need to install dependencies manually');
        }

        // Check Python dependencies
        console.log('\n🐍 Checking Python dependencies...');
        try {
            execSync('pip list | grep Flask', { stdio: 'pipe' });
            console.log('✅ Flask found');
        } catch (error) {
            console.log('⚠️ Flask not found - install with: pip install -r requirements.txt');
        }

        try {
            execSync('pip list | grep firebase-admin', { stdio: 'pipe' });
            console.log('✅ firebase-admin found');
        } catch (error) {
            console.log('⚠️ firebase-admin not found - install with: pip install -r requirements.txt');
        }
    }

    async validateSetup() {
        console.log('\n🔧 Validating setup...');
        
        // Check if test files exist
        const testFiles = [
            'tests/automated-test-suite.js',
            'tests/database-tests.js',
            'tests/api-tests.js',
            'tests/user-flow-tests.js'
        ];

        let testFilesFound = 0;
        for (const file of testFiles) {
            if (fs.existsSync(file)) {
                testFilesFound++;
                console.log(`✅ Test file found: ${file}`);
            } else {
                console.log(`❌ Test file missing: ${file}`);
            }
        }

        if (testFilesFound === testFiles.length) {
            console.log('✅ All test files found');
        } else {
            console.log(`⚠️ ${testFiles.length - testFilesFound} test files missing`);
        }

        // Check script files
        const scriptFiles = [
            'scripts/run-all-tests.js',
            'scripts/fix-priority-bugs.js'
        ];

        let scriptFilesFound = 0;
        for (const file of scriptFiles) {
            if (fs.existsSync(file)) {
                scriptFilesFound++;
                console.log(`✅ Script file found: ${file}`);
            } else {
                console.log(`❌ Script file missing: ${file}`);
            }
        }

        if (scriptFilesFound === scriptFiles.length) {
            console.log('✅ All script files found');
        } else {
            console.log(`⚠️ ${scriptFiles.length - scriptFilesFound} script files missing`);
        }
    }

    generateQuickStartGuide() {
        const guide = `
# Sentimental App Testing - Quick Start Guide

## 🚀 Getting Started

### 1. Start the Sentimental App
\`\`\`bash
python app.py
\`\`\`

### 2. Run All Tests
\`\`\`bash
npm run test:all
\`\`\`

### 3. Check Results
- View reports in \`/reports/\` directory
- Check bugs in \`/bugs/\` directory
- Read \`test-summary.md\` for overview

## 🔧 Individual Commands

### Testing
- \`npm run test:database\` - Test database operations
- \`npm run test:api\` - Test API endpoints
- \`npm run test:user-flows\` - Test user journeys
- \`npm run test:automated\` - Run automated test suite

### Bug Fixing
- \`npm run fix:bugs\` - Fix priority bugs
- \`npm run fix:critical\` - Fix critical bugs only

### Health Checks
- \`npm run health:check\` - System health overview
- \`npm run health:component\` - Component health details

## 📊 Understanding Results

### Test Status
- ✅ PASS - Test completed successfully
- ❌ FAIL - Test failed, needs attention
- ⏭️ SKIP - Test skipped (usually due to missing data)

### Bug Severity
- 🚨 CRITICAL - Fix immediately
- 🔥 HIGH - Fix within 24 hours
- ⚠️ MEDIUM - Fix within 1 week
- 📝 LOW - Fix when time permits

## 🆘 Troubleshooting

### Server Connection Issues
1. Ensure app is running: \`python app.py\`
2. Check port: \`curl http://localhost:5000/api/stories\`
3. Verify Firebase credentials

### Test Failures
1. Check \`/reports/\` for detailed error logs
2. Run individual test suites to isolate issues
3. Review \`/bugs/\` for known issues

### Dependencies
1. Node.js issues: \`npm install\`
2. Python issues: \`pip install -r requirements.txt\`

---
Generated by Sentimental App Testing Setup
`;

        fs.writeFileSync('QUICK_START.md', guide);
        console.log('📝 Quick start guide created: QUICK_START.md');
    }
}

// Run setup if called directly
if (require.main === module) {
    const setup = new TestingEnvironmentSetup();
    setup.setup().then(() => {
        setup.generateQuickStartGuide();
    }).catch(console.error);
}

module.exports = TestingEnvironmentSetup; 