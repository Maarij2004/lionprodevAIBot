// import { useState, useRef, useEffect } from 'react';
// import './App.css';

// function App() {
//     const [promptArea, setPromptArea] = useState('');
//     const [chatHistory, setChatHistory] = useState([
//         { sender: 'bot', message: 'Hi there 👋\nWe typically reply within a few minutes.' },
//     ]);
//     const [isLoading, setIsLoading] = useState(false);
//     const messagesEndRef = useRef(null); // Reference for auto-scrolling

//     // Auto-scroll to the bottom whenever the chatHistory changes
//     useEffect(() => {
//         if (messagesEndRef.current) {
//             messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
//         }
//     }, [chatHistory]);

//     const handleSubmit = async () => {
//         const userMessage = promptArea.trim();
//         if (!userMessage) return;

//         // Add user's message to chat history
//         setChatHistory((prev) => [
//             ...prev,
//             { sender: 'user', message: userMessage },
//         ]);
//         setPromptArea(''); // Clear the input after submitting
//         setIsLoading(true); // Start loading

//         const url = 'http://localhost:3050/api/prompt';
//         let tmpPromptResponse = '';
//         try {
//             const response = await fetch(url, {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json',
//                 },
//                 body: JSON.stringify({ prompt: userMessage }),
//             });

//             if (!response.body) throw new Error('No response body');

//             const reader = response.body.getReader();
//             const decoder = new TextDecoder();

//             while (true) {
//                 const { value, done } = await reader.read();
//                 if (done) break;

//                 tmpPromptResponse += decoder.decode(value, { stream: true });
//             }

//             // Fix: Adding line breaks and sanitizing for asterisks or any unwanted characters
//             tmpPromptResponse = tmpPromptResponse.replace(/\*/g, '');  // Remove asterisks (if any)
//             tmpPromptResponse = tmpPromptResponse.replace(/\n/g, '<br />');  // Adding line breaks

//             // Once the full response is received, update the state
//             setChatHistory((prev) => [
//                 ...prev,
//                 { sender: 'bot', message: tmpPromptResponse },
//             ]);
//         } catch (error) {
//             console.error('Error:', error);
//             setChatHistory((prev) => [
//                 ...prev,
//                 { sender: 'bot', message: 'Error communicating with the server.' },
//             ]);
//         } finally {
//             setIsLoading(false); // End loading
//         }
//     };

//     const handleKeyPress = (e) => {
//         if (e.key === 'Enter' && !e.shiftKey) {
//             e.preventDefault(); // Prevent default behavior of Enter key (adding new line)
//             handleSubmit();
//         }
//     };

//     return (
//         <div className="chat-container">
//             <div className="chat-card">
//                 <div className="chat-header">
//                     <h2>Chat with Our AI</h2>
//                 </div>
//                 <div className="chat-box">
//                     <div className="messages">
//                         {chatHistory.map((msg, index) => (
//                             <div
//                                 key={index}
//                                 className={`message ${msg.sender}`}
//                                 dangerouslySetInnerHTML={{ __html: msg.message }} // Render message with HTML (line breaks)
//                             >
//                             </div>
//                         ))}
//                         <div ref={messagesEndRef} /> {/* Scroll reference */}
//                     </div>
//                 </div>
//                 <div className="chat-input">
//                     <textarea
//                         className="input-textarea"
//                         rows={2}
//                         placeholder="Type your message..."
//                         onChange={(e) => setPromptArea(e.target.value)}
//                         value={promptArea}
//                         onKeyDown={handleKeyPress} // Listen for Enter key
//                     />
//                     <button className="send-button" onClick={handleSubmit} disabled={isLoading}>
//                         {isLoading ? 'Sending...' : 'Send'}
//                     </button>
//                 </div>
//             </div>
//         </div>
//     );
// }

// export default App;


import { useState, useRef, useEffect } from 'react';
import './App.css';

function App() {
    const [promptArea, setPromptArea] = useState('');
    const [chatHistory, setChatHistory] = useState([
        { sender: 'bot', message: 'Hello! How can I assist you today?' },
    ]);
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    useEffect(() => {
        if (messagesEndRef.current) {
            messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, [chatHistory]);

    const handleSubmit = async () => {
        const userMessage = promptArea.trim();
        if (!userMessage) return;

        setChatHistory((prev) => [
            ...prev,
            { sender: 'user', message: userMessage },
        ]);
        setPromptArea('');
        setIsLoading(true);

        const url = 'http://localhost:3050/api/prompt';
        let tmpPromptResponse = '';
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt: userMessage }),
            });

            if (!response.body) throw new Error('No response body');

            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            while (true) {
                const { value, done } = await reader.read();
                if (done) break;

                tmpPromptResponse += decoder.decode(value, { stream: true });
            }

            tmpPromptResponse = tmpPromptResponse.replace(/\*/g, '');
            tmpPromptResponse = tmpPromptResponse.replace(/\n/g, '<br />');

            setChatHistory((prev) => [
                ...prev,
                { sender: 'bot', message: tmpPromptResponse },
            ]);
        } catch (error) {
            console.error('Error:', error);
            setChatHistory((prev) => [
                ...prev,
                { sender: 'bot', message: 'Error communicating with the server.' },
            ]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit();
        }
    };

    return (
        <div className="chat-container">
            <div className="chat-card">
                <div className="chat-header">
                    <div className="header-content">
                        <h2>Lion Pro Dev AI Assistant</h2>
                        <div className="status-indicator">
                            <span className="status-dot"></span>
                            <span>Online</span>
                        </div>
                    </div>
                </div>
                <div className="chat-box">
                    <div className="messages">
                        {chatHistory.map((msg, index) => (
                            <div
                                key={index}
                                className={`message ${msg.sender}`}
                                dangerouslySetInnerHTML={{ __html: msg.message }}
                            />
                        ))}
                        <div ref={messagesEndRef} />
                    </div>
                </div>
                <div className="chat-input">
                    <textarea
                        className="input-textarea"
                        rows={2}
                        placeholder="Type your message..."
                        onChange={(e) => setPromptArea(e.target.value)}
                        value={promptArea}
                        onKeyDown={handleKeyPress}
                    />
                    <button className="send-button" onClick={handleSubmit} disabled={isLoading}>
                        {isLoading ? (
                            <span className="loading-dots">
                                <span>.</span><span>.</span><span>.</span>
                            </span>
                        ) : (
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                                <path d="M22 2L11 13" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                                <path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                            </svg>
                        )}
                    </button>
                </div>
            </div>
        </div>
    );
}

export default App;