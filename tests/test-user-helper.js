
// Enhanced user registration with conflict handling
function generateUniqueTestUser() {
    const timestamp = Date.now();
    const random = Math.random().toString(36).substr(2, 9);
    return {
        email: `test-${timestamp}-${random}@example.com`,
        password: 'testpassword123',
        name: `Test User ${random}`
    };
}

// Use this in all test files for user registration
const testUser = generateUniqueTestUser();
