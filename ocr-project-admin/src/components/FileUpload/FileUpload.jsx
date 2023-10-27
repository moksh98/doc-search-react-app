// import React, { useState } from 'react'
// import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
// import { faPlus } from '@fortawesome/free-solid-svg-icons'
// import './FileUpload.scss'
// import axios from 'axios'

// const FileUpload = ({ files, setFiles }) => {
//     const [isDisabled, setIsDisabled] = useState(false);

//     async function handleButtonClick() {
            
//     }

//     async function uploadHandler(event) {
//         const files = event.target.files;
//         if(!files) return;

        
//         for (let i = 0; i < files.length; i++) {
//             const file = files[i];
//             if (file.type !== "application/pdf") continue; // allow only PDF files


//             setIsDisabled(true);
//             const response = await fetch('http://localhost:8052/upload/get_storage_cap?current_size='+file.size);
//             const data = await response.json();
//             console.log(data)
//             if (data.result === "false") {
//                 alert("file size exceding current capacity!")
//                 setIsDisabled(false);
//                 return;
//             }

//             file.isUploading = true;


//             setFiles(prevFiles => [...prevFiles, file]);
//             // upload file
//             const formData = new FormData();
            
//             formData.append("files", file, file.name)

//             axios.post('http://localhost:8052/upload/upload-periodical', formData)
//                 .then((res) => {
//                     file.isUploading = false;
//                     setFiles(prevFiles => {
//                         const index = prevFiles.findIndex(f => f.name === file.name);
//                         const newFiles = [...prevFiles];
//                         newFiles[index] = file;
//                         return newFiles;
//                     });
//                 })
//                 .catch((err) => {
//                     // inform the user
//                     console.error(err)
//                 });
//         }
//     }

//     return (
//         <>
//             <div className="file-card">

//                 <div className="file-inputs">
//                     <input type="file" accept="application/pdf" onChange={function(event) { uploadHandler(event); }} multiple />
//                     <button onClick={handleButtonClick} disabled={isDisabled}>
//                         <i>
//                             <FontAwesomeIcon icon={faPlus} />
//                         </i>
//                         Upload
//                     </button>
//                 </div>

//                 <p className="main">Supported files</p>
//                 <p className="info">PDF</p>

//                 <p className="main">Filename format should be</p>
//                 <p className="info">{'<'}coll_id{'>'}_{'<'}date{'>'}_{'<'}volume{'>'}_{'<'}issue{'>'}.pdf</p>

//             </div>
//         </>
//     )
// }

// export default FileUpload


import React, { useEffect, useCallback } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPlus } from '@fortawesome/free-solid-svg-icons'
import './FileUpload.scss'
import axios from 'axios'

const FileUpload = ({ files, setFiles }) => {

    const handleFileUpload = (event) => {
        const files = event.target.files;
        const fileArray = [];
        for (let i = 0; i < files.length; i++) {
            console.log(files[i])
            fileArray.push({ file: files[i], isLoading: true, errorMessage: "", });
        }
        setFiles(fileArray);
    };

    // const validateFile = (async (index,file) => {
    //   setTimeout(() => {
    //     const newFiles = [...files];
    //     newFiles[index].isLoading = false;
    //     setFiles(newFiles);
    //   }, 10000);
    // });

    const validateFile = useCallback(async (index, file) => {
        const newFiles = [...files];
        if (file.type === 'application/pdf') {
            console.log(file.size)
            await fetch('http://localhost:8053/upload/get_storage_cap?current_size=' + file.size)
          .then(async (response) => {
            console.log(response.result)
            if (response.result === 'true') {
              const formData = new FormData();
              formData.append('files', file, file.name);
    
              await axios.post('http://localhost:8053/upload/upload-periodical', formData)
                .then(() => {
                  newFiles[index] = {
                    ...file,
                    isLoading: false,
                  };
                  setFiles(newFiles);
                })
                .catch((err) => {
                  console.error(err);
                  newFiles[index] = {
                    ...file,
                    isLoading: false,
                    errorMessage: err,
                  };
                  setFiles(newFiles);
                });
            } else {
              newFiles[index] = {
                ...file,
                isLoading: false,
                errorMessage: 'File size exceeding current capacity!',
              };
              setFiles(newFiles);
              // setIsDisabled(true);
            }
          })
          .catch((error) => {
            console.error(error);
            newFiles[index] = {
              ...file,
              isLoading: false,
              errorMessage: error,
            };
            setFiles(newFiles);
          });
            
        } else{
          newFiles[index] = {
            ...file,
            isLoading: false,
            errorMessage: 'File is not a PDF file!',
          };
          setFiles(newFiles);
        }
    
      }, [files, setFiles]);
      
      // useEffect(() => {
      //   files.forEach((file, index) => {
      //     if (file.isLoading) {
      //       validateFile(index);
      //     }
      //   });
      // }, [files, validateFile]);
      useEffect(() => {
        files.forEach((file, index) => {
            console.log(file.name+" "+index)
          if (file.isLoading) {
            validateFile(index, file);
          }
        });
      }, [files, validateFile]);

    return (
        <>
            <div className="file-card">
                <div className="file-inputs">
                    <input type="file" accept="application/pdf" onChange={handleFileUpload} multiple />
                    <button>
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