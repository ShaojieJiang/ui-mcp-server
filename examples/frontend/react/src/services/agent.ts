import { Client } from '@langchain/langgraph-sdk';

export interface MessageContent {
  type: 'text' | 'image_url';
  text?: string;
  image_url?: {
    url: string;
  };
}

export interface AgentMessage {
  role: 'human' | 'ai' | 'tool';
  content: string | MessageContent[];
  type?: string;
  tool_call_id?: string;
  id?: string;
}

export class AgentService {
  private threadId: string;
  private client: Client;
  private assistantId: string;

  constructor(threadId: string, baseUrl?: string) {
    this.threadId = threadId;
    // Convert relative path to full URL for the SDK
    const fullUrl = baseUrl 
      ? (baseUrl.startsWith('http') ? baseUrl : `${window.location.origin}${baseUrl}`)
      : undefined;
    this.client = new Client({ apiUrl: fullUrl });
    this.assistantId = 'ui_agent';
  }

  async maybeCreateThread(): Promise<void> {
    try {
      // Try to get the thread, if it doesn't exist, create it
      try {
        await this.client.threads.get(this.threadId);
      } catch (error: any) {
        if (error.status === 404) {
          await this.client.threads.create({
            threadId: this.threadId,
            ifExists: 'do_nothing',
          });
        } else {
          throw error;
        }
      }
    } catch (error) {
      console.error('Error creating thread:', error);
      throw error;
    }
  }

  async getPastMessages(): Promise<AgentMessage[]> {
    await this.maybeCreateThread();

    try {
      const history = await this.client.threads.getHistory(this.threadId);
      if (history.length > 0) {
        const state = history[0].values as any;
        return state.messages || [];
      }
      return [];
    } catch (error) {
      console.error('Error fetching past messages:', error);
      return [];
    }
  }

  async updateMessage(message: AgentMessage): Promise<void> {
    try {
      const pastMessages = await this.getPastMessages();

      await this.client.threads.updateState(this.threadId, {
        values: {
          messages: [...pastMessages, message],
        },
      });
    } catch (error) {
      console.error('Error updating message:', error);
      throw error;
    }
  }

  async clearHistory(): Promise<void> {
    try {
      await this.client.threads.updateState(this.threadId, {
        values: {
          messages: [],
        },
      });
    } catch (error) {
      console.error('Error clearing history:', error);
      throw error;
    }
  }

  private async fileToBase64(file: File): Promise<string> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        const result = reader.result as string;
        // Extract base64 part (remove data:image/...;base64, prefix)
        const base64 = result.split(',')[1];
        resolve(base64);
      };
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  }

  async getResponse(
    userInput: string | { text: string; files: File[] }
  ): Promise<AgentMessage[]> {
    try {
      const pastMessages = await this.getPastMessages();

      let messageContent: string | MessageContent[];

      if (typeof userInput === 'string') {
        messageContent = userInput;
      } else {
        // Convert to multi-content format
        const content: MessageContent[] = [];

        if (userInput.text) {
          content.push({
            type: 'text',
            text: userInput.text,
          });
        }

        // Convert files to base64 and add to content
        for (const file of userInput.files) {
          if (file.type.startsWith('image/')) {
            const base64 = await this.fileToBase64(file);
            content.push({
              type: 'image_url',
              image_url: {
                url: `data:${file.type};base64,${base64}`,
              },
            });
          }
        }

        messageContent = content;
      }

      const runResult = await this.client.runs.wait(
        this.threadId,
        this.assistantId,
        {
          input: {
            messages: [
              {
                role: 'human',
                content: messageContent,
              },
            ],
          },
        }
      );

      const runMessages = (runResult as any).messages as AgentMessage[];
      return runMessages.slice(pastMessages.length);
    } catch (error) {
      console.error('Error getting response:', error);
      throw error;
    }
  }

  async *getStreamingResponse(
    userInput: string | { text: string; files: File[] }
  ): AsyncGenerator<AgentMessage, void, unknown> {
    try {
      let messageContent: string | MessageContent[];

      if (typeof userInput === 'string') {
        messageContent = userInput;
      } else {
        // Convert to multi-content format
        const content: MessageContent[] = [];

        if (userInput.text) {
          content.push({
            type: 'text',
            text: userInput.text,
          });
        }

        // Convert files to base64 and add to content
        for (const file of userInput.files) {
          if (file.type.startsWith('image/')) {
            const base64 = await this.fileToBase64(file);
            content.push({
              type: 'image_url',
              image_url: {
                url: `data:${file.type};base64,${base64}`,
              },
            });
          }
        }

        messageContent = content;
      }

      const streamResponse = this.client.runs.stream(
        this.threadId,
        this.assistantId,
        {
          input: {
            messages: [
              {
                role: 'human',
                content: messageContent,
              },
            ],
          },
        }
      );

      for await (const chunk of streamResponse) {
        if (chunk.event === 'messages/partial' && chunk.data) {
          const messages = chunk.data as AgentMessage[];
          for (const message of messages) {
            yield message;
          }
        }
      }
    } catch (error) {
      console.error('Error getting streaming response:', error);
      throw error;
    }
  }
}
