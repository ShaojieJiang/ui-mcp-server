import React, { useState, useEffect, useRef } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { Settings, Trash2 } from 'lucide-react';
import { ChatMessage } from './ChatMessage';
import { ChatInput, ChatInputValue } from './ChatInput';
import { DirectorySettings } from './DirectorySettings';
import { AgentService, MessageContent } from '../services/agent';
import { Message, UIComponent } from '../types/ui-components';
import { Card, CardHeader, CardTitle } from './ui/Card';
import { Button } from './ui/Button';

export const Chat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [sessionId] = useState(() => uuidv4());
  const [agent] = useState(() => new AgentService(sessionId, '/api'));
  const [showDirectorySettings, setShowDirectorySettings] = useState(false);
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
        const convertedMessages: Message[] = pastMessages
          .filter((msg) => {
            // Filter out failed tool calls from past messages too
            if (msg.type === 'tool' && msg.content) {
              try {
                JSON.parse(msg.content as string);
                return true;
              } catch (error) {
                console.log(
                  'Filtering out failed tool call from history:',
                  msg.content
                );
                return false;
              }
            }
            return true;
          })
          .map((msg) => ({
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

  const handleSendMessage = async (input: ChatInputValue) => {
    if (loading) return;

    // Create display content for the user message
    const displayContent: MessageContent[] = [];
    if (input.text) {
      displayContent.push({ type: 'text' as const, text: input.text });
    }
    for (const file of input.files) {
      displayContent.push({
        type: 'image_url' as const,
        image_url: { url: URL.createObjectURL(file) },
      });
    }

    const userMessage: Message = {
      id: uuidv4(),
      type: 'human',
      content:
        displayContent.length === 1 && displayContent[0].type === 'text'
          ? displayContent[0].text || ''
          : displayContent,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const response = await agent.getResponse(input);

      const newMessages: Message[] = response
        .filter((msg) => {
          // Filter out the echo of user's message
          if (msg.type === 'human') return false;

          // Filter out empty AI messages
          if (
            msg.type === 'ai' &&
            (!msg.content ||
              (typeof msg.content === 'string' && msg.content.trim() === ''))
          )
            return false;

          // Filter out failed tool calls (tool messages that don't contain valid JSON)
          if (msg.type === 'tool' && msg.content) {
            try {
              JSON.parse(msg.content as string);
              return true;
            } catch (error) {
              console.log(
                'Filtering out failed tool call with invalid JSON:',
                msg.content
              );
              return false;
            }
          }

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

      const component: UIComponent = JSON.parse(message.content as string);
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
      const componentLabel = (component as any).label || 'component';
      const followUpContent = `My input to ${componentLabel} is ${value}`;
      await handleSendMessage({ text: followUpContent, files: [] });
    } catch (error) {
      console.error('Failed to submit component value:', error);
    }
  };

  const handleClearChat = async () => {
    try {
      await agent.clearHistory();
      setMessages([]);
    } catch (error) {
      console.error('Failed to clear chat history:', error);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-background">
      <Card className="m-4 mb-0">
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="text-center flex-1">
              Chat with UI MCP Server
            </CardTitle>
            <div className="flex items-center gap-2">
              <Button
                variant="ghost"
                size="sm"
                onClick={handleClearChat}
                className="flex items-center gap-2"
              >
                <Trash2 className="w-4 h-4" />
                Clear Chat
              </Button>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowDirectorySettings(true)}
                className="flex items-center gap-2"
              >
                <Settings className="w-4 h-4" />
                Local Files
              </Button>
            </div>
          </div>
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
            onRequestDirectoryAccess={() => setShowDirectorySettings(true)}
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

      <DirectorySettings
        isVisible={showDirectorySettings}
        onClose={() => setShowDirectorySettings(false)}
      />
    </div>
  );
};
