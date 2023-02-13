import './SignUpForm.css'
import { NavLink } from 'react-router-dom';
import { Router } from 'react-router-dom';

import { Route, Routes } from 'react-router-dom';
import { Component } from 'react';

class SignInForm extends Component {

    constructor() {
        super();

        this.state = {
            email: "",
            password: ""
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        let target = event.target;
        let value = target.type === "checkbox" ? target.checked : target.value;
        let name = target.name;

        this.setState({
            [name]: value
        });
    }

    handleSubmit(event) {
        event.preventDefault();

        console.log("The form was submitted with the following data:");
        console.log(this.state);
    }

    handleChange(event) {
        let target = event.target;
        let value = target.type === "checkbox" ? target.checked : target.value;
        let name = target.name;

        this.setState({
            [name]: value
        });
    }

    handleSubmit(e) {
        e.preventDefault();

        console.log("The form was submitted with the following data:");
        console.log(this.state);
    }


    render() {
        return (
            <div className="login">
                <div className="appAside" />
                <div className="appForm">
                    <div className="pageSwitcher">
                        <NavLink
                            to="/sign-in"
                            className={(element) => element.isActive ? 'formTitleLink-active' : 'formTitleLink'}
                        >
                            Sign In
                        </NavLink>
                        <NavLink
                            exact
                            to="/sign-up"
                            className={(element) => element.isActive ? 'formTitleLink-active' : 'formTitleLink'}
                        >
                            Sign Up
                        </NavLink>
                    </div>

                    <div className="formCenter">
                        <form className="formFields" onSubmit={this.handleSubmit}>
                            <div className="formField">
                                <label className="formFieldLabel" htmlFor="email">
                                    E-Mail Address
                                </label>
                                <input
                                    type="email"
                                    id="email"
                                    className="formFieldInput"
                                    placeholder="Enter your email"
                                    name="email"
                                    value={this.state.email}
                                    onChange={this.handleChange}
                                />
                            </div>

                            <div className="formField">
                                <label className="formFieldLabel" htmlFor="password">
                                    Password
                                </label>
                                <input
                                    type="password"
                                    id="password"
                                    className="formFieldInput"
                                    placeholder="Enter your password"
                                    name="password"
                                    value={this.state.password}
                                    onChange={this.handleChange}
                                />
                            </div>

                            <div className="formField">
                                <NavLink to="/">
                                    <button className="formFieldButton"> Sign In</button>
                                </NavLink>
                                

                                <NavLink to="/sign-up" className="formFieldLink">
                                    Create an account
                                </NavLink>
                            </div>

                        </form>
                    </div>
                </div>
            </div>

        )
    }
}

export default SignInForm;