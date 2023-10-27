import React, { useEffect, useState, useRef } from 'react'; 
import axios from 'axios';
import ReactPaginate from 'react-paginate';
import Multiselect from 'multiselect-react-dropdown';
import Loading from './LoadingComponent';
import { Card, CardImg, Breadcrumb, BreadcrumbItem, Form, FormGroup, Input, Col, Button } from 'reactstrap';
import { Link } from 'react-router-dom';
import RenderResultPDF from './ResultPDFComponentSearch';
import Keyboard from "react-simple-keyboard";
import arabic from "simple-keyboard-layouts/build/layouts/arabic";
import "react-simple-keyboard/build/css/index.css";

function RenderResultItem({result}) {
    return (
        <Card>
            <CardImg width="100%" src={"/assets/images/KA18920415_002.jpg"} alt={result.coll_name} />
        </Card>
    );
}

function RenderResultName({result, searchQuery, searchType}) {
    return (
        <>
            <h4>{result.coll_name}</h4>
            <h5>Page: {result.page_number}</h5>
            <p>Date: {result.date}</p>
            <p>Location: {result.coll_location}</p>
            <p>Source: {result.coll_source}</p>
            <RenderResultPDF result={result} searchQuery={searchQuery} searchType={searchType} display_name="Open"/>
        </>
    );
}

function PaginatedItems({ itemsPerPage, items, maxItems, searchQuery, searchType }) {
    const [currentItems, setCurrentItems] = useState(items.slice(0, itemsPerPage));
    const [pageCount, setPageCount] = useState(0);
    const [itemOffset, setItemOffset] = useState(0);

    useEffect(() => {
        const newOffset = itemOffset*itemsPerPage;
        const endOffset = newOffset + itemsPerPage < maxItems ? newOffset + itemsPerPage : maxItems;
        setCurrentItems(items.slice(newOffset, endOffset));
        setPageCount(Math.ceil(items.length / itemsPerPage));
    }, [itemOffset, itemsPerPage, items, maxItems]);
    
    const handlePageChange = (event) => {
        setItemOffset(event.selected);
    };
    
    return (
        <>
            <ReactPaginate
                previousLabel="Previous"
                nextLabel="Next"
                pageClassName="page-item"
                pageLinkClassName="page-link"
                previousClassName="page-item"
                previousLinkClassName="page-link"
                nextClassName="page-item"
                nextLinkClassName="page-link"
                breakLabel="..."
                breakClassName="page-item"
                breakLinkClassName="page-link"
                pageCount={pageCount}
                marginPagesDisplayed={3}
                pageRangeDisplayed={2}
                containerClassName="pagination"
                activeClassName="active"
                onPageChange={handlePageChange}
                forcePage={itemOffset}
            />
            <Results items={currentItems} searchQuery={searchQuery} searchType={searchType} />
            <ReactPaginate
                previousLabel="Previous"
                nextLabel="Next"
                pageClassName="page-item"
                pageLinkClassName="page-link"
                previousClassName="page-item"
                previousLinkClassName="page-link"
                nextClassName="page-item"
                nextLinkClassName="page-link"
                breakLabel="..."
                breakClassName="page-item"
                breakLinkClassName="page-link"
                pageCount={pageCount}
                marginPagesDisplayed={3}
                pageRangeDisplayed={2}
                containerClassName="pagination"
                activeClassName="active"
                onPageChange={handlePageChange}
                forcePage={itemOffset}
            />
        </>
    );
}

function Results({items, searchQuery, searchType}) {
    return (
        <div className="results">
            <div className="listing">
                {items &&
                    items.map((result) => (
                        <div key={result.date + result.date + result.coll_identifier + result.page_number
                        } className='row shadow-lg p-3 mb-5 bg-white rounded'>
                            <div className="col-12 col-md-6">
                                <RenderResultItem result={result} />
                            </div>
                            <div className="col-12 col-md-6">
                                <RenderResultName result={result} searchQuery={searchQuery} searchType={searchType}/>
                            </div>
                        </div>
                    ))
                }
            </div>
        </div>
    );
}

function RenderError({error}) {
    return (
        <div className='row'>
            <div className='col-12 col-md-6'>
                <h4>Error {error.status}: {error.statusText}</h4>
            </div>
        </div>
    );
}

