import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';

export default function Dashboard({ onUploadSuccess }) {
  const { getRootProps, getInputProps } = useDropzone({
    accept: 'application/pdf',
    maxFiles: 1,
    onDrop: async files => {
      const formData = new FormData();
      formData.append('file', files[0]);
      
      try {
        const response = await axios.post('http://localhost:5000/api/upload', formData);
        onUploadSuccess(response.data.questions);
      } catch (error) {
        console.error('Upload failed:', error);
      }
    }
  });

  return (
    <div {...getRootProps()} className="upload-container">
      <input {...getInputProps()} />
      <p>Drag & drop PDF here, or click to select</p>
    </div>
  );
}