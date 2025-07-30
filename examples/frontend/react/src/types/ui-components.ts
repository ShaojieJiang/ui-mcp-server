export interface BaseComponent {
  type: string;
  key: string;
}

export interface InputComponent extends BaseComponent {
  label: string;
  help?: string;
  value?: any;
}

export interface OutputComponent extends BaseComponent {}

export interface NumberInput extends InputComponent {
  type: 'number_input' | 'slider';
  min_value?: number;
  max_value?: number;
  step?: number;
  value?: number;
}

export interface Choice extends InputComponent {
  type: 'radio' | 'multiselect';
  options: string[];
  value?: number | string | string[];
}

export interface ColorPicker extends InputComponent {
  type: 'color_picker';
  value?: string;
}

export interface DateInput extends InputComponent {
  type: 'date_input';
  min_value?: string;
  max_value?: string;
  format: 'YYYY/MM/DD' | 'DD/MM/YYYY' | 'MM/DD/YYYY';
  value?: string;
}

export interface TimeInput extends InputComponent {
  type: 'time_input';
  value?: string;
  step?: number;
}

export interface AudioInput extends InputComponent {
  type: 'audio_input';
}

export interface CameraInput extends InputComponent {
  type: 'camera_input';
}

export interface Chart extends OutputComponent {
  type: 'line' | 'bar' | 'scatter';
  data: (number | { x: number; y: number })[];
  x_label: string;
  y_label: string;
}

export interface AudioOutput extends OutputComponent {
  type: 'audio';
  url: string;
  format: 'audio/mp3' | 'audio/wav' | 'audio/ogg';
  sample_rate?: number;
  loop?: boolean;
  autoplay?: boolean;
}

export interface VideoOutput extends OutputComponent {
  type: 'video';
  url: string;
  format: 'video/mp4' | 'video/webm' | 'video/ogg';
  subtitles?: string;
  muted?: boolean;
  loop?: boolean;
  autoplay?: boolean;
}

export interface ImageOutput extends OutputComponent {
  type: 'image';
  url: string;
  caption?: string;
  width?: number;
  clamp?: boolean;
  channels: 'RGB' | 'RGBA';
  output_format: 'auto' | 'JPEG' | 'PNG' | 'WEBP';
}

export type UIComponent =
  | NumberInput
  | Choice
  | ColorPicker
  | DateInput
  | TimeInput
  | AudioInput
  | CameraInput
  | Chart
  | AudioOutput
  | VideoOutput
  | ImageOutput;

export interface MessageContent {
  type: 'text' | 'image_url';
  text?: string;
  image_url?: {
    url: string;
  };
}

export interface Message {
  id: string;
  type: 'human' | 'ai' | 'tool';
  content: string | MessageContent[];
  tool_call_id?: string;
  timestamp: Date;
}

export interface ChatSession {
  id: string;
  messages: Message[];
}
