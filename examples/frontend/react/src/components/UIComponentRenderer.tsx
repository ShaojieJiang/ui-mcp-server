import React, { useState } from 'react';
import * as Select from '@radix-ui/react-select';
import * as Slider from '@radix-ui/react-slider';
import * as RadioGroup from '@radix-ui/react-radio-group';
import * as Checkbox from '@radix-ui/react-checkbox';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { ChevronDown, Check } from 'lucide-react';
import { UIComponent } from '../types/ui-components';
import { Button } from './ui/Button';
import { Input } from './ui/Input';
import { Label } from './ui/Label';
import { Card, CardContent } from './ui/Card';
import { cn } from '../lib/utils';

interface UIComponentRendererProps {
  component: UIComponent;
  onValueChange?: (value: any) => void;
  onSubmit?: (value: any) => void;
}

export const UIComponentRenderer: React.FC<UIComponentRendererProps> = ({
  component,
  onValueChange,
  onSubmit,
}) => {
  const [currentValue, setCurrentValue] = useState(component.value);

  const handleValueChange = (value: any) => {
    setCurrentValue(value);
    onValueChange?.(value);
  };

  const handleSubmit = () => {
    onSubmit?.(currentValue);
  };

  const renderInputComponent = () => {
    switch (component.type) {
      case 'number_input':
        return (
          <div className="space-y-2">
            <Label htmlFor={component.key}>{component.label}</Label>
            <Input
              id={component.key}
              type="number"
              value={currentValue || ''}
              min={component.min_value}
              max={component.max_value}
              step={component.step}
              onChange={(e) => handleValueChange(parseFloat(e.target.value))}
              placeholder={component.help}
            />
            {component.help && (
              <p className="text-sm text-muted-foreground">{component.help}</p>
            )}
          </div>
        );

      case 'slider':
        return (
          <div className="space-y-4">
            <Label>{component.label}</Label>
            <Slider.Root
              className="relative flex items-center select-none touch-none w-full h-5"
              value={[currentValue || component.min_value || 0]}
              max={component.max_value || 100}
              min={component.min_value || 0}
              step={component.step || 1}
              onValueChange={(value) => handleValueChange(value[0])}
            >
              <Slider.Track className="bg-secondary relative grow rounded-full h-2">
                <Slider.Range className="absolute bg-primary rounded-full h-full" />
              </Slider.Track>
              <Slider.Thumb className="block w-5 h-5 bg-primary border-2 border-primary rounded-full hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2" />
            </Slider.Root>
            <div className="text-sm text-muted-foreground">{currentValue}</div>
            {component.help && (
              <p className="text-sm text-muted-foreground">{component.help}</p>
            )}
          </div>
        );

      case 'radio':
        return (
          <div className="space-y-3">
            <Label>{component.label}</Label>
            <RadioGroup.Root
              className="flex flex-col gap-2"
              value={currentValue}
              onValueChange={handleValueChange}
            >
              {component.options.map((option, index) => (
                <div key={index} className="flex items-center space-x-2">
                  <RadioGroup.Item
                    className="bg-background w-4 h-4 rounded-full border border-input hover:bg-accent focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                    value={option}
                    id={`${component.key}-${index}`}
                  >
                    <RadioGroup.Indicator className="flex items-center justify-center w-full h-full relative after:content-[''] after:w-2 after:h-2 after:rounded-full after:bg-primary" />
                  </RadioGroup.Item>
                  <Label htmlFor={`${component.key}-${index}`}>{option}</Label>
                </div>
              ))}
            </RadioGroup.Root>
            {component.help && (
              <p className="text-sm text-muted-foreground">{component.help}</p>
            )}
          </div>
        );

      case 'multiselect':
        return (
          <div className="space-y-3">
            <Label>{component.label}</Label>
            <div className="flex flex-col gap-2">
              {component.options.map((option, index) => (
                <div key={index} className="flex items-center space-x-2">
                  <Checkbox.Root
                    className="flex h-4 w-4 items-center justify-center rounded-sm border border-input bg-background hover:bg-accent focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                    checked={
                      Array.isArray(currentValue) &&
                      currentValue.includes(option)
                    }
                    onCheckedChange={(checked) => {
                      const current = Array.isArray(currentValue)
                        ? currentValue
                        : [];
                      if (checked) {
                        handleValueChange([...current, option]);
                      } else {
                        handleValueChange(current.filter((v) => v !== option));
                      }
                    }}
                    id={`${component.key}-${index}`}
                  >
                    <Checkbox.Indicator>
                      <Check className="h-3 w-3" />
                    </Checkbox.Indicator>
                  </Checkbox.Root>
                  <Label htmlFor={`${component.key}-${index}`}>{option}</Label>
                </div>
              ))}
            </div>
            {component.help && (
              <p className="text-sm text-muted-foreground">{component.help}</p>
            )}
          </div>
        );

      case 'color_picker':
        return (
          <div className="space-y-2">
            <Label htmlFor={component.key}>{component.label}</Label>
            <Input
              id={component.key}
              type="color"
              value={currentValue || '#000000'}
              onChange={(e) => handleValueChange(e.target.value)}
              className="h-10 w-20 p-1 border rounded"
            />
            {component.help && (
              <p className="text-sm text-muted-foreground">{component.help}</p>
            )}
          </div>
        );

      case 'date_input':
        return (
          <div className="space-y-2">
            <Label htmlFor={component.key}>{component.label}</Label>
            <Input
              id={component.key}
              type="date"
              value={currentValue || ''}
              min={component.min_value}
              max={component.max_value}
              onChange={(e) => handleValueChange(e.target.value)}
            />
            {component.help && (
              <p className="text-sm text-muted-foreground">{component.help}</p>
            )}
          </div>
        );

      case 'time_input':
        return (
          <div className="space-y-2">
            <Label htmlFor={component.key}>{component.label}</Label>
            <Input
              id={component.key}
              type="time"
              value={currentValue || ''}
              onChange={(e) => handleValueChange(e.target.value)}
            />
            {component.help && (
              <p className="text-sm text-muted-foreground">{component.help}</p>
            )}
          </div>
        );

      case 'audio_input':
        return (
          <div className="space-y-2">
            <Label htmlFor={component.key}>{component.label}</Label>
            <Input
              id={component.key}
              type="file"
              accept="audio/*"
              onChange={(e) => handleValueChange(e.target.files?.[0])}
            />
            {component.help && (
              <p className="text-sm text-muted-foreground">{component.help}</p>
            )}
          </div>
        );

      case 'camera_input':
        return (
          <div className="space-y-2">
            <Label htmlFor={component.key}>{component.label}</Label>
            <Input
              id={component.key}
              type="file"
              accept="image/*"
              capture="environment"
              onChange={(e) => handleValueChange(e.target.files?.[0])}
            />
            {component.help && (
              <p className="text-sm text-muted-foreground">{component.help}</p>
            )}
          </div>
        );

      default:
        return <div>Unsupported input component: {component.type}</div>;
    }
  };

  const renderOutputComponent = () => {
    switch (component.type) {
      case 'line':
      case 'bar':
      case 'scatter':
        const chartData = Array.isArray(component.data)
          ? component.data.map((item, index) =>
              typeof item === 'object' ? item : { x: index, y: item }
            )
          : [];

        return (
          <Card>
            <CardContent className="p-6">
              <ResponsiveContainer width="100%" height={300}>
                {component.type === 'line' && (
                  <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="x" name={component.x_label} />
                    <YAxis name={component.y_label} />
                    <Tooltip />
                    <Line type="monotone" dataKey="y" stroke="#8884d8" />
                  </LineChart>
                )}
                {component.type === 'bar' && (
                  <BarChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="x" name={component.x_label} />
                    <YAxis name={component.y_label} />
                    <Tooltip />
                    <Bar dataKey="y" fill="#8884d8" />
                  </BarChart>
                )}
                {component.type === 'scatter' && (
                  <ScatterChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="x" name={component.x_label} />
                    <YAxis dataKey="y" name={component.y_label} />
                    <Tooltip />
                    <Scatter dataKey="y" fill="#8884d8" />
                  </ScatterChart>
                )}
              </ResponsiveContainer>
            </CardContent>
          </Card>
        );

      case 'image':
        return (
          <Card>
            <CardContent className="p-6">
              <img
                src={component.url}
                alt={component.caption || 'Image'}
                width={component.width}
                className={cn(
                  'max-w-full h-auto rounded-md',
                  component.clamp && 'object-cover'
                )}
              />
              {component.caption && (
                <p className="text-sm text-muted-foreground mt-2">
                  {component.caption}
                </p>
              )}
            </CardContent>
          </Card>
        );

      case 'audio':
        return (
          <Card>
            <CardContent className="p-6">
              <audio
                src={component.url}
                controls
                loop={component.loop}
                autoPlay={component.autoplay}
                className="w-full"
              />
            </CardContent>
          </Card>
        );

      case 'video':
        return (
          <Card>
            <CardContent className="p-6">
              <video
                src={component.url}
                controls
                loop={component.loop}
                muted={component.muted}
                autoPlay={component.autoplay}
                className="w-full rounded-md"
              >
                {component.subtitles && (
                  <track kind="subtitles" src={component.subtitles} />
                )}
              </video>
            </CardContent>
          </Card>
        );

      default:
        return <div>Unsupported output component: {component.type}</div>;
    }
  };

  const isInputComponent = [
    'number_input',
    'slider',
    'radio',
    'multiselect',
    'color_picker',
    'date_input',
    'time_input',
    'audio_input',
    'camera_input',
  ].includes(component.type);

  const isOutputComponent = [
    'line',
    'bar',
    'scatter',
    'image',
    'audio',
    'video',
  ].includes(component.type);

  if (isInputComponent) {
    return (
      <Card className="p-4 space-y-4">
        {renderInputComponent()}
        {onSubmit && (
          <div className="flex justify-start">
            <Button onClick={handleSubmit} size="sm">
              Submit
            </Button>
          </div>
        )}
      </Card>
    );
  }

  if (isOutputComponent) {
    return renderOutputComponent();
  }

  return <div>Unknown component type: {component.type}</div>;
};
