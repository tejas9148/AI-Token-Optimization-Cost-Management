import React, { useState, useEffect } from 'react';
import { useApi } from '../../hooks/useApi';
import type { ChatResponse } from '../../types/api';

const Chat: React.FC = () => {
  const { request, loading, error } = useApi();
  const [messages, setMessages] = useState<Array<{ role: 'user' | 'assistant'; content: string; timestamp: string }>>([]);
  const [input, setInput] = useState('');
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = {
      role: 'user' as const,
      content: input,
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    const response = await request<ChatResponse>('/chat', 'POST', {
      conversation_id: conversationId,
      user_message: input,
    });

    if (response.data && !response.error) {
      setConversationId(response.data.conversation_id);

      const assistantMessage = {
        role: 'assistant' as const,
        content: response.data.assistant_message,
        timestamp: new Date().toISOString(),
      };

      setMessages(prev => [...prev, assistantMessage]);
    } else {
      // Handle error - you could set an error state here
      console.error('Error:', response.error);
      // Remove the user message we just added since it failed
      setMessages(prev => prev.slice(0, -1));
    }

    setIsLoading(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  // Clear conversation button
  const clearConversation = () => {
    setMessages([]);
    setConversationId(null);
  };

  return (
    <div className="space-y-6 p-6">
      <div className="flex justify-between items-start">
        <h1 className="text-2xl font-bold">Chat - AI Conversations</h1>
        <div className="text-sm text-muted-foreground">
          Have conversations with automatic context compression
        </div>
      </div>

      {/* Chat Controls */}
      <div className="flex justify-end space-x-3">
        <button
          onClick={clearConversation}
          className="px-4 py-2 bg-muted text-muted-foreground hover:bg-muted/80 transition-colors rounded-md"
        >
          New Chat
        </button>
      </div>

      {/* Messages Container */}
      <div className="bg-card text-card-foreground shadow-sm rounded-lg border border-border p-4 h-[60vh] overflow-y-auto">
        {messages.length === 0 ? (
          <div className="text-center text-muted-foreground py-8">
            <p>Start a conversation by typing a message below.</p>
          </div>
        ) : (
          <div className="space-y-4">
            {messages.map((msg, index) => (
              <div key={index} className={msg.role === 'user' ? 'ml-auto' : 'mr-auto'}>
                <div className={`max-w-xs rounded-xl px-4 py-2 ${
                  msg.role === 'user' ? 'bg-primary text-primary-foreground' : 'bg-muted text-muted-foreground'
                }`}>
                  <p className="whitespace-pre-wrap">{msg.content}</p>
                  <span className="text-xs block text-opacity-70 mt-1">
                    {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="flex space-x-3">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          rows={2}
          placeholder="Type a message..."
          className="flex-1 min-h-[44px] w-0 px-4 py-2 bg-input text-input-foreground border border-input placeholder:text-muted-foreground/50 focus:ring-2 focus:ring-primary focus:ring-offset-0 disabled:opacity-50 resize-none"
          disabled={isLoading}
        />
        <button
          onClick={sendMessage}
          disabled={isLoading || !input.trim()}
          className="px-6 py-2 bg-primary text-primary-foreground hover:bg-primary/90 transition-colors disabled:opacity-50"
        >
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </div>

      {/* Loading State */}
      {loading && messages.length === 0 && (
        <div className="flex min-h-[200px] items-center justify-center">
          <div className="text-muted-foreground">Loading...</div>
        </div>
      )}

      {/* Error State */}
      {error && messages.length === 0 && (
        <div className="flex min-h-[200px] items-center justify-center text-red-500">
          Error: {error}
        </div>
      )}
    </div>
  );
};

export default Chat;