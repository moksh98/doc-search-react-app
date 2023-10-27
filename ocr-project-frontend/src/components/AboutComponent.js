import React from 'react';
import { Breadcrumb, BreadcrumbItem, Card, CardBody, CardHeader, Media } from 'reactstrap';
import { Link } from 'react-router-dom';

function About(props) {
    const leaders = props.leaders.map((leader) => {
        return (
            <div>
                <div key={leader.id}>
                    <RenderLeader leader={leader} />
                </div>
            </div>
        );
    });

    function RenderLeader({leader}) {
        return(
            <Media className="row row-content">
                <Media className="col-12 col-md-2">
                    <Media object src={leader.image} alt={leader.name} />
                </Media>
                <Media body className="col-12 col-md-10">
                    <Media heading>{leader.name}</Media>
                    <Media className="mt-2 mb-3" title>{leader.designation}</Media>
                    {leader.description}
                </Media>
            </Media>
        );
    }

    return(
        <div className="container">
            <div className="row">
                <Breadcrumb>
                    <BreadcrumbItem><Link to="/home">Home</Link></BreadcrumbItem>
                    <BreadcrumbItem active>About Us</BreadcrumbItem>
                </Breadcrumb>
                <div className="col-12">
                    <h3>About Us</h3>
                    <hr />
                </div>                
            </div>
            <div className="row row-content">
                <div className="col-12 col-md-6">
                    <h2>Our History</h2>
                    <p>
                        Early Arab immigrants in North and South America have left a remarkable legacy and history. Much of their histories have been recorded in millions of pages of Arabic newspapers, books, magazines, and other publications. Yet, this rich record has been largely inaccessible because it was dispersed and stored in disparate archives, and it was not digitally searchable.
                    </p>
                    <p>
                        In 2018 the <a style={{color: 'red'}} href="https://lebanesestudies.ncsu.edu/"><strong>Khayrallah Center</strong></a> set about to change this. We wanted to create a completely searchable database of these publications by developing Arabic OCR technology to render digitized images of these pages of history into searchable text. Now, through this open source website, you can search these records in Arabic and explore a heritage that spans 70 years, two continents, and tells the stories of these early Arab pioneers.
                    </p>
                    <p>
                        We welcome your support in maintaining and growing this free archive. Please consider donating a small gift to help sustain our efforts. Also, please let us know of any publications that we can add to this archive. You can email us information using the <Link style={{color: 'red'}} to="/contactus"><strong>form</strong></Link> below.
                    </p>
                </div>
                <div className="col-12 col-md-5">
                    <Card>
                        <CardHeader style={{background: '#B71B1C'}} className="text-white">Facts At a Glance</CardHeader>
                        <CardBody>
                            <dl className="row p-1">
                                <dt className="col-6">Started</dt>
                                <dd className="col-6">2018</dd>
                                <dt className="col-6">Major Stake Holder</dt>
                                <dd className="col-6">NC STATE</dd>
                                <dt className="col-6">Number of Archives</dt>
                                <dd className="col-6">500,000</dd>
                                <dt className="col-6">Employees</dt>
                                <dd className="col-6">15</dd>
                            </dl>
                        </CardBody>
                    </Card>
                </div>
            </div>
            {/* <div className="row">
                <div className="col-12">
                    <h2>Meet the Team</h2>
                </div>
                <div>
                    <Media list>
                        {leaders}
                    </Media>
                </div>
            </div> */}
        </div>
    );
}

export default About;