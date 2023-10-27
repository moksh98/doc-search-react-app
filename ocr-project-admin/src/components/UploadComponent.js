import { useState } from 'react'
// import './UploadComponent.scss';
import FileUpload from './FileUpload/FileUpload';
import FileList from './FileList/FileList';

function Upload() {
  const [files, setFiles] = useState([])

  return (
    <div className="App">
      <div className='file-container'>
        <FileUpload files={files} setFiles={setFiles} />
        <FileList files={files} /></div>
    </div>
  );
}

export default Upload;
