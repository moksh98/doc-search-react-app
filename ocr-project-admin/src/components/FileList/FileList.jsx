import React from 'react'
import FileItem from './../FileItem/FileItem'
import './FileList.scss'

const FileList = ({ files }) => {
    return (
        <div className='fl'>
        <div className="title">Uploaded files</div>
        <ul className="file-list">
        {files && files.map((f, index) => (
                    <FileItem key={index} file={f.file} fileName={f.file.name}/>
                ))}
        </ul>
    </div>
    )
}

export default FileList
