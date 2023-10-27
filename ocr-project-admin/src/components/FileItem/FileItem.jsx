import React from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faFileAlt, faSpinner, faCheck, faExclamation } from '@fortawesome/free-solid-svg-icons'
import './FileItem.scss'

const FileItem = ({ file, fileName }) => {
    return (
        <li className="file-item" key={file.name}>
            <FontAwesomeIcon icon={faFileAlt} />
            <p>{fileName}</p>
            <div className="actions">
                <div className="loading"></div>
                {file.isUploading && (
                    <FontAwesomeIcon
                        icon={faSpinner}
                        className="fa-spin"
                    />
                )}
                {!file.isUploading && file.errorMessage === "" ?
                        <FontAwesomeIcon icon={faCheck} /> : <FontAwesomeIcon icon={faExclamation} />
                }
            </div>
        </li>
    )
}

export default FileItem
