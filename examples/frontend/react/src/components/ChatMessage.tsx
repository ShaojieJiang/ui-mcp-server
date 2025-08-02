import React from 'react';
import { User, Bot, Wrench } from 'lucide-react';
import { Card, CardContent } from './ui/Card';
import { UIComponentRenderer } from './UIComponentRenderer';
import { Message, UIComponent } from '../types/ui-components';
import { cn } from '../lib/utils';

interface ChatMessageProps {
  message: Message;
  onComponentSubmit?: (messageId: string, value: any) => void;
  onRequestDirectoryAccess?: () => void;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({
  message,
  onComponentSubmit,
  onRequestDirectoryAccess,
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
    if (isUser) return 'bg-blue-500 text-white ml-12';
    if (isTool) return 'bg-accent text-accent-foreground';
    return 'bg-muted text-muted-foreground mr-12';
  };

  const renderContent = () => {
    if (isTool && message.content) {
      try {
        const component: UIComponent = JSON.parse(message.content as string);

        // Check if component type is valid before rendering
        const validInputTypes = [
          'number_input',
          'slider',
          'radio',
          'multiselect',
          'color_picker',
          'date_input',
          'time_input',
          'audio_input',
          'camera_input',
        ];

        const validOutputTypes = [
          'line',
          'bar',
          'scatter',
          'image',
          'audio',
          'video',
        ];

        const isValidComponent =
          validInputTypes.includes(component.type) ||
          validOutputTypes.includes(component.type);

        if (!isValidComponent) {
          console.log(
            'Filtering out tool message with invalid component type:',
            component.type
          );
          return null;
        }

        return (
          <UIComponentRenderer
            component={component}
            onSubmit={(value) => onComponentSubmit?.(message.id, value)}
            onRequestDirectoryAccess={onRequestDirectoryAccess}
          />
        );
      } catch (error) {
        // If parsing fails, don't render anything - this message should have been filtered out
        console.error('Failed to parse tool message content:', error);
        return null;
      }
    }

    // Handle multi-content messages (text + images)
    if (Array.isArray(message.content)) {
      return (
        <div className="space-y-2">
          {message.content.map((content, index) => (
            <div key={index}>
              {content.type === 'text' && content.text && (
                <div className="whitespace-pre-wrap break-words">
                  {content.text}
                </div>
              )}
              {content.type === 'image_url' && content.image_url && (
                <img
                  src={content.image_url.url}
                  alt="Uploaded image"
                  className="max-w-sm rounded-lg border"
                />
              )}
            </div>
          ))}
        </div>
      );
    }

    // Handle simple string content
    return (
      <div className="whitespace-pre-wrap break-words">{message.content}</div>
    );
  };

  const content = renderContent();

  // Don't render anything if content is null (failed tool calls)
  if (content === null) {
    return null;
  }

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
          <CardContent className="p-4">{content}</CardContent>
        </Card>
      </div>

      {isUser && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-blue-500 text-white flex items-center justify-center">
          {getIcon()}
        </div>
      )}
    </div>
  );
};
