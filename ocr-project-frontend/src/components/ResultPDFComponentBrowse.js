import React, { useState } from "react";
import { Button } from "reactstrap";
import Modal from "react-modal";
import { Worker, Viewer } from "@react-pdf-viewer/core";
import { defaultLayoutPlugin } from "@react-pdf-viewer/default-layout";
import { pageNavigationPlugin } from "@react-pdf-viewer/page-navigation";
import { searchPlugin } from "@react-pdf-viewer/search";

// Import styles
import "@react-pdf-viewer/default-layout/lib/styles/index.css";
import "@react-pdf-viewer/core/lib/styles/index.css";
import "@react-pdf-viewer/search/lib/styles/index.css";

const customStyles = {
  content: {
    top: "50%",
    left: "50%",
    right: "auto",
    bottom: "-50%",
    marginRight: "-50%",
    width: "70%",
    transform: "translate(-50%, -50%)",
  },
  overlay: { zIndex: 3 },
};

function get_new_file(s, val) {
  let ext = s.split(".")[1];
  let name = s.split(".")[0].split("_").slice(0, 4).join("_");
  let num = parseInt(s.split(".")[0].split("_")[4]);
  num += val;
  num = num.toString();
  return name + "_" + num + "." + ext;
}

const RenderResultPDF = (props) => {
  const [isOpen, setIsOpen] = useState(false);
  const defaultLayoutPluginInstance = defaultLayoutPlugin();
  const pageNavigationPluginInstance = pageNavigationPlugin();
  var searchPluginInstance = searchPlugin();
  const [maxPage, setMaxPage] = useState(
    parseInt(props.result.filename.split(".")[0].split("_")[4])
  );
  const [file, setFile] = useState(
    props.result.filename.split(".")[0].split("_").slice(0, 4).join("_") +
      "_1.pdf"
  );
  const [page, setPage] = useState("1");
  const [isPreviousButtonDisabled, setIsPreviousButtonDisabled] =
    useState(false);
  const [isNextButtonDisabled, setIsNextButtonDisabled] = useState(false);

  if (props.searchType === "exact") {
    searchPluginInstance = searchPlugin({ keyword: props.searchQuery });
  } else {
    searchPluginInstance = searchPlugin({
      keyword: props.searchQuery.split(" "),
      highlightAll: true,
    });
  }

  const openModal = () => {
    page === "1"
      ? setIsPreviousButtonDisabled(true)
      : setIsPreviousButtonDisabled(false);
    setIsOpen(true);
  };

  const closeModal = () => {
    setFile(props.result.filename);
    setPage("1");
    setMaxPage(parseInt(props.result.filename.split(".")[0].split("_")[4]));
    setFile(
      props.result.filename.split(".")[0].split("_").slice(0, 4).join("_") +
        "_1.pdf"
    );
    setIsNextButtonDisabled(false);
    setIsPreviousButtonDisabled(false);
    setIsOpen(false);
  };

  const get_next_page = () => {
    setFile(get_new_file(file, 1));
    setPage((parseInt(page) + 1).toString());
    page >= "1"
      ? setIsPreviousButtonDisabled(false)
      : setIsPreviousButtonDisabled(true);
    page === (maxPage - 1).toString()
      ? setIsNextButtonDisabled(true)
      : setIsNextButtonDisabled(false);
  };

  const get_previous_page = () => {
    setFile(get_new_file(file, -1));
    setPage((parseInt(page) - 1).toString());
    parseInt(page) <= maxPage
      ? setIsNextButtonDisabled(false)
      : setIsNextButtonDisabled(true);
    page === "2"
      ? setIsPreviousButtonDisabled(true)
      : setIsPreviousButtonDisabled(false);
  };

  return (
    <>
      <Button style={{ background: "#427E93" }} onClick={openModal}>
        {props.display_name}
      </Button>
      <Modal style={customStyles} isOpen={isOpen} onRequestClose={closeModal}>
        <div
          className="title"
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <div className="row">
            <div className="col-12">
              <span>Collection: </span>
              <span style={{ fontWeight: "bold" }}>
                {props.result.coll_name}
              </span>
              &emsp;<span>|</span>&emsp;
              <span>Date: </span>
              <span style={{ fontWeight: "bold" }}>{props.result.date}</span>
              &emsp;<span>|</span>&emsp;
              <span>Page: </span>
              <span style={{ fontWeight: "bold" }}>{page}</span>
              &emsp;<span>|</span>&emsp;
              <span>Source: </span>
              <span style={{ fontWeight: "bold" }}>
                {props.result.coll_source}
              </span>
              &emsp;<span>|</span>&emsp;
              <Button
                disabled={isPreviousButtonDisabled}
                onClick={get_previous_page}
              >
                Previous
              </Button>
              &emsp;
              <Button disabled={isNextButtonDisabled} onClick={get_next_page}>
                Next
              </Button>
              &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
              <Button onClick={closeModal} id="cancelBtn">
                X
              </Button>
            </div>
          </div>
        </div>
        <br></br>
        <div className="body">
          <Worker workerUrl={process.env.REACT_APP_PDF_WORKER}>
            <div>
              <Viewer
                theme="dark"
                fileUrl={process.env.REACT_APP_PDF_ENDPOINT + file}
                plugins={[
                  defaultLayoutPluginInstance,
                  pageNavigationPluginInstance,
                  searchPluginInstance,
                ]}
              />
            </div>
          </Worker>
        </div>
      </Modal>
    </>
  );
};

export default RenderResultPDF;
