import React, { useState, useEffect, useRef } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { ChatMessage } from './ChatMessage';
import { ChatInput } from './ChatInput';
import { AgentService } from '../services/agent';
import { Message, UIComponent } from '../types/ui-components';
import { Card, CardHeader, CardTitle } from './ui/Card';

export const Chat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [sessionId] = useState(() => uuidv4());
  const [agent] = useState(() => new AgentService(sessionId));
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Load past messages on component mount
    const loadPastMessages = async () => {
      try {
        const pastMessages = await agent.getPastMessages();
        const convertedMessages: Message[] = pastMessages.map((msg) => ({
          id: msg.id || uuidv4(),
          type:
            msg.role === 'human'
              ? 'human'
              : msg.type === 'tool'
                ? 'tool'
                : 'ai',
          content: msg.content,
          tool_call_id: msg.tool_call_id,
          timestamp: new Date(),
        }));
        setMessages(convertedMessages);
      } catch (error) {
        console.error('Failed to load past messages:', error);
      }
    };

    loadPastMessages();
  }, [agent]);

  const handleSendMessage = async (content: string) => {
    if (loading) return;

    const userMessage: Message = {
      id: uuidv4(),
      type: 'human',
      content,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const response = await agent.getResponse(content);

      const newMessages: Message[] = response
        .filter((msg) => {
          // Filter out the echo of user's message
          if (msg.type === 'human') return false;

          // Filter out empty AI messages
          if (msg.type === 'ai' && (!msg.content || msg.content.trim() === ''))
            return false;

          return true;
        })
        .map((msg) => ({
          id: msg.id || uuidv4(),
          type: msg.type === 'tool' ? 'tool' : 'ai',
          content: msg.content,
          tool_call_id: msg.tool_call_id,
          timestamp: new Date(),
        }));

      setMessages((prev) => [...prev, ...newMessages]);
    } catch (error) {
      console.error('Failed to get response:', error);
      const errorMessage: Message = {
        id: uuidv4(),
        type: 'ai',
        content:
          'Sorry, I encountered an error while processing your request. Please make sure the backend server is running.',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleComponentSubmit = async (messageId: string, value: any) => {
    try {
      // Find the message and update its component value
      const message = messages.find((m) => m.id === messageId);
      if (!message) return;

      const component: UIComponent = JSON.parse(message.content);
      const updatedComponent = { ...component, value };

      const updatedMessage = {
        ...message,
        content: JSON.stringify(updatedComponent),
      };

      // Update the message in the agent's state
      await agent.updateMessage({
        role: 'tool',
        content: updatedMessage.content,
        type: 'tool',
        tool_call_id: message.tool_call_id,
        id: message.id,
      });

      // Update local state
      setMessages((prev) =>
        prev.map((m) => (m.id === messageId ? updatedMessage : m))
      );

      // Send follow-up message about the input
      const followUpContent = `My input to ${component.label} is ${value}`;
      await handleSendMessage(followUpContent);
    } catch (error) {
      console.error('Failed to submit component value:', error);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-background">
      <Card className="m-4 mb-0">
        <CardHeader>
          <CardTitle className="text-center">Chat with UI MCP Server</CardTitle>
        </CardHeader>
      </Card>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && !loading && (
          <div className="text-center text-muted-foreground py-8">
            <p>Start a conversation by asking for UI components!</p>
            <p className="text-sm mt-2">
              Try: "Create a number input for age between 0 and 100"
            </p>
          </div>
        )}

        {messages.map((message) => (
          <ChatMessage
            key={message.id}
            message={message}
            onComponentSubmit={handleComponentSubmit}
          />
        ))}

        {loading && (
          <div className="flex justify-center py-4">
            <div className="animate-pulse text-muted-foreground">
              Thinking...
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <ChatInput onSendMessage={handleSendMessage} loading={loading} />
    </div>
  );
};
