import { useState } from "react";

// This component is an input field that allows users to upload PDF files.
function FileInput({handleFileChange, label}) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const id = Math.random().toString(36).substring(7);

  return (
    <div>
      <center>
        <input
          type="file"
          accept=".pdf"
          onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
            const file = event.target.files?.[0];
            setSelectedFile(file)
            return handleFileChange(event)
          }}
          className="hidden"
          id={`upload-${id}`}
        />
        <label
          htmlFor={`upload-${id}`}
          className="bg-golden text-white px-3 py-2 rounded cursor-pointer"
        >
          {label}
        </label>
        {selectedFile && <p className="text-green-600 mt-2">{selectedFile.name}</p>}

      </center>
    </div>
  );
}

export default FileInput;
