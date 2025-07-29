import React from 'react';
import { User, Bot, Wrench } from 'lucide-react';
import { Card, CardContent } from './ui/Card';
import { UIComponentRenderer } from './UIComponentRenderer';
import { Message, UIComponent } from '../types/ui-components';
import { cn } from '../lib/utils';

interface ChatMessageProps {
  message: Message;
  onComponentSubmit?: (messageId: string, value: any) => void;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({
  message,
  onComponentSubmit,
}) => {
  const isUser = message.type === 'human';
  const isAI = message.type === 'ai';
  const isTool = message.type === 'tool';

  const getIcon = () => {
    if (isUser) return <User className="w-5 h-5" />;
    if (isTool) return <Wrench className="w-5 h-5" />;
    return <Bot className="w-5 h-5" />;
  };

  const getMessageStyle = () => {
    if (isUser) return 'bg-primary text-primary-foreground ml-12';
    if (isTool) return 'bg-accent text-accent-foreground';
    return 'bg-muted text-muted-foreground mr-12';
  };

  const renderContent = () => {
    if (isTool && message.content) {
      try {
        const component: UIComponent = JSON.parse(message.content);
        return (
          <UIComponentRenderer
            component={component}
            onSubmit={(value) => onComponentSubmit?.(message.id, value)}
          />
        );
      } catch (error) {
        console.error('Failed to parse tool message content:', error);
        return (
          <div className="text-destructive">Failed to render UI component</div>
        );
      }
    }

    return (
      <div className="whitespace-pre-wrap break-words">{message.content}</div>
    );
  };

  return (
    <div
      className={cn(
        'flex gap-3 max-w-4xl mx-auto p-4',
        isUser && 'justify-end'
      )}
    >
      {!isUser && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-secondary flex items-center justify-center">
          {getIcon()}
        </div>
      )}

      <div className={cn('flex-1 min-w-0', isUser && 'flex justify-end')}>
        <Card className={cn('max-w-3xl', getMessageStyle())}>
          <CardContent className="p-4">{renderContent()}</CardContent>
        </Card>
      </div>

      {isUser && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary flex items-center justify-center">
          {getIcon()}
        </div>
      )}
    </div>
  );
};
