import React from 'react';
import logo from '../logo/kclds_logo.gif';

function Loading () {
    return (
        <div className="row">
            <div className="col-12" style={{display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
                <img src={logo} alt="Loading Logo" width="250px" />
            </div>
        </div>
    );
};

export default Loading;