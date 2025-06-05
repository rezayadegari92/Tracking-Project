document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Content Loaded - shipment_form.js');
    
    // Function to load cities based on selected country
    function loadCities(countrySelect, citySelect) {
        console.log('Loading cities for country:', countrySelect.value);
        const countryId = countrySelect.value;
        if (!countryId) {
            console.log('No country selected');
            citySelect.innerHTML = '<option value="">---------</option>';
            return;
        }

        const url = `/ajax/load-cities/?country_id=${countryId}`;
        console.log('Fetching cities from:', url);

        fetch(url)
            .then(response => {
                console.log('Response status:', response.status);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('Received cities:', data);
                if (!Array.isArray(data)) {
                    throw new Error('Invalid data format received');
                }
                citySelect.innerHTML = '<option value="">---------</option>';
                data.forEach(city => {
                    const option = document.createElement('option');
                    option.value = city.id;
                    option.textContent = city.name;
                    citySelect.appendChild(option);
                });
                console.log('Cities loaded into select');
            })
            .catch(error => {
                console.error('Error loading cities:', error);
                citySelect.innerHTML = '<option value="">Error loading cities</option>';
            });
    }

    // Get all country and city select elements
    const shipperCountry = document.getElementById('id_shipper_country');
    const shipperCity = document.getElementById('id_shipper_city');
    const receiverCountry = document.getElementById('id_receiver_country');
    const receiverCity = document.getElementById('id_receiver_city');

    console.log('Found elements:', {
        shipperCountry: !!shipperCountry,
        shipperCity: !!shipperCity,
        receiverCountry: !!receiverCountry,
        receiverCity: !!receiverCity
    });

    // Add event listeners for country changes
    if (shipperCountry && shipperCity) {
        console.log('Adding event listener for shipper country');
        shipperCountry.addEventListener('change', function() {
            console.log('Shipper country changed to:', this.value);
            loadCities(this, shipperCity);
        });
    }

    if (receiverCountry && receiverCity) {
        console.log('Adding event listener for receiver country');
        receiverCountry.addEventListener('change', function() {
            console.log('Receiver country changed to:', this.value);
            loadCities(this, receiverCity);
        });
    }

    // Load cities for initially selected countries
    if (shipperCountry && shipperCity && shipperCountry.value) {
        console.log('Loading initial cities for shipper');
        loadCities(shipperCountry, shipperCity);
    }

    if (receiverCountry && receiverCity && receiverCountry.value) {
        console.log('Loading initial cities for receiver');
        loadCities(receiverCountry, receiverCity);
    }

    // Handle form validation
    const form = document.getElementById('shipmentForm');
    if (form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    }

    // Handle dynamic form sections
    const cardHeaders = document.querySelectorAll('.card-header');
    cardHeaders.forEach(header => {
        header.addEventListener('click', function() {
            const targetId = this.getAttribute('data-bs-target');
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                const bsCollapse = new bootstrap.Collapse(targetElement, {
                    toggle: true
                });
            }
        });
    });
}); 