import React, { Component } from 'react';
import Home from './HomeComponent';
import Search from './SearchComponent';
import About from './AboutComponent.js';
import Contact from './ContactComponent';
import Header from './HeaderComponent';
import Footer from './FooterComponent';
import Browse from './BrowseComponent';
import { LEADERS } from '../shared/leaders';
import { Routes, Route, Navigate } from 'react-router-dom';

class Main extends Component {

	constructor(props) {
		super(props);

		this.state = {
			leaders: LEADERS,
		};
	}

	render () {

		const HomePage = () => {
			return (
				<Home />
			);
		}

		return (
			<div className='App'>
				<Header />
				<br></br>

				<Routes>
					<Route path="/home" element={<HomePage />} />
					<Route exact path="/search" element={<Search />} />
					<Route path="/aboutus" element={<About leaders={this.state.leaders} />} />
					<Route path="/browse" element={<Browse />} />
					<Route exact path="/contactus" element={<Contact />} />
					<Route path="*" element={<Navigate to="home"/>} />
				</Routes>
				
				<br></br>
				<Footer />
			</div>
		);
	}
}

export default Main;
