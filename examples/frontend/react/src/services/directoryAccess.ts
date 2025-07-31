/**
 * Directory Access Manager using File System Access API
 * Handles granting and managing access to local directories
 */

interface DirectoryHandle {
  name: string;
  path: string;
  handle: FileSystemDirectoryHandle;
}

class DirectoryAccessManager {
  private authorizedDirectories: Map<string, FileSystemDirectoryHandle> =
    new Map();
  private storageKey = 'authorized_directories';

  constructor() {
    this.loadSavedDirectories();
  }

  /**
   * Check if File System Access API is supported
   */
  isSupported(): boolean {
    return 'showDirectoryPicker' in window;
  }

  /**
   * Request access to a new directory
   */
  async requestDirectoryAccess(): Promise<DirectoryHandle | null> {
    if (!this.isSupported()) {
      throw new Error(
        'File System Access API is not supported in this browser'
      );
    }

    try {
      const directoryHandle = await (window as any).showDirectoryPicker({
        mode: 'read',
      });

      const path = await this.getDirectoryPath(directoryHandle);
      this.authorizedDirectories.set(path, directoryHandle);
      this.saveDirectories();

      return {
        name: directoryHandle.name,
        path,
        handle: directoryHandle,
      };
    } catch (error) {
      if (error.name === 'AbortError') {
        return null; // User cancelled
      }
      throw error;
    }
  }

  /**
   * Get approximate directory path (best effort)
   */
  private async getDirectoryPath(
    directoryHandle: FileSystemDirectoryHandle
  ): Promise<string> {
    // Try to resolve the path using the handle
    try {
      // This is a simplified approach - actual path resolution is limited in browsers
      return directoryHandle.name;
    } catch {
      return directoryHandle.name;
    }
  }

  /**
   * Get all authorized directories
   */
  getAuthorizedDirectories(): string[] {
    return Array.from(this.authorizedDirectories.keys());
  }

  /**
   * Check if a file path is accessible based on authorized directories
   */
  async canAccessFile(filePath: string): Promise<boolean> {
    for (const [dirPath, handle] of this.authorizedDirectories) {
      if (filePath.includes(dirPath) || filePath.startsWith('/')) {
        return true;
      }
    }
    return false;
  }

  /**
   * Get file from authorized directory
   */
  async getFile(filePath: string): Promise<File | null> {
    // Extract filename from path
    const fileName = filePath.split(/[/\\]/).pop();
    if (!fileName) return null;

    // Try to find the file in any authorized directory
    for (const [dirPath, directoryHandle] of this.authorizedDirectories) {
      try {
        // Search recursively through the directory
        const file = await this.searchFileInDirectory(
          directoryHandle,
          fileName
        );
        if (file) return file;
      } catch (error) {
        console.warn(`Could not access directory ${dirPath}:`, error);
        continue;
      }
    }

    return null;
  }

  /**
   * Recursively search for a file in directory and subdirectories
   */
  private async searchFileInDirectory(
    directoryHandle: FileSystemDirectoryHandle,
    fileName: string,
    maxDepth: number = 3,
    currentDepth: number = 0
  ): Promise<File | null> {
    if (currentDepth >= maxDepth) return null;

    try {
      // Try to get the file directly
      const fileHandle = await directoryHandle.getFileHandle(fileName);
      return await fileHandle.getFile();
    } catch {
      // File not found in this directory, search subdirectories
      for await (const [name, handle] of directoryHandle.entries()) {
        if (handle.kind === 'directory') {
          const result = await this.searchFileInDirectory(
            handle as FileSystemDirectoryHandle,
            fileName,
            maxDepth,
            currentDepth + 1
          );
          if (result) return result;
        }
      }
    }

    return null;
  }

  /**
   * Remove access to a directory
   */
  removeDirectoryAccess(path: string): void {
    this.authorizedDirectories.delete(path);
    this.saveDirectories();
  }

  /**
   * Save authorized directories to localStorage (handles only)
   */
  private saveDirectories(): void {
    const paths = Array.from(this.authorizedDirectories.keys());
    localStorage.setItem(this.storageKey, JSON.stringify(paths));
  }

  /**
   * Load saved directories from localStorage
   */
  private loadSavedDirectories(): void {
    try {
      const saved = localStorage.getItem(this.storageKey);
      if (saved) {
        // Note: We can't restore the actual handles from localStorage
        // Users will need to re-grant access after page refresh
        // This is a browser security limitation
      }
    } catch (error) {
      console.warn('Could not load saved directories:', error);
    }
  }

  /**
   * Clear all directory access
   */
  clearAllAccess(): void {
    this.authorizedDirectories.clear();
    localStorage.removeItem(this.storageKey);
  }
}

export const directoryAccessManager = new DirectoryAccessManager();
export type { DirectoryHandle };
