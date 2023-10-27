import React, { Component } from 'react';
import Header from './Header/HeaderComponent';
import Footer from './Footer/FooterComponent';
// import FileUpload from '../FileUpload';
import { Routes, Route, Navigate } from 'react-router-dom';
import Upload from './UploadComponent';

class Main extends Component {
	render () {

		const UploadPage = () => {
			return (
				<Upload />
			);
		}

		return (
			<div className='App'>
				<Header />
				<br></br>

				<Routes>
					<Route path="/admin" element={<UploadPage />} />
					<Route path="*" element={<Navigate to="/"/>} />
				</Routes>
				
				<br></br>
				<Footer />
			</div>
		);
	}
}

export default Main;
