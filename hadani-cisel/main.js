const url = "https://random-data-api.com/api/cannabis/random_cannabis?size=30"

function useData(response) {
	// Tady musí proběhnout veškeré operace se získanými daty. Tahle funkce už
	// asynchronní být nemusí.
	console.log(response);
}


async function main() {
	// dostaň odpověď od serveru a zavolej useData
	await axios.get(url).then(response => {
		useData(response);
	});
}

main();