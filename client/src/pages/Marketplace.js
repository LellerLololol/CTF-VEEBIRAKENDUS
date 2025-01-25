import '../App.css';
import '../components/offer'
import Offer from '../components/offer';
import { useEffect, useState } from 'react'
import Header from '../components/header';
import Showcase from '../components/showcase';
import LogIn from '../components/logIn';

function Marketplace() {

	const [offers, setOffers] = useState([])
	const [showcase, setShowcase] = useState(null)


	useEffect(() => {
		async function fetchOffers() {
			const response = await fetch('/api/getAllOffers', {
				method: 'GET'
			})
			const data = await response.json()
			setOffers(data)
		}
		fetchOffers()
	}, [])

	function closeShowcase(){
		setShowcase(null)
	}

	function showcaseOffer(offer) {
		setShowcase(offer)
	}

	return (<LogIn />)

	return (
		<div className="Marketplace">
			<Header />
			<div className='scrollable'>
				<Showcase offer={showcase} close={closeShowcase} />
				<div className='offerList'>
					{offers.map((offer) =>
						<Offer offer={offer} func={showcaseOffer} />
					)}
				</div>
			</div>
		</div>
	);
}

export default Marketplace;
