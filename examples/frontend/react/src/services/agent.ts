export interface AgentMessage {
  role: 'human' | 'ai' | 'tool';
  content: string;
  type?: string;
  tool_call_id?: string;
  id?: string;
}

export class AgentService {
  private threadId: string;
  private baseUrl: string;

  constructor(threadId: string, baseUrl: string = '/api') {
    this.threadId = threadId;
    this.baseUrl = baseUrl;
  }

  async maybeCreateThread(): Promise<void> {
    try {
      const response = await fetch(`${this.baseUrl}/threads/${this.threadId}`);
      if (!response.ok && response.status === 404) {
        await fetch(`${this.baseUrl}/threads`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            thread_id: this.threadId,
            if_exists: 'do_nothing',
          }),
        });
      }
    } catch (error) {
      console.error('Error creating thread:', error);
      throw error;
    }
  }

  async getPastMessages(): Promise<AgentMessage[]> {
    await this.maybeCreateThread();

    try {
      const response = await fetch(
        `${this.baseUrl}/threads/${this.threadId}/history`
      );
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const history = await response.json();
      if (history.length > 0) {
        return history[0].values.messages || [];
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

      await fetch(`${this.baseUrl}/threads/${this.threadId}/state`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          values: {
            messages: [...pastMessages, message],
          },
        }),
      });
    } catch (error) {
      console.error('Error updating message:', error);
      throw error;
    }
  }

  async getResponse(userInput: string): Promise<AgentMessage[]> {
    try {
      const pastMessages = await this.getPastMessages();

      const response = await fetch(`${this.baseUrl}/runs/wait`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          thread_id: this.threadId,
          assistant_id: 'ui_agent',
          input: {
            messages: [
              {
                role: 'human',
                content: userInput,
              },
            ],
          },
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      return result.messages.slice(pastMessages.length);
    } catch (error) {
      console.error('Error getting response:', error);
      throw error;
    }
  }
}
