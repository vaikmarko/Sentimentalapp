console.log('Simple JS file loaded!');

// Simple React app without JSX
const SimpleApp = () => {
  React.useEffect(() => {
    console.log('SimpleApp mounted!');
    // Hide loading screen
    const loadingElement = document.getElementById('loading');
    if (loadingElement) {
      loadingElement.style.display = 'none';
    }
  }, []);

  return React.createElement('div', { 
    style: { 
      padding: '40px', 
      textAlign: 'center',
      fontFamily: 'system-ui, -apple-system, sans-serif',
      maxWidth: '800px',
      margin: '0 auto'
    } 
  }, [
    React.createElement('h1', { 
      key: 'title',
      style: {
        background: 'linear-gradient(to right, #9333ea, #ec4899)',
        WebkitBackgroundClip: 'text',
        WebkitTextFillColor: 'transparent',
        fontSize: '3rem',
        marginBottom: '1rem'
      }
    }, 'Sentimental'),
    React.createElement('p', { 
      key: 'desc',
      style: {
        color: '#6b7280',
        fontSize: '1.2rem',
        marginBottom: '2rem'
      }
    }, 'Your Life, Your Story'),
    React.createElement('div', {
      key: 'content',
      style: {
        background: 'white',
        padding: '2rem',
        borderRadius: '1rem',
        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
        border: '1px solid #e5e7eb'
      }
    }, [
      React.createElement('h2', { key: 'welcome' }, 'Welcome to SentimentalApp!'),
      React.createElement('p', { key: 'message' }, 'The app is now loading successfully. We fixed all the deployment issues!')
    ])
  ]);
};

// Initialize the app
console.log('Initializing simple app...');
ReactDOM.render(React.createElement(SimpleApp), document.getElementById('sentimental-app'));

