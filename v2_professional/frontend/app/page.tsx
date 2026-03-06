"use client";
import React, { useState, useRef, useEffect } from 'react';
import { Send, Upload, FileText, Bot, User, Loader2 } from 'lucide-react';
import axios from 'axios';

interface Message {
    role: 'user' | 'assistant';
    content: string;
    sources?: string[];
}

export default function ChatPage() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [isUploading, setIsUploading] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [file, setFile] = useState<File | null>(null);
    const scrollRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFile = e.target.files?.[0];
        if (!selectedFile) return;

        setFile(selectedFile);
        setIsUploading(true);

        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            await axios.post('http://localhost:8000/upload', formData);
            setMessages([{ role: 'assistant', content: `Success! I've indexed ${selectedFile.name}. You can now ask questions about it.` }]);
        } catch (error) {
            setMessages([{ role: 'assistant', content: "Failed to upload document. Please try again." }]);
        } finally {
            setIsUploading(false);
        }
    };

    const handleSend = async () => {
        if (!input.trim() || isLoading) return;

        const userMsg = { role: 'user' as const, content: input };
        setMessages(prev => [...prev, userMsg]);
        setInput('');
        setIsLoading(true);

        try {
            const { data } = await axios.post('http://localhost:8000/chat', { message: input });
            setMessages(prev => [...prev, { role: 'assistant', content: data.answer, sources: data.sources }]);
        } catch (error) {
            setMessages(prev => [...prev, { role: 'assistant', content: "Sorry, I encountered an error processing your request." }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-screen bg-slate-50">
            {/* Header */}
            <header className="bg-white border-b px-6 py-4 flex justify-between items-center shadow-sm">
                <div className="flex items-center gap-2">
                    <div className="bg-blue-600 p-2 rounded-lg">
                        <Bot className="text-white" size={24} />
                    </div>
                    <h1 className="font-bold text-xl text-slate-800">AI Policy Navigator Pro</h1>
                </div>

                <label className="flex items-center gap-2 bg-slate-100 hover:bg-slate-200 px-4 py-2 rounded-full cursor-pointer transition-all border border-slate-200">
                    {isUploading ? <Loader2 className="animate-spin text-blue-600" size={20} /> : <Upload size={20} className="text-slate-600" />}
                    <span className="text-sm font-medium text-slate-700">{file ? file.name : 'Upload Document'}</span>
                    <input type="file" className="hidden" onChange={handleUpload} accept=".pdf,.docx,.txt" />
                </label>
            </header>

            {/* Chat Area */}
            <main className="flex-1 overflow-y-auto p-6 space-y-6">
                {messages.length === 0 && (
                    <div className="h-full flex flex-col items-center justify-center text-slate-400 space-y-4">
                        <FileText size={64} strokeWidth={1} />
                        <p className="text-lg">Upload a PDF, DOCX, or TXT to start your analysis</p>
                    </div>
                )}

                {messages.map((m, i) => (
                    <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-[80%] p-4 rounded-2xl shadow-sm ${m.role === 'user'
                                ? 'bg-blue-600 text-white rounded-tr-none'
                                : 'bg-white text-slate-800 rounded-tl-none border border-slate-100'
                            }`}>
                            <div className="flex items-center gap-2 mb-2">
                                {m.role === 'assistant' ? <Bot size={16} /> : <User size={16} />}
                                <span className="text-xs font-bold uppercase tracking-wider">
                                    {m.role === 'assistant' ? 'AI Assistant' : 'You'}
                                </span>
                            </div>
                            <p className="leading-relaxed whitespace-pre-wrap">{m.content}</p>
                            {m.sources && m.sources.length > 0 && (
                                <div className="mt-4 pt-2 border-t border-slate-100 text-[10px] font-mono text-slate-500 italic">
                                    Sources: {m.sources.join(', ')}
                                </div>
                            )}
                        </div>
                    </div>
                ))}
                <div ref={scrollRef} />
            </main>

            {/* Input Area */}
            <footer className="bg-white border-t p-6">
                <div className="max-w-4xl mx-auto flex gap-4">
                    <input
                        className="flex-1 bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all text-slate-800"
                        placeholder="Ask anything about the policy..."
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                    />
                    <button
                        className="bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-xl disabled:opacity-50 transition-all"
                        onClick={handleSend}
                        disabled={!file || isLoading}
                    >
                        {isLoading ? <Loader2 className="animate-spin" size={24} /> : <Send size={24} />}
                    </button>
                </div>
            </footer>
        </div>
    );
}
