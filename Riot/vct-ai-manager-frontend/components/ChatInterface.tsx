'use client';

import { useState, useRef, useEffect } from 'react';
import axios from 'axios';

export default function ChatInterface() {
    const [messages, setMessages] = useState<Array<{ role: string; content: string }>>([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<null | HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(scrollToBottom, [messages]);

    const sendMessage = async () => {
        if (!input.trim() || isLoading) return;

        const newMessages = [...messages, { role: 'user', content: input }];
        setMessages(newMessages);
        setInput('');
        setIsLoading(true);

        try {
            const response = await axios.post('http://localhost:8000/chat', { message: input });
            const aiResponse = response.data.message;

            // 移除AI响应开头的"Assistant:"（如果存在）
            const cleanedResponse = aiResponse.replace(/^Assistant:\s*/i, '').trim();

            setMessages([...newMessages, { role: 'ai', content: cleanedResponse }]);
        } catch (error) {
            console.error('Error sending message:', error);
            setMessages([...newMessages, { role: 'ai', content: '抱歉，发生了错误。请稍后再试。' }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="w-full bg-dark-gray shadow-lg rounded-lg overflow-hidden border border-teal">
            <div className="bg-deep-blue text-white p-4">
                <h3 className="text-xl font-montserrat font-bold">AI 助手</h3>
            </div>
            <div className="h-96 overflow-y-auto p-4 bg-gray-800">
                {messages.map((msg, index) => (
                    <div key={index} className={`mb-4 ${msg.role === 'user' ? 'text-right' : 'text-left'}`}>
                        <span className={`inline-block p-3 rounded-lg ${msg.role === 'user' ? 'bg-teal text-white' : 'bg-gray-700 text-light-gray'
                            } shadow`}>
                            {msg.content}
                        </span>
                    </div>
                ))}
                <div ref={messagesEndRef} />
            </div>
            <div className="border-t border-teal p-4 bg-gray-900">
                <div className="flex items-center">
                    <input
                        className="flex-grow shadow-sm appearance-none border border-gray-700 rounded-l-lg w-full py-2 px-3 bg-gray-800 text-light-gray leading-tight focus:outline-none focus:ring-2 focus:ring-teal"
                        type="text"
                        placeholder="输入您的问题..."
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                    />
                    <button
                        className={`bg-gray-800 border border-gray-700 border-l-0 text-teal hover:text-white hover:bg-teal font-bold py-2 px-4 rounded-r-lg focus:outline-none focus:ring-2 focus:ring-teal transition duration-300 ${isLoading ? 'opacity-50 cursor-not-allowed' : ''
                            }`}
                        onClick={sendMessage}
                        disabled={isLoading}
                    >
                        {isLoading ? 'Sending...' : 'Sending'}
                    </button>
                </div>
            </div>
        </div>
    );
}