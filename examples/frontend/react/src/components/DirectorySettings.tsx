import React, { useState, useEffect } from 'react';
import { FolderPlus, Folder, X, AlertCircle, CheckCircle } from 'lucide-react';
import { Button } from './ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';
import {
  directoryAccessManager,
  DirectoryHandle,
} from '../services/directoryAccess';

interface DirectorySettingsProps {
  isVisible: boolean;
  onClose: () => void;
}

export const DirectorySettings: React.FC<DirectorySettingsProps> = ({
  isVisible,
  onClose,
}) => {
  const [isSupported, setIsSupported] = useState(false);
  const [authorizedDirs, setAuthorizedDirs] = useState<string[]>([]);
  const [isAdding, setIsAdding] = useState(false);

  useEffect(() => {
    setIsSupported(directoryAccessManager.isSupported());
    setAuthorizedDirs(directoryAccessManager.getAuthorizedDirectories());
  }, [isVisible]);

  const handleAddDirectory = async () => {
    setIsAdding(true);
    try {
      const result = await directoryAccessManager.requestDirectoryAccess();
      if (result) {
        setAuthorizedDirs(directoryAccessManager.getAuthorizedDirectories());
      }
    } catch (error) {
      console.error('Failed to add directory:', error);
      alert('Failed to add directory access. Please try again.');
    } finally {
      setIsAdding(false);
    }
  };

  const handleRemoveDirectory = (path: string) => {
    directoryAccessManager.removeDirectoryAccess(path);
    setAuthorizedDirs(directoryAccessManager.getAuthorizedDirectories());
  };

  const handleClearAll = () => {
    if (confirm('Remove access to all directories?')) {
      directoryAccessManager.clearAllAccess();
      setAuthorizedDirs([]);
    }
  };

  if (!isVisible) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <Card className="w-full max-w-md mx-4">
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <Folder className="w-5 h-5" />
              Local Directory Access
            </CardTitle>
            <Button variant="ghost" size="sm" onClick={onClose}>
              <X className="w-4 h-4" />
            </Button>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          {!isSupported ? (
            <div className="flex items-start gap-3 p-3 bg-yellow-50 border border-yellow-200 rounded-md">
              <AlertCircle className="w-5 h-5 text-yellow-600 mt-0.5 flex-shrink-0" />
              <div className="text-sm">
                <p className="font-medium text-yellow-800">
                  Browser Not Supported
                </p>
                <p className="text-yellow-700 mt-1">
                  Your browser doesn't support the File System Access API. Try
                  using Chrome 86+, Edge 86+, or Safari 15.2+.
                </p>
              </div>
            </div>
          ) : (
            <>
              <div className="flex items-start gap-3 p-3 bg-blue-50 border border-blue-200 rounded-md">
                <CheckCircle className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
                <div className="text-sm">
                  <p className="font-medium text-blue-800">How it works</p>
                  <p className="text-blue-700 mt-1">
                    Grant access to directories containing media files. Then you
                    can ask the AI to display files from those directories using
                    their full paths.
                  </p>
                </div>
              </div>

              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <h3 className="font-medium">Authorized Directories</h3>
                  <Button
                    onClick={handleAddDirectory}
                    disabled={isAdding}
                    size="sm"
                    className="flex items-center gap-2"
                  >
                    <FolderPlus className="w-4 h-4" />
                    {isAdding ? 'Adding...' : 'Add Directory'}
                  </Button>
                </div>

                {authorizedDirs.length === 0 ? (
                  <p className="text-sm text-muted-foreground p-3 border border-dashed rounded-md text-center">
                    No directories authorized yet
                  </p>
                ) : (
                  <div className="space-y-2">
                    {authorizedDirs.map((path) => (
                      <div
                        key={path}
                        className="flex items-center justify-between p-2 bg-muted rounded-md"
                      >
                        <div className="flex items-center gap-2 min-w-0">
                          <Folder className="w-4 h-4 text-muted-foreground flex-shrink-0" />
                          <span className="text-sm truncate" title={path}>
                            {path}
                          </span>
                        </div>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleRemoveDirectory(path)}
                          className="flex-shrink-0"
                        >
                          <X className="w-3 h-3" />
                        </Button>
                      </div>
                    ))}

                    {authorizedDirs.length > 1 && (
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={handleClearAll}
                        className="w-full text-red-600 hover:text-red-700"
                      >
                        Clear All Access
                      </Button>
                    )}
                  </div>
                )}
              </div>

              <div className="text-xs text-muted-foreground space-y-1">
                <p>• Directory access is granted per browser session</p>
                <p>
                  • Files will be searched recursively in authorized directories
                </p>
                <p>
                  • Your privacy is protected - only you choose what to share
                </p>
              </div>
            </>
          )}
        </CardContent>
      </Card>
    </div>
  );
};