function ShowResults ({data, searchQuery, searchType}) {
    if(data.length > 0) {
        return (
            <div className='row'>
                <div className='col-12 col-md-6'>
                    <PaginatedItems itemsPerPage={5} items={data} maxItems={data.length} searchQuery={searchQuery} searchType={searchType}/>
                </div>
                <div className='col-12 col-md-6'>
                    {/* <Analytics /> */}
                </div>
            </div>
        );
    }
    else {
        return (
            <div className='row'>
                <div className='col-12'>
                    <h4>No Results Found! Please Try another Keyword</h4>
                </div>
            </div>
        )
    }
}
    
const Search = () => {
    
    const [layout, setLayout] = useState('default');
    const [input, setInput] = useState('');
    const [startDate, setStartDate] = useState(0);
    const [endDate, setEndDate] = useState(0);
    const [names, setNames] = useState([]);
    const [keyboardVisibility, setkeyboardVisibility] = useState(false);
    const [isShown, setIsShown] = useState(false);
    const [result, setResult] = useState([{}]);
    const [loading, setLoading] = useState(false);
    const [axiosErrorResponse, setAxiosErrorResponse] = useState({})
    const [searchType, setSearchType] = useState("any");

    const onChangeInput = event => {
        const input = event.target.value;
        setInput(input);
        keyboard.current.setInput(input);
    };

    const handleClick = event => {
        event.preventDefault();
        
        const coll = []
        for(var i = 0; i < names.length; i++) {
            coll.push(names[i][1]['name'])
        }

        if(startDate === '') {
            setStartDate(0);
        }
        if(endDate === '') {
            setEndDate(0);
        }

        const ip = {
            "search_query": input,
            "from_year": startDate,
            "to_year": endDate,
            "coll_identifier": coll,
            "match": searchType,
            "sorttype": "desc"
        }

        setLoading(true);

        axios.put(process.env.REACT_APP_SEARCH, {
            "search_query": input,
            "from_year": startDate,
            "to_year": endDate,
            "coll_identifier": coll,
            "match": searchType,
            "sorttype": "desc",
        },)
        .then(res => {
            setResult(res.data);
            setAxiosErrorResponse(res);
            setIsShown(true);
            setLoading(false);
        })
        .catch(function(error) {
            setAxiosErrorResponse(error.response)
            setLoading(false)
        });
    }


    const handleShift = () => {
        const layoutName = layout;
        if(layoutName === "default") {
            setLayout("shift");
        }
        else {
            setLayout("default")
        }
    };

    const onKeyPress = button => {     
        /**
        * If you want to handle the shift and caps lock buttons
        */
        if (button === "{shift}" || button === "{lock}") handleShift();
    };

    const onChange = input => {
        setInput(input);
    };

    const onChangeStartDate = input => {
        setStartDate(input.target.value);
    }

    const onChangeEndDate = input => {
        setEndDate(input.target.value);
    }

    const toggleKeyboard = () => {
        setkeyboardVisibility(!keyboardVisibility);
    }

    const handleOptionChange = (event) => {
        setSearchType(event.target.value);
    };

    const keyboard = useRef();

    const searchTypeOptions = [
        { value: "any", label: "Any Word" },
        { value: "all", label: "All Words" },
        { value: "exact", label: "Exact Word" },
    ];

    const collectionOptions = [
        { label: "ash Shams", name: "Sham", id: 0 },
        { label: "al-Ayam", name: "ayaam", id: 1 },
        { label: "el Diario Sirio Libanes", name: "DiSL", id: 2 },
        { label: "as-Sayeh", name: "sayeh", id: 3 },
        { label: "Jornal ABC", name: "Jorn", id: 4 },
        { label: "Renovacion", name: "Reno", id: 5 },
        { label: "Syrian American Commercial Magazine", name: "SACM", id: 6 },
        { label: "Nueva Vida", name: "Nuev", id: 7 },
        { label: "O Livre Pensador", name: "LiPe", id: 8 },
        { label: "al-Akhlak", name: "akhlak", id: 9 },
        { label: "al-Fajr", name: "fajr", id: 10 },
        { label: "La Salvacion", name: "Salv", id: 11 },
        { label: "La Union Arabiga", name: "UnAr", id: 12 },
        { label: "Las Fuentes", name: "Fuen", id: 13 },
        { label: "an Neser", name: "Nese", id: 14 },
        { label: "al-Bayan", name: "bayan", id: 15 },
        { label: "Mira'at al-Gharb", name: "mg", id: 16 },
        { label: "al-Kown", name: "kown", id: 17 },
        { label: "al-Funun", name: "funun", id: 18 },
        { label: "as Salam", name: "Sala", id: 19 },
        { label: "el Misionero", name: "Murs", id: 20 },
        { label: "Fatat Boston", name: "fatatboston", id: 21 },
        { label: "as-Sameer", name: "sameer", id: 22 },
        { label: "al Watan", name: "Wata", id: 23 },
        { label: "al-Wafa", name: "alwafa", id: 24 },
        { label: "Kawkab Amirka", name: "KA", id: 25 },
        { label: "al Haiat", name: "Haia", id: 26 },
        { label: "an Nahda", name: "NaAr", id: 27 },
        { label: "as-Salam", name: "sala", id: 28 },
        { label: "al-Hoda", name: "alhoda", id: 29 },
        { label: "Jurab al Kurdy", name: "Jurab", id: 30 },
            ];

    const onSelectNames = name => {
        const propertyValues = Object.entries(name);
        setNames(propertyValues);
    };
    
    const onRemoveNames = name => {
        const propertyValues = Object.entries(name);
        setNames(propertyValues);
    };
    
    return (
        <div className='container'>
            <div className='row'>
                <Breadcrumb>
                    <BreadcrumbItem>
                        <Link to='/home'>Home</Link>
                    </BreadcrumbItem>
                    <BreadcrumbItem active>Search</BreadcrumbItem>
                </Breadcrumb>
            </div>
            <div className='row'>
                <div className="col-12">
                    <h3>Search</h3>
                </div>
                <div className='col-12 col-md-9 mb-4'>
                    <Form>
                        <FormGroup row>
                            <Col md={4}>
                                <div className='row'>
                                    <Input type="text" id="search" name="Search" placeholder="Search" value={input} onChange={onChangeInput}/>
                                    <div className='col-md-3'>
                                        <span onClick={toggleKeyboard}><i className="fa fa-keyboard-o fa-4x pull-right"></i></span>
                                    </div>
                                    <div className='col-md-6'>
                                        <Input style={{marginTop: '10%'}} type="select" name="select" id="exampleSelect" value={searchType} onChange={handleOptionChange}>
                                            {searchTypeOptions.map((option) => (
                                                <option key={option.value} value={option.value}>
                                                    {option.label}
                                                </option>
                                            ))}
                                        </Input>
                                    </div>
                                </div>
                            </Col>
                            <Col md={2}>
                                <Multiselect
                                    placeholder="Collections"
                                    // displayValue="key"
                                    options={collectionOptions}
                                    // selectedValues={selectedValue} // Preselected value to persist in dropdown
                                    onSelect={onSelectNames} // Function will trigger on select event
                                    onRemove={onRemoveNames} // Function will trigger on remove event
                                    showCheckbox={true}
                                    displayValue="label" // Property name to display in the dropdown options
                                    avoidHighlightFirstOption={true}
                                />

                            </Col>
                            <Col md={2}>
                                <Input type="text" id="from-year" name="from-year" placeholder="From (Year)" onChange={onChangeStartDate}/>
                            </Col>
                            <Col md={2}>
                                <Input type="text" id="to-year" name="to-year" placeholder="To (Year)" onChange={onChangeEndDate}/>
                            </Col>
                            <Col md={0}>
                                <Button type="submit" color="primary" style={{background: '#427E93'}} onClick={handleClick}><i className="fa fa-search" /></Button>
                                {/* <Button type="submit" color="primary" style={{background: '#427E93'}} onClick={handleClick}>Search</Button> */}
                            </Col>
                        </FormGroup>
                    </Form>
                </div>
                <div className='row arabic-keyboard'>
                    {keyboardVisibility && <Keyboard
                        keyboardRef={r => (keyboard.current = r)}
                        layoutName={layout}
                        layout={arabic.layout}
                        onChange={onChange}
                        onKeyPress={onKeyPress}
                    />}
                </div>
            </div>
            <hr />
            {
                JSON.stringify(axiosErrorResponse) === JSON.stringify({}) || axiosErrorResponse.status === 200 ? 
                    loading ? 
                        <Loading />
                        : 
                        isShown && <ShowResults data={result} searchQuery={input} searchType={searchType}/> 
                    : 
                    <RenderError error={axiosErrorResponse} />
            }
        </div>
    );
}

export default Search;