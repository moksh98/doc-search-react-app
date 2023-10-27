import React, { useState, useEffect } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPlus } from '@fortawesome/free-solid-svg-icons'
import './FileUpload.scss'
import axios from 'axios'

const FileUpload = ({ files, setFiles }) => {
    const [files, setFiles] = useState([]);
    const [isDisabled, setIsDisabled] = useState(false);

    const handleFileUpload = (event) => {
        const files = event.target.files;
        const fileArray = [];
        for (let i = 0; i < files.length; i++) {
        fileArray.push({ file: files[i], isLoading: "started" });
        }
        setFiles(fileArray);
    };

    const validateFile = (index) => {
        const newFiles = [...files];
        if (newFiles[index].type !== "application/pdf") {
            newFiles[index].isLoading = "File is not a PDF file!"
            setFiles(newFiles);
            return;
        }

        fetch('http://localhost:8052/upload/get_storage_cap?current_size='+file.size)
        .then( response =>{
            if (response.result === "false") {
                // alert("File size exceding current capacity!")
                newFiles[index].isLoading = "File size exceding current capacity!"
                setFiles(newFiles)
                setIsDisabled(true);
                return;
            }
        }).catch(error => {
            console.error(error);
            newFiles[index].isLoading = error 
            setFiles(newFiles)
            return;
            // Handle error state here
        });

        
        const formData = new FormData();
        formData.append("files", file, file.name)

        axios.post('http://localhost:8052/upload/upload-periodical', formData)
            .then((res) => {
                newFiles[index].isLoading = "success"
            })
            .catch((err) => {
                // inform the user
                console.error(err)
                newFiles[index].isLoading = err

            });

        setFiles(newFiles);
    };

    useEffect(() => {
        files.forEach((file, index) => {
        if (file.isLoading) {
            validateFile(index);
        }
        });
    }, [files]);

    return (
        <>
            <div className="file-card">

                <div className="file-inputs">
                    <input type="file" accept="application/pdf" onChange={handleFileUpload} multiple />
                    <button onClick={handleButtonClick} disabled={isDisabled}>
                        <i>
                            <FontAwesomeIcon icon={faPlus} />
                        </i>
                        Upload
                    </button>
                </div>

                <p className="main">Supported files</p>
                <p className="info">PDF</p>

                <p className="main">Filename format should be</p>
                <p className="info">{'<'}coll_id{'>'}_{'<'}date{'>'}_{'<'}volume{'>'}_{'<'}issue{'>'}.pdf</p>

            </div>
        </>
    )
}

export default FileUpload;