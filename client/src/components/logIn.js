import { createRef, useState } from "react";

function LogIn({ }) {

	const usernameRef = createRef(null)
	const passwordRef = createRef(null)
	const [passwordInputType, setPasswordInputType] = useState('password')

	function seePassword(e) {
		if (e.target.checked) {
			setPasswordInputType('text')
		} else {
			setPasswordInputType('password')
		}
	}

	async function tryLogIn(e) {

		e.preventDefault()

		const username = usernameRef.current.value
		const password = passwordRef.current.value

		const message = { 'username': username, 'password': password }

		const response = await fetch('/api/logIn', {
			headers: {
				'Content-Type': 'application/json'
			},
			method: 'POST',
			body: JSON.stringify(message)
		})

		if (response.ok){
			window.location.href = '/Profile'
		}
		if (!response.ok) {
			console.log('Log In failed')
		}
	}

	return (
		<form onSubmit={tryLogIn} className="logIn borderdDiv">
			<div className="cardHeader">
				<h1>Login</h1>
			</div>
			<div className="inputBox">
				<label>Username</label>
				<input ref={usernameRef} placeholder="Enter Username"></input>
			</div>
			<div className="inputBox">
				<label>Password</label>
				<input type={passwordInputType} ref={passwordRef} placeholder="Password"></input>
				<input type="checkbox" onChange={seePassword} style={{ width: 'auto', height: 'auto', margin: 'none' }}></input>
				<span style={{ fontSize: '16px', fontWeight: '400', marginLeft: '5px' }}>See password</span>
			</div>
			<button type="submit">Log In</button>
		</form>
	);
}

export default LogIn;
