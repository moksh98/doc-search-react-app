import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from 'reactstrap'


function Home() {
    return (
        <div className='container'>
            <div className='row'>
                <div className='col-6 col-md m-1'>
                    <Link to="/browse" style={{ textDecoration: 'none' }}>
                        <div className='row'>
                            <Button className='btn-block btn-lg' block>Browse</Button>
                        </div>
                    </Link>
                </div>
                <div className='col-6 col-md m-1'>
                    <Link to="/search" style={{ textDecoration: 'none' }}>
                        <div className='row'>
                            <Button className='btn-block btn-lg' block>Search</Button>
                        </div>
                    </Link>
                </div>
            </div>
        </div>
    );
}

export default Home;