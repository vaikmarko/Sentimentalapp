console.log('Test JSX file loaded!');

const TestApp = () => {
  React.useEffect(() => {
    console.log('TestApp mounted!');
    const loadingElement = document.getElementById('loading');
    if (loadingElement) {
      loadingElement.style.display = 'none';
    }
  }, []);

  return React.createElement('div', { 
    style: { 
      padding: '20px', 
      textAlign: 'center',
      fontFamily: 'system-ui, -apple-system, sans-serif'
    } 
  }, [
    React.createElement('h1', { key: 'title' }, 'SentimentalApp Test'),
    React.createElement('p', { key: 'desc' }, 'If you see this, React is working!')
  ]);
};

// Initialize the test app
console.log('Initializing test app...');
ReactDOM.render(React.createElement(TestApp), document.getElementById('sentimental-app'));

