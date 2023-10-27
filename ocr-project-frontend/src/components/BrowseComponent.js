import React, { useState } from "react";
import axios from "axios";
import RenderResultPDF from "./ResultPDFComponentBrowse";

function swapKeysAndValues(obj) {
  return Object.keys(obj).reduce((acc, key) => {
    acc[obj[key]] = key;
    return acc;
  }, {});
}

function Browse() {
  const [result, setResult] = useState({});
  const [source, setSource] = useState("");
  const [reverseIndetifier, setReverseIndetifier] = useState([]);
  const [identifier, setIdentifier] = useState([]);
  const [showIdentifier, setShowIdentifier] = useState(false);
  const [decadeRange, setDecadeRange] = useState([]);
  const [showDecadeRange, setShowDecadeRange] = useState(false);
  const [decade, setDecade] = useState([]);
  const [showDecade, setShowDecade] = useState("");
  const [year, setYear] = useState([]);
  const [showYear, setShowYear] = useState("");
  const [month, setMonth] = useState([]);
  const [showMonth, setShowMonth] = useState("");

  const getResult = (event) => {
    axios
      .get(
        process.env.REACT_APP_BROWSE_BASE +
          "/?coll_type=" +
          event.target.innerText.toLowerCase()
      )
      .then((res) => {
        setIdentifier(res.data);
        setReverseIndetifier(swapKeysAndValues(res.data));
      });
    setShowIdentifier(true);
  };

  const handleIdentifier = (event) => {
    axios
      .get(
        process.env.REACT_APP_BROWSE_PERIODICAL +
          "?coll_identifier=" +
          reverseIndetifier[event.target.innerText]
      )
      .then((res) => {
        setResult(res.data);
      });
    axios
      .post(
        process.env.REACT_APP_COLLECTIONS_BY_IDENTIFIER +
          "?identifier=" +
          reverseIndetifier[event.target.innerText]
      )
      .then((res) => {
        setSource(res.data.coll_source);
      });
    setDecadeRange(Object.keys(result));
    setShowIdentifier(event.target.innerText);
    setShowDecadeRange(true);
    setShowDecade(false);
    setShowYear(false);
    setShowMonth(false);
  };

  const handleDecadeRange = (event) => {
    setDecade(Object.keys(result[event.target.innerText]));
    setShowDecadeRange(event.target.innerText);
    setShowDecade(true);
    setShowYear(false);
    setShowMonth(false);
  };

  const handleDecade = (event) => {
    setYear(Object.keys(result[showDecadeRange][event.target.innerText]));
    setShowYear(event.target.innerText);
    setShowMonth("");
  };

  const handleYear = (event) => {
    setMonth(
      Object.keys(result[showDecadeRange][showYear][event.target.innerText])
    );
    setShowMonth(event.target.innerText);
  };

  const cellStyle = {
    flex: 1,
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    borderColor: "black",
    borderStyle: "solid",
    backgroundColor: "#D3D3D3",
    outline: "none",
  };

  return (
    <div className="container">
      <div className="row">
        <div className="col-1">
          <a style={cellStyle} onClick={getResult}>
            Periodical
          </a>
        </div>
        <div className="col-4">
          {showIdentifier &&
            Object.values(identifier).map((item) => (
              <a style={cellStyle} key={item} onClick={handleIdentifier}>
                {item}
              </a>
            ))}
        </div>
        <div className="col-2">
          {showDecadeRange &&
            decadeRange.map((decade) => (
              <a style={cellStyle} onClick={handleDecadeRange}>
                {decade}
              </a>
            ))}
        </div>
        <div className="col-1">
          {showDecade &&
            decade.map((decade) => (
              <a style={cellStyle} onClick={handleDecade}>
                {decade}
              </a>
            ))}
        </div>
        <div className="col-1">
          {showYear &&
            year.map((month) => (
              <a style={cellStyle} onClick={handleYear}>
                {month}
              </a>
            ))}
        </div>
        <div className="col-2">
          {showMonth &&
            month.map((day) => (
              <div key={day}>
                <RenderResultPDF
                  result={{
                    filename: result[showDecadeRange][showYear][showMonth][day],
                    date: day,
                    coll_name: showIdentifier,
                    coll_source: source,
                  }}
                  searchQuery=""
                  searchType={null}
                  display_name={day}
                />
              </div>
            ))}
        </div>
      </div>
    </div>
  );
}

export default Browse;
