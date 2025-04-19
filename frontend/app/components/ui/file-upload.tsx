import React, { useState } from 'react';
import { Button } from './button';
import { FileText, UploadCloud } from 'lucide-react';

interface FileUploadProps {
  onFileUpload: (file: File) => void;
}

export function FileUpload({ onFileUpload }: FileUploadProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      onFileUpload(file);
    }
  };

  return (
    <div className="space-y-2">
      <label htmlFor="file-upload" className="block text-sm font-medium text-gray-700">
        Upload ESG Report
      </label>
      <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
        <div className="flex flex-col items-center justify-center space-y-4">
          <div className="flex items-center justify-center h-12 w-12 rounded-md bg-gray-50">
            <UploadCloud className="h-6 w-6 text-gray-400" />
          </div>
          <div className="flex flex-col items-center justify-center space-y-2">
            <div className="text-sm text-gray-600">
              <p>Drag and drop your file here, or click to browse</p>
              <p className="text-xs text-gray-500">PDF, DOCX, TXT up to 10MB</p>
            </div>
          </div>
          <Button
            variant="outline"
            className="mt-4"
            onClick={() => document.getElementById('file-upload')?.click()}
          >
            <FileText className="mr-2 h-4 w-4" />
            Upload File
          </Button>
        </div>
      </div>
      <input
        id="file-upload"
        type="file"
        className="hidden"
        onChange={handleFileChange}
        accept=".pdf,.docx,.txt"
      />
      {selectedFile && (
        <div className="mt-2 text-sm text-gray-500">
          Selected file: {selectedFile.name}
        </div>
      )}
    </div>
  );
}
